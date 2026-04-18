from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime
from kalibr_orchestrator import run_orchestrated_pipeline

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Enable CORS for Lovable frontend integration
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Store active searches
searches = {}

@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")

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

    # Run orchestrated pipeline via Kalibr
    try:
        result = run_orchestrated_pipeline(
            search_query,
            icp_criteria or None,
            max_results=8,
            enable_reasoning=enable_reasoning
        )

        searches[search_id]["status"] = result.get("status", "complete")
        searches[search_id]["results"] = result.get("leads", [])
        searches[search_id]["stats"] = result.get("stats", {})
        searches[search_id]["errors"] = result.get("errors", [])
    except Exception as e:
        searches[search_id]["status"] = "error"
        searches[search_id]["error"] = str(e)

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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
