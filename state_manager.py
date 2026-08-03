import json
import os

STATE_FILE = "seen_tenders.json"

def load_seen_tenders():
    """Loads the list of already seen tender reference numbers from a JSON file."""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_seen_tenders(seen_tenders):
    """Saves the list of seen tender reference numbers to a JSON file."""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(seen_tenders, f, ensure_ascii=False, indent=4)
