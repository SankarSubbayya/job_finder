from flask import Flask, render_template, request, jsonify
import json
import uuid
from datetime import datetime
from market_intelligence import run_agent

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Store active searches
searches = {}

@app.route("/")
def index():
    """Home page."""
    return render_template("index.html")

@app.route("/api/search", methods=["POST"])
def start_search():
    """Start a new lead search."""
    data = request.json
    search_query = data.get("query", "").strip()
    icp_criteria = data.get("icp", "").strip()

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

    # Run agent (in production, this would be async)
    try:
        results = run_agent(search_query, icp_criteria or None, max_results=8)
        searches[search_id]["status"] = "complete"
        searches[search_id]["results"] = results
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
        "error": search.get("error"),
    })

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
