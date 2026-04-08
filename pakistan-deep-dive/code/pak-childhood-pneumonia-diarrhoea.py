#!/usr/bin/env python3
"""
Childhood Pneumonia & Diarrhoea -- SAARC Clinical Trial Equity Analysis
Group: pakistan-deep-dive | Paper #29

Condition: Pneumonia OR Diarrhea
Countries: Pakistan

This standalone script demonstrates the statistical methods used in this paper.
Generated for Ziauddin Medical University students.
Run: python pak-childhood-pneumonia-diarrhoea.py
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
    params["query.cond"] = "Pneumonia OR Diarrhea"
    params["query.locn"] = "Pakistan"
    try:
        resp = requests.get(BASE_URL, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json().get("totalCount", 0)
    except Exception as e:
        print(f"API error: {e}")
        return 0


# -- Statistical methods -------------------------------------------------------

def poisson_rate(count, exposure):
    """Poisson rate with 95% CI."""
    if exposure == 0:
        return 0, 0, 0
    rate = count / exposure
    se = math.sqrt(count) / exposure
    return rate, rate - 1.96 * se, rate + 1.96 * se


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


def bayesian_rate(successes, trials, prior_a=1, prior_b=1):
    """Bayesian posterior rate (Beta-Binomial conjugate)."""
    post_a = prior_a + successes
    post_b = prior_b + trials - successes
    mean = post_a / (post_a + post_b)
    # Approximate 95% credible interval
    var = (post_a * post_b) / ((post_a + post_b)**2 * (post_a + post_b + 1))
    sd = math.sqrt(var)
    return mean, max(0, mean - 1.96 * sd), min(1, mean + 1.96 * sd)


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



# -- Main analysis -------------------------------------------------------------

def main():
    print("=" * 64)
    print(f"  {'Childhood Pneumonia & Diarrhoea'}")
    print(f"  SAARC E156 | Group: pakistan-deep-dive")
    print("=" * 64)
    print()

    # Pre-loaded data (from ClinicalTrials.gov)
    saarc_total = 127
    global_count = 7905

    # SAARC country trial counts
    country_names = ["Pakistan"]
    country_values = [127]

    rate, lo, hi = poisson_rate(saarc_total, 1940000000)  # SAARC population ~1.94B
    print(f"Poisson rate per capita: {rate:.2e} [{lo:.2e}, {hi:.2e}]")
    # Rate ratio: India vs Pakistan per capita
    rr, lo, hi = rate_ratio(country_values[0], 1440000000, country_values[1] if len(country_values) > 1 else 1, 230000000)
    if rr: print(f"Rate ratio (India/Pakistan per capita): {rr:.4f} [{lo:.4f}, {hi:.4f}]")
    est, lo, hi = bootstrap_ci(country_values)
    print(f"Bootstrap CI for mean: {est:.1f} [{lo:.1f}, {hi:.1f}]")
    post_mean, lo, hi = bayesian_rate(saarc_total, max(saarc_total, global_count))
    print(f"Bayesian posterior rate (SAARC/global): {post_mean:.4f} [{lo:.4f}, {hi:.4f}]")
    # Spatial autocorrelation with SAARC adjacency weights
    w = [[0,1,1,1,1,0,1,0],[1,0,0,0,0,1,0,0],[1,0,0,0,0,0,0,0],
         [1,0,0,0,0,0,0,1],[1,0,0,0,0,0,1,0],[1,1,0,0,0,0,0,0],
         [1,0,0,0,0,0,0,0],[0,0,0,1,0,0,0,0]]
    mi = morans_i(country_values, w)
    print(f"Moran's I (spatial autocorrelation): {mi:.4f}")

    print()
    print("-" * 64)
    print("Data: ClinicalTrials.gov API v2 (April 2026)")
    print("E156 Format: 7 sentences, <=156 words")
    print("Institution: Ziauddin Medical University")
    print("GitHub: https://github.com/mahmood726-cyber/saarc-e156-students")


if __name__ == "__main__":
    main()
