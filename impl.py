"""Main Job Finder Agent Implementation."""

from typing import Dict, List
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from pdf_parser import parse_resume
from scrapers.linkedin import scrape_linkedin_jobs
from scrapers.indeed import scrape_indeed_jobs
from scrapers.hackernews import scrape_hackernews_jobs
from matcher import rank_jobs, deduplicate_jobs
from enricher import enrich_with_company_info
from formatter import format_job_results, format_matching_summary


def run_job_finder(pdf_path: str, job_title: str = None, location: str = None) -> Dict:
    """
    Run the complete job finder pipeline.

    Args:
        pdf_path: Path to resume PDF
        job_title: Optional job title to search for (overrides resume)
        location: Optional location to search in (overrides resume)

    Returns:
        Dictionary with:
        - matched_jobs: List of matched jobs (ranked)
        - resume_info: Parsed resume information
        - summary: Human-readable summary
    """
    print("🔍 Job Finder Agent Starting...")

    # Step 1: Parse resume
    print("\n📄 Parsing resume...")
    try:
        resume_info = parse_resume(pdf_path)
    except Exception as e:
        return {
            "error": f"Failed to parse resume: {e}",
            "matched_jobs": [],
            "resume_info": {}
        }

    # Override with user inputs if provided
    if job_title:
        resume_info['title'] = job_title
    if location:
        resume_info['location'] = location

    print(f"  ✓ Extracted profile:")
    print(f"    - Title: {resume_info['title']}")
    print(f"    - Location: {resume_info['location']}")
    print(f"    - Level: {resume_info['level']}")
    print(f"    - Skills: {len(resume_info['skills'])} found")

    # Step 2: Scrape jobs from multiple sources (parallel)
    print("\n🕷️  Scraping job boards (LinkedIn, Indeed, HackerNews)...")
    jobs = _scrape_jobs_parallel(resume_info)

    print(f"  ✓ Found {len(jobs)} jobs from all sources")

    # Step 3: Deduplicate
    print("\n🔄 Deduplicating results...")
    jobs = deduplicate_jobs(jobs)
    print(f"  ✓ {len(jobs)} unique jobs after deduplication")

    # Step 4: Rank by match score
    print("\n⭐ Ranking jobs by match...")
    matched_jobs = rank_jobs(jobs, resume_info)
    print(f"  ✓ {len(matched_jobs)} jobs meet minimum score threshold")

    # Step 5: Enrich with company info
    print("\n🏢 Enriching with company information...")
    matched_jobs = enrich_with_company_info(matched_jobs, limit=5)
    print(f"  ✓ Company info added to top matches")

    # Step 6: Format output
    print("\n✨ Formatting results...")
    summary = format_matching_summary(matched_jobs, resume_info)
    results_text = format_job_results(matched_jobs, max_results=10)

    print("\n" + "=" * 60)
    print("✅ Job Finder Complete!")
    print("=" * 60)

    return {
        "matched_jobs": matched_jobs,
        "resume_info": resume_info,
        "summary": summary,
        "results": results_text,
        "total_matches": len(matched_jobs)
    }


def _scrape_jobs_parallel(resume_info: Dict) -> List[Dict]:
    """Scrape jobs from multiple sources in parallel."""
    title = resume_info.get("title", "Software Engineer")
    location = resume_info.get("location", "Remote")

    # Support comma-separated job titles as alternative searches
    titles = [t.strip() for t in title.split(',') if t.strip()]
    if not titles:
        titles = ["Software Engineer"]

    results = []

    # Scrape for each job title
    with ThreadPoolExecutor(max_workers=9) as executor:  # More workers for multiple titles
        futures = {}

        for search_title in titles:
            futures[executor.submit(scrape_linkedin_jobs, search_title, location)] = f"LinkedIn ({search_title})"
            futures[executor.submit(scrape_indeed_jobs, search_title, location)] = f"Indeed ({search_title})"

        # HackerNews is general, only do once
        futures[executor.submit(scrape_hackernews_jobs)] = "HackerNews"

        job_counts = {}
        for future in as_completed(futures):
            source_name = futures[future]
            try:
                jobs = future.result()
                # Deduplicate as we go
                unique_before = len(results)
                for job in jobs:
                    key = (job.get("title", "").lower(), job.get("company", "").lower())
                    if not any(k == key for k, _ in [(j.get("title", "").lower(), j.get("company", "").lower()) for j in results]):
                        results.append(job)

                print(f"  ✓ {source_name}: {len(jobs)} jobs ({len(results) - unique_before} new)")
            except Exception as e:
                print(f"  ⚠️  {source_name} failed: {e}")

    return results


def export_to_json(result: Dict, output_path: str = "job_matches.json"):
    """Export results to JSON file."""
    export_data = {
        "resume_info": result.get("resume_info", {}),
        "total_matches": result.get("total_matches", 0),
        "matched_jobs": [
            {
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "match_score": job.get("match_score"),
                "source": job.get("source"),
                "url": job.get("url"),
                "salary": job.get("salary")
            }
            for job in result.get("matched_jobs", [])
        ]
    }

    with open(output_path, "w") as f:
        json.dump(export_data, f, indent=2)

    print(f"\n💾 Results saved to {output_path}")


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Job Finder Agent")
    parser.add_argument("--resume", "-r", required=True, help="Path to resume PDF")
    parser.add_argument("--job-title", "-j", default=None, help="Job title to search for (overrides resume)")
    parser.add_argument("--location", "-l", default=None, help="Location to search in (overrides resume)")
    parser.add_argument("--output", "-o", default="job_matches.json", help="Output JSON file")
    parser.add_argument("--interactive", "-i", action="store_true", help="Ask for job title and location interactively")

    args = parser.parse_args()

    # Interactive mode
    job_title = args.job_title
    location = args.location

    if args.interactive or (not job_title and not location):
        print("\n" + "="*60)
        print("🎯 JOB FINDER - SEARCH PREFERENCES")
        print("="*60)

        user_input = input("\n🔍 What type of job are you looking for? (or press Enter to use resume): ").strip()
        if user_input:
            job_title = user_input

        user_input = input("📍 What location? (or press Enter to use resume): ").strip()
        if user_input:
            location = user_input

        print()

    # Run the job finder
    result = run_job_finder(args.resume, job_title=job_title, location=location)

    # Print results
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
    else:
        print(result["summary"])
        print(result["results"])
        export_to_json(result, args.output)
