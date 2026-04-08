"""Tests for lib/code_generator.py -- SAARC Python script generator."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.code_generator import generate_code_script, _METHOD_SNIPPETS


# ── Fixtures ──────────────────────────────────────────────────────

def _sample_paper():
    return {
        "slug": "saarc-trial-density-map",
        "title": "SAARC Trial Density Map",
        "group": "geographic-equity",
        "paper_num": 1,
        "query": {
            "condition": None,
            "countries": ["India", "Pakistan", "Bangladesh", "Sri Lanka",
                          "Nepal", "Afghanistan", "Bhutan", "Maldives"],
        },
        "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate",
                  "shannon_entropy", "theil_index"],
        "charts": ["choropleth", "lorenz"],
    }


def _sample_data():
    return {
        "slug": "saarc-trial-density-map",
        "country_counts": {
            "India": 48500, "Pakistan": 2100, "Bangladesh": 980,
            "Sri Lanka": 650, "Nepal": 410, "Afghanistan": 180,
            "Bhutan": 12, "Maldives": 8,
        },
        "saarc_total": 52840,
        "global_count": 520000,
        "metrics": {},
    }


def _sample_stats():
    return {
        "gini_coefficient": 0.91,
        "hhi_index": 0.84,
        "shannon_entropy": 1.23,
    }


def _generate():
    return generate_code_script(_sample_paper(), _sample_data(), _sample_stats())


# ── Tests ─────────────────────────────────────────────────────────

def test_script_is_valid_python():
    """Generated script must compile without SyntaxError."""
    script = _generate()
    compile(script, "<generated>", "exec")


def test_script_contains_imports():
    """Script must import requests, json, math, random."""
    script = _generate()
    assert "import json" in script
    assert "import math" in script
    assert "import random" in script
    assert "import requests" in script


def test_script_contains_api_url():
    """Script must reference the ClinicalTrials.gov API v2."""
    script = _generate()
    assert "clinicaltrials.gov/api/v2" in script


def test_script_contains_stat_methods():
    """Script must contain at least one statistical method function def."""
    script = _generate()
    # The paper requests gini_coefficient, bootstrap_ci, etc.
    assert "def gini_coefficient(" in script
    assert "def bootstrap_ci(" in script
    assert "def poisson_rate(" in script


def test_script_has_main_block():
    """Script must have an if __name__ block or print() calls."""
    script = _generate()
    assert 'if __name__' in script
    assert 'print(' in script


def test_script_references_saarc_countries():
    """Script must contain SAARC country names, not African countries."""
    script = _generate()
    assert "India" in script
    assert "Pakistan" in script
    assert "Bangladesh" in script
    assert "Sri Lanka" in script
    assert "Nepal" in script
    assert "Afghanistan" in script
    assert "Bhutan" in script
    assert "Maldives" in script


def test_method_snippets_cover_manifest_stats():
    """All 21 unique stats used in the manifest should have a snippet."""
    expected = {
        "atkinson_index", "bayesian_rate", "bootstrap_ci", "chi_squared",
        "cohens_d", "concentration_index", "gini_coefficient", "hhi_index",
        "kaplan_meier_survival", "kl_divergence", "linear_regression",
        "lorenz_area", "morans_i", "network_centrality", "odds_ratio",
        "permutation_test", "poisson_rate", "rate_ratio", "shannon_entropy",
        "spearman_correlation", "theil_index",
    }
    assert expected.issubset(set(_METHOD_SNIPPETS.keys())), (
        f"Missing snippets: {expected - set(_METHOD_SNIPPETS.keys())}"
    )


def test_all_snippets_are_valid_python():
    """Every snippet in _METHOD_SNIPPETS must be compilable Python."""
    for name, code in _METHOD_SNIPPETS.items():
        try:
            compile(code, f"<snippet:{name}>", "exec")
        except SyntaxError as e:
            raise AssertionError(f"Snippet '{name}' has SyntaxError: {e}")


def test_script_with_condition():
    """Paper with a specific condition should include it in API params."""
    paper = _sample_paper()
    paper["query"]["condition"] = "diabetes"
    script = generate_code_script(paper, _sample_data(), _sample_stats())
    assert "diabetes" in script
    compile(script, "<generated-condition>", "exec")


def test_script_with_other_terms():
    """Paper with other search terms should include them."""
    paper = _sample_paper()
    paper["query"]["other"] = "phase 3"
    script = generate_code_script(paper, _sample_data(), _sample_stats())
    assert "phase 3" in script
    compile(script, "<generated-other>", "exec")


def test_script_with_empty_data():
    """Script must compile even with empty data dict."""
    paper = _sample_paper()
    data = {"slug": "test", "country_counts": {}, "saarc_total": 0,
            "global_count": 0, "metrics": {}}
    script = generate_code_script(paper, data, {})
    compile(script, "<generated-empty>", "exec")
    # Should use placeholder values
    assert "country_values" in script


def test_script_with_fallback_methods():
    """Paper with unknown stats should get fallback methods."""
    paper = _sample_paper()
    paper["stats"] = ["nonexistent_method_xyz"]
    script = generate_code_script(paper, _sample_data(), _sample_stats())
    compile(script, "<generated-fallback>", "exec")
    # Should include at least the fallback methods
    assert "def gini_coefficient(" in script or "def bootstrap_ci(" in script


def test_script_contains_ziauddin():
    """Script must reference Ziauddin Medical University."""
    script = _generate()
    assert "Ziauddin" in script


def test_script_has_saarc_populations():
    """Script should contain SAARC population data."""
    script = _generate()
    assert "SAARC_POPULATIONS" in script
    assert "1_440_000_000" in script or "1440000000" in script


def test_different_papers_produce_different_scripts():
    """Two different papers should produce different scripts."""
    paper1 = _sample_paper()
    paper2 = _sample_paper()
    paper2["slug"] = "india-dominance-index"
    paper2["title"] = "India Dominance Index"
    paper2["stats"] = ["hhi_index", "gini_coefficient", "bootstrap_ci",
                       "concentration_index", "lorenz_area"]
    s1 = generate_code_script(paper1, _sample_data(), _sample_stats())
    s2 = generate_code_script(paper2, _sample_data(), _sample_stats())
    assert s1 != s2


def test_all_stat_methods_produce_valid_scripts():
    """Generate a script for each stat method and verify it compiles."""
    all_stats = list(_METHOD_SNIPPETS.keys())
    for stat in all_stats:
        paper = _sample_paper()
        paper["stats"] = [stat]
        script = generate_code_script(paper, _sample_data(), _sample_stats())
        try:
            compile(script, f"<generated-{stat}>", "exec")
        except SyntaxError as e:
            raise AssertionError(
                f"Script with stat '{stat}' has SyntaxError: {e}"
            )


def test_script_no_africa_references():
    """Script should not mention Africa (this is a SAARC project)."""
    script = _generate()
    # We check that "Africa E156" does not appear -- SAARC E156 should
    assert "Africa E156" not in script
    assert "africa_count" not in script
