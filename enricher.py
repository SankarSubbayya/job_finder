"""Enrich job listings with company information from you.com."""

from typing import List, Dict
import requests
from config import YOU_COM_SEARCH_URL, YOU_API_KEY


def enrich_with_company_info(
    jobs: List[Dict],
    limit: int = 5
) -> List[Dict]:
    """
    Enrich top jobs with company information from you.com.

    Args:
        jobs: List of job dictionaries (should be sorted by relevance)
        limit: Number of top jobs to enrich

    Returns:
        Jobs with added 'company_summary' field
    """
    if not YOU_API_KEY:
        print("WARNING: YOU_API_KEY not set. Skipping company enrichment.")
        return jobs

    enriched_jobs = []

    for i, job in enumerate(jobs[:limit]):
        company = job.get("company", "")

        if company:
            summary = _search_company_info(company)
            job_with_summary = job.copy()
            job_with_summary["company_summary"] = summary
            enriched_jobs.append(job_with_summary)
        else:
            enriched_jobs.append(job)

    # Add remaining non-enriched jobs
    enriched_jobs.extend(jobs[limit:])

    return enriched_jobs


def _search_company_info(company_name: str) -> str:
    """
    Search for company information using you.com Search API.

    Args:
        company_name: Name of the company

    Returns:
        Brief company description or empty string if not found
    """
    if not YOU_API_KEY:
        return ""

    query = f"{company_name} company about"

    try:
        headers = {
            "Authorization": f"Bearer {YOU_API_KEY}",
            "Content-Type": "application/json"
        }

        params = {
            "query": query,
            "count": 1,
            "offset": 0
        }

        response = requests.get(
            YOU_COM_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()

            # Extract first result snippet
            if "results" in data and len(data["results"]) > 0:
                result = data["results"][0]
                snippet = result.get("snippet", "")

                # Clean up and limit length
                if snippet:
                    return snippet[:200]  # First 200 chars

        return f"{company_name} is a company providing services."

    except requests.Timeout:
        return f"{company_name} is a company providing services."
    except Exception as e:
        print(f"Error enriching company info for {company_name}: {e}")
        return f"{company_name} is a company providing services."


def get_company_benefits(company_name: str) -> str:
    """Get company benefits/perks information."""
    if not YOU_API_KEY:
        return ""

    query = f"{company_name} company benefits perks"

    try:
        headers = {
            "Authorization": f"Bearer {YOU_API_KEY}",
            "Content-Type": "application/json"
        }

        params = {
            "query": query,
            "count": 1
        }

        response = requests.get(
            YOU_COM_SEARCH_URL,
            headers=headers,
            params=params,
            timeout=5
        )

        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                snippet = data["results"][0].get("snippet", "")
                return snippet[:150] if snippet else ""

        return ""

    except Exception as e:
        print(f"Error getting benefits for {company_name}: {e}")
        return ""
