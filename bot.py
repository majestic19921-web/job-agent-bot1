import requests
from bs4 import BeautifulSoup
import os

# -------------------
# CONFIG
# -------------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

ALLOWED_CITIES = ["erbil", "duhok", "iraq"]

KEYWORDS = [
    "it", "erp", "odoo", "crm", "manager", "system", "admin", "developer"
]


# -------------------
# TELEGRAM
# -------------------
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


# -------------------
# IQJSCOUT SCRAPER (SIMPLIFIED)
# -------------------
def scrape_iqjscout():
    url = "https://iqjscout.com/"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=10)
    text = res.text.lower()

    jobs = []

    # crude but effective detection
    blocks = text.split("<div")

    for block in blocks:
        if "job" in block or "position" in block or "crm" in block:
            jobs.append({
                "title": "IQJ Job Found",
                "raw": block[:1500]
            })

    return jobs


# -------------------
# JOBS.KRD SCRAPER
# -------------------
def scrape_jobs_krd():
    url = "https://jobs.krd"
    headers = {"User-Agent": "Mozilla/5.0"}

    res = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    for item in soup.find_all("a"):
        title = item.text.strip()
        link = item.get("href")

        if title and len(title) > 5:
            jobs.append({
                "title": title,
                "raw": title.lower(),
                "link": link
            })

    return jobs


# -------------------
# FILTER ENGINE
# -------------------
def is_relevant(job):
    text = (job["title"] + " " + job["raw"]).lower()

    city_match = any(city in text for city in ALLOWED_CITIES)
    keyword_match = any(keyword in text for keyword in KEYWORDS)

    return city_match and keyword_match


# -------------------
# MAIN
# -------------------
if __name__ == "__main__":

    all_jobs = []

    try:
        all_jobs += scrape_iqjscout()
    except Exception as e:
        print("IQJ error:", e)

    try:
        all_jobs += scrape_jobs_krd()
    except Exception as e:
        print("KRD error:", e)

    found = 0

    for job in all_jobs:
        if is_relevant(job):
            send_message(
                "🔥 Job Match Found!\n\n"
                f"Title: {job['title']}\n"
                f"Location filter: Erbil / Duhok\n"
            )
            found += 1

    if found == 0:
        send_message("No matching jobs found today.")
