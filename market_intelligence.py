#!/usr/bin/env python3
import json
import sys
from typing import List, Dict
from scraper import scrape_prospects
from enricher import enrich_prospect
from scorer import score_prospect

def run_agent(search_query: str, icp_criteria: str = None, max_results: int = 10) -> List[Dict]:
    """
    Run the MarketIntelligence agent end-to-end.

    Pipeline: Scrape → Enrich → Score

    Args:
        search_query: What prospects to find (e.g., "B2B SaaS in healthcare")
        icp_criteria: ICP description for scoring (default: generic)
        max_results: Max prospects to return

    Returns:
        List of scored prospects sorted by relevance (highest score first)
    """
    if not icp_criteria:
        icp_criteria = "B2B SaaS companies with 50+ employees"

    print(f"\n{'='*60}")
    print(f"MarketIntelligence Agent")
    print(f"{'='*60}")
    print(f"🎯 Query: {search_query}")
    print(f"🎯 ICP: {icp_criteria}")
    print(f"{'='*60}\n")

    # Step 1: Scrape
    print("STEP 1: Scraping prospects...")
    prospects = scrape_prospects(search_query, limit=max_results)
    print(f"✓ Scraped {len(prospects)} prospects\n")

    # Step 2: Enrich
    print("STEP 2: Enriching prospect data...")
    enriched = []
    for i, prospect in enumerate(prospects, 1):
        print(f"  [{i}/{len(prospects)}] Enriching {prospect.get('name', 'Unknown')}...")
        enriched_prospect = enrich_prospect(prospect)
        enriched.append(enriched_prospect)
    print(f"✓ Enriched {len(enriched)} prospects\n")

    # Step 3: Score
    print("STEP 3: Scoring leads...")
    scored = []
    for i, prospect in enumerate(enriched, 1):
        print(f"  [{i}/{len(enriched)}] Scoring {prospect.get('name', 'Unknown')}...")
        scored_prospect = score_prospect(prospect, icp_criteria)
        scored.append(scored_prospect)
    print(f"✓ Scored {len(scored)} prospects\n")

    # Sort by score (highest first)
    scored.sort(key=lambda p: p.get("score", 0), reverse=True)

    # Display results
    print(f"{'='*60}")
    print("QUALIFIED LEADS (sorted by relevance)")
    print(f"{'='*60}\n")
    for i, prospect in enumerate(scored, 1):
        print(f"{i}. {prospect.get('name', 'Unknown')}")
        print(f"   Score: {prospect.get('score', 0)}/100 ({prospect.get('engagement_level', 'N/A')})")
        print(f"   Reason: {prospect.get('score_reason', '')}")
        print(f"   Industry: {prospect.get('industry', 'N/A')}")
        print(f"   Company Size: {prospect.get('company_size', 'N/A')}")
        print()

    return scored

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else "B2B SaaS companies"
    icp = sys.argv[2] if len(sys.argv) > 2 else None
    results = run_agent(query, icp, max_results=5)

    # Save results
    with open("leads_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"✓ Results saved to leads_results.json")
