"""
Kalibr Router Integration - Actual multi-model routing and optimization.

Uses Kalibr's Router to select optimal models and handle recovery automatically.
This replaces the mock orchestrator with real multi-model optimization.
"""

import os
import json
from typing import Dict, List

try:
    import kalibr
    from kalibr import Router
    KALIBR_AVAILABLE = True
except ImportError:
    KALIBR_AVAILABLE = False
    print("⚠️  Kalibr SDK not installed. Install with: pip install kalibr")

def get_kalibr_router():
    """Initialize Kalibr Router with API credentials."""
    if not KALIBR_AVAILABLE:
        return None

    api_key = os.getenv("KALIBR_API_KEY")
    tenant_id = os.getenv("KALIBR_TENANT_ID")

    if not api_key or not tenant_id:
        print("⚠️  Kalibr credentials not set in .env")
        return None

    try:
        router = Router(
            api_key=api_key,
            tenant_id=tenant_id,
            goal="enrich_and_score_prospect",
            paths=["gpt-4o-mini", "claude-3-5-haiku-20241022"],
        )
        return router
    except Exception as e:
        print(f"⚠️  Failed to initialize Kalibr Router: {str(e)}")
        return None


def enrich_with_kalibr_routing(prospect: Dict) -> Dict:
    """
    Use Kalibr Router to select optimal model for enrichment.

    Kalibr automatically:
    - Routes between GPT-4o-mini and Claude Haiku
    - Selects based on latency/cost/quality
    - Handles failures with fallback
    """
    router = get_kalibr_router()
    if not router:
        # Fallback to direct Claude call
        from enricher import enrich_prospect
        return enrich_prospect(prospect)

    company_name = prospect.get("name", "Unknown")
    prompt = f"""Enrich this company data:
Name: {company_name}
Snippet: {prospect.get('snippet', '')}

Extract: industry, company_size (e.g., "50-200"), funding_stage, pain_points (max 2), decision_makers (max 2).
Respond as JSON with exact keys: industry, company_size, funding_stage, pain_points, decision_makers"""

    try:
        # Kalibr Router handles model selection and recovery
        response = router.completion(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )

        enrichment = json.loads(response)
        router.report(success=True)  # Report success for model optimization

        return {
            **prospect,
            "industry": enrichment.get("industry", ""),
            "company_size": enrichment.get("company_size", ""),
            "funding_stage": enrichment.get("funding_stage", ""),
            "pain_points": enrichment.get("pain_points", []),
            "decision_makers": enrichment.get("decision_makers", []),
            "model_routing": "kalibr_optimized"
        }
    except Exception as e:
        print(f"⚠️  Kalibr enrichment failed for {company_name}: {str(e)}")
        router.report(success=False)

        # Fallback to direct Claude
        from enricher import enrich_prospect
        return enrich_prospect(prospect)


def score_with_kalibr_routing(prospect: Dict, icp_criteria: str) -> Dict:
    """
    Use Kalibr Router to select optimal model for scoring.

    Faster scoring with cost optimization via Kalibr routing.
    """
    router = get_kalibr_router()
    if not router:
        # Fallback to direct Claude call
        from scorer import score_prospect
        return score_prospect(prospect, icp_criteria)

    company_name = prospect.get("name", "Unknown")
    prompt = f"""Score this prospect (0-100) against ICP:

ICP: {icp_criteria}
Company: {company_name}
Industry: {prospect.get('industry')}
Size: {prospect.get('company_size')}
Funding: {prospect.get('funding_stage')}
Pain Points: {', '.join(prospect.get('pain_points', []))}

Respond as JSON: {{"score": <0-100>, "reason": "...", "engagement_level": "high/medium/low"}}"""

    try:
        response = router.completion(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=200,
        )

        scoring = json.loads(response)
        router.report(success=True)

        return {
            **prospect,
            "score": scoring.get("score", 0),
            "score_reason": scoring.get("reason", ""),
            "engagement_level": scoring.get("engagement_level", "medium"),
            "model_routing": "kalibr_optimized"
        }
    except Exception as e:
        print(f"⚠️  Kalibr scoring failed for {company_name}: {str(e)}")
        router.report(success=False)

        # Fallback to direct Claude
        from scorer import score_prospect
        return score_prospect(prospect, icp_criteria)


def route_pipeline_with_kalibr(prospects: List[Dict], icp_criteria: str) -> List[Dict]:
    """
    Run enrichment and scoring through Kalibr Router for optimal model selection.

    Benefits:
    - Automatic model selection (GPT-4o vs Claude)
    - Cost optimization
    - Latency tracking
    - Failure recovery
    """
    print("\n🛣️  Using Kalibr Router for multi-model optimization...")

    enriched = []
    for i, prospect in enumerate(prospects, 1):
        print(f"  [{i}/{len(prospects)}] Enriching (Kalibr routed): {prospect.get('name')}...")
        enriched_prospect = enrich_with_kalibr_routing(prospect)
        enriched.append(enriched_prospect)

    scored = []
    for i, prospect in enumerate(enriched, 1):
        print(f"  [{i}/{len(enriched)}] Scoring (Kalibr routed): {prospect.get('name')}...")
        scored_prospect = score_with_kalibr_routing(prospect, icp_criteria)
        scored.append(scored_prospect)

    return sorted(scored, key=lambda p: p.get("score", 0), reverse=True)
