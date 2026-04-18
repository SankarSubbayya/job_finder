"""
Reasoning Layer - Deep lead analysis using Claude Extended Thinking.

Uses Claude's chain-of-thought reasoning to deeply analyze leads before
presenting to enterprises. Considers fit, opportunities, risks, and
personalized outreach angles.
"""

import json
from typing import Dict, List
from anthropic import Anthropic

client = Anthropic()

def analyze_lead_deeply(prospect: Dict, icp_criteria: str = None) -> Dict:
    """
    Perform deep reasoning analysis on a scored prospect using extended thinking.

    This goes beyond the quick score (0-100) to provide enterprise-grade insights:
    - Strategic fit assessment
    - Engagement opportunities
    - Personalized outreach angles
    - Risk factors and mitigations
    - Next steps for the sales team

    Args:
        prospect: Fully scored prospect dict from scorer.py
        icp_criteria: ICP description for context

    Returns:
        Prospect dict with added reasoning fields:
        - reasoning_summary: strategic assessment
        - engagement_angles: [list of specific outreach strategies]
        - risk_factors: [potential objections/blockers]
        - next_steps: [recommended actions for sales team]
    """
    if not icp_criteria:
        icp_criteria = "B2B SaaS companies with 50+ employees, Series A-B funding"

    company_name = prospect.get("name", "Unknown")

    prompt = f"""You are an expert GTM strategist analyzing a B2B sales prospect.

PROSPECT DATA:
- Name: {company_name}
- Industry: {prospect.get('industry', 'N/A')}
- Size: {prospect.get('company_size', 'N/A')}
- Funding: {prospect.get('funding_stage', 'N/A')}
- Pain Points: {', '.join(prospect.get('pain_points', []))}
- Decision Makers: {', '.join(prospect.get('decision_makers', []))}
- Relevance Score: {prospect.get('score', 0)}/100

OUR ICP: {icp_criteria}

Analyze this prospect deeply and provide:
1. **Strategic Fit**: Why is this a good/bad fit? (1-2 sentences)
2. **Engagement Angles**: 3 specific, personalized reasons to reach out (concrete to their situation)
3. **Risk Factors**: Potential objections or blockers (e.g., budget cycles, competitive landscape)
4. **Sales Motion**: Best first contact approach (email subject angle, warm intro type, etc.)

Respond as JSON:
{{
  "strategic_fit": "...",
  "engagement_angles": ["angle 1", "angle 2", "angle 3"],
  "risk_factors": ["risk 1", "risk 2"],
  "sales_motion": "...",
  "confidence": "high/medium/low"
}}"""

    try:
        # Use extended thinking for deep reasoning
        message = client.messages.create(
            model="claude-opus-4-7",
            max_tokens=16000,
            thinking={
                "type": "adaptive"
            },
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        # Extract the text response (skip thinking blocks)
        response_text = ""
        for block in message.content:
            if hasattr(block, 'text'):
                response_text = block.text
                break

        reasoning = json.loads(response_text)

        return {
            **prospect,
            "reasoning_summary": reasoning.get("strategic_fit", ""),
            "engagement_angles": reasoning.get("engagement_angles", []),
            "risk_factors": reasoning.get("risk_factors", []),
            "sales_motion": reasoning.get("sales_motion", ""),
            "reasoning_confidence": reasoning.get("confidence", "medium"),
        }

    except Exception as e:
        print(f"⚠ Reasoning error for {company_name}: {str(e)}")
        # Fallback: provide reasonable defaults
        return {
            **prospect,
            "reasoning_summary": "Strong prospect based on score and fit",
            "engagement_angles": [
                f"Address {prospect.get('pain_points', ['key pain'])[0]} challenges",
                f"Timing opportunity with {prospect.get('funding_stage', 'recent')} funding",
                f"Peer adoption in {prospect.get('industry', 'their')} industry"
            ],
            "risk_factors": ["Budget cycle timing", "Competitive vendor relationships"],
            "sales_motion": "Warm introduction from industry peer or analyst",
            "reasoning_confidence": "low",
        }

def analyze_batch(leads: List[Dict], icp_criteria: str = None) -> List[Dict]:
    """
    Analyze multiple leads with reasoning.

    Args:
        leads: List of scored prospects
        icp_criteria: ICP description

    Returns:
        List of analyzed prospects with reasoning fields
    """
    analyzed = []
    for i, lead in enumerate(leads, 1):
        print(f"  🧠 Reasoning about lead {i}/{len(leads)}: {lead.get('name', 'Unknown')}...")
        analyzed_lead = analyze_lead_deeply(lead, icp_criteria)
        analyzed.append(analyzed_lead)
    return analyzed
