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


def run_job_finder(pdf_path: str) -> Dict:
    """
    Run the complete job finder pipeline.

    Args:
        pdf_path: Path to resume PDF

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

    results = []

    # Try to scrape from all sources, but don't fail if one doesn't work
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(scrape_linkedin_jobs, title, location): "LinkedIn",
            executor.submit(scrape_indeed_jobs, title, location): "Indeed",
            executor.submit(scrape_hackernews_jobs): "HackerNews",
        }

        for future in as_completed(futures):
            source_name = futures[future]
            try:
                jobs = future.result()
                print(f"  ✓ {source_name}: {len(jobs)} jobs")
                results.extend(jobs)
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
    parser.add_argument("--output", "-o", default="job_matches.json", help="Output JSON file")

    args = parser.parse_args()

    # Run the job finder
    result = run_job_finder(args.resume)

    # Print results
    if "error" in result:
        print(f"\n❌ Error: {result['error']}")
    else:
        print(result["summary"])
        print(result["results"])
        export_to_json(result, args.output)
