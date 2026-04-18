import pytest
from scraper import _get_mock_prospects

class TestScraper:
    """Unit tests for scraper.py - mock data functions"""

    def test_get_mock_prospects_returns_list(self):
        """Mock prospects should return a list."""
        prospects = _get_mock_prospects(5)
        assert isinstance(prospects, list)
        assert len(prospects) == 5

    def test_get_mock_prospects_has_required_fields(self):
        """Each prospect should have required fields."""
        prospects = _get_mock_prospects(1)
        prospect = prospects[0]
        assert "name" in prospect
        assert "url" in prospect
        assert "snippet" in prospect
        assert "source" in prospect

    def test_mock_prospect_limit_respected(self):
        """Should respect max limit."""
        for limit in [1, 5, 10, 20]:
            prospects = _get_mock_prospects(limit)
            assert len(prospects) <= limit

    def test_mock_prospect_data_quality(self):
        """Mock prospects should have non-empty required fields."""
        prospects = _get_mock_prospects(3)
        for p in prospects:
            assert p["name"], "Prospect name should not be empty"
            assert p["url"], "Prospect URL should not be empty"
            assert p["snippet"], "Prospect snippet should not be empty"
            assert p["source"] == "mock", "Source should be 'mock'"

    def test_mock_prospects_are_unique(self):
        """Mock prospects should be distinct (no exact duplicates)."""
        prospects = _get_mock_prospects(5)
        names = [p["name"] for p in prospects]
        assert len(names) == len(set(names)), "All prospect names should be unique"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
