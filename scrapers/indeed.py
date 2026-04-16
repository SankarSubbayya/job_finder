"""Indeed job scraper using Apify."""

from typing import List, Dict
from .apify_client import run_actor_with_timeout
from config import INDEED_ACTOR_ID, JOBS_PER_SOURCE


def scrape_indeed_jobs(
    job_title: str,
    location: str,
    limit: int = JOBS_PER_SOURCE
) -> List[Dict]:
    """
    Scrape jobs from Indeed using Apify actor.

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
            "source": "indeed"
        }
    """
    run_input = {
        "position": job_title,
        "location": location,
        "maxResults": limit
    }

    try:
        results = run_actor_with_timeout(INDEED_ACTOR_ID, run_input, timeout_secs=600)

        # Normalize results to consistent format
        normalized = []
        for job in results:
            normalized.append({
                "title": job.get("title", ""),
                "company": job.get("company", ""),
                "location": job.get("location", location),
                "description": job.get("description", ""),
                "url": job.get("link", "") or job.get("url", ""),
                "salary": job.get("salary"),
                "source": "indeed"
            })

        return normalized

    except Exception as e:
        print(f"Error scraping Indeed: {e}")
        return []
