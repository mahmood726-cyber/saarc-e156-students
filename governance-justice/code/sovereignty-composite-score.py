#!/usr/bin/env python3
"""
Sovereignty Composite Score -- SAARC Clinical Trial Equity Analysis
Group: governance-justice | Paper #35

Condition: all interventional
Countries: India, Pakistan, Bangladesh, Sri Lanka, Nepal, Afghanistan, Bhutan, Maldives

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python sovereignty-composite-score.py
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


def atkinson_index(values, epsilon=0.5):
    """Atkinson inequality index (0=equal, 1=maximal inequality)."""
    n = len(values)
    if n == 0:
        return 0.0
    mu = sum(values) / n
    if mu == 0:
        return 0.0
    if epsilon == 1.0:
        # Geometric mean case
        log_sum = sum(math.log(max(v, 1e-10)) for v in values)
        geo_mean = math.exp(log_sum / n)
        return 1 - geo_mean / mu
    powered = sum((max(v, 1e-10) / mu) ** (1 - epsilon) for v in values) / n
    return 1 - powered ** (1 / (1 - epsilon))



# -- Main analysis -------------------------------------------------------------

def main():
    print("=" * 64)
    print(f"  {'Sovereignty Composite Score'}")
    print(f"  SAARC E156 | Group: governance-justice")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 11116
    global_count = 442199

    # SAARC country trial counts
    country_names = ["India", "Pakistan", "Bangladesh", "Nepal", "Sri Lanka", "Afghanistan", "Bhutan", "Maldives"]
    country_values = [5398, 4669, 652, 294, 75, 22, 6, 0]

    g = gini_coefficient(country_values)
    print(f"Gini coefficient: {g:.4f}")
    h = shannon_entropy(country_values)
    print(f"Shannon entropy: {h:.3f} bits")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    t = theil_index(country_values)
    print(f"Theil index: {t:.4f}")
    ai = atkinson_index(country_values, epsilon=0.5)
    print(f"Atkinson index (e=0.5): {ai:.4f}")

    print()
    print("-" * 64)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("Institution: Ziauddin Medical University")
    print("GitHub: https://github.com/mahmood726-cyber/saarc-e156-students")


if __name__ == "__main__":
    main()
