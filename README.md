# MarketIntelligence

> **An autonomous lead intelligence GTM agent that discovers, enriches, and qualifies prospects using advanced web scraping and AI-powered scoring.**

Discover. Score. Engage.

---

## Overview

MarketIntelligence is a GTM agent built for the **Marketing Agents Hackathon** (April 18, 2026). It automates the end-to-end prospect discovery and qualification workflow:

1. **Discover** — Scrape target companies via Apify web scraping
2. **Enrich** — Analyze company data with Claude AI (industry, size, funding, pain points)
3. **Score** — Intelligently qualify leads with AI-powered relevance scoring (0-100)
4. **Engage** — Present actionable, ranked prospects ready for outreach

Perfect for GTM teams that need to **find ICPs, qualify leads, and scale outreach**.

---

## ✨ Features

- 🕷️ **Apify Web Scraping** — Discovers high-intent prospects at scale
- 🧠 **Claude AI Enrichment** — Intelligent company research and analysis
- ⭐ **AI-Powered Scoring** — Semantic relevance scoring (0-100) with reasoning
- 🌐 **Modern Web UI** — Claude-inspired interface with real-time progress
- ⚡ **End-to-End Pipeline** — Scrape → Enrich → Score in minutes
- 📊 **Structured Output** — JSON results ready for CRM integration
- 🧪 **Comprehensive Tests** — Unit and integration test coverage

---

## Tech Stack

- **Python 3.8+** — Core orchestration
- **Apify** — Web scraping actor platform
- **Claude API** (Anthropic) — AI enrichment and scoring
- **Flask** — Web server for UI
- **pytest** — Testing framework

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

## Usage

### Option 1: Web UI (Recommended)

```bash
python app.py
```

Visit `http://localhost:5000` and search for prospects in the Claude-style interface.

### Option 2: CLI

```bash
python market_intelligence.py "B2B SaaS companies in fintech" "Series A-B, 50+ employees"
```

Output: `leads_results.json` with scored prospects

### Option 3: Python API

```python
from market_intelligence import run_agent

results = run_agent(
    search_query="Fintech startups",
    icp_criteria="Series A-B with 50+ employees",
    max_results=10
)

for prospect in results:
    print(f"{prospect['name']}: {prospect['score']}/100")
```

---

## Project Structure

```
MarketIntelligence/
├── scraper.py                  # Apify integration for prospect discovery
├── enricher.py                 # Claude-powered company enrichment
├── scorer.py                   # AI lead qualification (0-100 scoring)
├── market_intelligence.py      # CLI orchestrator & main entry point
├── app.py                      # Flask web server
├── templates/
│   └── index.html              # Claude-style web UI
├── static/
│   └── style.css               # Modern dark-mode design
├── test_components.py          # Unit tests for each component
├── test_integration.py         # End-to-end pipeline tests
├── requirements.txt            # Python dependencies
└── .env.example                # Environment config template
```

---

## Pipeline Architecture

```
User Input (search query + ICP)
    ↓
[Scraper] Apify Google Search
    ↓ (prospects: name, URL, snippet)
[Enricher] Claude Analysis
    ↓ (enriched: industry, size, funding, pain points)
[Scorer] Claude Relevance Scoring
    ↓ (scored: 0-100, reason, engagement level)
[UI] Web Interface or JSON Export
    ↓
Ready-to-engage prospect list
```

---

## Example Output

```json
[
  {
    "name": "TechFlow Systems",
    "url": "https://techflow.io",
    "industry": "B2B SaaS",
    "company_size": "100-200",
    "funding_stage": "Series B",
    "pain_points": ["Process automation", "Team scaling"],
    "score": 92,
    "score_reason": "Excellent ICP fit: Series B SaaS, right size, matching pain points",
    "engagement_level": "high"
  },
  ...
]
```

---

## Testing

### Run All Tests

```bash
pytest test_components.py test_integration.py -v
```

### Run Specific Test

```bash
pytest test_components.py::TestScraper -v
```

Tests include:
- ✅ Component unit tests (scraper, enricher, scorer)
- ✅ End-to-end pipeline integration tests
- ✅ Error handling and fallback logic
- ✅ Data validation

---

## API Reference

### `scraper.scrape_prospects(query, limit=10)`
Discover prospects using Apify Google Search actor.
- **Returns:** List of prospect dicts with `name`, `url`, `snippet`, `source`

### `enricher.enrich_prospect(prospect)`
Enrich raw prospect with Claude analysis.
- **Returns:** Prospect dict with added `industry`, `company_size`, `funding_stage`, `pain_points`, `decision_makers`

### `scorer.score_prospect(enriched_prospect, icp_criteria)`
Score prospect relevance (0-100) against ICP.
- **Returns:** Prospect dict with added `score`, `score_reason`, `engagement_level`

### `market_intelligence.run_agent(search_query, icp_criteria, max_results)`
Run full pipeline end-to-end.
- **Returns:** List of scored prospects sorted by relevance (highest first)

---

## Hackathon Details

Built for the **Marketing Agents Hackathon** presented by The AI Collective × Lynk.

**Challenge:** Build orchestrated agent systems that find ICPs, qualify leads, ship campaigns, and report results.

**Sponsors:** Apify, Lovable, Minds AI, Kalibr, Pixero, Red Bull

**Key Features for Judges:**
- 🥇 **Best use of Apify** — Full web scraping integration for prospect discovery
- 🧠 **Multi-stage reasoning** — Scrape → Enrich → Score pipeline demonstrates agent orchestration
- 📊 **Measurable outcomes** — Prospect scores with reasoning for transparency
- 🎨 **Production-ready UI** — Claude-inspired web interface

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
