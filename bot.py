if __name__ == "__main__":

    queries = [
        "site:iqjscout.com crm manager erbil",
        "site:jobs.krd it manager erbil",
        "site:iqjscout.com erbil jobs",
        "site:jobs.krd duhok jobs"
    ]

    found = 0

    for q in queries:
        print("\n========================")
        print("QUERY:", q)

        results = google_search(q)

        print("RESULTS COUNT:", len(results))

        for i, r in enumerate(results[:5]):  # only first 5
            print(f"\n--- RESULT {i} ---")
            print(r[:500])  # show preview

            if is_relevant(r):
                print(">>> MATCH FOUND")
                send_message(
                    "🔥 Job Match Found!\n\n" + r[:500]
                )
                found += 1
            else:
                print("no match")

    if found == 0:
        send_message("No matching jobs found today.")

    print("\nDONE. TOTAL MATCHES:", found)
