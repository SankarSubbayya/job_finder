import os
import json
from typing import List, Dict
from dotenv import load_dotenv
from apify_client import ApifyClient

load_dotenv()

def scrape_prospects(query: str, limit: int = 10) -> List[Dict]:
    """
    Discover prospects using Apify Google Search actor.

    Args:
        query: Search query (e.g., "B2B SaaS companies in healthcare")
        limit: Max number of prospects to return

    Returns:
        List of dicts with: {name, url, snippet, source}
    """
    apify_token = os.getenv("APIFY_TOKEN")
    if not apify_token:
        raise ValueError("APIFY_TOKEN not set in .env")

    client = ApifyClient(apify_token)

    # Use Google Search Results actor for discovering companies
    actor_id = "apify/google-search"
    run_input = {
        "queries": [query],
        "maxPagesPerQuery": 1,
        "resultsPerPage": limit,
    }

    print(f"🔍 Scraping prospects for: {query}")

    try:
        run = client.actor(actor_id).call(run_input=run_input)
        results = client.dataset(run["defaultDatasetId"]).list_items()

        prospects = []
        for item in results.items:
            prospect = {
                "name": item.get("title", "Unknown"),
                "url": item.get("url", ""),
                "snippet": item.get("description", ""),
                "source": "google_search"
            }
            prospects.append(prospect)
            if len(prospects) >= limit:
                break

        print(f"✓ Found {len(prospects)} prospects")
        return prospects

    except Exception as e:
        print(f"✗ Scraping error: {str(e)}")
        # Return mock data for demo purposes
        return _get_mock_prospects(limit)

def _get_mock_prospects(limit: int = 10) -> List[Dict]:
    """Mock prospects for demo/testing when Apify fails."""
    mock = [
        {"name": "TechCorp Inc", "url": "https://techcorp.com", "snippet": "Leading B2B SaaS platform for enterprise", "source": "mock"},
        {"name": "DataFlow Systems", "url": "https://dataflow.io", "snippet": "Real-time data pipeline and analytics", "source": "mock"},
        {"name": "CloudFirst AI", "url": "https://cloudfirst.ai", "snippet": "AI-powered cloud infrastructure", "source": "mock"},
        {"name": "SecureVault Pro", "url": "https://securevault.pro", "snippet": "Enterprise security and compliance", "source": "mock"},
        {"name": "Growth Analytics Co", "url": "https://growthanalytics.io", "snippet": "Customer analytics and insights", "source": "mock"},
    ]
    return mock[:limit]
