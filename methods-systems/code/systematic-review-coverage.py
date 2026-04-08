#!/usr/bin/env python3
"""
Systematic Review Coverage -- SAARC Clinical Trial Equity Analysis
Group: methods-systems | Paper #30

Condition: all interventional
Countries: India, Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan, Bhutan, Maldives

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python systematic-review-coverage.py
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


def chi_squared(observed, expected):
    """Chi-squared test statistic."""
    chi2 = 0.0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += (o - e) ** 2 / e
    return chi2


def shannon_entropy(values):
    """Shannon entropy in bits."""
    total = sum(values)
    if total == 0:
        return 0.0
    h = 0.0
    for v in values:
        if v > 0:
            p = v / total
            h -= p * math.log2(p)
    return h


def poisson_rate(count, exposure):
    """Poisson rate with 95% CI."""
    if exposure == 0:
        return 0, 0, 0
    rate = count / exposure
    se = math.sqrt(count) / exposure
    return rate, rate - 1.96 * se, rate + 1.96 * se



# -- Main analysis -------------------------------------------------------------

def main():
    print("=" * 64)
    print(f"  {'Systematic Review Coverage'}")
    print(f"  SAARC E156 | Group: methods-systems")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 11116
    global_count = 442199

    # SAARC country trial counts
    country_names = ["India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka", "Afghanistan", "Bhutan", "Maldives"]
    country_values = [5398, 4669, 652, 294, 75, 22, 6, 0]

    # Rate ratio: India vs Pakistan per capita
    rr, lo, hi = rate_ratio(country_values[0], 1440000000, country_values[1] if len(country_values) > 1 else 1, 230000000)
    if rr: print(f"Rate ratio (India/Pakistan per capita): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    n_countries = len(country_values)
    expected = [sum(country_values)/n_countries] * n_countries
    chi2 = chi_squared(country_values, expected)
    print(f"Chi-squared (vs uniform): {chi2:.2f}")
    h = shannon_entropy(country_values)
    print(f"Shannon entropy: {h:.3f} bits")
    rate, lo, hi = poisson_rate(saarc_total, 1940000000)  # SAARC population ~1.94B
    print(f"Poisson rate per capita: {rate:.2e} [{lo:.2e}, {hi:.2e}]")

    print()
    print("-" * 64)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("Institution: Ziauddin Medical University")
    print("GitHub: https://github.com/mahmood726-cyber/saarc-e156-students")


if __name__ == "__main__":
    main()
