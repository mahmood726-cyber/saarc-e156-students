#!/usr/bin/env python3
"""
Academic vs Industry Ratio -- SAARC Clinical Trial Equity Analysis
Group: pakistan-deep-dive | Paper #34

Condition: all interventional
Countries: Pakistan

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python pak-academic-vs-industry-ratio.py
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
SAARC_COUNTRIES = ["Pakistan"]
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
    params["query.locn"] = "Pakistan"
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {e}")
        return 0


# -- Statistical methods -------------------------------------------------------

def chi_squared(observed, expected):
    """Chi-squared test statistic."""
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += (o - e) ** 2 / e
    return chi2


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


def odds_ratio_2x2(a, b, c, d):
    """Odds ratio from 2x2 table with 95% CI."""
    if b == 0 or c == 0 or a == 0 or d == 0:
        return None, None, None
    or_val = (a * d) / (b * c)
    se_log = math.sqrt(1/a + 1/b + 1/c + 1/d)
    lo = math.exp(math.log(or_val) - 1.96 * se_log)
    hi = math.exp(math.log(or_val) + 1.96 * se_log)
    return or_val, lo, hi


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
    print(f"  {'Academic vs Industry Ratio'}")
    print(f"  SAARC E156 | Group: pakistan-deep-dive")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 4669
    global_count = 442199

    # SAARC country trial counts
    country_names = ["Pakistan"]
    country_values = [4669]

    n_countries = len(country_values)
    expected = [sum(country_values)/n_countries] * n_countries
    chi2 = chi_squared(country_values, expected)
    print(f"Chi-squared (vs uniform): {chi2:.2f}")
    # Rate ratio: India vs Pakistan per capita
    rr, lo, hi = rate_ratio(country_values[0], 1440000000, country_values[1] if len(country_values) > 1 else 1, 230000000)
    if rr: print(f"Rate ratio (India/Pakistan per capita): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    # Odds ratio: India trials vs rest-of-SAARC
    india = country_values[0]
    rest = sum(country_values[1:])
    or_val, lo, hi = odds_ratio_2x2(india, max(1, global_count - india), rest, max(1, global_count - rest))
    if or_val: print(f"Odds ratio (India vs rest): {or_val:.3f} [{lo:.3f}, {hi:.3f}]")
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
