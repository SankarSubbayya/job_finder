#!/usr/bin/env python3
"""
Test the Kalibr orchestrator with mock data to demonstrate full pipeline.
"""

from kalibr_orchestrator import KalibrOrchestrator
from unittest.mock import patch, MagicMock

def test_orchestrator_with_mocks():
    """Test full orchestrator pipeline with mocked APIs."""

    # Mock data for each stage
    mock_prospects = [
        {
            "name": "CloudFirst AI",
            "url": "https://cloudfirst.ai",
            "snippet": "Enterprise AI infrastructure",
            "source": "google"
        },
        {
            "name": "DataFlow Systems",
            "url": "https://dataflow.io",
            "snippet": "Real-time data pipeline",
            "source": "google"
        },
    ]

    mock_enriched = [
        {
            **p,
            "industry": "Enterprise AI/ML",
            "company_size": "100-200",
            "funding_stage": "Series B",
            "pain_points": ["ML Operations", "Data Governance"],
            "decision_makers": ["VP Engineering", "CTO"]
        }
        for p in mock_prospects
    ]

    mock_scored = [
        {
            **e,
            "score": 85 if i == 0 else 75,
            "score_reason": "Excellent ICP fit" if i == 0 else "Good match",
            "engagement_level": "high"
        }
        for i, e in enumerate(mock_enriched)
    ]

    mock_reasoned = [
        {
            **s,
            "reasoning_summary": "Strong prospect with clear product-market fit",
            "engagement_angles": [
                "Address ML Operations challenges",
                "Series B funding shows growth trajectory",
                "Enterprise AI is hot market"
            ],
            "risk_factors": ["Existing vendor relationships"],
            "sales_motion": "Warm introduction from industry analyst",
            "reasoning_confidence": "high"
        }
        for s in mock_scored
    ]

    # Patch the pipeline stages
    with patch('kalibr_orchestrator.scrape_prospects', return_value=mock_prospects):
        with patch('kalibr_orchestrator.enrich_prospect', side_effect=lambda p: next(e for e in mock_enriched if e['name'] == p['name'])):
            with patch('kalibr_orchestrator.score_prospect', side_effect=lambda p, icp: next(s for s in mock_scored if s['name'] == p['name'])):
                with patch('kalibr_orchestrator.analyze_lead_deeply', side_effect=lambda p, icp: next(r for r in mock_reasoned if r['name'] == p['name'])):

                    orchestrator = KalibrOrchestrator()
                    result = orchestrator.execute_pipeline(
                        "B2B SaaS companies",
                        "Series A-B, 50+ employees",
                        max_results=2,
                        enable_reasoning=True
                    )

    return result

if __name__ == "__main__":
    print("\n" + "="*70)
    print("Testing Kalibr Orchestrator with Mock Data")
    print("="*70 + "\n")

    result = test_orchestrator_with_mocks()

    print(f"\n{'='*70}")
    print("ORCHESTRATION RESULTS")
    print(f"{'='*70}\n")

    print(f"Status: {result['status']}")
    print(f"Leads Processed: {result['stats']['successfully_processed']}/{result['stats']['total_queried']}")
    print(f"Duration: {result['stats']['duration_seconds']}s")
    print(f"Reasoning Enabled: {result['stats']['reasoning_enabled']}")

    if result['leads']:
        print(f"\n{'='*70}")
        print("TOP LEAD")
        print(f"{'='*70}\n")

        lead = result['leads'][0]
        print(f"Company: {lead['name']}")
        print(f"Score: {lead['score']}/100")
        print(f"Industry: {lead['industry']}")
        print(f"Size: {lead['company_size']}")
        print(f"Funding: {lead['funding_stage']}")
        print(f"Strategic Summary: {lead.get('reasoning_summary', 'N/A')}")
        print(f"Engagement Angles:")
        for angle in lead.get('engagement_angles', []):
            print(f"  • {angle}")
        print(f"Risk Factors:")
        for risk in lead.get('risk_factors', []):
            print(f"  • {risk}")
        print(f"Sales Motion: {lead.get('sales_motion', 'N/A')}")
        print(f"Reasoning Confidence: {lead.get('reasoning_confidence', 'N/A')}")

    print(f"\n{'='*70}")
    print("✅ Orchestrator test passed!")
    print(f"{'='*70}\n")
