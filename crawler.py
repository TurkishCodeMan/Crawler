import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from state_manager import load_seen_tenders, save_seen_tenders
from telegram import send_alert

# Load environment variables from .env file
load_dotenv()

URL = "https://ihale.tpic.gov.tr/"

# Default keywords if none provided in environment
DEFAULT_KEYWORDS = ['kamyon', 'kepçe', 'araç', "binek","4x4",'traktör', 'kiralama', 'doğrudan temin', 'arazöz', 'sulama', 'tanker','beko-loder','beko','loder','jcb','kullan','öde','temin','kira','Ay']

def get_keywords():
    """Returns a list of keywords to search for."""
    env_keywords = os.environ.get("KEYWORDS")
    if env_keywords:
        return [k.strip().lower() for k in env_keywords.split(",") if k.strip()]
    return DEFAULT_KEYWORDS

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_tenders():
    """Fetches and parses tenders from the TPIC website."""
    # Siteyi mobil modda (iPhone) ziyaret ettiğimizi belirtiyoruz ki bize Div'leri versin
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    try:
        r = requests.get(URL, headers=headers, timeout=15, verify=False)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL {URL}: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    tenders = []
    
    # Yeni div yapısına (mobil/responsive) göre ayrıştırma
    items = soup.find_all("div", class_="border-b border-gray-200 p-4 hover:bg-gray-50")
    
    for item in items:
        try:
            # Başlık (Title)
            title_el = item.find("h4")
            if not title_el:
                continue
            title = title_el.text.strip()
            
            # Detaylar (Tarih, Referans, Tür)
            spans = item.find_all("span", class_="block")
            date = spans[0].text.strip() if len(spans) > 0 else "Belirtilmemiş"
            ref_no = spans[1].text.strip() if len(spans) > 1 else "Belirtilmemiş"
            tender_type = spans[2].text.strip() if len(spans) > 2 else "Belirtilmemiş"
            
            # Link
            link = URL
            a_tag = item.find("a", href=True)
            if a_tag:
                href = a_tag["href"]
                if not href.startswith("http"):
                    link = f"https://ihale.tpic.gov.tr{href}"
                else:
                    link = href
                    
            tenders.append({
                "ref_no": ref_no,
                "title": title,
                "type": tender_type,
                "date": date,
                "link": link
            })
        except Exception as e:
            # Beklenmeyen bir yapı gelirse es geç
            continue
            
    return tenders

def format_message(tender):
    """Formats the tender info into a readable Telegram message."""
    return (
        f"🚨 <b>Yeni TPIC İhale Bildirimi</b>\n\n"
        f"<b>Başlık:</b> {tender['title']}\n"
        f"<b>Referans:</b> {tender['ref_no']}\n"
        f"<b>Tür:</b> {tender['type']}\n"
        f"<b>Tarih:</b> {tender['date']}\n\n"
        f"<a href='{tender['link']}'>İlana Git</a>"
    )

def main():
    keywords = get_keywords()
    print(f"Searching with keywords: {keywords}")
    
    seen_tenders = load_seen_tenders()
    tenders = fetch_tenders()
    
    new_seen_tenders = set(seen_tenders)
    
    for t in tenders:
        ref_no = t["ref_no"]
        if ref_no in seen_tenders:
            continue
            
        # Check keywords
        title_lower = t["title"].lower()
        if any(k in title_lower for k in keywords):
            print(f"Match found: {t['title']} ({ref_no})")
            
            msg = format_message(t)
            if send_alert(msg):
                new_seen_tenders.add(ref_no)
            else:
                print(f"Failed to send alert for {ref_no}, will try again next time.")
                
    # Save the updated list of seen tenders
    save_seen_tenders(list(new_seen_tenders))
    print("Done checking tenders.")

if __name__ == "__main__":
    main()
