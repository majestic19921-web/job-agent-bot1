import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

KEYWORDS = ["it", "erp", "odoo", "crm", "manager", "system", "admin"]
CITIES = ["erbil", "duhok"]


def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


# -------------------------
# GOOGLE SEARCH SCRAPER
# -------------------------
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []

    for g in soup.find_all("div"):
        text = g.text.lower()

        if len(text) > 50:
            results.append(text)

    return results


def is_relevant(text):
    city_match = any(c in text for c in CITIES)
    keyword_match = any(k in text for k in KEYWORDS)
    return city_match and keyword_match


if __name__ == "__main__":

    queries = [
        "site:iqjscout.com crm manager erbil",
        "site:jobs.krd it manager erbil",
        "site:iqjscout.com erbil jobs",
        "site:jobs.krd duhok jobs"
    ]

    found = 0

    for q in queries:
        results = google_search(q)

        for r in results:
            if is_relevant(r):
                send_message(
                    "🔥 Job Match Found!\n\n"
                    f"{r[:500]}"
                )
                found += 1

    if found == 0:
        send_message("No matching jobs found today.")
