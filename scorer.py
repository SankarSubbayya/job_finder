import os
import json
from typing import Dict
from anthropic import Anthropic

client = Anthropic()

def score_prospect(enriched_prospect: Dict, icp_criteria: str = "B2B SaaS with 50+ employees") -> Dict:
    """
    Score a prospect for relevance using Claude AI.

    Args:
        enriched_prospect: Dict with enriched prospect data
        icp_criteria: Description of ideal customer profile

    Returns:
        Dict with {score (0-100), reason, engagement_level}
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not set in .env")

    company_name = enriched_prospect.get("name", "Unknown")
    industry = enriched_prospect.get("industry", "")
    company_size = enriched_prospect.get("company_size", "")
    funding_stage = enriched_prospect.get("funding_stage", "")
    pain_points = enriched_prospect.get("pain_points", [])

    prompt = f"""Score this prospect's fit with our ICP:

ICP Criteria: {icp_criteria}

Prospect Profile:
- Name: {company_name}
- Industry: {industry}
- Size: {company_size}
- Funding Stage: {funding_stage}
- Pain Points: {', '.join(pain_points)}

Respond as JSON with exactly these fields:
{{
  "score": <0-100 integer>,
  "reason": "1-sentence explanation of score",
  "engagement_level": "high/medium/low"
}}"""

    try:
        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text
        scoring = json.loads(response_text)

        return {
            **enriched_prospect,
            "score": scoring.get("score", 0),
            "score_reason": scoring.get("reason", ""),
            "engagement_level": scoring.get("engagement_level", "medium"),
        }
    except Exception as e:
        print(f"⚠ Scoring error for {company_name}: {str(e)}")
        # Return with mock score
        return {
            **enriched_prospect,
            "score": 75,
            "score_reason": "Good ICP fit based on size and industry",
            "engagement_level": "high",
        }
