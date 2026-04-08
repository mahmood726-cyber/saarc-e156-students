#!/usr/bin/env python3
"""
Karachi Trial Density Map -- SAARC Clinical Trial Equity Analysis
Group: pakistan-deep-dive | Paper #46

Condition: all interventional
Countries: Pakistan

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python karachi-trial-density-map.py
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

def hhi_index(values):
    """Herfindahl-Hirschman Index (0=fragmented, 1=monopoly)."""
    total = sum(values)
    if total == 0:
        return 0.0
    return sum((v / total) ** 2 for v in values)


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


def morans_i(values, weights_matrix):
    """Moran's I spatial autocorrelation statistic.
    values: list of numeric values per location.
    weights_matrix: n x n spatial weights (1=neighbour, 0=not).
    Returns: Moran's I in range [-1, 1].
    """
    n = len(values)
    if n < 2:
        return 0.0
    mu = sum(values) / n
    deviations = [v - mu for v in values]
    numerator = 0.0
    w_sum = 0.0
    for i in range(n):
        for j in range(n):
            w = weights_matrix[i][j]
            numerator += w * deviations[i] * deviations[j]
            w_sum += w
    denominator = sum(d ** 2 for d in deviations)
    if w_sum == 0 or denominator == 0:
        return 0.0
    return (n / w_sum) * (numerator / denominator)


def concentration_index(values):
    """Health concentration index (based on Lorenz curve)."""
    vals = sorted(values)
    n = len(vals)
    total = sum(vals)
    if n == 0 or total == 0:
        return 0.0
    cum = 0.0
    weighted = 0.0
    for i, v in enumerate(vals):
        cum += v
        weighted += (2 * (i + 1) - n - 1) * v
    return weighted / (n * total)



# -- Main analysis -------------------------------------------------------------

def main():
    print("=" * 64)
    print(f"  {'Karachi Trial Density Map'}")
    print(f"  SAARC E156 | Group: pakistan-deep-dive")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 4669
    global_count = 442199

    # SAARC country trial counts
    country_names = ["Pakistan"]
    country_values = [4669]

    hhi = hhi_index(country_values)
    print(f"HHI concentration: {hhi:.4f}")
    g = gini_coefficient(country_values)
    print(f"Gini coefficient: {g:.4f}")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    # Spatial autocorrelation with SAARC adjacency weights
    w = [[0,1,1,1,1,0,1,0],[1,0,0,0,0,1,0,0],[1,0,0,0,0,0,0,0],
         [1,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,0],[1,1,0,0,0,0,0,0],
         [1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]
    mi = morans_i(country_values, w)
    print(f"Moran's I (spatial autocorrelation): {mi:.4f}")
    ci = concentration_index(country_values)
    print(f"Concentration index: {ci:.4f}")

    print()
    print("-" * 64)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("Institution: Ziauddin Medical University")
    print("GitHub: https://github.com/mahmood726-cyber/saarc-e156-students")


if __name__ == "__main__":
    main()
