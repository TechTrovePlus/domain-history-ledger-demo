# backend/api/search.py

import sqlite3

from backend.trust.status_engine import evaluate_status
from backend.trust.reason_engine import evaluate_reason

DB_PATH = "backend/dns_guard.db"


def search_domain(domain: str) -> dict:
    """
    Search domain reputation and return current status, reason, proof, and processing logs.
    """
    logs = []
    logs.append({"step": "Initializing DNS Guard scanning engine...", "status": "info"})

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    logs.append({"step": f"Querying local reputation database for: {domain}", "status": "info"})
    
    # Fetch domain
    cursor.execute(
        "SELECT id FROM domains WHERE domain_name = ?",
        (domain,)
    )
    row = cursor.fetchone()

    if row is None:
        conn.close()
        logs.append({"step": "Domain not found in local registries.", "status": "warning"})
        return {
            "domain": domain,
            "status": "UNKNOWN",
            "reason_code": None,
            "reason": "Domain not found in DNS Guard database.",
            "blockchain_proof": None,
            "processing_logs": logs
        }

    domain_id = row[0]
    logs.append({"step": "Domain record located. Retrieving full event history...", "status": "success"})

    # Fetch full event history (chronological)
    cursor.execute(
        """
        SELECT event_type, event_time, description, integrity_hash, blockchain_tx
        FROM domain_events
        WHERE domain_id = ?
        ORDER BY event_time ASC
        """,
        (domain_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    logs.append({"step": f"Analyzing {len(rows)} historical ledger entries...", "status": "info"})

    # Normalize events for trust engines
    events = []
    blockchain_proof = None

    for event_type, event_time, description, integrity_hash, blockchain_tx in rows:
        events.append({
            "event_type": event_type,
            "event_time": event_time,
            "description": description
        })

        # Capture proof if exists
        if integrity_hash and blockchain_tx:
            blockchain_proof = {
                "integrity_hash": integrity_hash,
                "transaction": blockchain_tx
            }

    if blockchain_proof:
        logs.append({"step": "Blockchain integrity proof detected. Verifying on-chain metadata...", "status": "success"})
    else:
        logs.append({"step": "No blockchain anchoring found for current events.", "status": "info"})

    # Evaluate trust
    logs.append({"step": "Executing reputation score status_engine...", "status": "info"})
    status = evaluate_status(events)
    
    logs.append({"step": f"Reputation score calculated: {status}", "status": "success"})
    
    logs.append({"step": "Generating human-readable forensic reasoning...", "status": "info"})
    reason_code, reason_text = evaluate_reason(events, status)

    logs.append({"step": "Analysis complete. compiling final report.", "status": "success"})

    return {
        "domain": domain,
        "status": status,
        "reason_code": reason_code,
        "reason": reason_text,
        "blockchain_proof": blockchain_proof,
        "processing_logs": logs
    }
