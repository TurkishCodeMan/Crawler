import os
import requests
from bs4 import BeautifulSoup
from state_manager import load_seen_tenders, save_seen_tenders
from telegram import send_alert

URL = "https://ihale.tpic.gov.tr/"

# Default keywords if none provided in environment
DEFAULT_KEYWORDS = ["boru", "pompa", "vinç", "kamyon", "kiralama", "hidrolik", "jeneratör"]

def get_keywords():
    """Returns a list of keywords to search for."""
    env_keywords = os.environ.get("KEYWORDS")
    if env_keywords:
        return [k.strip().lower() for k in env_keywords.split(",") if k.strip()]
    return DEFAULT_KEYWORDS

def fetch_tenders():
    """Fetches and parses tenders from the TPIC website."""
    try:
        r = requests.get(URL, timeout=15)
        r.raise_for_status()
    except Exception as e:
        print(f"Error fetching URL {URL}: {e}")
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    tenders = []
    
    # Example table parsing logic, assuming standard <tr> tags
    # Adjust according to the actual HTML structure of the site
    for row in soup.find_all("tr"):
        cols = row.find_all("td")
        if not cols:
            continue
            
        # Assuming the structure is roughly:
        # [0] Reference No, [1] Title, [2] Type, [3] Date, [4] Details Link
        try:
            ref_no = cols[0].text.strip()
            title = cols[1].text.strip()
            tender_type = cols[2].text.strip() if len(cols) > 2 else "Belirtilmemiş"
            date = cols[3].text.strip() if len(cols) > 3 else "Belirtilmemiş"
            
            link = ""
            a_tag = row.find("a", href=True)
            if a_tag:
                link = a_tag["href"]
                if not link.startswith("http"):
                    link = f"https://ihale.tpic.gov.tr/{link.lstrip('/')}"
            else:
                link = URL
                
            tenders.append({
                "ref_no": ref_no,
                "title": title,
                "type": tender_type,
                "date": date,
                "link": link
            })
        except IndexError:
            # If the row format is unexpected, just skip it
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
