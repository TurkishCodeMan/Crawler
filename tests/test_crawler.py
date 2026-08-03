import pytest
import responses
from crawler import fetch_tenders, get_keywords, format_message, URL

@pytest.fixture
def mock_html():
    return """
    <html>
        <body>
            <div class="bg-white rounded-lg shadow-lg overflow-hidden">
                <div class="max-h-96 overflow-y-auto">
                    <!-- Item 1 -->
                    <div class="border-b border-gray-200 p-4 hover:bg-gray-50">
                        <div class="flex justify-between items-start gap-3">
                            <div class="flex-1">
                                <h4 class="text-sm font-medium text-gray-900 break-words">Boru Alımı</h4>
                                <div class="mt-1 text-xs text-gray-500">
                                    <span class="block">01.01.2026 08:00</span>
                                    <span class="block">REF-001</span>
                                    <span class="block">İhale</span>
                                </div>
                            </div>
                            <div class="flex-shrink-0">
                                <a target="_blank" href="/detay/1">Detay</a>
                            </div>
                        </div>
                    </div>
                    <!-- Item 2 -->
                    <div class="border-b border-gray-200 p-4 hover:bg-gray-50">
                        <div class="flex justify-between items-start gap-3">
                            <div class="flex-1">
                                <h4 class="text-sm font-medium text-gray-900 break-words">Pompa Kiralama</h4>
                                <div class="mt-1 text-xs text-gray-500">
                                    <span class="block">02.01.2026 09:00</span>
                                    <span class="block">REF-002</span>
                                    <span class="block">Doğrudan Alım</span>
                                </div>
                            </div>
                            <div class="flex-shrink-0">
                                <a target="_blank" href="https://other.com/detay/2">Detay</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </body>
    </html>
    """

def test_get_keywords_default(monkeypatch):
    monkeypatch.delenv("KEYWORDS", raising=False)
    keywords = get_keywords()
    assert "boru" in keywords
    assert "pompa" in keywords

def test_get_keywords_custom(monkeypatch):
    monkeypatch.setenv("KEYWORDS", "test, ARABA,  Kamyon ")
    keywords = get_keywords()
    assert keywords == ["test", "araba", "kamyon"]

@responses.activate
def test_fetch_tenders_success(mock_html):
    responses.add(responses.GET, URL, body=mock_html, status=200)
    
    tenders = fetch_tenders()
    assert len(tenders) == 2
    
    assert tenders[0]["ref_no"] == "REF-001"
    assert tenders[0]["title"] == "Boru Alımı"
    assert tenders[0]["link"] == "https://ihale.tpic.gov.tr/detay/1"
    
    assert tenders[1]["ref_no"] == "REF-002"
    assert tenders[1]["link"] == "https://other.com/detay/2"

@responses.activate
def test_fetch_tenders_failure():
    responses.add(responses.GET, URL, status=500)
    tenders = fetch_tenders()
    assert tenders == []

def test_format_message():
    tender = {
        "ref_no": "123",
        "title": "Test Title",
        "type": "Test Type",
        "date": "01.01.2026",
        "link": "https://example.com"
    }
    msg = format_message(tender)
    assert "Test Title" in msg
    assert "123" in msg
    assert "https://example.com" in msg
