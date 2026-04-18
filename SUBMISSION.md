# MarketIntelligence - Marketing Agents Hackathon Submission

## Project Summary

**MarketIntelligence** is an autonomous lead intelligence GTM agent that discovers, enriches, and qualifies prospects in minutes. It demonstrates orchestrated multi-stage AI reasoning for marketing automation.

**Tagline:** Discover. Score. Engage.

---

## The Challenge

Marketing teams spend hours finding and qualifying prospects manually. We needed a system that:
- Finds high-intent prospects at scale
- Enriches data with company research
- Scores leads intelligently for relevance
- Presents actionable insights ready for outreach

---

## The Solution

A **three-stage orchestrated agent pipeline**:

1. **Discover** (Apify Scraper)
   - Uses Apify Google Search to find target companies
   - Returns prospect metadata: name, URL, snippet

2. **Enrich** (Claude AI)
   - Analyzes each prospect with Claude API
   - Extracts: industry, company size, funding stage, pain points, decision-makers
   - Structured JSON output for downstream processing

3. **Score** (Claude AI)
   - Intelligently scores each prospect (0-100) against ICP
   - Provides reasoning for each score
   - Assigns engagement level (high/medium/low)
   - Results sorted by relevance

---

## Key Features

### ✅ Technology Stack

- **Apify** — Web scraping actor platform (core sponsor integration)
- **Claude API** — Intelligence and reasoning (enrichment + scoring)
- **Flask** — Modern web interface
- **Python 3.8+** — Robust, maintainable code

### ✅ Demo-Ready

- **Web UI** — Claude-inspired interface at `localhost:5000`
- **CLI** — Standalone command-line usage
- **Python API** — Programmatic access for integrations
- **Demo Script** — Works without API keys (uses mock data)

### ✅ Production-Quality Code

- Unit tests for each component (scraper, enricher, scorer)
- Integration tests for full pipeline
- Error handling with graceful fallbacks
- Comprehensive documentation (README + docstrings)
- Git history showing development progression

### ✅ Hackathon Alignment

- **Solves GTM problem:** Automates prospect discovery and qualification
- **Orchestrated agent system:** Multi-stage reasoning pipeline
- **Measurable outcomes:** Prospect scores with transparency
- **Apify integration:** Full web scraping capability (sponsor feature)
- **AI reasoning:** Claude provides intelligent analysis + scoring (sponsor feature)

---

## Architecture

```
┌─────────────────────────────────┐
│    User Input (Web UI / CLI)    │
│  "Find B2B SaaS companies"      │
└──────────────┬──────────────────┘
               │
       ┌───────▼────────┐
       │  SCRAPER       │
       │  (Apify)       │◄─── Apify Google Search Actor
       └───────┬────────┘
               │
         (raw prospects)
               │
       ┌───────▼────────┐
       │  ENRICHER      │
       │  (Claude)      │◄─── Claude API: Analyze & Extract
       └───────┬────────┘
               │
     (enriched prospects)
               │
       ┌───────▼────────┐
       │  SCORER        │
       │  (Claude)      │◄─── Claude API: Score & Rank
       └───────┬────────┘
               │
    (qualified leads)
               │
     ┌─────────▼──────────┐
     │   Web UI / JSON    │
     │   (Display Results)│
     └───────────────────┘
```

---

## Demo Results

Run `python demo.py` to see sample output:

```
CloudFirst AI 🟢
Score: 95/100 (high)
Reason: Exceptional ICP fit: right stage, size, and pain points
Industry: Enterprise AI/ML
Size: 50-200 employees
Funding: Series B
```

---

## Files Overview

| File | Purpose |
|------|---------|
| `scraper.py` | Apify integration for prospect discovery |
| `enricher.py` | Claude-powered company enrichment |
| `scorer.py` | AI lead qualification & scoring |
| `market_intelligence.py` | CLI orchestrator |
| `app.py` | Flask web server |
| `templates/index.html` | Web UI (Claude-inspired) |
| `static/style.css` | Modern dark-mode styling |
| `test_components.py` | Unit tests |
| `test_integration.py` | Integration tests |
| `demo.py` | Works without API keys |
| `README.md` | Complete documentation |

---

## How to Run

### Quick Demo (No API Keys Needed)
```bash
python demo.py
```

### Web UI (Requires API Keys)
```bash
1. cp .env.example .env
2. Add APIFY_TOKEN and ANTHROPIC_API_KEY to .env
3. python app.py
4. Visit http://localhost:5000
```

### CLI (Requires API Keys)
```bash
python market_intelligence.py "B2B SaaS in fintech"
```

---

## Judge Evaluation Points

### 🏆 Best Use of Apify
- ✅ Integrated Apify Google Search actor for prospect discovery
- ✅ Handles API errors gracefully with fallbacks
- ✅ Demonstrates real-time web scraping capability

### 🧠 Multi-Stage AI Reasoning
- ✅ Three-stage pipeline showing orchestrated reasoning
- ✅ Each stage builds on previous: Scrape → Enrich → Score
- ✅ Claude used for semantic analysis (not just API calls)

### 📊 Measurable Outcomes
- ✅ Prospects scored 0-100 with reasoning
- ✅ Engagement level assessment (high/medium/low)
- ✅ Structured output ready for CRM integration

### 🎨 Production Quality
- ✅ Modern Claude-inspired web UI
- ✅ Comprehensive test coverage
- ✅ Error handling and graceful degradation
- ✅ Complete documentation

---

## Sponsor Awards

This project specifically targets:

1. **Best Use of Apify** ($500 cash)
   - Core integration: Apify Google Search for prospect discovery
   - Demonstrates scraping at scale

2. **General Hackathon Prizes**
   - Complete orchestrated agent system
   - Addresses "find ICPs, qualify leads" requirement
   - Production-ready code + UI

---

## Future Enhancements

- Async pipeline for parallel processing
- CRM integrations (Salesforce, HubSpot)
- Advanced filtering (location, funding, industry)
- Email template generation
- Analytics dashboard

---

## Contact & Links

- **Demo:** Run `python demo.py`
- **Live UI:** `python app.py` → http://localhost:5000
- **Docs:** See README.md

---

*Built for the Marketing Agents Hackathon 2026*
*Presented by The AI Collective × Lynk*
