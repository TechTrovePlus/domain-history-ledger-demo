import json
import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from backend.api.search import search_domain
from backend.api.timeline import get_domain_timeline
from backend.ingestion.ingest_wave_1 import ingest_wave_1
from backend.ingestion.ingest_wave_2 import ingest_wave_2
from backend.ingestion.ingest_wave_3 import ingest_wave_3
from backend.ingestion.ingest_wave_4 import ingest_wave_4
from backend.database_setup import init_db

app = Flask(__name__)
CORS(app)

DATA_FILES = {
    "registrar_1": "backend/data/registrar_feed_1.json",
    "registrar_2": "backend/data/registrar_feed_2.json",
    "abuse_1": "backend/data/abuse_feed_1.json",
    "abuse_2": "backend/data/abuse_feed_2.json"
}

DB_PATH = "backend/dns_guard.db"

@app.route("/search")
def search():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "domain parameter is required"}), 400
    result = search_domain(domain)
    return jsonify(result)

@app.route("/timeline")
def timeline():
    domain = request.args.get("domain")
    if not domain:
        return jsonify({"error": "domain parameter is required"}), 400
    result = get_domain_timeline(domain)
    return jsonify(result)

@app.route("/api/feed/<feed_type>/<wave_num>", methods=["GET", "POST"])
def manage_feed(feed_type, wave_num):
    key = f"{feed_type}_{wave_num}"
    if key not in DATA_FILES:
        return jsonify({"error": "Invalid wave or feed type"}), 400
    
    file_path = DATA_FILES[key]
    
    if request.method == "GET":
        with open(file_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    
    if request.method == "POST":
        data = request.json
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        return jsonify({"status": "success", "message": f"{key} updated"})

@app.route("/api/system/ingest/<wave_id>", methods=["POST"])
def trigger_ingest(wave_id):
    try:
        # Map user waves to internal scripts
        # Registrar Wave 1 -> Wave 1
        # Abuse Wave 1     -> Wave 2
        # Registrar Wave 2 -> Wave 3
        # Abuse Wave 2     -> Wave 4
        if wave_id == "registrar_1": ingest_wave_1()
        elif wave_id == "abuse_1": ingest_wave_2()
        elif wave_id == "registrar_2": ingest_wave_3()
        elif wave_id == "abuse_2": ingest_wave_4()
        else: return jsonify({"error": "Unknown wave id"}), 400

        return jsonify({"status": "success", "message": f"Data for {wave_id} successfully injected and anchored."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/api/system/reset", methods=["POST"])
def reset_system():
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
        init_db()
        return jsonify({"status": "success", "message": "Database reset and re-initialized."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
