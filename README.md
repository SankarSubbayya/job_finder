# MarketIntelligence — Enterprise Lead Intelligence Platform

> **An orchestrated multi-model GTM agent that discovers, reasons about, and qualifies B2B prospects for enterprise sales teams.**

**Discover. Reason. Engage.**

---

## Overview

MarketIntelligence is an enterprise-grade lead intelligence system built for the **Marketing Agents Hackathon** (April 18, 2026). It orchestrates a sophisticated multi-stage pipeline:

1. **🔍 DISCOVER** — Apify scrapes target companies from the web
2. **📊 ENRICH** — Claude analyzes company data (industry, size, funding, pain points, decision-makers)
3. **⭐ SCORE** — Claude scores prospects for ICP fit (0-100)
4. **🧠 REASON** — Claude extended thinking performs deep strategic analysis
5. **📈 PRESENT** — Lovable enterprise dashboard visualizes insights for sales teams

The **Kalibr orchestrator** manages the entire pipeline with multi-model routing, error recovery, and performance optimization. Perfect for GTM teams that need **intelligent prospect qualification at scale**.

---

## ✨ Features

### Core Pipeline
- 🕷️ **Apify Web Scraping** — Discovers thousands of prospects efficiently
- 🧠 **Multi-Stage Claude Analysis** — Enrichment → Scoring → Deep Reasoning
- 💭 **Extended Thinking** — Claude's chain-of-thought for strategic insights
- 🛣️ **Kalibr Orchestration** — Multi-model routing, error recovery, optimization

### Intelligence
- ⭐ **Prospect Scoring** — Semantic relevance (0-100) with reasoning
- 🎯 **Engagement Angles** — Personalized outreach strategies per prospect
- ⚠️ **Risk Assessment** — Identifies blockers and objections
- 💼 **Sales Motion** — Recommends contact approach per prospect

### Enterprise UI
- 📊 **Lovable Dashboard** — Modern, responsive interface (React/Next.js)
- 🔍 **Search & Insights** — Historical analysis of top industries/funding stages
- 📈 **Analytics** — ICP pattern discovery, lead ranking
- 💾 **Export** — CSV download, CRM integration ready

### Developer Experience
- 🧪 **Comprehensive Testing** — Unit tests + orchestrator validation
- 📚 **Full Documentation** — API specs, deployment guides
- 🔌 **REST API** — CORS-enabled for cross-origin requests
- 📦 **Modular Architecture** — Reusable components

---

## Tech Stack

### Backend
- **Python 3.8+** — Core application
- **Apify** — Web scraping (hackathon sponsor)
- **Kalibr** — Multi-model orchestration (hackathon sponsor)
- **Claude API** (Anthropic) — Enrichment, scoring, reasoning (Opus 4.7)
- **Flask** — REST API server
- **flask-cors** — Cross-origin support for Lovable

### Frontend
- **Lovable** — Enterprise dashboard builder (hackathon sponsor)
- **React/Next.js** — Generated UI framework
- **Modern CSS** — Dark mode, responsive design

### Testing & Tools
- **pytest** — Test framework
- **Mock data** — Demo without API keys

---

## Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with uv (preferred):
```bash
uv pip install -r requirements.txt
```

### 2. Get API Keys

- **Apify Token**: [https://console.apify.com/account/integrations](https://console.apify.com/account/integrations)
- **Anthropic API Key**: [https://console.anthropic.com/account/keys](https://console.anthropic.com/account/keys)

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your API keys:
# APIFY_TOKEN=sk-xxx...
# ANTHROPIC_API_KEY=sk-ant-xxx...
```

---

## Architecture

```
┌──────────────────────────────────────────┐
│   Lovable Enterprise Dashboard           │
│   (React/Next.js UI on lovable.dev)      │
└────────────────┬─────────────────────────┘
                 │ REST API (CORS)
    ┌────────────▼──────────────────────┐
    │   Flask Backend (app.py)           │
    │  ┌──────────────────────────────┐ │
    │  │  Kalibr Orchestrator         │ │
    │  │  - Multi-model routing       │ │
    │  │  - Error recovery            │ │
    │  │  - Performance monitoring    │ │
    │  └──────────────────────────────┘ │
    │                                   │
    │  ┌──────────────────────────────┐ │
    │  │  Reasoning Layer             │ │
    │  │  - Extended thinking         │ │
    │  │  - Strategic analysis        │ │
    │  └──────────────────────────────┘ │
    │                                   │
    │  ┌──────────────────────────────┐ │
    │  │  Enrichment & Scoring        │ │
    │  │  - Claude Opus enrichment    │ │
    │  │  - Claude Opus scoring       │ │
    │  └──────────────────────────────┘ │
    │                                   │
    │  ┌──────────────────────────────┐ │
    │  │  Scraping                    │ │
    │  │  - Apify actor integration   │ │
    │  └──────────────────────────────┘ │
    └────────────────────────────────────┘
```

---

## Usage

### Option 1: Enterprise Dashboard (Recommended)

1. **Build with Lovable**
   ```bash
   # Instructions at LOVABLE_PROMPT.md
   # Copy prompt to lovable.dev to generate UI
   ```

2. **Start Flask backend**
   ```bash
   python app.py
   ```
   Server runs on `http://localhost:5000`

3. **Connect Lovable dashboard**
   - Point to `http://localhost:5000`
   - Search for prospects with deep reasoning
   - View engagement angles, risk factors, sales motion
   - Analyze ICP patterns and insights

### Option 2: REST API (For Integrations)

```bash
python app.py
```

**Endpoints:**
- `POST /api/search` — Trigger discovery pipeline
- `GET /api/results/{id}` — Get results with reasoning
- `GET /api/history` — Search history
- `GET /api/leads` — All discovered leads
- `GET /api/insights` — ICP analytics

### Option 3: Python CLI

```bash
python market_intelligence.py "B2B SaaS in fintech" "Series A-B"
```

Or with orchestration:
```python
from kalibr_orchestrator import run_orchestrated_pipeline

result = run_orchestrated_pipeline(
    search_query="Fintech startups",
    icp_criteria="Series A-B, 50+ employees",
    enable_reasoning=True
)

for lead in result['leads']:
    print(f"{lead['name']}: {lead['score']}/100")
    print(f"  Angles: {lead['engagement_angles']}")
    print(f"  Risks: {lead['risk_factors']}")
```

### Option 4: Demo (No API Keys)

```bash
python demo.py
```

See full pipeline with mock data — perfect for testing without credentials.

---

## Project Structure

```
MarketIntelligence/
├── Core Pipeline
│   ├── scraper.py                  # Apify integration
│   ├── enricher.py                 # Claude enrichment (industry, size, pain points)
│   ├── scorer.py                   # Claude scoring (0-100 relevance)
│   ├── reasoning_layer.py          # Extended thinking deep analysis
│   └── market_intelligence.py      # Legacy orchestrator (backward compat)
│
├── Orchestration
│   ├── kalibr_orchestrator.py      # Multi-model routing & recovery
│   └── app.py                      # Flask REST API
│
├── Frontend & Docs
│   ├── templates/index.html        # Built-in web UI
│   ├── static/style.css            # Dark mode CSS
│   ├── LOVABLE_PROMPT.md           # Lovable dashboard spec
│   └── README.md                   # This file
│
├── Testing & Demo
│   ├── test_components.py          # Unit tests
│   ├── test_orchestrator.py        # Orchestrator validation
│   ├── demo.py                     # Works without API keys
│   └── demo_results.json           # Sample output
│
├── Config & Docs
│   ├── requirements.txt            # Python dependencies
│   ├── pyproject.toml              # Project metadata
│   ├── .env.example                # API key template
│   └── SUBMISSION.md               # Hackathon submission
```

---

## Multi-Model Orchestration

The **Kalibr orchestrator** manages the full pipeline:

```
Stage 1: SCRAPE (Apify)
  ↓ (error recovery: fallback to mock data)
Stage 2: ENRICH (Claude Opus)
  ↓ (field extraction: industry, size, funding, pain points)
Stage 3: SCORE (Claude Opus)
  ↓ (relevance scoring: 0-100 with reasoning)
Stage 4: REASON (Extended Thinking)
  ↓ (strategic analysis: engagement angles, risks, sales motion)
Output: Enriched leads ready for Lovable dashboard
```

Each stage includes:
- **Error handling** — Graceful degradation if APIs fail
- **Recovery** — Fallback to mock data or previous stage results
- **Monitoring** — Track latency and success rates
- **Model selection** — Choose optimal Claude model per task

---

## Example Output (With Deep Reasoning)

```json
{
  "name": "CloudFirst AI",
  "url": "https://cloudfirst.ai",
  "industry": "Enterprise AI/ML",
  "company_size": "100-200",
  "funding_stage": "Series B",
  "pain_points": ["ML Operations", "Data Governance"],
  "decision_makers": ["VP Engineering", "CTO"],
  "score": 85,
  "score_reason": "Excellent ICP fit: Series B, right size, strong pain point alignment",
  "engagement_level": "high",
  "reasoning_summary": "Strong prospect with clear product-market fit",
  "engagement_angles": [
    "Address ML Operations challenges in enterprise",
    "Series B funding shows growth trajectory and budget",
    "Peer adoption in Enterprise AI industry"
  ],
  "risk_factors": [
    "Existing vendor relationships may create inertia",
    "Long enterprise sales cycles"
  ],
  "sales_motion": "Warm introduction from industry analyst + ROI case study",
  "reasoning_confidence": "high"
}
```

---

## Testing

### Run All Tests

```bash
source .venv/bin/activate
pytest test_components.py -v
```

### Test Orchestrator with Mocks

```bash
python test_orchestrator.py
```

Shows full 4-stage pipeline (Scrape → Enrich → Score → Reason) without API calls.

### Demo (No API Keys Required)

```bash
python demo.py
```

Tests include:
- ✅ Scraper mock data validation
- ✅ Orchestrator multi-stage flow
- ✅ Error recovery patterns
- ✅ Reasoning output quality

---

## API Reference

### REST Endpoints

#### `POST /api/search`
Trigger the orchestrated pipeline.
```json
{ "query": "B2B SaaS", "icp": "Series A-B", "reasoning": true }
```
Returns: `{ "search_id": "uuid" }`

#### `GET /api/results/{search_id}`
Get results with full lead intelligence.
- **Status:** `success` | `partial` | `error`
- **Leads:** Full prospect objects with reasoning
- **Stats:** Pipeline duration, success rates

#### `GET /api/history`
Return past searches and their stats.

#### `GET /api/leads`
All discovered leads across all searches.

#### `GET /api/insights`
ICP analytics: top industries, funding stages, pain points.

### Python SDK

#### `kalibr_orchestrator.run_orchestrated_pipeline(query, icp, max_results, enable_reasoning)`
Run the full multi-model pipeline with orchestration.
```python
from kalibr_orchestrator import run_orchestrated_pipeline

result = run_orchestrated_pipeline(
    search_query="Fintech SaaS",
    icp_criteria="Series A-B, 50+ employees",
    max_results=10,
    enable_reasoning=True  # Include extended thinking
)

for lead in result['leads']:
    print(f"{lead['name']}: {lead['reasoning_summary']}")
    for angle in lead['engagement_angles']:
        print(f"  → {angle}")
```

---

## Hackathon Integration

### Sponsor Awards

Built for the **Marketing Agents Hackathon** (April 18, 2026) with deep integration of sponsor tools:

| Sponsor | Integration | Award Path |
|---------|-------------|------------|
| **Apify** | Google Search actor for prospect discovery | 🥇 Best use of Apify ($500 cash) |
| **Kalibr** | Multi-model orchestration, error recovery, routing | Orchestration excellence |
| **Lovable** | Enterprise dashboard builder (React/Next.js) | Production UI |

### Challenge Alignment

✅ **"Find ICPs, qualify leads, ship campaigns"**
- Discover: Apify finds target companies
- Qualify: Claude scores with reasoning
- Ship: Lovable dashboard → Sales team

✅ **"Orchestrated agent systems"**
- Kalibr manages 4-stage pipeline
- Each stage can fail independently with recovery
- Multi-model routing (Claude Opus for enrichment + reasoning)

✅ **"Measurable outcomes"**
- Prospect scores (0-100) with explanations
- Engagement angles (personalized per prospect)
- Risk assessment and sales motion recommendations
- Historical pattern analysis

---

## Future Enhancements

- Async pipeline for real-time processing
- CRM integration (Salesforce, HubSpot)
- Advanced filtering (location, industry, funding)
- Email outreach templating
- Performance analytics

---

## License

MIT

---

*Built with ❤️ for the Marketing Agents Hackathon 2026*
