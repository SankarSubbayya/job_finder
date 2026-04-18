import pytest
import json
from unittest.mock import patch, MagicMock
from market_intelligence import run_agent

class TestIntegration:
    """Integration tests for end-to-end pipeline"""

    @patch('market_intelligence.scrape_prospects')
    @patch('market_intelligence.enrich_prospect')
    @patch('market_intelligence.score_prospect')
    def test_end_to_end_pipeline(self, mock_score, mock_enrich, mock_scrape):
        """Test full pipeline: scrape -> enrich -> score."""
        # Setup mocks
        mock_scrape.return_value = [
            {
                "name": "TechCorp",
                "url": "https://techcorp.com",
                "snippet": "A tech company",
                "source": "google"
            }
        ]

        mock_enrich.return_value = {
            "name": "TechCorp",
            "url": "https://techcorp.com",
            "snippet": "A tech company",
            "source": "google",
            "industry": "Technology",
            "company_size": "100-500",
            "funding_stage": "Series B",
            "pain_points": ["Scaling", "Automation"],
            "decision_makers": ["VP Ops"]
        }

        mock_score.return_value = {
            "name": "TechCorp",
            "url": "https://techcorp.com",
            "snippet": "A tech company",
            "source": "google",
            "industry": "Technology",
            "company_size": "100-500",
            "funding_stage": "Series B",
            "pain_points": ["Scaling", "Automation"],
            "decision_makers": ["VP Ops"],
            "score": 85,
            "score_reason": "Good ICP fit",
            "engagement_level": "high"
        }

        # Run agent
        results = run_agent("B2B SaaS", "Series B tech companies", max_results=1)

        # Assertions
        assert isinstance(results, list)
        assert len(results) == 1
        assert results[0]["score"] == 85
        assert results[0]["name"] == "TechCorp"
        assert "industry" in results[0]
        assert "engagement_level" in results[0]

    @patch('market_intelligence.scrape_prospects')
    @patch('market_intelligence.enrich_prospect')
    @patch('market_intelligence.score_prospect')
    def test_pipeline_sorts_by_score(self, mock_score, mock_enrich, mock_scrape):
        """Results should be sorted by score (highest first)."""
        mock_scrape.return_value = [
            {"name": "Company1", "url": "https://c1.com", "snippet": "C1", "source": "g"},
            {"name": "Company2", "url": "https://c2.com", "snippet": "C2", "source": "g"},
            {"name": "Company3", "url": "https://c3.com", "snippet": "C3", "source": "g"},
        ]

        # Enrichment returns same data
        mock_enrich.side_effect = lambda p: {
            **p,
            "industry": "Tech",
            "company_size": "50+",
            "funding_stage": "A",
            "pain_points": []
        }

        # Scoring with different scores
        scores = [50, 90, 70]
        mock_score.side_effect = [
            {**p, "score": s, "score_reason": f"Score {s}", "engagement_level": "medium"}
            for p, s in zip(mock_enrich.side_effect({"name": "C", "url": "", "snippet": "", "source": ""}), scores)
        ]

        # We need to mock properly for 3 companies
        def score_side_effect(prospect, icp=None):
            name_to_score = {"Company1": 50, "Company2": 90, "Company3": 70}
            score = name_to_score.get(prospect.get("name"), 0)
            return {
                **prospect,
                "score": score,
                "score_reason": f"Score {score}",
                "engagement_level": "high" if score >= 80 else "medium"
            }

        mock_score.side_effect = score_side_effect

        results = run_agent("B2B SaaS", max_results=3)

        # Check ordering
        assert results[0]["score"] == 90  # Highest first
        assert results[1]["score"] == 70
        assert results[2]["score"] == 50

    @patch('market_intelligence.scrape_prospects')
    def test_pipeline_handles_no_results(self, mock_scrape):
        """Pipeline should handle gracefully when no prospects found."""
        mock_scrape.return_value = []
        results = run_agent("nonexistent query", max_results=5)
        assert isinstance(results, list)
        assert len(results) == 0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
