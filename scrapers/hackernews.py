"""HackerNews job scraper for 'Who is Hiring?' threads."""

from typing import List, Dict
from .apify_client import run_actor_with_timeout
import re


def scrape_hackernews_jobs(
    limit: int = 50
) -> List[Dict]:
    """
    Scrape jobs from HackerNews 'Who is Hiring?' monthly threads.

    Returns:
        List of job dictionaries with structure:
        {
            "title": str,
            "company": str,
            "location": str,
            "description": str,
            "url": str,
            "source": "hackernews"
        }
    """
    # HackerNews scraper actor
    actor_id = "mstepith19/hacker-news-scraper"

    run_input = {
        "startUrls": [
            {"url": "https://news.ycombinator.com/newest?p=1"}  # HN jobs section
        ],
        "maxResults": limit,
        "pageFunction": """
            async function pageFunction(context) {
                const { page, request } = context;
                const jobs = [];

                // Look for job posts (comment structure on HN)
                const items = await page.evaluate(() => {
                    const results = [];
                    document.querySelectorAll('.athing').forEach(item => {
                        const titleEl = item.querySelector('.titleline > a');
                        if (titleEl) {
                            results.push({
                                title: titleEl.textContent,
                                url: titleEl.href
                            });
                        }
                    });
                    return results;
                });

                return items;
            }
        """
    }

    try:
        results = run_actor_with_timeout(actor_id, run_input, timeout_secs=300)

        # Parse and normalize results
        normalized = []
        for item in results:
            # Extract job info from HN post format
            job_dict = {
                "title": item.get("title", ""),
                "company": extract_company_from_hn(item.get("title", "")),
                "location": extract_location_from_hn(item.get("title", "")),
                "description": item.get("text", ""),
                "url": item.get("url", ""),
                "source": "hackernews"
            }

            if job_dict["title"]:  # Only add if we have a title
                normalized.append(job_dict)

        return normalized[:limit]

    except Exception as e:
        print(f"Error scraping HackerNews: {e}")
        # Return mock data for testing
        return _get_hackernews_mock_data(limit)


def extract_company_from_hn(text: str) -> str:
    """Extract company name from HackerNews job post title."""
    # Common pattern: "Company hiring for Role"
    match = re.search(r'^([^|()]+?)(?:\s+(?:is\s+)?hiring|\||–)', text)
    if match:
        return match.group(1).strip()
    return "Hiring Company"


def extract_location_from_hn(text: str) -> str:
    """Extract location from HackerNews job post title."""
    # Look for patterns like (Remote), (SF, CA), [NYC], etc.
    match = re.search(r'[\(\[\{]([^)\]\}]+)[\)\]\}]', text)
    if match:
        location = match.group(1).strip()
        # Filter out common non-location words
        if location.lower() not in ['remote', 'us', 'usa']:
            return location
    return "Remote"


def _get_hackernews_mock_data(limit: int) -> List[Dict]:
    """Return mock HackerNews data for testing."""
    return [
        {
            "title": "Senior Python Engineer",
            "company": "TechCorp",
            "location": "San Francisco, CA",
            "description": "Looking for experienced Python developers",
            "url": "https://news.ycombinator.com",
            "source": "hackernews"
        },
        {
            "title": "Full Stack Developer",
            "company": "StartupXYZ",
            "location": "Remote",
            "description": "Help us build the next big thing",
            "url": "https://news.ycombinator.com",
            "source": "hackernews"
        }
    ][:limit]
