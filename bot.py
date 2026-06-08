import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    print("SENDING MESSAGE:")
    print(text)
    print("TOKEN:", BOT_TOKEN)
    print("CHAT ID:", CHAT_ID)


def scrape_test():
    print("SCRAPING TEST RUNNING...")
    return [
        {
            "title": "CRM Manager - Harlem Group",
            "raw": "erbil iraq crm manager automotive"
        }
    ]


def is_relevant(job):
    print("CHECKING JOB:", job["title"])

    text = job["title"] + " " + job["raw"]

    keywords = ["crm", "manager", "it", "erp"]
    cities = ["erbil", "duhok", "iraq"]

    city_match = any(c in text.lower() for c in cities)
    keyword_match = any(k in text.lower() for k in keywords)

    print("CITY MATCH:", city_match)
    print("KEYWORD MATCH:", keyword_match)

    return city_match and keyword_match


if __name__ == "__main__":
    print("BOT STARTED")

    jobs = scrape_test()

    found = 0

    for job in jobs:
        if is_relevant(job):
            send_message("🔥 MATCH FOUND: " + job["title"])
            found += 1

    print("TOTAL FOUND:", found)
