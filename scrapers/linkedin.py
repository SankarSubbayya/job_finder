"""LinkedIn job scraper using Apify."""

from typing import List, Dict
from .apify_client import run_actor_with_timeout
from config import LINKEDIN_ACTOR_ID, JOBS_PER_SOURCE


def scrape_linkedin_jobs(
    job_title: str,
    location: str,
    limit: int = JOBS_PER_SOURCE
) -> List[Dict]:
    """
    Scrape jobs from LinkedIn using Apify actor.

    Args:
        job_title: Job title to search for
        location: Location to search in
        limit: Max number of results

    Returns:
        List of job dictionaries with structure:
        {
            "title": str,
            "company": str,
            "location": str,
            "description": str,
            "url": str,
            "salary": str (optional),
            "source": "linkedin"
        }
    """
    run_input = {
        "keywords": job_title,
        "location": location,
        "limit": limit
    }

    try:
        results = run_actor_with_timeout(LINKEDIN_ACTOR_ID, run_input, timeout_secs=600)

        # Normalize results to consistent format
        normalized = []
        for job in results:
            normalized.append({
                "title": job.get("positionTitle", ""),
                "company": job.get("companyName", ""),
                "location": job.get("location", location),
                "description": job.get("jobDescription", ""),
                "url": job.get("link", ""),
                "salary": job.get("salary"),
                "source": "linkedin"
            })

        return normalized

    except Exception as e:
        print(f"Error scraping LinkedIn: {e}")
        return []
