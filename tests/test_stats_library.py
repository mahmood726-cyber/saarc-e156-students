"""
Tests for stats_library.py — 31+ pure-Python statistical methods.

Covers all 21 required public functions plus internal helpers.
"""

import sys
import os
import math

# Ensure lib/ is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lib'))

from stats_library import (
    _normal_cdf, _normal_ppf, _chi2_cdf, _chi2_ppf,
    _mean, _var, _std, _rank, _gaussian_kde,
    gini_coefficient, shannon_entropy, herfindahl_hirschman_index,
    theil_index, atkinson_index, kl_divergence,
    bootstrap_ci, poisson_rate, rate_ratio, bayesian_rate,
    chi_squared, morans_i, spearman_correlation, linear_regression,
    network_centrality, kaplan_meier_survival, odds_ratio, cohens_d,
    permutation_test, concentration_index, lorenz_area,
    normalized_entropy, lorenz_curve, interrupted_time_series,
    changepoint_detection, power_law_fit, jaccard_similarity,
    mutual_information, zero_inflated_poisson_em,
    logistic_growth_fit, arima_forecast, benford_test,
)


# ===== Internal helpers =====

class TestNormalCdf:
    def test_normal_cdf_symmetry(self):
        """cdf(0)=0.5, cdf(1.96) ~ 0.975"""
        assert abs(_normal_cdf(0.0) - 0.5) < 1e-6
        assert abs(_normal_cdf(1.96) - 0.975) < 0.01
        assert abs(_normal_cdf(-1.96) - 0.025) < 0.01

    def test_normal_cdf_tails(self):
        assert _normal_cdf(-10.0) == 0.0
        assert _normal_cdf(10.0) == 1.0

    def test_normal_ppf_roundtrip(self):
        for p in [0.025, 0.1, 0.5, 0.9, 0.975]:
            z = _normal_ppf(p)
            p_back = _normal_cdf(z)
            assert abs(p_back - p) < 0.025, f"Roundtrip failed for p={p}: got {p_back}"

    def test_normal_ppf_boundaries(self):
        assert _normal_ppf(0.0) < -7
        assert _normal_ppf(1.0) > 7
        assert abs(_normal_ppf(0.5)) < 1e-6


class TestChi2:
    def test_chi2_cdf_basics(self):
        # chi2(3.84, df=1) ~ 0.95
        val = _chi2_cdf(3.84, 1)
        assert abs(val - 0.95) < 0.02

    def test_chi2_ppf_basics(self):
        # chi2_ppf(0.95, 1) ~ 3.84
        val = _chi2_ppf(0.95, 1)
        assert abs(val - 3.84) < 0.2

    def test_chi2_edge_cases(self):
        assert _chi2_cdf(0, 5) == 0.0
        assert _chi2_cdf(-1, 5) == 0.0
        assert _chi2_ppf(0, 5) == 0.0


class TestBasicHelpers:
    def test_mean(self):
        assert _mean([1, 2, 3, 4, 5]) == 3.0
        assert _mean([]) == 0.0

    def test_var(self):
        v = _var([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(v - 4.571428571) < 0.01

    def test_std(self):
        s = _std([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(s - math.sqrt(4.571428571)) < 0.01

    def test_rank_no_ties(self):
        r = _rank([10, 30, 20])
        assert r == [1.0, 3.0, 2.0]

    def test_rank_with_ties(self):
        r = _rank([10, 20, 20, 30])
        assert r[0] == 1.0
        assert r[1] == 2.5
        assert r[2] == 2.5
        assert r[3] == 4.0


class TestGaussianKde:
    def test_kde_basic(self):
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = _gaussian_kde(data, n_points=20)
        assert len(result["x"]) == 20
        assert len(result["density"]) == 20
        assert all(d >= 0 for d in result["density"])

    def test_kde_empty(self):
        result = _gaussian_kde([])
        assert result["x"] == []
        assert result["density"] == []


# ===== Public functions =====

class TestGini:
    def test_gini_perfect_equality(self):
        """All equal values -> gini ~ 0"""
        result = gini_coefficient([10, 10, 10, 10, 10])
        assert abs(result["gini"]) < 0.01

    def test_gini_high_inequality(self):
        """One dominates -> gini > 0.7"""
        result = gini_coefficient([0, 0, 0, 0, 100])
        assert result["gini"] > 0.7

    def test_gini_returns_mean(self):
        result = gini_coefficient([10, 20, 30])
        assert abs(result["mean"] - 20.0) < 0.01

    def test_gini_empty(self):
        result = gini_coefficient([])
        assert result["gini"] == 0.0


class TestShannonEntropy:
    def test_shannon_entropy_uniform(self):
        """Uniform distribution -> entropy = log2(n)"""
        n = 8
        result = shannon_entropy([1] * n)
        expected = math.log2(n)
        assert abs(result["entropy"] - expected) < 0.01

    def test_shannon_entropy_concentrated(self):
        """One dominates -> entropy ~ 0"""
        result = shannon_entropy([1000, 0.001, 0.001, 0.001])
        assert result["entropy"] < 0.1

    def test_shannon_entropy_empty(self):
        result = shannon_entropy([])
        assert result["entropy"] == 0.0


class TestHHI:
    def test_hhi_monopoly(self):
        """Single entity -> HHI = 10000"""
        result = herfindahl_hirschman_index([100])
        assert abs(result["hhi"] - 10000) < 1

    def test_hhi_even_split(self):
        """Equal split among 4 -> HHI = 2500"""
        result = herfindahl_hirschman_index([25, 25, 25, 25])
        assert abs(result["hhi"] - 2500) < 1

    def test_hhi_empty(self):
        result = herfindahl_hirschman_index([])
        assert result["hhi"] == 0.0


class TestTheil:
    def test_theil_index_nonneg(self):
        """Theil >= 0 for any valid input"""
        result = theil_index([10, 20, 30, 40, 50])
        assert result["theil"] >= 0

    def test_theil_equality(self):
        """All equal -> theil ~ 0"""
        result = theil_index([5, 5, 5, 5])
        assert abs(result["theil"]) < 0.01

    def test_theil_empty(self):
        result = theil_index([])
        assert result["theil"] == 0.0


class TestAtkinson:
    def test_atkinson_range(self):
        result = atkinson_index([10, 20, 30, 40, 50], epsilon=0.5)
        assert 0 <= result["atkinson"] <= 1

    def test_atkinson_equality(self):
        result = atkinson_index([5, 5, 5, 5], epsilon=0.5)
        assert abs(result["atkinson"]) < 0.01


class TestKLDivergence:
    def test_kl_identical(self):
        """Identical distributions -> KL = 0"""
        result = kl_divergence([1, 2, 3], [1, 2, 3])
        assert abs(result["kl"]) < 0.01

    def test_kl_different(self):
        """Different distributions -> KL > 0"""
        result = kl_divergence([1, 0.01, 0.01], [0.01, 0.01, 1])
        assert result["kl"] > 0

    def test_kl_mismatched_length(self):
        result = kl_divergence([1, 2], [1])
        assert result["kl"] is None


class TestBootstrapCI:
    def test_bootstrap_ci_basic(self):
        """ci_lo < mean < ci_hi"""
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = bootstrap_ci(data, n_boot=500, seed=42)
        assert result["ci_lo"] < result["mean"]
        assert result["mean"] < result["ci_hi"]

    def test_bootstrap_ci_mean(self):
        data = [5, 5, 5, 5, 5]
        result = bootstrap_ci(data, n_boot=200, seed=42)
        assert abs(result["mean"] - 5.0) < 0.01

    def test_bootstrap_ci_empty(self):
        result = bootstrap_ci([])
        assert result["mean"] is None


class TestPoissonRate:
    def test_poisson_rate_basic(self):
        """rate > 0, ci_lo < rate < ci_hi"""
        result = poisson_rate(50, 1000)
        assert result["rate"] > 0
        assert result["ci_lo"] < result["rate"]
        assert result["rate"] < result["ci_hi"]

    def test_poisson_rate_zero(self):
        result = poisson_rate(0, 1000)
        assert result["rate"] == 0.0
        assert result["ci_lo"] == 0.0
        assert result["ci_hi"] > 0

    def test_poisson_rate_bad_exposure(self):
        result = poisson_rate(10, 0)
        assert result["rate"] is None


class TestRateRatio:
    def test_rate_ratio_positive(self):
        """rr > 0 for valid inputs"""
        result = rate_ratio(50, 1000, 30, 1000)
        assert result["rr"] > 0
        assert result["ci_lo"] is not None
        assert result["ci_hi"] is not None

    def test_rate_ratio_equal(self):
        result = rate_ratio(50, 1000, 50, 1000)
        assert abs(result["rr"] - 1.0) < 0.01


class TestBayesianRate:
    def test_bayesian_rate_basic(self):
        """0 < mean < 1, ci_lo < mean < ci_hi"""
        result = bayesian_rate(30, 100)
        assert 0 < result["mean"] < 1
        assert result["ci_lo"] < result["mean"]
        assert result["mean"] < result["ci_hi"]

    def test_bayesian_rate_uniform_prior(self):
        result = bayesian_rate(0, 0, prior_a=1, prior_b=1)
        assert abs(result["mean"] - 0.5) < 0.01


class TestChiSquared:
    def test_chi_squared_basic(self):
        """chi2 > 0, 0 <= p <= 1"""
        obs = [10, 20, 30, 40]
        exp = [25, 25, 25, 25]
        result = chi_squared(obs, exp)
        assert result["chi2"] > 0
        assert 0 <= result["p_value"] <= 1

    def test_chi_squared_perfect(self):
        """Perfect match -> chi2 = 0, p ~ 1"""
        obs = [25, 25, 25, 25]
        exp = [25, 25, 25, 25]
        result = chi_squared(obs, exp)
        assert abs(result["chi2"]) < 0.01

    def test_chi_squared_mismatched(self):
        result = chi_squared([1, 2], [1])
        assert result["chi2"] is None


class TestMoransI:
    def test_morans_i_clustered(self):
        """Spatially clustered -> positive I"""
        values = [1, 1, 1, 10, 10, 10]
        adj = [
            [0, 1, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 1, 0],
        ]
        result = morans_i(values, adj)
        assert result["I"] is not None
        assert result["I"] > 0

    def test_morans_i_empty(self):
        result = morans_i([], [])
        assert result["I"] is None


class TestSpearmanCorrelation:
    def test_spearman_correlation_perfect_positive(self):
        """Perfect positive -> rho ~ 1"""
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        y = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        result = spearman_correlation(x, y)
        assert abs(result["rho"] - 1.0) < 0.01

    def test_spearman_correlation_negative(self):
        x = [1, 2, 3, 4, 5]
        y = [5, 4, 3, 2, 1]
        result = spearman_correlation(x, y)
        assert abs(result["rho"] - (-1.0)) < 0.01

    def test_spearman_empty(self):
        result = spearman_correlation([], [])
        assert result["rho"] is None


class TestLinearRegression:
    def test_linear_regression_perfect(self):
        """Perfect linear -> r_squared = 1"""
        x = [1, 2, 3, 4, 5]
        y = [2, 4, 6, 8, 10]
        result = linear_regression(x, y)
        assert abs(result["slope"] - 2.0) < 0.01
        assert abs(result["intercept"] - 0.0) < 0.01
        assert abs(result["r_squared"] - 1.0) < 0.01

    def test_linear_regression_intercept(self):
        x = [1, 2, 3, 4, 5]
        y = [3, 5, 7, 9, 11]
        result = linear_regression(x, y)
        assert abs(result["slope"] - 2.0) < 0.01
        assert abs(result["intercept"] - 1.0) < 0.01


class TestNetworkCentrality:
    def test_network_centrality_3_nodes(self):
        """3 nodes, correct centrality values"""
        # Node 0 connects to 1 and 2; node 1 connects to 0; node 2 connects to 0
        adj = [
            [0, 1, 1],
            [1, 0, 0],
            [1, 0, 0],
        ]
        result = network_centrality(adj)
        assert len(result["centrality"]) == 3
        assert abs(result["centrality"][0] - 1.0) < 0.01  # node 0: degree 2/2 = 1.0
        assert abs(result["centrality"][1] - 0.5) < 0.01  # node 1: degree 1/2 = 0.5
        assert abs(result["centrality"][2] - 0.5) < 0.01  # node 2: degree 1/2 = 0.5

    def test_network_centrality_empty(self):
        result = network_centrality([])
        assert result["centrality"] == []


class TestKaplanMeier:
    def test_kaplan_meier_basic(self):
        """Survival starts at 1 and decreases"""
        events = [1, 2, 3, 4, 5]
        result = kaplan_meier_survival(events)
        assert len(result["times"]) == 5
        assert len(result["survival"]) == 5
        assert result["survival"][0] <= 1.0
        assert result["survival"][-1] < result["survival"][0]

    def test_kaplan_meier_with_censoring(self):
        events = [(1, True), (2, False), (3, True), (4, False), (5, True)]
        result = kaplan_meier_survival(events)
        assert len(result["times"]) > 0
        assert all(0 <= s <= 1 for s in result["survival"])


class TestOddsRatio:
    def test_odds_ratio_basic(self):
        result = odds_ratio(10, 5, 3, 12)
        assert result["or"] > 1
        assert result["ci_lo"] is not None
        assert result["ci_hi"] is not None
        assert result["ci_lo"] < result["or"] < result["ci_hi"]

    def test_odds_ratio_with_zeros(self):
        """Zero cell -> continuity correction applied"""
        result = odds_ratio(10, 0, 5, 10)
        assert result["or"] is not None


class TestCohensD:
    def test_cohens_d_different(self):
        g1 = [10, 11, 12, 13, 14]
        g2 = [1, 2, 3, 4, 5]
        result = cohens_d(g1, g2)
        assert result["d"] is not None
        assert result["d"] > 2  # large effect

    def test_cohens_d_same(self):
        g = [5, 5, 5, 5, 5]
        result = cohens_d(g, g)
        assert abs(result["d"]) < 0.01

    def test_cohens_d_empty(self):
        result = cohens_d([], [1, 2, 3])
        assert result["d"] is None


class TestPermutationTest:
    def test_permutation_test_different(self):
        g1 = [10, 11, 12, 13, 14, 15]
        g2 = [1, 2, 3, 4, 5, 6]
        result = permutation_test(g1, g2, n_perm=500, seed=42)
        assert result["p_value"] < 0.05

    def test_permutation_test_same(self):
        g = [5, 5, 5, 5, 5]
        result = permutation_test(g, g, n_perm=200, seed=42)
        assert result["p_value"] > 0.5


class TestConcentrationIndex:
    def test_concentration_index_equal(self):
        result = concentration_index([10, 10, 10, 10, 10])
        assert abs(result["ci"]) < 0.01

    def test_concentration_index_gradient(self):
        """Increasing values -> positive CI"""
        result = concentration_index([1, 2, 3, 4, 5])
        assert result["ci"] > 0


class TestLorenzArea:
    def test_lorenz_area_equality(self):
        """All equal -> area ~ 0"""
        result = lorenz_area([10, 10, 10, 10])
        assert abs(result["area"]) < 0.01

    def test_lorenz_area_inequality(self):
        """Unequal -> area > 0"""
        result = lorenz_area([0, 0, 0, 100])
        assert result["area"] > 0.2

    def test_lorenz_area_empty(self):
        result = lorenz_area([])
        assert result["area"] == 0.0


# ===== Additional methods (beyond 21 required) =====

class TestNormalizedEntropy:
    def test_normalized_entropy_uniform(self):
        result = normalized_entropy([1, 1, 1, 1])
        assert abs(result["normalized_entropy"] - 1.0) < 0.01

    def test_normalized_entropy_single(self):
        result = normalized_entropy([10])
        assert result["normalized_entropy"] == 0.0


class TestLorenzCurve:
    def test_lorenz_curve_endpoints(self):
        result = lorenz_curve([10, 20, 30])
        pts = result["points"]
        assert pts[0] == (0.0, 0.0)
        assert pts[-1] == (1.0, 1.0)


class TestInterruptedTimeSeries:
    def test_its_level_change(self):
        pre = [1, 2, 3, 4, 5]
        post = [10, 11, 12, 13, 14]
        result = interrupted_time_series(pre, post)
        assert result["level_change"] is not None
        assert result["level_change"] > 0


class TestChangepointDetection:
    def test_changepoint_basic(self):
        values = [1, 1, 1, 1, 1, 10, 10, 10, 10, 10]
        result = changepoint_detection(values, min_segment=3)
        assert result["changepoint_index"] is not None
        assert 3 <= result["changepoint_index"] <= 7


class TestPowerLawFit:
    def test_power_law_basic(self):
        values = [1, 2, 3, 4, 5, 10, 20, 50, 100]
        result = power_law_fit(values)
        assert result["alpha"] is not None
        assert result["alpha"] > 1


class TestJaccardSimilarity:
    def test_jaccard_identical(self):
        result = jaccard_similarity([1, 2, 3], [1, 2, 3])
        assert abs(result["jaccard"] - 1.0) < 0.01

    def test_jaccard_disjoint(self):
        result = jaccard_similarity([1, 2], [3, 4])
        assert abs(result["jaccard"]) < 0.01


class TestMutualInformation:
    def test_mi_identical(self):
        x = list(range(20))
        result = mutual_information(x, x)
        assert result["mutual_information"] > 0

    def test_mi_empty(self):
        result = mutual_information([], [])
        assert result["mutual_information"] is None


class TestZeroInflatedPoisson:
    def test_zip_basic(self):
        data = [0, 0, 0, 0, 0, 1, 2, 3, 1, 0, 0, 2, 0, 1, 0]
        result = zero_inflated_poisson_em(data)
        assert result["pi"] is not None
        assert result["lambda_"] is not None
        assert 0 <= result["pi"] <= 1
        assert result["lambda_"] >= 0


class TestLogisticGrowthFit:
    def test_logistic_basic(self):
        x = list(range(10))
        y = [1 / (1 + math.exp(-(xi - 5))) * 100 for xi in x]
        result = logistic_growth_fit(x, y)
        assert result["r_squared"] is not None
        assert result["r_squared"] > 0.5


class TestArimaForecast:
    def test_arima_basic(self):
        values = [1, 2, 3, 4, 5, 6, 7, 8]
        result = arima_forecast(values, steps=3)
        assert len(result["forecast"]) == 3
        assert result["forecast"][0] > values[-1]  # upward trend

    def test_arima_short(self):
        result = arima_forecast([1, 2])
        assert result["forecast"] == []


class TestBenfordTest:
    def test_benford_basic(self):
        import random as _rng
        _rng.seed(42)
        values = [_rng.randint(1, 10000) for _ in range(500)]
        result = benford_test(values)
        assert result["chi2"] is not None
        assert result["chi2"] > 0
        assert 0 <= result["p_value"] <= 1


# ===== Effect size from summary stats (bonus) =====

class TestEffectSizeSummary:
    """Test the summary-stat based Cohen's d via the public function."""
    def test_cohens_d_direction(self):
        """Positive d when group1 > group2."""
        g1 = [20, 21, 22, 23, 24]
        g2 = [10, 11, 12, 13, 14]
        result = cohens_d(g1, g2)
        assert result["d"] > 0
