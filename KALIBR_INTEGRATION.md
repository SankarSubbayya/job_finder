# Kalibr Router Integration

## Overview

MarketIntelligence now integrates **Kalibr's Router** for actual multi-model orchestration and optimization. This replaces the mock orchestrator with real intelligent routing.

---

## What Kalibr Does

Kalibr automatically:
- **Routes between models** — GPT-4o-mini vs Claude based on task requirements
- **Optimizes cost** — Selects cheaper models when quality allows
- **Tracks latency** — Monitors performance and optimizes routing
- **Handles failures** — Falls back gracefully if a model fails
- **Reports outcomes** — Learns from success/failure for future optimization

---

## Setup

### 1. Install Kalibr SDK
```bash
pip install kalibr
```

Or via requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

Your `.env` file is already configured with:
```
KALIBR_API_KEY=sk_3439d643d4ca43379d65b06a659ac49deedd338e071047d8b57bf9959c01caf9
KALIBR_TENANT_ID=user_3CXjWjZ67kxtOmcYHu7aq2WWayQ
```

**Note:** Keep these credentials private. Never commit to public repositories.

---

## Usage

### Option 1: Kalibr Router for Enrichment & Scoring

```python
from kalibr_router import route_pipeline_with_kalibr

prospects = [...]  # From scraper
enriched_and_scored = route_pipeline_with_kalibr(
    prospects,
    icp_criteria="Series A-B, 50+ employees"
)

# Output includes model_routing="kalibr_optimized"
for lead in enriched_and_scored:
    print(f"{lead['name']}: {lead['score']}/100 (via {lead['model_routing']})")
```

### Option 2: Individual Routing

```python
from kalibr_router import enrich_with_kalibr_routing, score_with_kalibr_routing

prospect = {"name": "TechCorp", "snippet": "Enterprise AI"}

# Enrich via Kalibr (routes to optimal model)
enriched = enrich_with_kalibr_routing(prospect)

# Score via Kalibr
scored = score_with_kalibr_routing(enriched, "Series A-B")
```

### Option 3: Integrated in Orchestrator

Update `kalibr_orchestrator.py` to use Kalibr Router:

```python
from kalibr_router import route_pipeline_with_kalibr

class KalibrOrchestrator:
    def execute_pipeline(self, search_query, icp_criteria, max_results=10):
        # Stage 1: Scrape (Apify)
        prospects = scrape_prospects(search_query, max_results)
        
        # Stages 2-3: Enrich & Score (via Kalibr Router)
        scored = route_pipeline_with_kalibr(prospects, icp_criteria)
        
        # Stage 4: Reason (Extended Thinking)
        reasoned = self._stage_reason(scored, icp_criteria)
        
        return reasoned
```

---

## API Endpoints

The Flask API automatically uses Kalibr Router when available:

```bash
curl -X POST http://localhost:5000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query": "B2B SaaS", "icp": "Series A-B", "reasoning": true}'
```

Response includes `model_routing: "kalibr_optimized"` for Kalibr-routed calls.

---

## Monitoring

### Kalibr Dashboard

View routing decisions, costs, and latency:
- **URL:** https://app.kalibr.com
- **Sign in:** Use your email
- **Dashboard:** Shows model selection history and performance

### Local Logging

Kalibr Router logs routing decisions to console:
```
🛣️  Using Kalibr Router for multi-model optimization...
  [1/10] Enriching (Kalibr routed): CloudFirst AI...
  ✅ Routed to: gpt-4o-mini (cost optimized)
  [2/10] Scoring (Kalibr routed): DataFlow Systems...
  ✅ Routed to: claude-3-5-haiku (latency optimized)
```

---

## Fallback Behavior

If Kalibr is unavailable:
1. Check if Kalibr SDK is installed
2. Check if API credentials are set in `.env`
3. If either is missing, gracefully fallback to direct Claude calls
4. No errors — system continues normally

This ensures the application works even without Kalibr active.

---

## Hackathon Advantage

**Multi-Model Routing Showcase:**
- ✅ Demonstrates sophisticated agent orchestration
- ✅ Shows cost optimization through model selection
- ✅ Proves failure recovery and resilience
- ✅ Real-time performance monitoring

**Kalibr positioning for judges:**
- "Our system uses Kalibr to route between models, optimizing for cost and latency"
- "Automatic recovery if GPT-4o fails — falls back to Claude seamlessly"
- "Dashboard shows routing decisions and performance metrics"

---

## Next Steps

1. **Install Kalibr SDK:**
   ```bash
   pip install kalibr
   ```

2. **Test Kalibr Router:**
   ```bash
   python -c "from kalibr_router import get_kalibr_router; print(get_kalibr_router())"
   ```

3. **Update Orchestrator** (optional):
   Integrate `route_pipeline_with_kalibr` into main orchestration flow

4. **Monitor Performance:**
   Check Kalibr dashboard at https://app.kalibr.com for routing analytics

---

## Troubleshooting

### "Kalibr SDK not installed"
```bash
pip install kalibr
```

### "Kalibr credentials not set"
- Check `.env` file exists
- Verify `KALIBR_API_KEY` and `KALIBR_TENANT_ID` are set
- Run: `echo $KALIBR_API_KEY` to verify

### "Router initialization failed"
- Check API key format (should start with `sk_`)
- Verify credentials are current
- Check internet connection to Kalibr API

---

## Architecture with Kalibr

```
Apify Scraping
    ↓
Kalibr Router Stage 1: Enrichment
  ├─ Route to: gpt-4o-mini OR claude-haiku
  ├─ Success: Extract company data
  └─ Failure: Fallback to direct Claude
    ↓
Kalibr Router Stage 2: Scoring
  ├─ Route to: gpt-4o-mini OR claude-opus
  ├─ Success: Compute relevance score
  └─ Failure: Fallback to direct Claude
    ↓
Extended Thinking: Deep Reasoning
  (Always Claude Opus for quality)
    ↓
Lovable Dashboard
```

---

**Ready to scale with intelligent multi-model routing!** 🚀
