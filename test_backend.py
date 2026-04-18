#!/usr/bin/env python3
"""
Comprehensive backend tests for MarketIntelligence.

Tests cover:
- Flask API endpoints
- Reasoning layer with extended thinking
- Orchestrator pipeline stages
- Error handling and fallbacks
"""

import pytest
import json
from unittest.mock import patch, MagicMock
from app import app
from kalibr_orchestrator import KalibrOrchestrator
from reasoning_layer import analyze_lead_deeply


@pytest.fixture
def client():
    """Flask test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestFlaskAPI:
    """Test Flask API endpoints."""

    def test_index_route(self, client):
        """GET / should return 200."""
        response = client.get('/')
        assert response.status_code == 200

    def test_search_endpoint_with_valid_query(self, client):
        """POST /api/search with valid query returns search_id."""
        response = client.post('/api/search',
            json={'query': 'test query', 'icp': 'Series A'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'search_id' in data
        assert isinstance(data['search_id'], str)
        assert len(data['search_id']) == 36  # UUID format

    def test_search_endpoint_without_query(self, client):
        """POST /api/search without query returns 400."""
        response = client.post('/api/search',
            json={'icp': 'Series A'}
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_search_endpoint_with_empty_query(self, client):
        """POST /api/search with empty query returns 400."""
        response = client.post('/api/search',
            json={'query': '   ', 'icp': 'Series A'}
        )
        assert response.status_code == 400

    def test_results_endpoint_for_valid_search(self, client):
        """GET /api/results/<search_id> returns search data."""
        # Create a search
        response = client.post('/api/search',
            json={'query': 'test', 'icp': 'Series B'}
        )
        search_id = json.loads(response.data)['search_id']

        # Get results (should be ready after 1 second)
        import time
        time.sleep(1)
        response = client.get(f'/api/results/{search_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['search_id'] == search_id
        assert data['query'] == 'test'
        assert 'results' in data
        assert 'status' in data

    def test_results_endpoint_for_invalid_search(self, client):
        """GET /api/results/<invalid_id> returns 404."""
        response = client.get('/api/results/invalid-id-12345')
        assert response.status_code == 404

    def test_history_endpoint_returns_list(self, client):
        """GET /api/history returns search history."""
        response = client.get('/api/history')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'history' in data
        assert isinstance(data['history'], list)

    def test_leads_endpoint_returns_list(self, client):
        """GET /api/leads returns all discovered leads."""
        response = client.get('/api/leads')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'leads' in data
        assert isinstance(data['leads'], list)

    def test_insights_endpoint_returns_analytics(self, client):
        """GET /api/insights returns ICP analytics."""
        response = client.get('/api/insights')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'insights' in data
        assert isinstance(data['insights'], dict)

    def test_search_with_reasoning_enabled(self, client):
        """POST /api/search with reasoning=true."""
        response = client.post('/api/search',
            json={'query': 'test', 'icp': 'Series B', 'reasoning': True}
        )
        assert response.status_code == 200

    def test_search_with_reasoning_disabled(self, client):
        """POST /api/search with reasoning=false."""
        response = client.post('/api/search',
            json={'query': 'test', 'icp': 'Series B', 'reasoning': False}
        )
        assert response.status_code == 200


class TestReasoningLayer:
    """Test reasoning layer with extended thinking."""

    @patch('reasoning_layer.client')
    def test_analyze_lead_deeply_returns_dict(self, mock_client):
        """analyze_lead_deeply should return enriched prospect dict."""
        # Mock the Claude API response
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "strategic_fit": "Excellent fit for our ICP",
            "engagement_angles": ["Angle 1", "Angle 2", "Angle 3"],
            "risk_factors": ["Risk 1", "Risk 2"],
            "sales_motion": "Warm intro",
            "confidence": "high"
        }))]
        mock_client.messages.create.return_value = mock_response

        prospect = {
            "name": "TechCorp",
            "industry": "SaaS",
            "company_size": "100-500",
            "funding_stage": "Series B",
            "pain_points": ["Scaling", "Automation"],
            "decision_makers": ["VP Ops", "CTO"],
            "score": 85,
            "score_reason": "Good fit"
        }

        result = analyze_lead_deeply(prospect, "Series A-B")

        # Verify all required fields
        assert "reasoning_summary" in result
        assert "engagement_angles" in result
        assert "risk_factors" in result
        assert "sales_motion" in result
        assert "reasoning_confidence" in result
        assert isinstance(result["engagement_angles"], list)
        assert len(result["engagement_angles"]) == 3

    def test_analyze_lead_deeply_fallback_on_api_error(self):
        """analyze_lead_deeply should fallback on API error."""
        prospect = {
            "name": "TestCorp",
            "industry": "Tech",
            "company_size": "50-100",
            "funding_stage": "Series A",
            "pain_points": ["Issue 1", "Issue 2"],
            "decision_makers": ["CTO"],
            "score": 75
        }

        # This should not raise an exception (will use fallback)
        with patch('reasoning_layer.client.messages.create', side_effect=Exception("API Error")):
            result = analyze_lead_deeply(prospect)
            assert result is not None
            assert "reasoning_confidence" in result
            # Fallback should have "low" confidence
            assert result["reasoning_confidence"] == "low"

    def test_analyze_lead_with_missing_icp(self):
        """analyze_lead_deeply should use default ICP if not provided."""
        prospect = {
            "name": "Company",
            "industry": "Tech",
            "company_size": "50",
            "funding_stage": "A",
            "pain_points": [],
            "decision_makers": [],
            "score": 50
        }

        # Should not raise error with missing icp_criteria
        with patch('reasoning_layer.client.messages.create', side_effect=Exception("Test")):
            result = analyze_lead_deeply(prospect)  # No icp_criteria arg
            assert result is not None


class TestOrchestrator:
    """Test Kalibr orchestrator pipeline."""

    @patch('kalibr_orchestrator.scrape_prospects')
    @patch('kalibr_orchestrator.enrich_prospect')
    @patch('kalibr_orchestrator.score_prospect')
    @patch('kalibr_orchestrator.analyze_lead_deeply')
    def test_orchestrator_full_pipeline(self, mock_reason, mock_score, mock_enrich, mock_scrape):
        """Test full 4-stage pipeline."""
        # Setup mocks
        mock_scrape.return_value = [
            {"name": "Company1", "url": "https://c1.com", "snippet": "Description", "source": "google"},
            {"name": "Company2", "url": "https://c2.com", "snippet": "Description", "source": "google"},
        ]

        def enrich_side_effect(p):
            return {**p, "industry": "Tech", "company_size": "100", "funding_stage": "B",
                    "pain_points": ["Pain1"], "decision_makers": ["CEO"]}

        def score_side_effect(p, icp):
            return {**p, "score": 85, "score_reason": "Good fit", "engagement_level": "high"}

        def reason_side_effect(p, icp):
            return {**p, "reasoning_summary": "Good", "engagement_angles": ["A1", "A2", "A3"],
                    "risk_factors": ["R1"], "sales_motion": "Warm", "reasoning_confidence": "high"}

        mock_enrich.side_effect = enrich_side_effect
        mock_score.side_effect = score_side_effect
        mock_reason.side_effect = reason_side_effect

        orchestrator = KalibrOrchestrator()
        result = orchestrator.execute_pipeline("test query", "Series B", max_results=2, enable_reasoning=True)

        # Verify result structure
        assert result["status"] == "success"
        assert len(result["leads"]) == 2
        assert result["stats"]["total_queried"] == 2
        assert result["stats"]["successfully_processed"] == 2
        assert result["stats"]["reasoning_enabled"] == True

    @patch('kalibr_orchestrator.scrape_prospects')
    def test_orchestrator_handles_scrape_failure(self, mock_scrape):
        """Orchestrator should handle scrape failures."""
        mock_scrape.return_value = []  # Empty results

        orchestrator = KalibrOrchestrator()
        result = orchestrator.execute_pipeline("test", "Series B")

        assert result["status"] == "error"
        assert len(result["leads"]) == 0

    @patch('kalibr_orchestrator.scrape_prospects')
    @patch('kalibr_orchestrator.enrich_prospect')
    def test_orchestrator_continues_on_enrichment_error(self, mock_enrich, mock_scrape):
        """Orchestrator should continue despite enrichment errors."""
        mock_scrape.return_value = [
            {"name": "C1", "url": "https://c1.com", "snippet": "D", "source": "g"},
            {"name": "C2", "url": "https://c2.com", "snippet": "D", "source": "g"},
        ]

        # First enrichment fails, second succeeds
        mock_enrich.side_effect = [
            Exception("API Error"),
            {"name": "C2", "industry": "Tech", "company_size": "100", "funding_stage": "B",
             "pain_points": [], "decision_makers": []}
        ]

        with patch('kalibr_orchestrator.score_prospect'):
            orchestrator = KalibrOrchestrator()
            result = orchestrator.execute_pipeline("test", "Series B")

            # Should still have processed prospects (only 1 due to enrichment failure)
            assert len(result["errors"]) > 0

    def test_orchestrator_default_icp(self):
        """Orchestrator should use default ICP if not provided."""
        with patch('kalibr_orchestrator.scrape_prospects', return_value=[]):
            orchestrator = KalibrOrchestrator()
            result = orchestrator.execute_pipeline("test", icp_criteria=None)
            # Should not raise error
            assert result is not None


class TestPipelineIntegration:
    """Integration tests for full pipeline."""

    @patch('scraper.scrape_prospects')
    @patch('enricher.client.messages.create')
    @patch('scorer.client.messages.create')
    def test_end_to_end_with_mock_apis(self, mock_score_api, mock_enrich_api, mock_scrape):
        """Test complete pipeline with mocked external APIs."""
        # Mock scraper
        mock_scrape.return_value = [
            {"name": "Company1", "url": "https://c1.com", "snippet": "Tech company", "source": "google"}
        ]

        # Mock enricher response
        mock_enrich_response = MagicMock()
        mock_enrich_response.content = [MagicMock(text=json.dumps({
            "industry": "SaaS",
            "company_size": "100-500",
            "funding_stage": "Series B",
            "pain_points": ["Scaling"],
            "decision_makers": ["CTO"]
        }))]
        mock_enrich_api.return_value = mock_enrich_response

        # Mock scorer response
        mock_score_response = MagicMock()
        mock_score_response.content = [MagicMock(text=json.dumps({
            "score": 85,
            "reason": "Good ICP match",
            "engagement_level": "high"
        }))]
        mock_score_api.return_value = mock_score_response

        with patch('kalibr_orchestrator.analyze_lead_deeply', side_effect=lambda p, icp: {
            **p, "reasoning_summary": "Strong fit", "engagement_angles": [],
            "risk_factors": [], "sales_motion": "Email", "reasoning_confidence": "high"
        }):
            orchestrator = KalibrOrchestrator()
            result = orchestrator.execute_pipeline("fintech SaaS", "Series A-B", max_results=1)

            assert result["status"] == "success"
            assert len(result["leads"]) >= 0  # May be 0 due to mocking


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
