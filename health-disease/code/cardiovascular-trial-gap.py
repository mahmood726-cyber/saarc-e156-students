#!/usr/bin/env python3
"""
Cardiovascular Trial Gap -- SAARC Clinical Trial Equity Analysis
Group: health-disease | Paper #1

Condition: Cardiovascular Diseases
Countries: India, Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan, Bhutan, Maldives

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python cardiovascular-trial-gap.py
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
    params["query.cond"] = "Cardiovascular Diseases"
    params["query.locn"] = "India OR Pakistan OR Bangladesh OR Sri Lanka OR Nepal OR Afghanistan OR Bhutan OR Maldives"
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {e}")
        return 0


# -- Statistical methods -------------------------------------------------------

def rate_ratio(count_a, pop_a, count_b, pop_b):
    """Rate ratio with 95% CI (Wald method on log scale)."""
    if pop_a == 0 or pop_b == 0 or count_a == 0 or count_b == 0:
        return None, None, None
    rate_a = count_a / pop_a
    rate_b = count_b / pop_b
    rr = rate_a / rate_b
    se_log = math.sqrt(1/count_a + 1/count_b)
    lo = math.exp(math.log(rr) - 1.96 * se_log)
    hi = math.exp(math.log(rr) + 1.96 * se_log)
    return rr, lo, hi


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


def poisson_rate(count, exposure):
    """Poisson rate with 95% CI."""
    if exposure == 0:
        return 0, 0, 0
    rate = count / exposure
    se = math.sqrt(count) / exposure
    return rate, rate - 1.96 * se, rate + 1.96 * se


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


def gini_coefficient(values):
    """Compute Gini coefficient (0=perfect equality, 1=perfect inequality)."""
    vals = sorted(values)
    n = len(vals)
    if n == 0 or sum(vals) == 0:
        return 0.0
    cum = 0.0
    weighted_sum = 0.0
    for i, v in enumerate(vals):
        cum += v
        weighted_sum += (2 * (i + 1) - n - 1) * v
    return weighted_sum / (n * cum)



# -- Main analysis -------------------------------------------------------------

def main():
    print("=" * 64)
    print(f"  {'Cardiovascular Trial Gap'}")
    print(f"  SAARC E156 | Group: health-disease")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 1024
    global_count = 43872

    # SAARC country trial counts
    country_names = ["India", "Pakistan", "Nepal", "Bangladesh", "Sri Lanka", "Afghanistan", "Bhutan", "Maldives"]
    country_values = [513, 422, 40, 33, 16, 0, 0, 0]

    # Rate ratio: India vs Pakistan per capita
    rr, lo, hi = rate_ratio(country_values[0], 1440000000, country_values[1] if len(country_values) > 1 else 1, 230000000)
    if rr: print(f"Rate ratio (India/Pakistan per capita): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    rate, lo, hi = poisson_rate(saarc_total, 1940000000)  # SAARC population ~1.94B
    print(f"Poisson rate per capita: {rate:.2e} [{lo:.2e}, {hi:.2e}]")
    area = lorenz_area(country_values)
    gini_from_lorenz = 1 - 2 * area
    print(f"Lorenz area: {area:.4f} (Gini = {gini_from_lorenz:.4f})")
    g = gini_coefficient(country_values)
    print(f"Gini coefficient: {g:.4f}")

    print()
    print("-" * 64)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("Institution: Ziauddin Medical University")
    print("GitHub: https://github.com/mahmood726-cyber/saarc-e156-students")


if __name__ == "__main__":
    main()
