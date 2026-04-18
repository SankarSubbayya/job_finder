# MarketIntelligence - Lovable Enterprise Dashboard

## Build Instructions for Lovable

Paste this prompt into [lovable.dev](https://lovable.dev) to generate the enterprise dashboard UI.

---

## Lovable Build Prompt

```
Build an enterprise B2B lead intelligence dashboard called "MarketIntelligence" 
that connects to a Flask REST API.

## Design Requirements

- **Theme**: Modern dark mode (navy #0d0d0d, card bg #1a1a1a)
- **Color Scheme**: Emerald green accents (#10b981), blue highlights (#3b82f6)
- **Typography**: Clean sans-serif (system fonts), high contrast
- **Responsive**: Works on desktop, tablet, mobile
- **Inspiration**: claude.ai interface — minimal, focused, professional

## Core Features

### 1. Search Panel (Top)
- **Search Input**: "Find prospects like..." placeholder
- **ICP Input**: "Your ICP description..." placeholder
- **Options Toggle**: Enable/disable "Deep Reasoning"
- **Search Button**: Large CTA, triggers POST /api/search

### 2. Results Grid
Each lead card shows:
- **Rank Badge**: #1, #2, etc.
- **Company Name** (large, bold)
- **Industry** tag
- **Company Size** (e.g., "100-200 employees")
- **Funding Stage** badge
- **Relevance Score**: Large badge (0-100), color-coded:
  - Green (#10b981) if >= 75
  - Amber (#f59e0b) if 50-74
  - Red (#ef4444) if < 50
- **Strategic Summary**: 1-line reasoning summary
- **Engagement Angles**: Bullet list of 3 personalized outreach strategies
- **Risk Factors**: Collapsible list of potential blockers
- **Sales Motion**: Recommended first contact approach
- **Decision Makers**: Title tags (e.g., "VP Ops", "CTO")
- **Pain Points**: Concept tags

### 3. Insights Dashboard (Right Sidebar or Tab)
Shows aggregated ICP patterns:
- **Top Industries**: Bar chart (industry name → frequency)
- **Funding Stage Distribution**: Pie chart (Series A/B/C → count)
- **Company Sizes**: Horizontal bar (size band → count)
- **Top Pain Points**: Word cloud or bar chart (pain point → frequency)

### 4. Search History (Left Sidebar)
- **Recent Searches**: List with:
  - Query name
  - Date created
  - Result count
  - Status badge (✅ complete / ⏳ running / ❌ error)
- **Click to Reload**: Selecting a past search loads its results

### 5. Actions & Export
- **Copy Outreach Email**: Button to draft personalized outreach from lead data
- **Export to CSV**: Download all leads as structured CSV
- **Load More**: If results exceed initial display, load next batch

## API Integration

### Base URL
`http://localhost:5000` (user configurable in settings)

### Endpoints

**POST /api/search**
```json
{
  "query": "B2B SaaS in fintech",
  "icp": "Series A, 50+ employees",
  "reasoning": true
}
```
Returns: `{ "search_id": "uuid" }`

**GET /api/results/{search_id}**
Returns:
```json
{
  "search_id": "uuid",
  "query": "...",
  "icp": "...",
  "status": "success|partial|error",
  "leads": [
    {
      "name": "TechCorp",
      "score": 85,
      "industry": "Enterprise AI",
      "company_size": "100-200",
      "funding_stage": "Series B",
      "pain_points": ["ML Ops", "Data Governance"],
      "decision_makers": ["VP Eng", "CTO"],
      "reasoning_summary": "Strong strategic fit...",
      "engagement_angles": ["...", "...", "..."],
      "risk_factors": ["...", "..."],
      "sales_motion": "...",
      "reasoning_confidence": "high"
    }
  ],
  "stats": {
    "total_queried": 10,
    "successfully_processed": 9,
    "duration_seconds": 45.2
  }
}
```

**GET /api/history**
Returns: `{ "history": [{ search_id, query, created_at, result_count, status }] }`

**GET /api/leads**
Returns: `{ "leads": [...all leads...], "total": 42 }`

**GET /api/insights**
Returns:
```json
{
  "top_industries": [["Enterprise AI", 12], ["Data Infrastructure", 10]],
  "funding_distribution": [["Series B", 8], ["Series A", 5]],
  "company_sizes": [["100-500", 15], ["50-100", 8]],
  "top_pain_points": [["Process Automation", 18], ["Scaling", 15]]
}
```

## UX Flows

### Search Flow
1. User enters query + ICP + toggles reasoning
2. Clicks "Find Prospects"
3. Loading spinner with progress ("Scraping → Enriching → Scoring → Reasoning...")
4. Results load and auto-scroll
5. User can click leads for expanded details, copy outreach, or export

### Deep Reasoning Feature
- When enabled: adds 20-40s latency but includes strategic analysis
- Provides engagement_angles, risk_factors, sales_motion per lead
- Confidence badges so user knows reasoning quality

### Insights Analysis
- Charts update as new searches are added
- Shows user what industries/stages are scoring highest historically
- Helps refine future search queries

## Technical Notes

- **Real-time updates**: Poll /api/results/{search_id} every 2s until status changes
- **CORS**: Backend has CORS enabled for cross-origin requests
- **Mobile**: Stack panels vertically on mobile (search → results → insights)
- **Performance**: Lazy-load lead details; show summary first
- **Error Handling**: Show error banner if /api/search fails; retry button

## Branding

- **App Name**: MarketIntelligence
- **Tagline**: "Discover. Score. Engage."
- **Logo Color**: Gradient blue→green
- **Tone**: Professional, data-driven, actionable
```

---

## How to Deploy

1. Go to [lovable.dev](https://lovable.dev)
2. Create a new project
3. Paste the **Lovable Build Prompt** above into the builder
4. Lovable generates the full React/Next.js app
5. Update `VITE_API_BASE_URL` env var to point to your Flask backend
6. Deploy via Lovable's hosting or export code to your infrastructure

## API Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Add APIFY_TOKEN and ANTHROPIC_API_KEY

# Run Flask server
python app.py
# Server runs on http://localhost:5000
```

Lovable dashboard connects to http://localhost:5000/api/* automatically.

---

## Architecture

```
┌─────────────────────────────────┐
│   Lovable Enterprise Dashboard  │
│   (React/Next.js)               │
└──────────────┬──────────────────┘
               │ REST API (CORS)
    ┌──────────▼──────────────┐
    │   Flask API (app.py)    │
    │   ┌────────────────────┐│
    │   │ Kalibr Orchestrator││
    │   └────────┬───────────┘│
    │            │            │
    │  ┌─────────▼──────────┐ │
    │  │ Extended Thinking  │ │
    │  │ (Reasoning Layer)  │ │
    │  └────────────────────┘ │
    │  ┌────────────────────┐  │
    │  │ Claude Enrichment  │  │
    │  │ Claude Scoring     │  │
    │  └────────────────────┘  │
    │  ┌────────────────────┐  │
    │  │ Apify Scraping     │  │
    │  └────────────────────┘  │
    └────────────────────────────┘
```

---

**Ready to build?** Paste the prompt into Lovable and the dashboard will be generated automatically.
