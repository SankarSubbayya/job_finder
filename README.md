# MarketIntelligence

> **An autonomous lead intelligence agent that discovers, enriches, and qualifies prospects using advanced web scraping and AI-powered scoring.**

---

## Overview

MarketIntelligence is a GTM agent built for the Marketing Agents Hackathon (April 18, 2026). It automates prospect discovery and qualification by:

1. **Scraping data** via Apify to identify target prospects
2. **Enriching leads** with company and contact information
3. **Qualifying prospects** using AI-powered relevance scoring
4. **Delivering actionable insights** for sales and marketing teams

---

## Features

- 🕷️ **Apify Integration** — Web scraping for prospect discovery
- 🧠 **Intelligent Scoring** — AI-powered lead qualification
- 📊 **Lead Enrichment** — Company research and data synthesis
- ⚡ **Fast Processing** — Parallel scraping and scoring
- 📈 **Actionable Insights** — Qualified prospects ready for outreach

---

## Tech Stack

- **Python 3.8+** — Core agent logic
- **Apify** — Web scraping actors
- **Claude API** — Lead scoring and enrichment
- **Flask** — Web UI (optional)

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Fill in: APIFY_API_KEY, CLAUDE_API_KEY

# Run agent
python market_intelligence.py
```

---

## Project Structure

```
├── market_intelligence.py    # Main agent logic
├── scraper.py              # Apify integration
├── enricher.py             # Lead enrichment
├── scorer.py               # AI-powered qualification
├── app.py                  # Web UI (optional)
└── requirements.txt        # Dependencies
```

---

## Hackathon Challenge

Built for Marketing Agents Hackathon 2026:
- **Goal:** Find ICPs, qualify leads, ship campaigns, report results
- **Sponsors:** Apify, Lovable, Minds AI, Kalibr, Pixero
- **Deadline:** April 18, 2026 (3 PM PT)

---

## License

MIT
