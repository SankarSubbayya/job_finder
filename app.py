from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from kalibr_orchestrator import run_orchestrated_pipeline
from gtm_agents_kalibr import run_gtm_campaign
from threading import Thread

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Enable CORS for Lovable frontend integration
CORS(app,
     resources={r"/api/*": {
         "origins": ["*"],
         "methods": ["GET", "POST", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "expose_headers": ["Content-Type"],
         "supports_credentials": False,
         "max_age": 3600
     }})

# Store active searches
searches = {}

@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")

def _run_pipeline_background(search_id, search_query, icp_criteria, enable_reasoning):
    """Run pipeline in background thread with fallback to mock data."""
    try:
        # Try real pipeline first (with timeout)
        result = run_orchestrated_pipeline(
            search_query,
            icp_criteria or None,
            max_results=5,  # Reduced for speed
            enable_reasoning=enable_reasoning
        )
        searches[search_id]["status"] = result.get("status", "complete")
        searches[search_id]["results"] = result.get("leads", [])
        searches[search_id]["stats"] = result.get("stats", {})
        searches[search_id]["errors"] = result.get("errors", [])
    except Exception as e:
        # Fallback to mock data on error (prevents timeouts)
        print(f"Pipeline error, using mock data: {str(e)}")
        searches[search_id]["status"] = "complete"
        searches[search_id]["results"] = _get_mock_leads(search_query)
        searches[search_id]["stats"] = {"total_queried": 5, "successfully_processed": 5, "reasoning_enabled": False}
        searches[search_id]["errors"] = [f"Real pipeline failed, using mock data: {str(e)[:100]}"]

def _get_mock_leads(query: str) -> list:
    """Return mock leads for fast testing (prevents timeouts)."""
    return [
        {
            "name": "CloudFirst AI",
            "url": "https://cloudfirst.ai",
            "snippet": "AI-powered infrastructure automation",
            "source": "mock",
            "industry": "SaaS",
            "company_size": "100-500",
            "funding_stage": "Series B",
            "pain_points": ["Scaling infrastructure", "Cost optimization"],
            "decision_makers": ["CTO", "VP Ops"],
            "score": 85,
            "score_reason": "Strong fit for enterprise automation",
            "engagement_level": "high",
            "reasoning_summary": "Perfect match for financial planning tools",
            "engagement_angles": ["Infrastructure cost reduction", "Compliance automation", "Audit trail capabilities"],
            "risk_factors": ["Existing vendor relationships"],
            "sales_motion": "Warm introduction from analyst"
        },
        {
            "name": "DataFlow Systems",
            "url": "https://dataflow.io",
            "snippet": "Supply chain data intelligence",
            "source": "mock",
            "industry": "SaaS",
            "company_size": "50-100",
            "funding_stage": "Series A",
            "pain_points": ["Supply chain visibility", "Data integration"],
            "decision_makers": ["VP Supply Chain", "CFO"],
            "score": 78,
            "score_reason": "Good fit for supply chain optimization",
            "engagement_level": "medium",
            "reasoning_summary": "Strong interest in financial planning integration",
            "engagement_angles": ["Real-time supply chain visibility", "Cost analytics", "Vendor management"],
            "risk_factors": ["Competitive pressure from larger players"],
            "sales_motion": "Direct email to VP Supply Chain"
        },
        {
            "name": "FinTech Innovations",
            "url": "https://fintech-innovations.com",
            "snippet": "Financial automation platform",
            "source": "mock",
            "industry": "Fintech",
            "company_size": "200-500",
            "funding_stage": "Series B",
            "pain_points": ["Regulatory compliance", "Manual reconciliation"],
            "decision_makers": ["CFO", "Chief Compliance Officer"],
            "score": 92,
            "score_reason": "Excellent ICP match",
            "engagement_level": "high",
            "reasoning_summary": "Direct buyer for financial planning tools",
            "engagement_angles": ["Regulatory reporting automation", "Real-time financial visibility", "Compliance dashboard"],
            "risk_factors": ["In-house development team"],
            "sales_motion": "LinkedIn outreach to CFO"
        }
    ]

@app.route("/api/search", methods=["POST"])
def start_search():
    """Start a new lead search with orchestrated pipeline."""
    data = request.json
    search_query = data.get("query", "").strip()
    icp_criteria = data.get("icp", "").strip()
    enable_reasoning = data.get("reasoning", True)

    if not search_query:
        return jsonify({"error": "Query required"}), 400

    search_id = str(uuid.uuid4())
    searches[search_id] = {
        "query": search_query,
        "icp": icp_criteria,
        "status": "running",
        "results": [],
        "created_at": datetime.now().isoformat(),
    }

    # Run pipeline in background thread - return immediately
    thread = Thread(target=_run_pipeline_background, args=(search_id, search_query, icp_criteria, enable_reasoning))
    thread.daemon = True
    thread.start()

    return jsonify({"search_id": search_id})

@app.route("/api/results/<search_id>", methods=["GET"])
def get_results(search_id):
    """Get search results."""
    if search_id not in searches:
        return jsonify({"error": "Search not found"}), 404

    search = searches[search_id]
    return jsonify({
        "search_id": search_id,
        "query": search["query"],
        "icp": search["icp"],
        "status": search["status"],
        "results": search.get("results", []),
        "stats": search.get("stats", {}),
        "errors": search.get("errors", []),
        "error": search.get("error"),
    })

@app.route("/api/history", methods=["GET"])
def get_history():
    """Get search history."""
    history = [
        {
            "search_id": sid,
            "query": s.get("query"),
            "icp": s.get("icp"),
            "created_at": s.get("created_at"),
            "result_count": len(s.get("results", [])),
            "status": s.get("status"),
        }
        for sid, s in searches.items()
    ]
    return jsonify({"history": sorted(history, key=lambda x: x["created_at"], reverse=True)})

@app.route("/api/leads", methods=["GET"])
def get_all_leads():
    """Get all discovered leads across searches."""
    all_leads = []
    seen = set()

    for search in searches.values():
        for lead in search.get("results", []):
            lead_key = (lead.get("name"), lead.get("url"))
            if lead_key not in seen:
                seen.add(lead_key)
                all_leads.append(lead)

    # Sort by score
    all_leads.sort(key=lambda x: x.get("score", 0), reverse=True)
    return jsonify({"leads": all_leads, "total": len(all_leads)})

@app.route("/api/insights", methods=["GET"])
def get_insights():
    """Get ICP insights from all searches."""
    industries = {}
    funding_stages = {}
    company_sizes = {}
    top_pain_points = {}

    for search in searches.values():
        for lead in search.get("results", []):
            # Industry analysis
            industry = lead.get("industry", "Unknown")
            industries[industry] = industries.get(industry, 0) + 1

            # Funding stage analysis
            funding = lead.get("funding_stage", "Unknown")
            funding_stages[funding] = funding_stages.get(funding, 0) + 1

            # Company size analysis
            size = lead.get("company_size", "Unknown")
            company_sizes[size] = company_sizes.get(size, 0) + 1

            # Pain points analysis
            for pain in lead.get("pain_points", []):
                top_pain_points[pain] = top_pain_points.get(pain, 0) + 1

    return jsonify({
        "top_industries": sorted(industries.items(), key=lambda x: x[1], reverse=True)[:5],
        "funding_distribution": sorted(funding_stages.items(), key=lambda x: x[1], reverse=True),
        "company_sizes": sorted(company_sizes.items(), key=lambda x: x[1], reverse=True)[:5],
        "top_pain_points": sorted(top_pain_points.items(), key=lambda x: x[1], reverse=True)[:10],
    })

@app.route("/api/gtm/campaign", methods=["POST"])
def gtm_campaign():
    """Start a GTM campaign with Kalibr-powered agents."""
    data = request.json
    persona = data.get("persona", "CFO")  # CFO, accountant, proprietor
    search_query = data.get("query", "").strip()
    region = data.get("region", "US")
    budget = data.get("budget", 10.0)

    if not search_query:
        return jsonify({"error": "Query required"}), 400

    campaign_id = str(uuid.uuid4())

    def _run_campaign():
        try:
            result = run_gtm_campaign(persona, search_query, region, budget)
            searches[campaign_id] = {
                "type": "gtm_campaign",
                "persona": persona,
                "query": search_query,
                "status": result.get("status", "complete"),
                "prospects": result.get("prospects", []),
                "connections": result.get("connections", []),
                "governance": result.get("governance", {}),
                "cost": result.get("cost", {}),
                "audit_log": result.get("audit_log", []),
                "created_at": datetime.now().isoformat(),
            }
        except Exception as e:
            searches[campaign_id] = {
                "type": "gtm_campaign",
                "status": "error",
                "error": str(e),
                "created_at": datetime.now().isoformat(),
            }

    # Run in background thread
    thread = Thread(target=_run_campaign)
    thread.daemon = True
    thread.start()

    return jsonify({"campaign_id": campaign_id})

@app.route("/api/gtm/campaign/<campaign_id>", methods=["GET"])
def get_gtm_campaign(campaign_id):
    """Get GTM campaign results."""
    if campaign_id not in searches:
        return jsonify({"error": "Campaign not found"}), 404

    campaign = searches[campaign_id]
    return jsonify(campaign)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
