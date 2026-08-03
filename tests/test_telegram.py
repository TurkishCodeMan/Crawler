import os
import pytest
import responses
from telegram import send_alert

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "fake_token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "12345")

@responses.activate
def test_send_alert_success(mock_env_vars):
    url = "https://api.telegram.org/botfake_token/sendMessage"
    responses.add(responses.POST, url, json={"ok": True}, status=200)
    
    assert send_alert("Test message") == True
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == url

@responses.activate
def test_send_alert_failure(mock_env_vars):
    url = "https://api.telegram.org/botfake_token/sendMessage"
    responses.add(responses.POST, url, json={"ok": False}, status=400)
    
    assert send_alert("Test message") == False

def test_send_alert_missing_env_vars(monkeypatch):
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    
    assert send_alert("Test message") == False
