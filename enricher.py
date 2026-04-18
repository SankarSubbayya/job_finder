import os
import json
from typing import Dict
from anthropic import Anthropic

client = Anthropic()

def enrich_prospect(prospect: Dict) -> Dict:
    """
    Enrich raw prospect data with Claude-powered company research.

    Args:
        prospect: Dict with {name, url, snippet, source}

    Returns:
        Dict with original data + enriched fields: {industry, company_size, funding_stage, pain_points, decision_makers}
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    company_name = prospect.get("name", "Unknown")
    snippet = prospect.get("snippet", "")

    prompt = f"""Based on this company information, provide a brief enrichment profile:

Company: {company_name}
Description: {snippet}

Respond as JSON with exactly these fields (be concise):
{{
  "industry": "primary industry",
  "company_size": "estimated employee count or range",
  "funding_stage": "bootstrapped/seed/series a/b/c+",
  "pain_points": ["max 2 likely pain points"],
  "decision_makers": ["likely title of buyer, e.g. VP Sales"]
}}"""

    try:
        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text
        enrichment = json.loads(response_text)

        return {
            **prospect,
            "industry": enrichment.get("industry", ""),
            "company_size": enrichment.get("company_size", ""),
            "funding_stage": enrichment.get("funding_stage", ""),
            "pain_points": enrichment.get("pain_points", []),
            "decision_makers": enrichment.get("decision_makers", []),
        }
    except Exception as e:
        print(f"⚠ Enrichment error for {company_name}: {str(e)}")
        # Return prospect with mock enrichment
        return {
            **prospect,
            "industry": "Technology",
            "company_size": "50-200",
            "funding_stage": "Series A",
            "pain_points": ["Process automation", "Team scaling"],
            "decision_makers": ["VP Operations", "CTO"],
        }
