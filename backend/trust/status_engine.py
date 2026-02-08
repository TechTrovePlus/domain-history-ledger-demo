# backend/trust/status_engine.py

from datetime import datetime, timedelta

from backend.config.event_types import ABUSE_FLAG, OWNERSHIP_CHANGED


def parse_date(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


def evaluate_status(events: list[dict]) -> str:
    """
    events: list of dicts with keys:
      - event_type
      - event_time
      - description
    Events must be pre-sorted by event_time ASC.
    """

    now = max(parse_date(e["event_time"]) for e in events)

    # 🔴 Rule 1 — RED
    for e in events:
        if e["event_type"] == ABUSE_FLAG:
            return "RED"

    # 🟡 Rule 2 — YELLOW

    # Domain age
    first_seen = parse_date(events[0]["event_time"])
    if (now - first_seen).days <= 30:
        return "YELLOW"

    # Ownership change within 90 days
    for e in events:
        if e["event_type"] == OWNERSHIP_CHANGED:
            if (now - parse_date(e["event_time"])).days <= 90:
                return "YELLOW"

    # Re-registration within 180 days (encoded in description)
    for e in events:
        if e["description"].startswith("RE_REGISTERED"):
            if (now - parse_date(e["event_time"])).days <= 180:
                return "YELLOW"

    # 🟢 Rule 3 — GREEN
    return "GREEN"
