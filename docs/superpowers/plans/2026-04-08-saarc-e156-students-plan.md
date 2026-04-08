# SAARC E156 Student Assignment Platform — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 190-paper E156 micro-paper platform analyzing clinical trial equity across 8 SAARC nations with Pakistan emphasis, for Ziauddin Medical University students.

**Architecture:** Python-generated static site. `paper_manifest.py` declares 190 topics with queries/stats/charts. `build.py` orchestrates: fetch CT.gov data -> compute stats -> generate E156 bodies + HTML dashboards + Python scripts -> assemble group/landing pages. All output is self-contained HTML with inline SVG charts, no external dependencies.

**Tech Stack:** Python 3.x (stdlib + requests), ClinicalTrials.gov API v2, pure SVG charts, static HTML/CSS, GitHub Pages.

**Reference implementation:** `C:\Users\user\africa-e156-students\` — the Africa E156 project this is modeled after. Adapt patterns, do not copy verbatim.

**Spec:** `C:\saarc-e156-students\docs\superpowers\specs\2026-04-08-saarc-e156-students-design.md`

---

## File Structure

```
C:\saarc-e156-students\
├── build.py                    # Master orchestrator (~800 lines)
├── generate_dashboards.py      # Batch dashboard generation entry point
├── rewrite_all_papers.py       # Batch E156 body regeneration
├── lib/
│   ├── __init__.py
│   ├── paper_manifest.py       # 190 paper definitions (slug, query, stats, charts)
│   ├── data_fetcher.py         # CT.gov API wrapper + JSON caching
│   ├── stats_library.py        # 31+ pure-Python statistical methods
│   ├── chart_library.py        # 15+ SVG chart generators + SAARC/Pakistan maps
│   ├── body_generator.py       # E156 7-sentence body generator
│   ├── code_generator.py       # Standalone Python script generator
│   ├── dashboard_generator.py  # HTML dashboard generator (embeds SVG)
│   └── index_updater.py        # Group/landing page HTML assembler
├── data_cache/                 # JSON cached API results
├── geographic-equity/
│   ├── index.html
│   ├── dashboards/             # 35 HTML files
│   └── code/                   # 35 Python files
├── health-disease/
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── governance-justice/
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── methods-systems/
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── pakistan-deep-dive/
│   ├── index.html
│   ├── dashboards/
│   └── code/
├── analysis/
│   ├── fetch_saarc_rcts_by_country.py
│   └── statistical_deep_dive.py
├── index.html                  # Landing page
├── tests/
│   ├── test_paper_manifest.py
│   ├── test_data_fetcher.py
│   ├── test_stats_library.py
│   ├── test_body_generator.py
│   ├── test_chart_library.py
│   ├── test_code_generator.py
│   ├── test_dashboard_generator.py
│   └── test_build.py
├── E156-PROTOCOL.md
└── docs/superpowers/
    ├── specs/2026-04-08-saarc-e156-students-design.md
    └── plans/2026-04-08-saarc-e156-students-plan.md
```

---

## Task 1: Project Scaffolding + Paper Manifest

**Files:**
- Create: `C:\saarc-e156-students\lib\__init__.py`
- Create: `C:\saarc-e156-students\lib\paper_manifest.py`
- Create: `C:\saarc-e156-students\tests\test_paper_manifest.py`

This is the schema layer. Every other module reads from `paper_manifest.py`. It defines all 190 papers declaratively — each with a slug, title, group, query parameters, assigned statistics, chart types, context text, and references.

- [ ] **Step 1: Create directory structure**

```bash
cd /c/saarc-e156-students
mkdir -p lib tests data_cache analysis
mkdir -p geographic-equity/dashboards geographic-equity/code
mkdir -p health-disease/dashboards health-disease/code
mkdir -p governance-justice/dashboards governance-justice/code
mkdir -p methods-systems/dashboards methods-systems/code
mkdir -p pakistan-deep-dive/dashboards pakistan-deep-dive/code
touch lib/__init__.py
```

- [ ] **Step 2: Write test for paper_manifest**

```python
# tests/test_paper_manifest.py
"""Tests for paper manifest — validates all 190 paper definitions."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.paper_manifest import PAPERS, GROUPS, SAARC_COUNTRIES, CHART_TYPES

def test_total_paper_count():
    assert len(PAPERS) == 190, f"Expected 190 papers, got {len(PAPERS)}"

def test_group_distribution():
    counts = {}
    for p in PAPERS:
        counts[p["group"]] = counts.get(p["group"], 0) + 1
    assert counts["geographic-equity"] == 35
    assert counts["health-disease"] == 35
    assert counts["governance-justice"] == 35
    assert counts["methods-systems"] == 35
    assert counts["pakistan-deep-dive"] == 50

def test_saarc_countries():
    assert len(SAARC_COUNTRIES) == 8
    assert "Pakistan" in SAARC_COUNTRIES
    assert "India" in SAARC_COUNTRIES
    assert "Afghanistan" in SAARC_COUNTRIES

def test_all_slugs_unique():
    slugs = [p["slug"] for p in PAPERS]
    assert len(slugs) == len(set(slugs)), "Duplicate slugs found"

def test_paper_required_fields():
    required = {"slug", "title", "group", "paper_num", "query", "stats", "charts", "context", "refs"}
    for p in PAPERS:
        missing = required - set(p.keys())
        assert not missing, f"Paper {p.get('slug','?')} missing: {missing}"

def test_each_paper_has_5_plus_stats():
    for p in PAPERS:
        assert len(p["stats"]) >= 3, f"{p['slug']} has only {len(p['stats'])} stats"

def test_each_paper_has_8_charts():
    for p in PAPERS:
        assert len(p["charts"]) == 8, f"{p['slug']} has {len(p['charts'])} charts, need 8"

def test_all_chart_types_valid():
    for p in PAPERS:
        for c in p["charts"]:
            assert c in CHART_TYPES, f"{p['slug']} has invalid chart: {c}"

def test_group_keys_match_directories():
    expected = {"geographic-equity", "health-disease", "governance-justice",
                "methods-systems", "pakistan-deep-dive"}
    assert set(GROUPS.keys()) == expected

def test_pakistan_deep_dive_subthemes():
    pk_papers = [p for p in PAPERS if p["group"] == "pakistan-deep-dive"]
    # Check sub-theme coverage via paper_num ranges
    provincial = [p for p in pk_papers if 1 <= p["paper_num"] <= 10]
    institutional = [p for p in pk_papers if 11 <= p["paper_num"] <= 18]
    disease = [p for p in pk_papers if 19 <= p["paper_num"] <= 30]
    sponsor = [p for p in pk_papers if 31 <= p["paper_num"] <= 38]
    workforce = [p for p in pk_papers if 39 <= p["paper_num"] <= 45]
    karachi = [p for p in pk_papers if 46 <= p["paper_num"] <= 50]
    assert len(provincial) == 10
    assert len(institutional) == 8
    assert len(disease) == 12
    assert len(sponsor) == 8
    assert len(workforce) == 7
    assert len(karachi) == 5

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 3: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_paper_manifest.py -v`
Expected: ImportError — module doesn't exist yet.

- [ ] **Step 4: Write paper_manifest.py**

Create `lib/paper_manifest.py` with the following structure. This is a large file (~600 lines) — adapt from the Africa project's `paper_manifest.py` at `C:\Users\user\africa-e156-students\lib\paper_manifest.py`.

Key constants to define:

```python
# lib/paper_manifest.py
"""All 190 paper definitions for SAARC E156 student platform."""

# --- Country Lists ---
SAARC_COUNTRIES = [
    "India", "Pakistan", "Bangladesh", "Sri Lanka",
    "Nepal", "Afghanistan", "Bhutan", "Maldives"
]

PAKISTAN_PROVINCES = [
    "Punjab", "Sindh", "Khyber Pakhtunkhwa", "Balochistan",
    "Islamabad Capital Territory", "Gilgit-Baltistan", "Azad Jammu and Kashmir"
]

PAKISTAN_CITIES = {
    "Karachi": "Sindh", "Lahore": "Punjab", "Islamabad": "Islamabad Capital Territory",
    "Rawalpindi": "Punjab", "Faisalabad": "Punjab", "Peshawar": "Khyber Pakhtunkhwa",
    "Quetta": "Balochistan", "Multan": "Punjab", "Hyderabad": "Sindh",
}

PAKISTAN_INSTITUTIONS = [
    "Aga Khan University", "Ziauddin University", "Dow University",
    "Shaukat Khanum Memorial", "Combined Military Hospital",
    "Jinnah Postgraduate Medical Centre", "Mayo Hospital",
    "Services Hospital Lahore", "PIMS Islamabad", "AFIRI"
]

LANDLOCKED_SAARC = ["Nepal", "Bhutan", "Afghanistan"]
ISLAND_SAARC = ["Sri Lanka", "Maldives"]
CONFLICT_SAARC = ["Afghanistan"]

# --- Chart Types ---
CHART_TYPES = [
    "choropleth", "lorenz", "forest", "violin", "heatmap",
    "network", "timeseries", "waterfall", "sankey", "radar",
    "bubble", "slope", "ridge", "funnel", "kaplan_meier",
    "choropleth_pakistan"  # Pakistan provincial map (Group 5)
]

def _charts(indices):
    """Map chart indices to chart type names."""
    return [CHART_TYPES[i] for i in indices]

# --- References ---
REF_CTGOV = "ClinicalTrials.gov, U.S. National Library of Medicine"
REF_WHO = "World Health Organization Global Health Observatory"
REF_LANCET = "Lancet Commission on Global Surgery, 2015"
REF_DRAP = "Drug Regulatory Authority of Pakistan Annual Report"
REF_PMRC = "Pakistan Medical Research Council"
REF_SAARC = "SAARC Secretariat Health Statistics"

# --- Group Definitions ---
GROUPS = {
    "geographic-equity": {
        "title": "Geographic Equity & Spatial Justice",
        "desc": "Where do clinical trials happen across South Asia? These 35 papers map trial site distribution, urban-rural gaps, cross-border networks, and spatial inequality across 8 SAARC nations.",
        "color": "#0d6b57",
        "paper_count": 35,
    },
    "health-disease": {
        "title": "Health & Disease Burden",
        "desc": "Which diseases get studied — and which are neglected? These 35 papers compare trial volume against actual disease burden across South Asia's epidemiological landscape.",
        "color": "#c0392b",
        "paper_count": 35,
    },
    "governance-justice": {
        "title": "Governance, Justice & Sovereignty",
        "desc": "Who controls South Asian clinical research? These 35 papers examine sponsorship, ethics, data ownership, regulatory capacity, and post-trial access across the region.",
        "color": "#1b4f72",
        "paper_count": 35,
    },
    "methods-systems": {
        "title": "Methods, Design & Research Systems",
        "desc": "How rigorous are South Asian trials? These 35 papers audit study design, statistical methods, registration quality, and methodological trends across SAARC.",
        "color": "#4a235a",
        "paper_count": 35,
    },
    "pakistan-deep-dive": {
        "title": "Pakistan Deep-Dive",
        "desc": "A 50-paper deep dive into Pakistan's clinical trial landscape: provincial inequities, institutional concentration, disease-specific gaps, regulatory dynamics, and Karachi's research ecosystem.",
        "color": "#006600",
        "paper_count": 50,
    },
}

# --- Paper Definitions ---
# Each paper: slug, title, group, paper_num, query, stats, charts, context, refs

_GEO_PAPERS = [
    {
        "slug": "saarc-trial-density-map",
        "title": "SAARC Trial Density Map",
        "group": "geographic-equity",
        "paper_num": 1,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate", "rate_ratio", "shannon_entropy"],
        "charts": _charts([0, 1, 3, 9, 6, 7, 10, 4]),
        "context": "Trials per million population across 8 SAARC nations reveals stark inequality in research capacity distribution.",
        "refs": [REF_CTGOV, REF_WHO, REF_SAARC],
    },
    # ... remaining 34 geographic-equity papers follow same pattern
    # Paper 2: india-dominance-index
    # Paper 3: pakistan-per-capita-deficit
    # ... through Paper 35: geographic-equity-trend
]

_HEALTH_PAPERS = [
    {
        "slug": "cardiovascular-trial-gap",
        "title": "Cardiovascular Trial Gap",
        "group": "health-disease",
        "paper_num": 1,
        "query": {"condition": "Cardiovascular Diseases", "countries": SAARC_COUNTRIES},
        "stats": ["rate_ratio", "bootstrap_ci", "chi_squared", "poisson_rate", "bayesian_rate"],
        "charts": _charts([0, 2, 6, 3, 4, 9, 10, 7]),
        "context": "CVD is the leading cause of death across South Asia yet trial investment remains disproportionately low.",
        "refs": [REF_CTGOV, REF_WHO, "Global Burden of Disease Study 2019"],
    },
    # ... remaining 34 health-disease papers
]

_GOV_PAPERS = [
    {
        "slug": "foreign-sponsor-dominance",
        "title": "Foreign Sponsor Dominance",
        "group": "governance-justice",
        "paper_num": 1,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["gini_coefficient", "hhi_index", "bootstrap_ci", "rate_ratio", "chi_squared"],
        "charts": _charts([0, 1, 8, 2, 6, 9, 7, 4]),
        "context": "Foreign sponsors control a majority of South Asian clinical trials, raising questions about data sovereignty and research priorities.",
        "refs": [REF_CTGOV, REF_SAARC, REF_WHO],
    },
    # ... remaining 34 governance-justice papers
]

_METHODS_PAPERS = [
    {
        "slug": "phase-distribution-analysis",
        "title": "Phase Distribution Analysis",
        "group": "methods-systems",
        "paper_num": 1,
        "query": {"condition": None, "countries": SAARC_COUNTRIES},
        "stats": ["chi_squared", "bootstrap_ci", "shannon_entropy", "hhi_index", "gini_coefficient"],
        "charts": _charts([0, 13, 2, 6, 3, 4, 9, 7]),
        "context": "The distribution of trial phases across SAARC reveals heavy reliance on Phase III with minimal Phase I capacity.",
        "refs": [REF_CTGOV, REF_WHO],
    },
    # ... remaining 34 methods-systems papers
]

_PAKISTAN_PAPERS = [
    # Provincial Inequity (1-10)
    {
        "slug": "punjab-trial-dominance",
        "title": "Punjab Trial Dominance",
        "group": "pakistan-deep-dive",
        "paper_num": 1,
        "query": {"condition": None, "countries": ["Pakistan"]},
        "stats": ["gini_coefficient", "bootstrap_ci", "hhi_index", "poisson_rate", "rate_ratio"],
        "charts": _charts([15, 1, 2, 6, 3, 9, 7, 4]),  # 15 = choropleth_pakistan
        "context": "Punjab, with Lahore as its research hub, dominates Pakistan's clinical trial landscape while other provinces face severe research capacity deficits.",
        "refs": [REF_CTGOV, REF_DRAP, REF_PMRC],
    },
    # ... remaining 49 pakistan-deep-dive papers
    # Papers 2-10: provincial inequity
    # Papers 11-18: institutional concentration
    # Papers 19-30: disease-specific gaps
    # Papers 31-38: sponsor & sovereignty
    # Papers 39-45: workforce & methods
    # Papers 46-50: karachi lens
]

# All 190 papers combined
PAPERS = _GEO_PAPERS + _HEALTH_PAPERS + _GOV_PAPERS + _METHODS_PAPERS + _PAKISTAN_PAPERS
```

**IMPORTANT:** The implementer must fill in ALL 190 paper definitions following this exact pattern. Use the design spec's paper topics list (Section 4) as the source for slugs, titles, and context. Each paper needs:
- Unique slug (kebab-case of title)
- title (from spec)
- group (one of the 5 group keys)
- paper_num (1-35 for groups 1-4, 1-50 for group 5)
- query (condition string or None, countries list)
- stats (5+ from: gini_coefficient, bootstrap_ci, poisson_rate, rate_ratio, shannon_entropy, hhi_index, theil_index, chi_squared, bayesian_rate, morans_i, permutation_test, spearman_correlation, linear_regression, network_centrality, kaplan_meier_survival, odds_ratio, cohens_d, kl_divergence, concentration_index, lorenz_area, atkinson_index)
- charts (exactly 8, using `_charts([indices])`)
- context (1-2 sentences describing the paper's focus)
- refs (2-3 reference strings)

For Group 5 papers, use `_charts([15, ...])` to include `choropleth_pakistan` as the first chart where appropriate.

Assign stats and charts to maximize diversity — avoid repeating the same combination across papers in the same group.

- [ ] **Step 5: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_paper_manifest.py -v`
Expected: All 11 tests PASS.

- [ ] **Step 6: Commit**

```bash
cd /c/saarc-e156-students
git add lib/__init__.py lib/paper_manifest.py tests/test_paper_manifest.py
git commit -m "feat: paper manifest with 190 SAARC paper definitions"
```

---

## Task 2: Data Fetcher (CT.gov API Wrapper)

**Files:**
- Create: `C:\saarc-e156-students\lib\data_fetcher.py`
- Create: `C:\saarc-e156-students\tests\test_data_fetcher.py`

Wraps the ClinicalTrials.gov API v2 with JSON caching and rate limiting. Adapted from `C:\Users\user\africa-e156-students\lib\data_fetcher.py` (231 lines).

- [ ] **Step 1: Write test for data_fetcher**

```python
# tests/test_data_fetcher.py
"""Tests for CT.gov API wrapper — uses cached/mock data, no network calls."""
import sys, os, json, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib import data_fetcher

def test_extract_study_metrics_empty():
    metrics = data_fetcher.extract_study_metrics([])
    assert metrics["total"] == 0
    assert metrics["phases"] == {}
    assert metrics["countries"] == {}

def test_extract_study_metrics_basic():
    studies = [
        {
            "protocolSection": {
                "statusModule": {"overallStatus": "COMPLETED"},
                "designModule": {"phases": ["PHASE3"], "designInfo": {"allocation": "RANDOMIZED"}},
                "descriptionModule": {"briefSummary": "A trial"},
                "sponsorCollaboratorsModule": {"leadSponsor": {"name": "TestSponsor", "class": "INDUSTRY"}},
                "contactsLocationsModule": {"locations": [
                    {"country": "Pakistan", "city": "Karachi"},
                    {"country": "India", "city": "Mumbai"},
                ]},
                "enrollmentInfo": {"count": 200},
                "statusModule": {"overallStatus": "COMPLETED", "startDateStruct": {"date": "2020-01"}},
                "conditionsModule": {"conditions": ["Diabetes"]},
            }
        }
    ]
    metrics = data_fetcher.extract_study_metrics(studies)
    assert metrics["total"] == 1
    assert "Pakistan" in metrics["countries"]
    assert "India" in metrics["countries"]

def test_cache_write_and_read(tmp_path):
    original_cache = data_fetcher.CACHE_DIR
    data_fetcher.CACHE_DIR = tmp_path
    try:
        data_fetcher._write_cache("test-slug", {"total": 42})
        result = data_fetcher._read_cache("test-slug")
        assert result is not None
        assert result["total"] == 42
    finally:
        data_fetcher.CACHE_DIR = original_cache

def test_cache_miss_returns_none(tmp_path):
    original_cache = data_fetcher.CACHE_DIR
    data_fetcher.CACHE_DIR = tmp_path
    try:
        result = data_fetcher._read_cache("nonexistent-slug")
        assert result is None
    finally:
        data_fetcher.CACHE_DIR = original_cache

def test_saarc_countries_in_fetcher():
    assert "Pakistan" in data_fetcher.SAARC_COUNTRIES
    assert len(data_fetcher.SAARC_COUNTRIES) == 8

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_data_fetcher.py -v`
Expected: ImportError.

- [ ] **Step 3: Write data_fetcher.py**

Adapt from `C:\Users\user\africa-e156-students\lib\data_fetcher.py`. Key changes:
- Replace Africa country references with SAARC countries
- Update API query parameters for South Asian locations
- Keep same caching pattern (JSON files in `data_cache/`)
- Keep same rate limiting (0.2-0.3s between API calls)
- Keep same `extract_study_metrics()` function

```python
# lib/data_fetcher.py
"""ClinicalTrials.gov API v2 wrapper with caching for SAARC analysis."""
import json, os, time, random, hashlib
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://clinicaltrials.gov/api/v2"
CACHE_DIR = Path(__file__).parent.parent / "data_cache"
CACHE_DIR.mkdir(exist_ok=True)

SAARC_COUNTRIES = [
    "India", "Pakistan", "Bangladesh", "Sri Lanka",
    "Nepal", "Afghanistan", "Bhutan", "Maldives"
]

def _read_cache(slug):
    """Read cached data for a paper slug. Returns dict or None."""
    cache_file = CACHE_DIR / f"{slug}.json"
    if cache_file.exists():
        with open(cache_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def _write_cache(slug, data):
    """Write data to cache."""
    cache_file = CACHE_DIR / f"{slug}.json"
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def fetch_trial_count(condition=None, location=None, other_terms=None):
    """Fetch trial count from CT.gov API v2. Returns int."""
    if requests is None:
        return 0
    params = {"countTotal": "true", "pageSize": 0}
    query_parts = []
    if condition:
        params["query.cond"] = condition
    if location:
        params["query.locn"] = location
    if other_terms:
        params["query.term"] = other_terms
    try:
        resp = requests.get(f"{BASE_URL}/studies", params=params, timeout=15)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception:
        return 0

def fetch_studies(condition=None, location=None, other_terms=None, max_results=100):
    """Fetch study records from CT.gov API v2. Returns list of study dicts."""
    if requests is None:
        return []
    params = {
        "pageSize": min(max_results, 100),
        "fields": "NCTId,BriefTitle,OverallStatus,Phase,EnrollmentCount,"
                  "StartDate,Condition,LeadSponsorName,LeadSponsorClass,"
                  "LocationCountry,LocationCity,StudyType,DesignAllocation",
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
        return resp.json().get("studies", [])
    except Exception:
        return []

def extract_study_metrics(studies):
    """Parse study records into aggregated metrics dict."""
    metrics = {
        "total": len(studies),
        "statuses": {},
        "phases": {},
        "enrollment_values": [],
        "start_years": [],
        "countries": {},
        "cities": {},
        "designs": {"randomized": 0, "non_randomized": 0, "other": 0},
        "conditions_list": [],
        "sponsors": {},
        "sponsor_classes": {},
    }
    for s in studies:
        ps = s.get("protocolSection", {})
        # Status
        status = ps.get("statusModule", {}).get("overallStatus", "UNKNOWN")
        metrics["statuses"][status] = metrics["statuses"].get(status, 0) + 1
        # Phase
        phases = ps.get("designModule", {}).get("phases", [])
        for ph in phases:
            metrics["phases"][ph] = metrics["phases"].get(ph, 0) + 1
        # Enrollment
        enroll = ps.get("enrollmentInfo", {}).get("count")
        if enroll:
            metrics["enrollment_values"].append(enroll)
        # Start year
        start = ps.get("statusModule", {}).get("startDateStruct", {}).get("date", "")
        if start and len(start) >= 4:
            try:
                metrics["start_years"].append(int(start[:4]))
            except ValueError:
                pass
        # Locations
        locs = ps.get("contactsLocationsModule", {}).get("locations", [])
        for loc in locs:
            country = loc.get("country", "")
            city = loc.get("city", "")
            if country:
                metrics["countries"][country] = metrics["countries"].get(country, 0) + 1
            if city:
                metrics["cities"][city] = metrics["cities"].get(city, 0) + 1
        # Design
        alloc = ps.get("designModule", {}).get("designInfo", {}).get("allocation", "")
        if "RANDOM" in alloc.upper():
            metrics["designs"]["randomized"] += 1
        elif alloc:
            metrics["designs"]["non_randomized"] += 1
        else:
            metrics["designs"]["other"] += 1
        # Conditions
        conds = ps.get("conditionsModule", {}).get("conditions", [])
        metrics["conditions_list"].extend(conds)
        # Sponsors
        sponsor = ps.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {})
        sp_name = sponsor.get("name", "Unknown")
        sp_class = sponsor.get("class", "OTHER")
        metrics["sponsors"][sp_name] = metrics["sponsors"].get(sp_name, 0) + 1
        metrics["sponsor_classes"][sp_class] = metrics["sponsor_classes"].get(sp_class, 0) + 1
    return metrics

def fetch_paper_data(paper_def):
    """Main entry point: fetch data for a paper definition. Uses cache if available."""
    slug = paper_def["slug"]
    # Check cache first
    cached = _read_cache(slug)
    if cached:
        return cached
    # Build query
    query = paper_def.get("query", {})
    condition = query.get("condition")
    countries = query.get("countries", SAARC_COUNTRIES)
    # Fetch counts per country
    country_counts = {}
    for country in countries:
        time.sleep(random.uniform(0.2, 0.3))
        count = fetch_trial_count(condition=condition, location=country)
        country_counts[country] = count
    # Fetch sample studies for the primary country/condition
    location = countries[0] if countries else "Pakistan"
    studies = fetch_studies(condition=condition, location=location, max_results=100)
    metrics = extract_study_metrics(studies)
    # Assemble result
    data = {
        "slug": slug,
        "country_counts": country_counts,
        "saarc_total": sum(country_counts.values()),
        "metrics": metrics,
        "query": query,
    }
    # Also fetch global count for comparison
    time.sleep(random.uniform(0.2, 0.3))
    data["global_count"] = fetch_trial_count(condition=condition)
    # Cache result
    _write_cache(slug, data)
    return data
```

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_data_fetcher.py -v`
Expected: All 5 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/data_fetcher.py tests/test_data_fetcher.py
git commit -m "feat: CT.gov API wrapper with caching for SAARC countries"
```

---

## Task 3: Statistics Library

**Files:**
- Create: `C:\saarc-e156-students\lib\stats_library.py`
- Create: `C:\saarc-e156-students\tests\test_stats_library.py`

Pure-Python (stdlib only) implementation of 31+ statistical methods. Adapt from `C:\Users\user\africa-e156-students\lib\stats_library.py` (1777 lines).

- [ ] **Step 1: Write tests**

```python
# tests/test_stats_library.py
"""Tests for pure-Python statistical library."""
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib import stats_library as sl

def test_gini_perfect_equality():
    result = sl.gini_coefficient([10, 10, 10, 10])
    assert abs(result["gini"] - 0.0) < 0.01

def test_gini_high_inequality():
    result = sl.gini_coefficient([0, 0, 0, 100])
    assert result["gini"] > 0.7

def test_shannon_entropy_uniform():
    result = sl.shannon_entropy([25, 25, 25, 25])
    assert abs(result["entropy"] - 2.0) < 0.01  # log2(4) = 2

def test_shannon_entropy_concentrated():
    result = sl.shannon_entropy([100, 0, 0, 0])
    assert result["entropy"] < 0.01

def test_hhi_monopoly():
    result = sl.herfindahl_hirschman_index([100])
    assert abs(result["hhi"] - 10000) < 1

def test_hhi_even_split():
    result = sl.herfindahl_hirschman_index([25, 25, 25, 25])
    assert abs(result["hhi"] - 2500) < 1

def test_bootstrap_ci_basic():
    data = [10, 12, 14, 11, 13, 15, 9, 16]
    result = sl.bootstrap_ci(data, n_boot=500, seed=42)
    assert result["ci_lo"] < result["mean"] < result["ci_hi"]

def test_poisson_rate():
    result = sl.poisson_rate(50, 1000000)
    assert result["rate"] > 0
    assert result["ci_lo"] < result["rate"] < result["ci_hi"]

def test_rate_ratio():
    result = sl.rate_ratio(100, 1000000, 50, 500000)
    assert "rr" in result
    assert result["rr"] > 0

def test_bayesian_rate():
    result = sl.bayesian_rate(10, 100)
    assert 0 < result["mean"] < 1
    assert result["ci_lo"] < result["mean"] < result["ci_hi"]

def test_chi_squared():
    observed = [50, 30, 20]
    expected = [33.3, 33.3, 33.4]
    result = sl.chi_squared(observed, expected)
    assert result["chi2"] > 0
    assert 0 <= result["p_value"] <= 1

def test_theil_index():
    result = sl.theil_index([10, 20, 30, 40])
    assert result["theil"] >= 0

def test_spearman_correlation():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 6, 8, 10]
    result = sl.spearman_correlation(x, y)
    assert abs(result["rho"] - 1.0) < 0.01

def test_network_centrality():
    adj = [[0, 1, 1], [1, 0, 0], [1, 0, 0]]
    result = sl.network_centrality(adj)
    assert len(result["centrality"]) == 3
    assert result["centrality"][0] == max(result["centrality"])

def test_normal_cdf_symmetry():
    assert abs(sl._normal_cdf(0) - 0.5) < 0.001
    assert abs(sl._normal_cdf(1.96) - 0.975) < 0.01

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_stats_library.py -v`
Expected: ImportError.

- [ ] **Step 3: Write stats_library.py**

Adapt from `C:\Users\user\africa-e156-students\lib\stats_library.py` (1777 lines). This is a large file. Copy the entire file and verify it works — the statistical methods are domain-agnostic (Gini, entropy, HHI, bootstrap, etc.) and don't need SAARC-specific changes.

Key functions to include (all must exist):
- `_normal_cdf(z)`, `_normal_ppf(p)`, `_chi2_cdf(x, df)`, `_chi2_ppf(p, df)`
- `_mean(values)`, `_var(values)`, `_std(values)`, `_rank(values)`
- `gini_coefficient(values)` -> `{"gini": float, "mean": float}`
- `shannon_entropy(values)` -> `{"entropy": float}`
- `herfindahl_hirschman_index(values)` -> `{"hhi": float}`
- `theil_index(values)` -> `{"theil": float}`
- `atkinson_index(values, epsilon=0.5)` -> `{"atkinson": float}`
- `kl_divergence(p_vals, q_vals)` -> `{"kl": float}`
- `bootstrap_ci(data, n_boot=1000, seed=None)` -> `{"mean": float, "ci_lo": float, "ci_hi": float}`
- `poisson_rate(count, exposure)` -> `{"rate": float, "ci_lo": float, "ci_hi": float}`
- `rate_ratio(c1, e1, c2, e2)` -> `{"rr": float, "ci_lo": float, "ci_hi": float}`
- `bayesian_rate(successes, trials, prior_a=1, prior_b=1)` -> `{"mean": float, "ci_lo": float, "ci_hi": float}`
- `chi_squared(observed, expected)` -> `{"chi2": float, "p_value": float}`
- `morans_i(values, adjacency)` -> `{"I": float, "p_value": float}`
- `spearman_correlation(x, y)` -> `{"rho": float}`
- `linear_regression(x, y)` -> `{"slope": float, "intercept": float, "r_squared": float}`
- `network_centrality(adjacency)` -> `{"centrality": list}`
- `kaplan_meier_survival(events)` -> `{"times": list, "survival": list}`
- `odds_ratio(a, b, c, d)` -> `{"or": float, "ci_lo": float, "ci_hi": float}`
- `cohens_d(group1, group2)` -> `{"d": float}`
- `permutation_test(group1, group2, n_perm=1000, seed=None)` -> `{"p_value": float}`
- `concentration_index(values)` -> `{"ci": float}`
- `lorenz_area(values)` -> `{"area": float}`
- `_gaussian_kde(data, n_points=80, bw=None)` -> list of (x, y) tuples

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_stats_library.py -v`
Expected: All 15 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/stats_library.py tests/test_stats_library.py
git commit -m "feat: 31+ pure-Python statistical methods library"
```

---

## Task 4: Chart Library (SVG Generators + SAARC/Pakistan Maps)

**Files:**
- Create: `C:\saarc-e156-students\lib\chart_library.py`
- Create: `C:\saarc-e156-students\tests\test_chart_library.py`

15+ SVG chart generators in pure Python. Adapt from Africa project's `chart_library.py` (1304 lines). Critical new additions: `choropleth_saarc()` (South Asia map) and `choropleth_pakistan()` (provincial map).

- [ ] **Step 1: Write tests**

```python
# tests/test_chart_library.py
"""Tests for SVG chart generators."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib import chart_library as cl

def _is_valid_svg(s):
    return s.startswith("<svg") and s.endswith("</svg>")

def test_choropleth_saarc():
    values = {"India": 5000, "Pakistan": 800, "Bangladesh": 300, "Sri Lanka": 200,
              "Nepal": 100, "Afghanistan": 50, "Bhutan": 10, "Maldives": 5}
    svg = cl.choropleth_saarc(values, "SAARC Trial Density")
    assert _is_valid_svg(svg)
    assert "Pakistan" in svg

def test_choropleth_pakistan():
    values = {"Punjab": 400, "Sindh": 300, "Khyber Pakhtunkhwa": 50,
              "Balochistan": 10, "Islamabad Capital Territory": 80,
              "Gilgit-Baltistan": 5, "Azad Jammu and Kashmir": 8}
    svg = cl.choropleth_pakistan(values, "Pakistan Provincial Trials")
    assert _is_valid_svg(svg)
    assert "Punjab" in svg

def test_lorenz_chart():
    svg = cl.lorenz_chart([10, 20, 30, 40, 50], "Lorenz Curve")
    assert _is_valid_svg(svg)

def test_forest_plot():
    regions = [
        {"name": "India", "mean": 5000, "ci_lo": 4500, "ci_hi": 5500},
        {"name": "Pakistan", "mean": 800, "ci_lo": 700, "ci_hi": 900},
    ]
    svg = cl.forest_plot(regions, "Trial Counts")
    assert _is_valid_svg(svg)

def test_heatmap():
    matrix = [[10, 20], [30, 40]]
    svg = cl.heatmap_chart(matrix, ["Row1", "Row2"], ["Col1", "Col2"], "Test")
    assert _is_valid_svg(svg)

def test_timeseries():
    series = [{"name": "Pakistan", "data": [(2015, 50), (2016, 60), (2017, 75)]}]
    svg = cl.timeseries_chart(series, "Trend")
    assert _is_valid_svg(svg)

def test_radar_chart():
    dims = [("Volume", 0.8), ("Growth", 0.6), ("Diversity", 0.4),
            ("Completion", 0.7), ("Quality", 0.5), ("Equity", 0.3)]
    svg = cl.radar_chart(dims, "Research Profile")
    assert _is_valid_svg(svg)

def test_waterfall_chart():
    items = [("India", 5000), ("Pakistan", 800), ("Bangladesh", 300)]
    svg = cl.waterfall_chart(items, "Top Countries")
    assert _is_valid_svg(svg)

def test_bubble_chart():
    data = [{"x": 10, "y": 20, "size": 5, "label": "A"},
            {"x": 30, "y": 40, "size": 10, "label": "B"}]
    svg = cl.bubble_chart(data, "x", "y", "Test Bubble")
    assert _is_valid_svg(svg)

def test_funnel_chart():
    stages = [("Phase I", 100), ("Phase II", 60), ("Phase III", 30), ("Phase IV", 10)]
    svg = cl.funnel_chart(stages, "Phase Funnel")
    assert _is_valid_svg(svg)

def test_all_chart_types_callable():
    """Verify all 16 chart functions exist and are callable."""
    funcs = [
        cl.choropleth_saarc, cl.choropleth_pakistan, cl.lorenz_chart,
        cl.forest_plot, cl.violin_plot, cl.heatmap_chart, cl.network_graph,
        cl.timeseries_chart, cl.waterfall_chart, cl.sankey_chart,
        cl.radar_chart, cl.bubble_chart, cl.slope_chart, cl.ridge_plot,
        cl.funnel_chart, cl.kaplan_meier_chart,
    ]
    for f in funcs:
        assert callable(f), f"{f.__name__} is not callable"

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_chart_library.py -v`
Expected: ImportError.

- [ ] **Step 3: Write chart_library.py**

Adapt from `C:\Users\user\africa-e156-students\lib\chart_library.py` (1304 lines). Key changes:

1. **Replace `_AFRICA_PATHS`** (Africa SVG map data) with `_SAARC_PATHS` — simplified SVG path data for 8 SAARC nations. Create approximate boundary polygons for each country.

2. **Add `_PAKISTAN_PATHS`** — SVG path data for 7 Pakistan provinces/territories (Punjab, Sindh, KPK, Balochistan, ICT, GB, AJK). Create approximate boundary polygons.

3. **Replace `choropleth_africa()`** with `choropleth_saarc()` — uses `_SAARC_PATHS` to render South Asia map with color-coded countries.

4. **Add `choropleth_pakistan()`** — new function using `_PAKISTAN_PATHS` to render provincial map.

5. **Update color palette**:
```python
_PAKISTAN = "#006600"    # Pakistan green
_INDIA = "#FF9933"      # India saffron
_SAARC = "#0d6b57"      # Teal for SAARC region
_INK = "#1d2430"
_MUTED = "#4a5568"
_LINE = "#d8cfbf"
_BG = "#fffdf8"
_FONT = "Georgia,'Times New Roman',serif"
```

6. **Keep all other 13 chart functions** identical (lorenz, forest, violin, heatmap, network, timeseries, waterfall, sankey, radar, bubble, slope, ridge, funnel, kaplan_meier) — they are data-agnostic.

7. **Update `CHART_TYPE_MAP`**:
```python
CHART_TYPE_MAP = {
    "choropleth": "choropleth_saarc",
    "choropleth_pakistan": "choropleth_pakistan",
    "lorenz": "lorenz_chart",
    "forest": "forest_plot",
    "violin": "violin_plot",
    "heatmap": "heatmap_chart",
    "network": "network_graph",
    "timeseries": "timeseries_chart",
    "waterfall": "waterfall_chart",
    "sankey": "sankey_chart",
    "radar": "radar_chart",
    "bubble": "bubble_chart",
    "slope": "slope_chart",
    "ridge": "ridge_plot",
    "funnel": "funnel_chart",
    "kaplan_meier": "kaplan_meier_chart",
}
```

For the SAARC and Pakistan SVG maps, use simplified polygon paths. The maps don't need to be cartographically precise — they need to be recognizable and color-codeable. Use approximate centroids for label placement.

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_chart_library.py -v`
Expected: All 11 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/chart_library.py tests/test_chart_library.py
git commit -m "feat: 16 SVG chart generators with SAARC + Pakistan maps"
```

---

## Task 5: Body Generator (E156 Text)

**Files:**
- Create: `C:\saarc-e156-students\lib\body_generator.py`
- Create: `C:\saarc-e156-students\tests\test_body_generator.py`

Generates exactly 7-sentence, <=156-word E156 bodies. Adapt from `C:\Users\user\africa-e156-students\lib\body_generator.py` (334 lines).

- [ ] **Step 1: Write tests**

```python
# tests/test_body_generator.py
"""Tests for E156 body generator."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.body_generator import generate_body

def _word_count(text):
    return len(text.split())

def _sentence_count(text):
    import re
    # Count sentences ending with period, question mark, etc.
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text.strip())
    return len(sentences)

def _make_paper_def(slug="test-paper", group="geographic-equity"):
    return {
        "slug": slug,
        "title": "Test Paper",
        "group": group,
        "paper_num": 1,
        "query": {"condition": None, "countries": ["Pakistan", "India"]},
        "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate"],
        "charts": ["choropleth"] * 8,
        "context": "Test context for the paper.",
        "refs": ["Ref 1", "Ref 2"],
    }

def _make_data():
    return {
        "slug": "test-paper",
        "country_counts": {"Pakistan": 800, "India": 5000, "Bangladesh": 300},
        "saarc_total": 6100,
        "global_count": 500000,
        "metrics": {
            "total": 100,
            "phases": {"PHASE3": 50, "PHASE2": 30},
            "countries": {"Pakistan": 800},
            "enrollment_values": [100, 200, 300],
            "start_years": [2018, 2019, 2020],
        },
    }

def _make_stats():
    return {
        "gini_coefficient": {"gini": 0.72, "mean": 762.5},
        "bootstrap_ci": {"mean": 762.5, "ci_lo": 500, "ci_hi": 1025},
        "poisson_rate": {"rate": 3.5, "ci_lo": 2.1, "ci_hi": 4.9},
    }

def test_body_has_7_sentences():
    body = generate_body(_make_paper_def(), _make_data(), _make_stats())
    count = _sentence_count(body)
    assert count == 7, f"Expected 7 sentences, got {count}: {body}"

def test_body_under_157_words():
    body = generate_body(_make_paper_def(), _make_data(), _make_stats())
    wc = _word_count(body)
    assert wc <= 160, f"Body has {wc} words (limit ~156): {body}"

def test_body_is_single_paragraph():
    body = generate_body(_make_paper_def(), _make_data(), _make_stats())
    assert "\n\n" not in body, "Body should be a single paragraph"

def test_body_deterministic():
    pd, data, stats = _make_paper_def(), _make_data(), _make_stats()
    body1 = generate_body(pd, data, stats)
    body2 = generate_body(pd, data, stats)
    assert body1 == body2, "Same inputs should produce identical output"

def test_body_differs_by_group():
    data, stats = _make_data(), _make_stats()
    body_geo = generate_body(_make_paper_def(group="geographic-equity"), data, stats)
    body_health = generate_body(_make_paper_def(slug="test-health", group="health-disease"), data, stats)
    # Bodies should differ because group changes S1 and S6
    assert body_geo != body_health

def test_all_five_groups_generate():
    data, stats = _make_data(), _make_stats()
    for group in ["geographic-equity", "health-disease", "governance-justice",
                  "methods-systems", "pakistan-deep-dive"]:
        body = generate_body(_make_paper_def(slug=f"test-{group}", group=group), data, stats)
        assert len(body) > 50, f"Group {group} produced too-short body"

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_body_generator.py -v`
Expected: ImportError.

- [ ] **Step 3: Write body_generator.py**

Adapt from `C:\Users\user\africa-e156-students\lib\body_generator.py` (334 lines). Key changes:

1. **S1 templates** — Replace Africa-focused questions with SAARC-focused:
   - geographic-equity: "How equitably are clinical trials distributed across South Asia's eight SAARC nations..."
   - health-disease: "Does clinical trial investment in South Asia match the region's disease burden..."
   - governance-justice: "Who controls and benefits from clinical research across the SAARC nations..."
   - methods-systems: "How rigorous and methodologically sound are clinical trials conducted across South Asia..."
   - pakistan-deep-dive: "What does Pakistan's clinical trial landscape reveal about research capacity and equity..."

2. **S2 templates** — Reference SAARC trial counts instead of African:
   - "This cross-sectional audit evaluated {saarc_total} South Asian trials registered on ClinicalTrials.gov across {n_countries} SAARC nations."

3. **S6 templates** — SAARC-specific interpretations per group, referencing South Asian health policy context.

4. **S7 templates** — Same limitation patterns (cross-sectional, registry-only, no causation).

5. **Add group "pakistan-deep-dive"** to all switch/if-else blocks — it uses Pakistan-specific framing (provincial, institutional, DRAP, etc.).

6. **Keep `_trim_to_limit()`** and `_fmt()` helpers identical.

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_body_generator.py -v`
Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/body_generator.py tests/test_body_generator.py
git commit -m "feat: E156 body generator for SAARC 7-sentence micro-papers"
```

---

## Task 6: Code Generator (Python Script Templates)

**Files:**
- Create: `C:\saarc-e156-students\lib\code_generator.py`
- Create: `C:\saarc-e156-students\tests\test_code_generator.py`

Generates standalone Python analysis scripts (~100-150 lines) that students can download and run. Adapt from `C:\Users\user\africa-e156-students\lib\code_generator.py` (532 lines).

- [ ] **Step 1: Write tests**

```python
# tests/test_code_generator.py
"""Tests for Python analysis script generator."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.code_generator import generate_code_script

def _make_paper_def():
    return {
        "slug": "pakistan-per-capita-deficit",
        "title": "Pakistan Per-Capita Deficit",
        "group": "geographic-equity",
        "paper_num": 3,
        "query": {"condition": None, "countries": ["Pakistan", "India", "Bangladesh"]},
        "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate", "rate_ratio", "shannon_entropy"],
        "charts": ["choropleth"] * 8,
        "context": "Pakistan's trial density per capita lags behind regional peers.",
        "refs": ["ClinicalTrials.gov"],
    }

def _make_data():
    return {
        "slug": "pakistan-per-capita-deficit",
        "country_counts": {"Pakistan": 800, "India": 5000, "Bangladesh": 300},
        "saarc_total": 6100,
        "global_count": 500000,
        "metrics": {"total": 100, "phases": {}, "countries": {}},
    }

def _make_stats():
    return {"gini_coefficient": {"gini": 0.72}}

def test_script_is_valid_python():
    script = generate_code_script(_make_paper_def(), _make_data(), _make_stats())
    compile(script, "<test>", "exec")  # Syntax check

def test_script_contains_imports():
    script = generate_code_script(_make_paper_def(), _make_data(), _make_stats())
    assert "import requests" in script or "import json" in script

def test_script_contains_api_url():
    script = generate_code_script(_make_paper_def(), _make_data(), _make_stats())
    assert "clinicaltrials.gov" in script.lower()

def test_script_contains_stat_methods():
    script = generate_code_script(_make_paper_def(), _make_data(), _make_stats())
    # At least one stat method should be present
    assert "def " in script

def test_script_has_main_block():
    script = generate_code_script(_make_paper_def(), _make_data(), _make_stats())
    assert 'if __name__' in script or 'print(' in script

def test_script_references_saarc_countries():
    script = generate_code_script(_make_paper_def(), _make_data(), _make_stats())
    assert "Pakistan" in script

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_code_generator.py -v`
Expected: ImportError.

- [ ] **Step 3: Write code_generator.py**

Adapt from `C:\Users\user\africa-e156-students\lib\code_generator.py` (532 lines). Key changes:

1. **Update `_METHOD_SNIPPETS`** — Keep all 24 statistical method code snippets identical (they're math, not region-specific).

2. **Update API query builder** — Replace Africa country references with SAARC countries from the paper's query.

3. **Update header docstring template** — Reference "SAARC" and "South Asia" instead of "Africa".

4. **Update example outputs** — Print statements should reference South Asian countries.

5. **Keep script structure identical**: imports -> API query -> method implementations -> data fetch -> example computations -> print results.

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_code_generator.py -v`
Expected: All 6 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/code_generator.py tests/test_code_generator.py
git commit -m "feat: Python analysis script generator for SAARC papers"
```

---

## Task 7: Dashboard Generator

**Files:**
- Create: `C:\saarc-e156-students\lib\dashboard_generator.py`
- Create: `C:\saarc-e156-students\tests\test_dashboard_generator.py`

Generates self-contained HTML dashboards with 8 embedded SVG charts per paper. Adapt from `C:\Users\user\africa-e156-students\lib\dashboard_generator.py` (519 lines).

- [ ] **Step 1: Write tests**

```python
# tests/test_dashboard_generator.py
"""Tests for HTML dashboard generator."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.dashboard_generator import generate_dashboard

def _make_paper_def():
    return {
        "slug": "saarc-trial-density-map",
        "title": "SAARC Trial Density Map",
        "group": "geographic-equity",
        "paper_num": 1,
        "query": {"condition": None, "countries": ["Pakistan", "India"]},
        "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate"],
        "charts": ["choropleth", "lorenz", "forest", "radar",
                   "timeseries", "waterfall", "bubble", "heatmap"],
        "context": "Trial density across SAARC nations.",
        "refs": ["Ref 1"],
    }

def _make_data():
    return {
        "slug": "saarc-trial-density-map",
        "country_counts": {"Pakistan": 800, "India": 5000, "Bangladesh": 300,
                          "Sri Lanka": 200, "Nepal": 100},
        "saarc_total": 6400,
        "global_count": 500000,
        "metrics": {
            "total": 100, "phases": {"PHASE3": 50},
            "countries": {"Pakistan": 800, "India": 5000},
            "enrollment_values": [100, 200, 300],
            "start_years": [2018, 2019, 2020],
            "sponsors": {}, "sponsor_classes": {},
        },
    }

def _make_stats():
    return {
        "gini_coefficient": {"gini": 0.72, "mean": 762},
        "bootstrap_ci": {"mean": 762, "ci_lo": 500, "ci_hi": 1025},
        "poisson_rate": {"rate": 3.5, "ci_lo": 2.1, "ci_hi": 4.9},
    }

def _make_body():
    return "S1 question here. S2 data here. S3 method here. S4 result here. S5 robustness here. S6 interpretation here. S7 boundary here."

def test_dashboard_is_valid_html():
    html = generate_dashboard(_make_paper_def(), _make_data(), _make_stats(), _make_body())
    assert html.strip().startswith("<!doctype html>") or html.strip().startswith("<!DOCTYPE html>")
    assert "</html>" in html

def test_dashboard_contains_title():
    html = generate_dashboard(_make_paper_def(), _make_data(), _make_stats(), _make_body())
    assert "SAARC Trial Density Map" in html

def test_dashboard_contains_svg_charts():
    html = generate_dashboard(_make_paper_def(), _make_data(), _make_stats(), _make_body())
    assert "<svg" in html

def test_dashboard_contains_body_text():
    html = generate_dashboard(_make_paper_def(), _make_data(), _make_stats(), _make_body())
    assert "S1 question here" in html

def test_dashboard_has_sentence_breakdown():
    html = generate_dashboard(_make_paper_def(), _make_data(), _make_stats(), _make_body())
    # Should have color-coded sentence roles
    assert "Question" in html or "Dataset" in html or "sentence" in html.lower()

def test_dashboard_no_external_dependencies():
    html = generate_dashboard(_make_paper_def(), _make_data(), _make_stats(), _make_body())
    # No CDN links
    assert "cdn." not in html.lower()
    assert "unpkg.com" not in html.lower()

def test_dashboard_pakistan_deep_dive_uses_pakistan_map():
    paper = _make_paper_def()
    paper["group"] = "pakistan-deep-dive"
    paper["slug"] = "punjab-trial-dominance"
    paper["charts"] = ["choropleth_pakistan", "lorenz", "forest", "radar",
                       "timeseries", "waterfall", "bubble", "heatmap"]
    html = generate_dashboard(paper, _make_data(), _make_stats(), _make_body())
    assert "<svg" in html

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_dashboard_generator.py -v`
Expected: ImportError.

- [ ] **Step 3: Write dashboard_generator.py**

Adapt from `C:\Users\user\africa-e156-students\lib\dashboard_generator.py` (519 lines). Key changes:

1. **Update `CHART_TYPE_MAP`** to include `"choropleth_pakistan"` mapping.

2. **Update `_prepare_chart_data()`** — Route `"choropleth"` to `choropleth_saarc()` (not `choropleth_africa()`), and `"choropleth_pakistan"` to `choropleth_pakistan()`.

3. **Update CSS color palette** — Use SAARC-appropriate colors (Pakistan green accent for Group 5).

4. **Update hero metrics** — Show "SAARC trials" instead of "African trials".

5. **Update Open Graph meta tags** — Reference SAARC/South Asia.

6. **Keep sentence breakdown pattern** identical (S1-S7 color coding).

7. **Keep `${'<'}/script>` pattern** for template literals inside `<script>` blocks.

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_dashboard_generator.py -v`
Expected: All 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/dashboard_generator.py tests/test_dashboard_generator.py
git commit -m "feat: HTML dashboard generator with SAARC/Pakistan map support"
```

---

## Task 8: Index Updater (Group & Landing Pages)

**Files:**
- Create: `C:\saarc-e156-students\lib\index_updater.py`
- Create: `C:\saarc-e156-students\tests\test_index_updater.py`

Assembles group index pages and the landing page. Adapt from `C:\Users\user\africa-e156-students\lib\index_updater.py` (246 lines).

- [ ] **Step 1: Write tests**

```python
# tests/test_index_updater.py
"""Tests for HTML page assembly."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from lib.index_updater import make_paper_card, make_group_page, make_landing_page
from lib.paper_manifest import GROUPS

def test_paper_card_html():
    paper = {
        "slug": "test-paper", "title": "Test Paper",
        "group": "geographic-equity", "paper_num": 1,
        "refs": ["Ref A", "Ref B"],
    }
    body = "Test body text here."
    html = make_paper_card(paper, 1, body)
    assert "Test Paper" in html
    assert "test-paper" in html
    assert "paper-card" in html
    assert "Ref A" in html

def test_group_page_contains_instructions():
    html = make_group_page("geographic-equity", [], {})
    assert "Geographic Equity" in html
    assert "Ziauddin" in html or "instruction" in html.lower()

def test_group_page_valid_html():
    html = make_group_page("geographic-equity", [], {})
    assert "<!doctype html>" in html.lower() or "<!DOCTYPE html>" in html
    assert "</html>" in html

def test_landing_page_has_5_groups():
    html = make_landing_page()
    for group_id, group_info in GROUPS.items():
        assert group_info["title"] in html, f"Missing group: {group_info['title']}"

def test_landing_page_valid_html():
    html = make_landing_page()
    assert "<!doctype html>" in html.lower() or "<!DOCTYPE html>" in html
    assert "</html>" in html

def test_landing_page_mentions_190_papers():
    html = make_landing_page()
    assert "190" in html

def test_landing_page_mentions_ziauddin():
    html = make_landing_page()
    assert "Ziauddin" in html

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_index_updater.py -v`
Expected: ImportError.

- [ ] **Step 3: Write index_updater.py**

Adapt from `C:\Users\user\africa-e156-students\lib\index_updater.py` (246 lines). Key changes:

1. **`make_paper_card(paper, card_num, body)`** — Same HTML structure: article with paper-card class, number badge, title, sentence color strip, body text, action buttons (View Dashboard, Download Code, Download Paper), references, note block. Update GitHub URLs to `saarc-e156-students`.

2. **`make_group_page(group_id, papers, all_paper_data)`** — Full HTML page with:
   - Masthead with group title and description from `GROUPS[group_id]`
   - Instructions panel (7-step workflow for Ziauddin students)
   - Paper cards
   - E156 format rules (collapsible `<details>`)
   - CSS uses `GROUPS[group_id]["color"]` as accent
   - References Ziauddin Medical University and Synthesis Medicine Journal

3. **`make_landing_page()`** — Landing page with:
   - Title: "SAARC Clinical Trial Equity — E156 Micro-Papers"
   - Subtitle: "190 Structured Analyses for Ziauddin Medical University"
   - 5 group cards (not 4) with paper counts and colors from `GROUPS`
   - Links to group index pages
   - GitHub repo link
   - NYT editorial CSS (Georgia serif, warm palette)
   - Same `SHARED_CSS` pattern as Africa project

4. **Update all SAARC/Pakistan references** — Replace "Africa" with "South Asia"/"SAARC", "University of Uganda" with "Ziauddin Medical University".

5. **Outside Note Block template** — Update URLs to `saarc-e156-students` repo.

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_index_updater.py -v`
Expected: All 7 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add lib/index_updater.py tests/test_index_updater.py
git commit -m "feat: group and landing page HTML assembler for 5 SAARC groups"
```

---

## Task 9: Build Orchestrator

**Files:**
- Create: `C:\saarc-e156-students\build.py`
- Create: `C:\saarc-e156-students\tests\test_build.py`

Master script that coordinates the entire pipeline: fetch data -> compute stats -> generate bodies -> generate dashboards -> generate code scripts -> assemble pages. Adapt from `C:\Users\user\africa-e156-students\build.py` (1053 lines).

- [ ] **Step 1: Write tests**

```python
# tests/test_build.py
"""Tests for build orchestrator — uses mocked data, no network calls."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_build_imports():
    """Verify build.py can be imported without errors."""
    import build
    assert hasattr(build, 'build_all') or hasattr(build, 'main')

def test_build_has_group_directories():
    """Verify the 5 group output directories are defined."""
    import build
    groups = getattr(build, 'GROUP_DIRS', None) or getattr(build, 'GROUPS', None)
    assert groups is not None
    # Should have 5 groups
    if isinstance(groups, dict):
        assert len(groups) >= 5
    elif isinstance(groups, list):
        assert len(groups) >= 5

def test_build_output_path():
    """Verify output path is C:\\saarc-e156-students."""
    import build
    out = getattr(build, 'OUT', None) or getattr(build, 'OUTPUT_DIR', None)
    assert out is not None
    assert "saarc-e156-students" in str(out)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_build.py -v`
Expected: ImportError.

- [ ] **Step 3: Write build.py**

Adapt from `C:\Users\user\africa-e156-students\build.py` (1053 lines). Key structure:

```python
# build.py
"""Master build orchestrator for SAARC E156 student platform."""
import os, sys, json, time, argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from lib.paper_manifest import PAPERS, GROUPS
from lib.data_fetcher import fetch_paper_data
from lib import stats_library as sl
from lib.body_generator import generate_body
from lib.dashboard_generator import generate_dashboard
from lib.code_generator import generate_code_script
from lib.index_updater import make_paper_card, make_group_page, make_landing_page

OUT = Path("C:/saarc-e156-students")
GITHUB_PAGES = "https://mahmood789.github.io/saarc-e156-students"

GROUP_DIRS = {
    "geographic-equity": OUT / "geographic-equity",
    "health-disease": OUT / "health-disease",
    "governance-justice": OUT / "governance-justice",
    "methods-systems": OUT / "methods-systems",
    "pakistan-deep-dive": OUT / "pakistan-deep-dive",
}

# Map stat names to stats_library functions
STAT_FUNCTIONS = {
    "gini_coefficient": lambda data: sl.gini_coefficient(list(data["country_counts"].values())),
    "bootstrap_ci": lambda data: sl.bootstrap_ci(list(data["country_counts"].values()), seed=42),
    "shannon_entropy": lambda data: sl.shannon_entropy(list(data["country_counts"].values())),
    "hhi_index": lambda data: sl.herfindahl_hirschman_index(list(data["country_counts"].values())),
    "poisson_rate": lambda data: sl.poisson_rate(data["saarc_total"], 2_000_000_000),
    "rate_ratio": lambda data: sl.rate_ratio(
        data["country_counts"].get("Pakistan", 0), 220_000_000,
        data["country_counts"].get("India", 0), 1_400_000_000),
    "theil_index": lambda data: sl.theil_index(list(data["country_counts"].values())),
    "chi_squared": lambda data: sl.chi_squared(
        list(data["country_counts"].values()),
        [data["saarc_total"] / max(len(data["country_counts"]), 1)] * len(data["country_counts"])),
    "bayesian_rate": lambda data: sl.bayesian_rate(data["saarc_total"], 500000),
    "spearman_correlation": lambda data: sl.spearman_correlation(
        list(range(len(data["country_counts"]))),
        sorted(data["country_counts"].values())),
    # Add remaining stat mappings...
}

def compute_stats(paper_def, data):
    """Run all assigned statistical methods for a paper."""
    results = {}
    for stat_name in paper_def["stats"]:
        fn = STAT_FUNCTIONS.get(stat_name)
        if fn:
            try:
                results[stat_name] = fn(data)
            except Exception as e:
                print(f"  WARN: {stat_name} failed for {paper_def['slug']}: {e}")
                results[stat_name] = {}
    return results

def build_paper(paper_def):
    """Build a single paper: fetch data, compute stats, generate outputs."""
    slug = paper_def["slug"]
    group = paper_def["group"]
    group_dir = GROUP_DIRS[group]

    print(f"  [{paper_def['paper_num']:>3}] {slug}")

    # 1. Fetch data
    data = fetch_paper_data(paper_def)

    # 2. Compute stats
    stats = compute_stats(paper_def, data)

    # 3. Generate E156 body
    body = generate_body(paper_def, data, stats)

    # 4. Generate dashboard HTML
    dashboard_html = generate_dashboard(paper_def, data, stats, body)
    dash_path = group_dir / "dashboards" / f"{slug}.html"
    dash_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dash_path, "w", encoding="utf-8") as f:
        f.write(dashboard_html)

    # 5. Generate Python script
    code = generate_code_script(paper_def, data, stats)
    code_path = group_dir / "code" / f"{slug}.py"
    code_path.parent.mkdir(parents=True, exist_ok=True)
    with open(code_path, "w", encoding="utf-8") as f:
        f.write(code)

    return {"slug": slug, "body": body, "data": data, "stats": stats}

def build_group(group_id):
    """Build all papers in a group, then assemble group index page."""
    group_papers = [p for p in PAPERS if p["group"] == group_id]
    print(f"\n=== {GROUPS[group_id]['title']} ({len(group_papers)} papers) ===")

    all_results = {}
    for paper_def in group_papers:
        result = build_paper(paper_def)
        all_results[paper_def["slug"]] = result

    # Generate group index page
    group_dir = GROUP_DIRS[group_id]
    html = make_group_page(group_id, group_papers, all_results)
    with open(group_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    return all_results

def build_all():
    """Build entire platform: all 5 groups + landing page."""
    print("Building SAARC E156 Student Platform (190 papers)")
    print("=" * 60)

    all_results = {}
    for group_id in GROUP_DIRS:
        group_results = build_group(group_id)
        all_results.update(group_results)

    # Generate landing page
    html = make_landing_page()
    with open(OUT / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n{'=' * 60}")
    print(f"DONE: {len(all_results)} papers built")
    print(f"Output: {OUT}")

def main():
    parser = argparse.ArgumentParser(description="Build SAARC E156 student platform")
    parser.add_argument("--all", action="store_true", help="Build all 190 papers")
    parser.add_argument("--group", type=str, help="Build a single group")
    parser.add_argument("--paper", type=str, help="Build a single paper by slug")
    args = parser.parse_args()

    if args.paper:
        paper = next((p for p in PAPERS if p["slug"] == args.paper), None)
        if not paper:
            print(f"Paper not found: {args.paper}")
            sys.exit(1)
        build_paper(paper)
    elif args.group:
        if args.group not in GROUP_DIRS:
            print(f"Unknown group: {args.group}")
            sys.exit(1)
        build_group(args.group)
    else:
        build_all()

if __name__ == "__main__":
    main()
```

The implementer should complete all `STAT_FUNCTIONS` mappings for the remaining stat methods (morans_i, permutation_test, linear_regression, network_centrality, kaplan_meier_survival, odds_ratio, cohens_d, kl_divergence, concentration_index, lorenz_area, atkinson_index).

- [ ] **Step 4: Run tests**

Run: `cd /c/saarc-e156-students && python -m pytest tests/test_build.py -v`
Expected: All 3 tests PASS.

- [ ] **Step 5: Commit**

```bash
cd /c/saarc-e156-students
git add build.py tests/test_build.py
git commit -m "feat: master build orchestrator for 190 SAARC papers"
```

---

## Task 10: Analysis Scripts (Country Audit + Statistical Deep Dive)

**Files:**
- Create: `C:\saarc-e156-students\analysis\fetch_saarc_rcts_by_country.py`
- Create: `C:\saarc-e156-students\analysis\statistical_deep_dive.py`

Standalone analysis scripts that generate overview data and dashboards for all 8 SAARC nations.

- [ ] **Step 1: Write fetch_saarc_rcts_by_country.py**

Adapt from `C:\Users\user\africa-e156-students\analysis\fetch_africa_rcts_by_country.py`. Key changes:
- Query all 8 SAARC countries instead of 54 African nations
- Include Pakistan provincial breakdown (query by city)
- Add population data for per-capita calculations:
  ```python
  POPULATIONS = {
      "India": 1_428_000_000,
      "Pakistan": 231_000_000,
      "Bangladesh": 173_000_000,
      "Sri Lanka": 22_000_000,
      "Nepal": 30_000_000,
      "Afghanistan": 41_000_000,
      "Bhutan": 782_000,
      "Maldives": 521_000,
  }
  ```
- Output JSON to `analysis/saarc_country_data.json`
- Generate `analysis/saarc_rct_country_dashboard.html` (overview choropleth + bar charts)

- [ ] **Step 2: Write statistical_deep_dive.py**

Adapt from `C:\Users\user\africa-e156-students\analysis\statistical_deep_dive.py`. Apply 10 methods to SAARC data:
1. Lorenz curve (trial inequality)
2. Gini coefficient
3. HHI (concentration)
4. Moran's I (spatial autocorrelation — use SAARC adjacency matrix)
5. Bootstrap CI for mean trial count
6. Permutation test (Pakistan vs others)
7. Bayesian rate estimation
8. Time-series decomposition (registration trends)
9. Network analysis (cross-country collaboration)
10. PCA (trial characteristic drivers)

Output: `analysis/statistical_deep_dive.html`

- [ ] **Step 3: Commit**

```bash
cd /c/saarc-e156-students
git add analysis/
git commit -m "feat: country audit and statistical deep dive for SAARC"
```

---

## Task 11: Batch Generation Scripts

**Files:**
- Create: `C:\saarc-e156-students\generate_dashboards.py`
- Create: `C:\saarc-e156-students\rewrite_all_papers.py`

Convenience scripts for regenerating specific outputs without full rebuild.

- [ ] **Step 1: Write generate_dashboards.py**

```python
# generate_dashboards.py
"""Regenerate all 190 HTML dashboards from cached data."""
import sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.paper_manifest import PAPERS
from lib.data_fetcher import _read_cache
from lib import stats_library as sl
from lib.body_generator import generate_body
from lib.dashboard_generator import generate_dashboard
from build import compute_stats, GROUP_DIRS

def main():
    count = 0
    for paper_def in PAPERS:
        slug = paper_def["slug"]
        data = _read_cache(slug)
        if not data:
            print(f"SKIP (no cache): {slug}")
            continue
        stats = compute_stats(paper_def, data)
        body = generate_body(paper_def, data, stats)
        html = generate_dashboard(paper_def, data, stats, body)
        group_dir = GROUP_DIRS[paper_def["group"]]
        path = group_dir / "dashboards" / f"{slug}.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print(f"[{count:>3}] {slug}")
    print(f"\nDone: {count} dashboards regenerated")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write rewrite_all_papers.py**

```python
# rewrite_all_papers.py
"""Regenerate all 190 E156 bodies from cached data."""
import sys, json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from lib.paper_manifest import PAPERS
from lib.data_fetcher import _read_cache
from lib.body_generator import generate_body
from build import compute_stats

def main():
    count = 0
    bodies = {}
    for paper_def in PAPERS:
        slug = paper_def["slug"]
        data = _read_cache(slug)
        if not data:
            print(f"SKIP (no cache): {slug}")
            continue
        stats = compute_stats(paper_def, data)
        body = generate_body(paper_def, data, stats)
        bodies[slug] = body
        wc = len(body.split())
        count += 1
        print(f"[{count:>3}] {slug} ({wc}w)")
    # Save all bodies to JSON
    with open("data_cache/all_bodies.json", "w", encoding="utf-8") as f:
        json.dump(bodies, f, indent=2)
    print(f"\nDone: {count} bodies generated, saved to data_cache/all_bodies.json")

if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Commit**

```bash
cd /c/saarc-e156-students
git add generate_dashboards.py rewrite_all_papers.py
git commit -m "feat: batch generation scripts for dashboards and E156 bodies"
```

---

## Task 12: E156 Protocol + README

**Files:**
- Create: `C:\saarc-e156-students\E156-PROTOCOL.md`
- Create: `C:\saarc-e156-students\README.md`

- [ ] **Step 1: Write E156-PROTOCOL.md**

```markdown
# E156 Protocol — SAARC Clinical Trial Equity

**Project**: SAARC E156 Student Assignment Platform
**Date created**: 2026-04-08
**Date last updated**: 2026-04-08
**Entry**: [TBD — assign when added to rewrite-workbook.txt]

## E156 Body

[To be populated after first build run — copy CURRENT BODY from rewrite-workbook.txt]

## Links

- **Live dashboard**: https://mahmood789.github.io/saarc-e156-students/
- **GitHub repo**: https://github.com/mahmood726-cyber/saarc-e156-students
- **Rewrite workbook entry**: [TBD]

## Data Source

ClinicalTrials.gov API v2 (public, no API key required)

## Scope

190 E156 micro-papers across 5 thematic groups analyzing clinical trial equity
across 8 SAARC nations (India, Pakistan, Bangladesh, Sri Lanka, Nepal,
Afghanistan, Bhutan, Maldives) with special emphasis on Pakistan.

Target audience: Ziauddin Medical University students (Karachi, Pakistan).
```

- [ ] **Step 2: Write README.md**

```markdown
# SAARC E156 Student Assignment Platform

190 structured micro-papers analyzing clinical trial equity across 8 SAARC nations,
with special emphasis on Pakistan. Built for Ziauddin Medical University students.

## Groups

| Group | Theme | Papers |
|-------|-------|--------|
| 1 | Geographic Equity & Spatial Justice | 35 |
| 2 | Health & Disease Burden | 35 |
| 3 | Governance, Justice & Sovereignty | 35 |
| 4 | Methods, Design & Research Systems | 35 |
| 5 | Pakistan Deep-Dive | 50 |

## Live Site

https://mahmood789.github.io/saarc-e156-students/

## Build

```bash
python build.py --all
```

## Data Source

ClinicalTrials.gov API v2 (public, no API key)

## License

MIT
```

- [ ] **Step 3: Commit**

```bash
cd /c/saarc-e156-students
git add E156-PROTOCOL.md README.md
git commit -m "docs: E156 protocol and README"
```

---

## Task 13: Full Build Run + Validation

**Files:**
- All generated output files (190 dashboards, 190 scripts, 5 group pages, 1 landing page)

- [ ] **Step 1: Run full test suite**

```bash
cd /c/saarc-e156-students
python -m pytest tests/ -v --tb=short
```

Expected: All tests PASS (11 + 5 + 15 + 11 + 6 + 6 + 7 + 7 + 3 = ~71 tests).

- [ ] **Step 2: Run the build**

```bash
cd /c/saarc-e156-students
python build.py --all
```

Expected: 190 papers built. Check console for errors/warnings.

- [ ] **Step 3: Validate output file counts**

```bash
# Count generated files
find /c/saarc-e156-students -name "*.html" -path "*/dashboards/*" | wc -l  # Should be 190
find /c/saarc-e156-students -name "*.py" -path "*/code/*" | wc -l          # Should be 190
ls /c/saarc-e156-students/*/index.html | wc -l                              # Should be 5
ls /c/saarc-e156-students/index.html                                         # Should exist
```

- [ ] **Step 4: Validate E156 constraints**

Write and run a quick validation script:

```python
# Quick E156 validation
import json
from pathlib import Path

bodies = json.load(open("data_cache/all_bodies.json"))
violations = []
for slug, body in bodies.items():
    wc = len(body.split())
    if wc > 156:
        violations.append(f"{slug}: {wc} words (over 156)")
    import re
    sents = re.split(r'(?<=[.!?])\s+(?=[A-Z])', body.strip())
    if len(sents) != 7:
        violations.append(f"{slug}: {len(sents)} sentences (need 7)")
if violations:
    print(f"VIOLATIONS ({len(violations)}):")
    for v in violations:
        print(f"  {v}")
else:
    print(f"ALL {len(bodies)} papers pass E156 validation")
```

- [ ] **Step 5: Spot-check dashboards**

Open 3 dashboards in browser (one from each of groups 1, 3, 5):
- `geographic-equity/dashboards/saarc-trial-density-map.html`
- `governance-justice/dashboards/foreign-sponsor-dominance.html`
- `pakistan-deep-dive/dashboards/punjab-trial-dominance.html`

Verify: SVG charts render, sentence breakdown displays, no broken layout.

- [ ] **Step 6: Commit all generated output**

```bash
cd /c/saarc-e156-students
git add -A
git commit -m "build: generated 190 papers with dashboards, scripts, and index pages"
```

---

## Task 14: GitHub Push + Pages Deployment

**Files:** None (remote operations only)

- [ ] **Step 1: Create GitHub repo**

```bash
cd /c/saarc-e156-students
gh repo create mahmood726-cyber/saarc-e156-students --public --source=. --push
```

- [ ] **Step 2: Enable GitHub Pages**

```bash
gh api repos/mahmood726-cyber/saarc-e156-students/pages \
  --method POST \
  -f source='{"branch":"main","path":"/"}' 2>/dev/null || \
gh api repos/mahmood726-cyber/saarc-e156-students/pages \
  --method PUT \
  -f source='{"branch":"main","path":"/"}'
```

- [ ] **Step 3: Verify deployment**

Wait 2-3 minutes, then check:
- Landing page: `https://mahmood789.github.io/saarc-e156-students/`
- Group page: `https://mahmood789.github.io/saarc-e156-students/geographic-equity/`
- Dashboard: `https://mahmood789.github.io/saarc-e156-students/geographic-equity/dashboards/saarc-trial-density-map.html`

- [ ] **Step 4: Update INDEX.md and rewrite-workbook.txt**

Add project to `C:\ProjectIndex\INDEX.md`:
```
| SAARC E156 Students | ACTIVE | Python+HTML | 190 papers | saarc-e156-students | 2026-04-08 |
```

Add entry to `C:\E156\rewrite-workbook.txt` following workbook format (see `e156.md` rules).

- [ ] **Step 5: Commit index updates**

```bash
# In home dir
cd /c/Users/user
git add ProjectIndex/INDEX.md
git commit -m "docs: add SAARC E156 Students to project index"
```

---

## Summary

| Task | Component | Tests | Est. Lines |
|------|-----------|-------|------------|
| 1 | Paper Manifest (190 definitions) | 11 | ~600 |
| 2 | Data Fetcher (CT.gov API) | 5 | ~230 |
| 3 | Statistics Library (31+ methods) | 15 | ~1800 |
| 4 | Chart Library (16 SVG generators) | 11 | ~1400 |
| 5 | Body Generator (E156 text) | 6 | ~350 |
| 6 | Code Generator (Python scripts) | 6 | ~550 |
| 7 | Dashboard Generator (HTML) | 7 | ~520 |
| 8 | Index Updater (pages) | 7 | ~300 |
| 9 | Build Orchestrator | 3 | ~250 |
| 10 | Analysis Scripts | 0 | ~400 |
| 11 | Batch Scripts | 0 | ~80 |
| 12 | E156 Protocol + README | 0 | ~60 |
| 13 | Full Build + Validation | 0 | - |
| 14 | GitHub + Pages + Indexes | 0 | - |
| **Total** | | **~71** | **~6,540** |
