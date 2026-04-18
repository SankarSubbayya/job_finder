#!/usr/bin/env python3
"""
MarketIntelligence Demo - Showcase the agent without requiring API keys.
Uses mock data to demonstrate the full pipeline.
"""

import json
from typing import List, Dict

def demo_scrape() -> List[Dict]:
    """Mock scraping results."""
    return [
        {
            "name": "CloudFirst AI",
            "url": "https://cloudfirst.ai",
            "snippet": "Enterprise AI infrastructure for data teams",
            "source": "google"
        },
        {
            "name": "DataFlow Systems",
            "url": "https://dataflow.io",
            "snippet": "Real-time data pipeline and analytics platform",
            "source": "google"
        },
        {
            "name": "SecureVault Pro",
            "url": "https://securevault.pro",
            "snippet": "Enterprise security and compliance automation",
            "source": "google"
        },
        {
            "name": "Growth Analytics Co",
            "url": "https://growthanalytics.io",
            "snippet": "Customer analytics and predictive insights",
            "source": "google"
        },
    ]

def demo_enrich(prospect: Dict) -> Dict:
    """Mock enrichment with company data."""
    enrichment_map = {
        "CloudFirst AI": {
            "industry": "Enterprise AI/ML",
            "company_size": "50-200",
            "funding_stage": "Series B",
            "pain_points": ["ML Operations", "Data Governance"],
            "decision_makers": ["VP Engineering", "CTO"]
        },
        "DataFlow Systems": {
            "industry": "Data Infrastructure",
            "company_size": "100-300",
            "funding_stage": "Series B",
            "pain_points": ["Pipeline Reliability", "Cost Optimization"],
            "decision_makers": ["VP Data", "Head of Eng"]
        },
        "SecureVault Pro": {
            "industry": "Enterprise Security",
            "company_size": "150-400",
            "funding_stage": "Series C",
            "pain_points": ["Compliance Automation", "Incident Response"],
            "decision_makers": ["CISO", "VP Security"]
        },
        "Growth Analytics Co": {
            "industry": "MarTech/Analytics",
            "company_size": "75-250",
            "funding_stage": "Series A",
            "pain_points": ["Attribution", "Real-time Analytics"],
            "decision_makers": ["VP Product", "Head of Analytics"]
        },
    }

    name = prospect.get("name", "")
    enrichment = enrichment_map.get(name, {
        "industry": "Technology",
        "company_size": "50-200",
        "funding_stage": "Series A",
        "pain_points": ["Process automation", "Team scaling"],
        "decision_makers": ["VP Operations"]
    })

    return {**prospect, **enrichment}

def demo_score(prospect: Dict) -> Dict:
    """Mock scoring based on company data."""
    # Scoring logic: higher score for Series A/B, good size match, relevant pain points
    funding_stage = prospect.get("funding_stage", "")
    company_size = prospect.get("company_size", "")

    base_score = 50
    if funding_stage in ["Series A", "Series B"]:
        base_score += 20
    if "50" in company_size or "100" in company_size:
        base_score += 15

    # Add variance based on name (for demo)
    name = prospect.get("name", "")
    if "Cloud" in name:
        base_score += 10
    elif "Data" in name:
        base_score += 5

    score = min(100, base_score)
    engagement = "high" if score >= 75 else "medium" if score >= 50 else "low"

    reason = {
        90: "Exceptional ICP fit: right stage, size, and pain points",
        80: "Strong match: Series B status, good size, aligned needs",
        70: "Good fit: relevant industry and funding stage",
        60: "Moderate fit: some ICP alignment, worth reaching out",
        50: "Fair prospect: could be valuable with right positioning"
    }

    return {
        **prospect,
        "score": score,
        "score_reason": reason.get(score // 10 * 10, "Potential lead"),
        "engagement_level": engagement
    }

def main():
    """Run the demo pipeline."""
    print("\n" + "="*70)
    print("MarketIntelligence Agent - Demo Mode")
    print("="*70)
    print("🎯 Query: B2B SaaS companies with $50M+ ARR")
    print("🎯 ICP: Series A-B, 50-500 employees, enterprise focus")
    print("="*70 + "\n")

    # Step 1: Scrape
    print("STEP 1: Scraping prospects...")
    prospects = demo_scrape()
    print(f"✓ Found {len(prospects)} prospects\n")

    # Step 2: Enrich
    print("STEP 2: Enriching prospect data...")
    enriched = []
    for i, prospect in enumerate(prospects, 1):
        print(f"  [{i}/{len(prospects)}] Enriching {prospect['name']}...")
        enriched_prospect = demo_enrich(prospect)
        enriched.append(enriched_prospect)
    print(f"✓ Enriched {len(enriched)} prospects\n")

    # Step 3: Score
    print("STEP 3: Scoring leads...")
    scored = []
    for i, prospect in enumerate(enriched, 1):
        print(f"  [{i}/{len(enriched)}] Scoring {prospect['name']}...")
        scored_prospect = demo_score(prospect)
        scored.append(scored_prospect)
    print(f"✓ Scored {len(scored)} prospects\n")

    # Sort by score
    scored.sort(key=lambda p: p.get("score", 0), reverse=True)

    # Display results
    print("="*70)
    print("QUALIFIED LEADS (sorted by relevance)")
    print("="*70 + "\n")

    for i, prospect in enumerate(scored, 1):
        score = prospect.get("score", 0)
        score_color = "🟢" if score >= 75 else "🟡" if score >= 50 else "🔴"

        print(f"{i}. {prospect['name']} {score_color}")
        print(f"   Score: {score}/100 ({prospect.get('engagement_level', 'N/A')})")
        print(f"   Reason: {prospect.get('score_reason', '')}")
        print(f"   Industry: {prospect.get('industry', 'N/A')}")
        print(f"   Size: {prospect.get('company_size', 'N/A')}")
        print(f"   Funding: {prospect.get('funding_stage', 'N/A')}")
        print()

    # Save results
    with open("demo_results.json", "w") as f:
        json.dump(scored, f, indent=2)

    print("="*70)
    print("✅ Demo complete! Results saved to demo_results.json")
    print("="*70)
    print("\n🚀 To use with real data:")
    print("   1. Set up .env with APIFY_TOKEN and ANTHROPIC_API_KEY")
    print("   2. Run: python app.py")
    print("   3. Visit: http://localhost:5000")
    print()

if __name__ == "__main__":
    main()
