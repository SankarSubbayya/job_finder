"""
Kalibr Orchestrator - Multi-model agent workflow management.

Orchestrates the complete MarketIntelligence pipeline with:
- Multi-stage routing (scrape → enrich → score → reason)
- Error recovery and fallback logic
- Performance monitoring
- Model selection and optimization
"""

import json
from typing import Dict, List, Optional
from datetime import datetime
import traceback

from scraper import scrape_prospects
from enricher import enrich_prospect
from scorer import score_prospect
from reasoning_layer import analyze_lead_deeply

class KalibrOrchestrator:
    """
    Orchestrates multi-model pipeline with routing, error handling, and recovery.

    Implements Kalibr patterns:
    - Stage routing: each stage can fail independently with recovery
    - Model selection: choose optimal model for each task
    - Error handling: graceful degradation on API failures
    - Performance tracking: monitor latency and success rates
    """

    def __init__(self):
        self.stage_results = {}
        self.errors = []
        self.performance = {}

    def execute_pipeline(
        self,
        search_query: str,
        icp_criteria: str = None,
        max_results: int = 10,
        enable_reasoning: bool = True
    ) -> Dict:
        """
        Execute full multi-stage pipeline with orchestration.

        Stages:
        1. SCRAPE: Apify discovers prospects
        2. ENRICH: Claude analyzes companies
        3. SCORE: Claude ranks by relevance
        4. REASON: Extended thinking for deep analysis (optional)

        Args:
            search_query: What prospects to find
            icp_criteria: Ideal customer profile
            max_results: Max prospects to return
            enable_reasoning: Include deep reasoning stage

        Returns:
            {
                "status": "success" | "partial" | "error",
                "leads": [...analyzed prospects...],
                "stats": {
                    "total_queried": int,
                    "successfully_processed": int,
                    "failed": int,
                    "reasoning_enabled": bool,
                    "duration_seconds": float
                },
                "errors": [list of errors if any]
            }
        """
        start_time = datetime.now()

        if not icp_criteria:
            icp_criteria = "B2B SaaS companies with 50+ employees"

        print(f"\n{'='*60}")
        print(f"🚀 Kalibr Orchestrator - Multi-Model Pipeline")
        print(f"{'='*60}")
        print(f"Query: {search_query}")
        print(f"ICP: {icp_criteria}")
        print(f"Reasoning: {'Enabled' if enable_reasoning else 'Disabled'}")
        print(f"{'='*60}\n")

        try:
            # STAGE 1: SCRAPE (Apify)
            print("📍 STAGE 1: SCRAPE (Apify)")
            prospects = self._stage_scrape(search_query, max_results)
            if not prospects:
                return self._error_response("Scraping failed - no prospects found", start_time)

            # STAGE 2: ENRICH (Claude)
            print("\n📍 STAGE 2: ENRICH (Claude API)")
            enriched = self._stage_enrich(prospects)

            # STAGE 3: SCORE (Claude)
            print("\n📍 STAGE 3: SCORE (Claude API)")
            scored = self._stage_score(enriched, icp_criteria)
            scored.sort(key=lambda p: p.get("score", 0), reverse=True)

            # STAGE 4: REASON (Extended Thinking) - Optional
            if enable_reasoning:
                print("\n📍 STAGE 4: REASON (Extended Thinking)")
                reasoned = self._stage_reason(scored, icp_criteria)
            else:
                reasoned = scored

            # Success response
            duration = (datetime.now() - start_time).total_seconds()
            return {
                "status": "success",
                "leads": reasoned,
                "stats": {
                    "total_queried": len(prospects),
                    "successfully_processed": len(reasoned),
                    "failed": len(prospects) - len(reasoned),
                    "reasoning_enabled": enable_reasoning,
                    "duration_seconds": round(duration, 2),
                },
                "errors": self.errors,
            }

        except Exception as e:
            return self._error_response(f"Pipeline error: {str(e)}", start_time)

    def _stage_scrape(self, query: str, limit: int) -> List[Dict]:
        """Stage 1: Scrape prospects via Apify."""
        try:
            print(f"  🔍 Scraping {limit} prospects...")
            prospects = scrape_prospects(query, limit=limit)
            print(f"  ✅ Found {len(prospects)} prospects")
            return prospects
        except Exception as e:
            self.errors.append(f"Scrape failed: {str(e)}")
            print(f"  ❌ Scrape error: {str(e)}")
            return []

    def _stage_enrich(self, prospects: List[Dict]) -> List[Dict]:
        """Stage 2: Enrich with company research."""
        enriched = []
        for i, prospect in enumerate(prospects, 1):
            try:
                print(f"  [{i}/{len(prospects)}] Enriching {prospect.get('name', 'Unknown')}...")
                enriched_prospect = enrich_prospect(prospect)
                enriched.append(enriched_prospect)
            except Exception as e:
                self.errors.append(f"Enrichment failed for {prospect.get('name')}: {str(e)}")
                print(f"  ⚠ Enrichment error: {str(e)}")
                # Continue with next prospect (graceful degradation)
        print(f"  ✅ Enriched {len(enriched)}/{len(prospects)} prospects")
        return enriched

    def _stage_score(self, prospects: List[Dict], icp_criteria: str) -> List[Dict]:
        """Stage 3: Score prospects."""
        scored = []
        for i, prospect in enumerate(prospects, 1):
            try:
                print(f"  [{i}/{len(prospects)}] Scoring {prospect.get('name', 'Unknown')}...")
                scored_prospect = score_prospect(prospect, icp_criteria)
                scored.append(scored_prospect)
            except Exception as e:
                self.errors.append(f"Scoring failed for {prospect.get('name')}: {str(e)}")
                print(f"  ⚠ Scoring error: {str(e)}")
        print(f"  ✅ Scored {len(scored)}/{len(prospects)} prospects")
        return scored

    def _stage_reason(self, prospects: List[Dict], icp_criteria: str) -> List[Dict]:
        """Stage 4: Deep reasoning with extended thinking."""
        reasoned = []
        for i, prospect in enumerate(prospects, 1):
            try:
                print(f"  [{i}/{len(prospects)}] Reasoning about {prospect.get('name', 'Unknown')}...")
                reasoned_prospect = analyze_lead_deeply(prospect, icp_criteria)
                reasoned.append(reasoned_prospect)
            except Exception as e:
                self.errors.append(f"Reasoning failed for {prospect.get('name')}: {str(e)}")
                print(f"  ⚠ Reasoning error: {str(e)}")
                # Fall back to scored prospect without reasoning
                reasoned.append(prospect)
        print(f"  ✅ Reasoned about {len(reasoned)}/{len(prospects)} prospects")
        return reasoned

    def _error_response(self, error: str, start_time) -> Dict:
        """Format error response."""
        duration = (datetime.now() - start_time).total_seconds()
        self.errors.append(error)
        return {
            "status": "error",
            "leads": [],
            "error": error,
            "stats": {
                "duration_seconds": round(duration, 2),
            },
            "errors": self.errors,
        }


# Global instance
orchestrator = KalibrOrchestrator()


def run_orchestrated_pipeline(
    search_query: str,
    icp_criteria: str = None,
    max_results: int = 10,
    enable_reasoning: bool = True
) -> Dict:
    """
    Execute the orchestrated multi-model pipeline.

    This is the main entry point for the app and Lovable UI.

    Args:
        search_query: Prospect search query
        icp_criteria: ICP description
        max_results: Max prospects
        enable_reasoning: Include extended thinking analysis

    Returns:
        Pipeline result dict with leads and stats
    """
    return orchestrator.execute_pipeline(
        search_query,
        icp_criteria,
        max_results,
        enable_reasoning
    )
