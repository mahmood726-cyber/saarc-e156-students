#!/usr/bin/env python3
"""
Cancer Trial Disparity -- SAARC Clinical Trial Equity Analysis
Group: health-disease | Paper #11

Condition: Cancer
Countries: India, Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan, Bhutan, Maldives

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python cancer-trial-disparity.py
"""

import json
import math
import random
import sys

try:
    import requests
except ImportError:
    print("Optional: pip install requests (for live API queries)")
    requests = None

seed = 42
random.seed(seed)

# -- SAARC countries and populations -------------------------------------------
SAARC_COUNTRIES = ["India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal", "Afghanistan", "Bhutan", "Maldives"]
SAARC_POPULATIONS = {
    "India": 1_440_000_000, "Pakistan": 230_000_000,
    "Bangladesh": 170_000_000, "Sri Lanka": 22_000_000,
    "Nepal": 30_000_000, "Afghanistan": 42_000_000,
    "Bhutan": 800_000, "Maldives": 520_000,
}

# -- ClinicalTrials.gov API v2 query ------------------------------------------
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"


def fetch_trials(condition=None, location=None):
    """Fetch trial count from ClinicalTrials.gov API v2."""
    if requests is None:
        return 0
    params = {
        "format": "json",
        "pageSize": 0,
        "countTotal": "true",
        "filter.advanced": "AREA[StudyType]INTERVENTIONAL",
    }
    params["query.cond"] = "Cancer"
    params["query.locn"] = "India OR Pakistan OR Bangladesh OR Sri Lanka OR Nepal OR Afghanistan OR Bhutan OR Maldives"
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {e}")
        return 0


# -- Statistical methods -------------------------------------------------------

def hhi_index(values):
    """Herfindahl-Hirschman Index (0=fragmented, 1=monopoly)."""
    total = sum(values)
    if total == 0:
        return 0.0
    return sum((v / total) ** 2 for v in values)


def chi_squared(observed, expected):
    """Chi-squared test statistic."""
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += (o - e) ** 2 / e
    return chi2


def bootstrap_ci(data, n_boot=5000, seed=42):
    """Bootstrap 95% confidence interval for the mean."""
    rng = random.Random(seed)
    n = len(data)
    if n == 0:
        return None, None, None
    observed = sum(data) / n
    means = []
    for _ in range(n_boot):
        sample = [data[rng.randint(0, n - 1)] for _ in range(n)]
        means.append(sum(sample) / n)
    means.sort()
    lo = means[int(0.025 * n_boot)]
    hi = means[int(0.975 * n_boot)]
    return observed, lo, hi


def theil_index(values):
    """Theil T index of inequality."""
    n = len(values)
    if n == 0:
        return 0.0
    mu = sum(values) / n
    if mu == 0:
        return 0.0
    t = 0.0
    for v in values:
        if v > 0:
            t += (v / mu) * math.log(v / mu)
    return t / n


def lorenz_area(values):
    """Area under the Lorenz curve (used to compute Gini = 1 - 2*area)."""
    vals = sorted(values)
    n = len(vals)
    total = sum(vals)
    if total == 0:
        return 0.5
    cum = 0.0
    area = 0.0
    for i, v in enumerate(vals):
        cum += v
        area += cum / total
    return area / n



# -- Main analysis -------------------------------------------------------------

def main():
    print("=" * 64)
    print(f"  {'Cancer Trial Disparity'}")
    print(f"  SAARC E156 | Group: health-disease")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 1047
    global_count = 93922

    # SAARC country trial counts
    country_names = ["India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka", "Bhutan", "Afghanistan", "Maldives"]
    country_values = [855, 141, 34, 11, 5, 1, 0, 0]

    hhi = hhi_index(country_values)
    print(f"HHI concentration: {hhi:.4f}")
    n_countries = len(country_values)
    expected = [sum(country_values)/n_countries] * n_countries
    chi2 = chi_squared(country_values, expected)
    print(f"Chi-squared (vs uniform): {chi2:.2f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    t = theil_index(country_values)
    print(f"Theil index: {t:.4f}")
    area = lorenz_area(country_values)
    gini_from_lorenz = 1 - 2 * area
    print(f"Lorenz area: {area:.4f} (Gini = {gini_from_lorenz:.4f})")

    print()
    print("-" * 64)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("Institution: Ziauddin Medical University")
    print("GitHub: https://github.com/mahmood726-cyber/saarc-e156-students")


if __name__ == "__main__":
    main()
