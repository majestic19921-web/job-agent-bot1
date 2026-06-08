import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# -------------------
# TELEGRAM FUNCTION
# -------------------
def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": text})


# -------------------
# FILTER RULES
# -------------------
ALLOWED_CITIES = ["erbil", "duhok"]

KEYWORDS = [
    "it", "erp", "odoo", "crm", "manager", "system", "admin", "developer"
]


# -------------------
# IQJSCOUT SCRAPER
# -------------------
def scrape_iqjscout():
    url = "https://iqjscout.com/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    for item in soup.find_all("h3"):
        title = item.text.strip()

        # try to find nearby text (city usually in same block)
        parent_text = item.find_parent().text.lower()

        jobs.append({
            "title": title,
            "raw": parent_text
        })

    return jobs


# -------------------
# JOBS.KRD SCRAPER
# -------------------
def scrape_jobs_krd():
    url = "https://jobs.krd"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    jobs = []

    for item in soup.find_all(["h2", "h3", "a"]):
        title = item.text.strip()
        if len(title) > 5:
            jobs.append({
                "title": title,
                "raw": soup.text.lower()
            })

    return jobs


# -------------------
# FILTER FUNCTION
# -------------------
def is_relevant(job):
    text = job["title"].lower() + " " + job["raw"]

    city_match = any(city in text for city in ALLOWED_CITIES)
    keyword_match = any(keyword in text for keyword in KEYWORDS)

    return city_match and keyword_match


# -------------------
# MAIN RUN
# -------------------
if __name__ == "__main__":

    all_jobs = []

    all_jobs += scrape_iqjscout()
    all_jobs += scrape_jobs_krd()

    found = 0

    for job in all_jobs:
        if is_relevant(job):
            send_message(
                "🔥 Job Match Found!\n\n"
                f"Title: {job['title']}\n\n"
                f"Location Filter: Erbil/Duhok\n"
            )
            found += 1

    if found == 0:
        send_message("No matching jobs found today.")
