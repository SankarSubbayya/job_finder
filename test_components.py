import pytest
from unittest.mock import patch, MagicMock
from scraper import scrape_prospects, _get_mock_prospects
from enricher import enrich_prospect
from scorer import score_prospect

class TestScraper:
    """Unit tests for scraper.py"""

    def test_get_mock_prospects_returns_list(self):
        """Mock prospects should return a list."""
        prospects = _get_mock_prospects(5)
        assert isinstance(prospects, list)
        assert len(prospects) == 5

    def test_get_mock_prospects_has_required_fields(self):
        """Each prospect should have required fields."""
        prospects = _get_mock_prospects(1)
        assert "name" in prospects[0]
        assert "url" in prospects[0]
        assert "snippet" in prospects[0]
        assert "source" in prospects[0]

    def test_mock_prospect_limit(self):
        """Should respect max limit."""
        prospects = _get_mock_prospects(10)
        assert len(prospects) <= 10

    @patch('scraper.ApifyClient')
    def test_scrape_prospects_fallback_on_error(self, mock_apify):
        """Should fallback to mock data on Apify error."""
        mock_apify.side_effect = Exception("API Error")
        prospects = scrape_prospects("test query", limit=5)
        assert isinstance(prospects, list)
        assert len(prospects) > 0

class TestEnricher:
    """Unit tests for enricher.py"""

    def test_enrich_prospect_preserves_original_fields(self):
        """Enrichment should preserve original prospect data."""
        prospect = {
            "name": "Test Corp",
            "url": "https://testcorp.com",
            "snippet": "A test company"
        }
        result = enrich_prospect(prospect)
        assert result["name"] == "Test Corp"
        assert result["url"] == "https://testcorp.com"

    def test_enrich_prospect_adds_enrichment_fields(self):
        """Enrichment should add expected fields."""
        prospect = {
            "name": "Test Corp",
            "url": "https://testcorp.com",
            "snippet": "A test company"
        }
        result = enrich_prospect(prospect)
        assert "industry" in result
        assert "company_size" in result
        assert "funding_stage" in result
        assert "pain_points" in result
        assert "decision_makers" in result

    def test_enrich_prospect_fallback_on_error(self):
        """Should provide fallback enrichment if Claude fails."""
        prospect = {"name": "Test", "url": "https://test.com", "snippet": "test"}
        with patch('enricher.client.messages.create') as mock:
            mock.side_effect = Exception("API Error")
            result = enrich_prospect(prospect)
            assert result["industry"] == "Technology"
            assert result["company_size"] == "50-200"

class TestScorer:
    """Unit tests for scorer.py"""

    def test_score_prospect_adds_score_fields(self):
        """Scoring should add score fields to prospect."""
        prospect = {
            "name": "Test Corp",
            "industry": "Technology",
            "company_size": "50-200",
            "funding_stage": "Series A",
            "pain_points": ["Automation"]
        }
        result = score_prospect(prospect)
        assert "score" in result
        assert "score_reason" in result
        assert "engagement_level" in result

    def test_score_prospect_score_range(self):
        """Score should be between 0-100."""
        prospect = {
            "name": "Test",
            "industry": "Tech",
            "company_size": "50+",
            "funding_stage": "A",
            "pain_points": []
        }
        result = score_prospect(prospect)
        assert 0 <= result["score"] <= 100

    def test_score_prospect_engagement_valid(self):
        """Engagement level should be valid."""
        prospect = {
            "name": "Test",
            "industry": "Tech",
            "company_size": "50+",
            "funding_stage": "A",
            "pain_points": []
        }
        result = score_prospect(prospect)
        assert result["engagement_level"] in ["high", "medium", "low"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
