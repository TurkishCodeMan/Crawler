import os
import json
import pytest
from state_manager import load_seen_tenders, save_seen_tenders, STATE_FILE

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: ensure file does not exist before each test
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    yield
    # Teardown: ensure file is removed after each test
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def test_load_seen_tenders_empty():
    assert load_seen_tenders() == []

def test_save_and_load_seen_tenders():
    data = ["REF123", "REF456"]
    save_seen_tenders(data)
    
    assert os.path.exists(STATE_FILE)
    loaded = load_seen_tenders()
    assert loaded == data

def test_load_seen_tenders_invalid_json():
    with open(STATE_FILE, "w") as f:
        f.write("invalid json {")
    
    # Should handle decode error and return empty list
    assert load_seen_tenders() == []
