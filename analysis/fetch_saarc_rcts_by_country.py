"""Fetch clinical trial counts for all 8 SAARC nations from ClinicalTrials.gov."""
import json, time, random
try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://clinicaltrials.gov/api/v2"
SAARC = ["India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal", "Afghanistan", "Bhutan", "Maldives"]
POPULATIONS = {
    "India": 1_428_000_000, "Pakistan": 231_000_000, "Bangladesh": 173_000_000,
    "Sri Lanka": 22_000_000, "Nepal": 30_000_000, "Afghanistan": 41_000_000,
    "Bhutan": 782_000, "Maldives": 521_000,
}

def fetch_count(country):
    if not requests: return 0
    try:
        r = requests.get(f"{BASE_URL}/studies", params={"query.locn": country, "countTotal": "true", "pageSize": 0}, timeout=15)
        return r.json().get("totalCount", 0)
    except Exception:
        return 0

def main():
    results = {}
    for c in SAARC:
        time.sleep(random.uniform(0.3, 0.5))
        count = fetch_count(c)
        pop = POPULATIONS[c]
        results[c] = {"trials": count, "population": pop, "per_million": round(count / pop * 1_000_000, 2) if pop else 0}
        print(f"{c}: {count} trials ({results[c]['per_million']}/M)")
    with open("analysis/saarc_country_data.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to analysis/saarc_country_data.json")

if __name__ == "__main__":
    main()
