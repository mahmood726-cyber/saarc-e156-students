"""
Fetch trial data from ClinicalTrials.gov API v2 for SAARC paper topics.
Uses JSON file caching to avoid redundant API calls.
Rate-limited with random delays between requests.
"""

import json
import random
import time
import sys
from pathlib import Path

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ═══════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════

SAARC_COUNTRIES = [
    "India", "Pakistan", "Bangladesh", "Sri Lanka",
    "Nepal", "Afghanistan", "Bhutan", "Maldives",
]

BASE_URL = "https://clinicaltrials.gov/api/v2"
CACHE_DIR = Path(__file__).resolve().parent.parent / "data_cache"


# ═══════════════════════════════════════════════════════════
#  CACHE HELPERS
# ═══════════════════════════════════════════════════════════

def _read_cache(slug, cache_dir=None):
    """Read cached JSON for a given slug. Returns dict or None."""
    d = Path(cache_dir) if cache_dir else CACHE_DIR
    cache_file = d / f"{slug}.json"
    if cache_file.exists():
        try:
            with open(cache_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
    return None


def _write_cache(slug, data, cache_dir=None):
    """Write dict to cache as JSON."""
    d = Path(cache_dir) if cache_dir else CACHE_DIR
    d.mkdir(parents=True, exist_ok=True)
    cache_file = d / f"{slug}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=str)


# ═══════════════════════════════════════════════════════════
#  API FUNCTIONS
# ═══════════════════════════════════════════════════════════

def _rate_limit():
    """Random delay between API calls (0.2-0.3s)."""
    time.sleep(random.uniform(0.2, 0.3))


def fetch_trial_count(condition=None, location=None, other_terms=None):
    """
    GET total trial count from ClinicalTrials.gov API v2.
    Returns int (0 if requests is missing or API fails).
    """
    if not HAS_REQUESTS:
        return 0

    params = {
        "format": "json",
        "pageSize": 0,
        "countTotal": "true",
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
    }
    if condition:
        params["query.cond"] = condition
    if location:
        params["query.locn"] = location
    if other_terms:
        params["query.term"] = other_terms

    try:
        resp = requests.get(f"{BASE_URL}/studies", params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"  API error (count): {e}")
        return 0


def fetch_studies(condition=None, location=None, other_terms=None, max_results=100):
    """
    GET study records from ClinicalTrials.gov API v2.
    Returns list of study dicts (empty if requests is missing or API fails).
    """
    if not HAS_REQUESTS:
        return []

    params = {
        "format": "json",
        "pageSize": min(max_results, 200),
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
    }
    if condition:
        params["query.cond"] = condition
    if location:
        params["query.locn"] = location
    if other_terms:
        params["query.term"] = other_terms

    try:
        resp = requests.get(f"{BASE_URL}/studies", params=params, timeout=60)
        resp.raise_for_status()
        return resp.json().get("studies", [])
    except Exception as e:
        print(f"  API error (studies): {e}")
        return []


# ═══════════════════════════════════════════════════════════
#  METRICS EXTRACTION
# ═══════════════════════════════════════════════════════════

def extract_study_metrics(studies):
    """
    Parse a list of CT.gov study records into a metrics dict.

    Keys: total, statuses, phases, enrollment_values, start_years,
          countries, cities, designs, conditions_list, sponsors,
          sponsor_classes.
    """
    metrics = {
        "total": len(studies),
        "statuses": {},
        "phases": {},
        "enrollment_values": [],
        "start_years": [],
        "countries": {},
        "cities": {},
        "designs": {"randomized": 0, "non_randomized": 0, "observational": 0},
        "conditions_list": [],
        "sponsors": {},
        "sponsor_classes": {},
    }

    for s in studies:
        proto = s.get("protocolSection", {})
        status_mod = proto.get("statusModule", {})
        design_mod = proto.get("designModule", {})
        id_mod = proto.get("identificationModule", {})
        loc_mod = proto.get("contactsLocationsModule", {})
        sponsor_mod = proto.get("sponsorCollaboratorsModule", {})

        # --- Status ---
        status = status_mod.get("overallStatus", "UNKNOWN")
        metrics["statuses"][status] = metrics["statuses"].get(status, 0) + 1

        # --- Phase ---
        phases = design_mod.get("phases", [])
        for ph in phases:
            metrics["phases"][ph] = metrics["phases"].get(ph, 0) + 1

        # --- Enrollment ---
        enroll = design_mod.get("enrollmentInfo", {})
        count = enroll.get("count")
        if count is not None and isinstance(count, (int, float)) and count > 0:
            metrics["enrollment_values"].append(int(count))

        # --- Start year ---
        start = status_mod.get("startDateStruct", {}).get("date", "")
        if start and len(start) >= 4:
            try:
                year = int(start[:4])
                if 1990 <= year <= 2030:
                    metrics["start_years"].append(year)
            except ValueError:
                pass

        # --- Countries and cities ---
        locations = loc_mod.get("locations", [])
        for loc in locations:
            country = loc.get("country", "")
            if country:
                metrics["countries"][country] = metrics["countries"].get(country, 0) + 1
            city = loc.get("city", "")
            if city:
                metrics["cities"][city] = metrics["cities"].get(city, 0) + 1

        # --- Design type ---
        design_info = design_mod.get("designInfo", {})
        alloc = design_info.get("allocation", "")
        if "RANDOMIZED" in alloc.upper() if alloc else False:
            metrics["designs"]["randomized"] += 1
        elif alloc:
            metrics["designs"]["non_randomized"] += 1

        # --- Conditions ---
        conds = proto.get("conditionsModule", {}).get("conditions", [])
        metrics["conditions_list"].extend(conds[:3])

        # --- Sponsors ---
        lead = sponsor_mod.get("leadSponsor", {})
        sponsor_name = lead.get("name", "")
        if sponsor_name:
            metrics["sponsors"][sponsor_name] = metrics["sponsors"].get(sponsor_name, 0) + 1
        sponsor_class = lead.get("class", "")
        if sponsor_class:
            metrics["sponsor_classes"][sponsor_class] = metrics["sponsor_classes"].get(sponsor_class, 0) + 1

    return metrics


# ═══════════════════════════════════════════════════════════
#  MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════

def fetch_paper_data(paper_def):
    """
    Main entry point: fetch all data needed for a single paper.

    Workflow:
        1. Check cache -> return if hit
        2. Fetch per-country counts from CT.gov API
        3. Fetch sample studies for the overall SAARC region
        4. Extract metrics from sample studies
        5. Cache result
        6. Return data dict

    Returns dict with keys:
        slug, country_counts, saarc_total, metrics, query, global_count
    """
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    slug = paper_def["slug"]

    # 1. Check cache
    cached = _read_cache(slug)
    if cached is not None:
        return cached

    q = paper_def.get("query", {})
    condition = q.get("condition")
    other = q.get("other")
    countries = q.get("countries", SAARC_COUNTRIES)

    data = {
        "slug": slug,
        "country_counts": {},
        "saarc_total": 0,
        "metrics": {},
        "query": q,
        "global_count": 0,
    }

    # 2. Fetch per-country counts
    for country in countries:
        count = fetch_trial_count(condition, country, other)
        data["country_counts"][country] = count
        _rate_limit()

    data["saarc_total"] = sum(data["country_counts"].values())

    # 3. Global count (no location filter)
    data["global_count"] = fetch_trial_count(condition, None, other)
    _rate_limit()

    # 4. Fetch sample studies from SAARC region
    #    Use the first country with the most trials, or all SAARC as location
    location_query = " OR ".join(countries) if len(countries) <= 8 else "India"
    studies = fetch_studies(condition, location_query, other, max_results=100)
    _rate_limit()

    # 5. Extract metrics
    data["metrics"] = extract_study_metrics(studies)

    # 6. Cache result
    _write_cache(slug, data)

    return data
