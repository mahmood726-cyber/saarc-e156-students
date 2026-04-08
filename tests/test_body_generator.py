"""Tests for body_generator.py — validates E156 7-sentence micro-paper generation."""

import sys
import os
import re

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.body_generator import (
    generate_body,
    _word_count,
    _sentence_count,
    _trim_to_limit,
    _fmt,
    _pick_estimand,
    _gen_s1,
    _gen_s2,
    _gen_s3,
    _gen_s4,
    _gen_s5,
    _gen_s6,
    _gen_s7_variants,
)


# ---------------------------------------------------------------------------
# Mock data fixtures — one per group
# ---------------------------------------------------------------------------

MOCK_DATA_GEO = {
    "saarc_total": 28500,
    "country_counts": {
        "India": 25000, "Pakistan": 1800, "Bangladesh": 900,
        "Sri Lanka": 350, "Nepal": 250, "Afghanistan": 80,
        "Bhutan": 15, "Maldives": 105,
    },
    "global_count": 500000,
}

MOCK_DATA_HEALTH = {
    "saarc_total": 4200,
    "country_counts": {
        "India": 3600, "Pakistan": 300, "Bangladesh": 150,
        "Sri Lanka": 60, "Nepal": 50, "Afghanistan": 20,
        "Bhutan": 5, "Maldives": 15,
    },
}

MOCK_DATA_GOV = {
    "saarc_total": 28500,
    "country_counts": {
        "India": 25000, "Pakistan": 1800, "Bangladesh": 900,
        "Sri Lanka": 350, "Nepal": 250, "Afghanistan": 80,
        "Bhutan": 15, "Maldives": 105,
    },
}

MOCK_DATA_METHODS = {
    "saarc_total": 28500,
    "country_counts": {
        "India": 25000, "Pakistan": 1800, "Bangladesh": 900,
        "Sri Lanka": 350, "Nepal": 250, "Afghanistan": 80,
        "Bhutan": 15, "Maldives": 105,
    },
}

MOCK_DATA_PAKISTAN = {
    "saarc_total": 1800,
    "country_counts": {"Pakistan": 1800},
}

MOCK_STATS_GINI = {
    "gini_coefficient": {"gini": 0.872},
    "bootstrap_ci": {"ci_lower": 0.81, "ci_upper": 0.93},
    "shannon_entropy": {"entropy": 1.45},
}

MOCK_STATS_RATIO = {
    "rate_ratio": {"rate_ratio": 4.7},
    "bootstrap_ci": {"ci_lower": 3.2, "ci_upper": 6.1},
}

MOCK_STATS_HHI = {
    "hhi_index": {"hhi": 0.412},
    "theil_index": {"theil": 0.693},
}

MOCK_STATS_EMPTY = {}


# Paper definitions for each group

PAPER_GEO = {
    "slug": "saarc-trial-density-map",
    "title": "SAARC Trial Density Map",
    "group": "geographic-equity",
    "paper_num": 1,
    "query": {"condition": None, "countries": ["India", "Pakistan", "Bangladesh",
              "Sri Lanka", "Nepal", "Afghanistan", "Bhutan", "Maldives"]},
    "stats": ["gini_coefficient", "bootstrap_ci", "poisson_rate", "shannon_entropy"],
    "context": "Trials per million population across 8 SAARC nations reveals stark inequality in research capacity, with India hosting the vast majority.",
}

PAPER_HEALTH = {
    "slug": "saarc-cardiovascular-burden",
    "title": "SAARC Cardiovascular Burden",
    "group": "health-disease",
    "paper_num": 1,
    "query": {"condition": "Cardiovascular Diseases", "countries": ["India", "Pakistan"]},
    "stats": ["rate_ratio", "bootstrap_ci", "poisson_rate"],
    "context": "South Asia has the world's highest cardiovascular mortality rate, with events occurring a decade earlier than in Europe.",
}

PAPER_GOV = {
    "slug": "saarc-sponsor-dependency",
    "title": "SAARC Sponsor Dependency",
    "group": "governance-justice",
    "paper_num": 1,
    "query": {"condition": None, "countries": ["India", "Pakistan"]},
    "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci"],
    "context": "Foreign pharmaceutical companies sponsor the majority of SAARC trials, using South Asian populations for global evidence generation.",
}

PAPER_METHODS = {
    "slug": "saarc-rct-proportion",
    "title": "SAARC Randomised Trial Proportion",
    "group": "methods-systems",
    "paper_num": 1,
    "query": {"condition": None, "countries": ["India", "Pakistan"]},
    "stats": ["chi_squared", "odds_ratio"],
    "context": "The proportion of randomised trials across SAARC varies dramatically, with some nations conducting mostly observational work.",
}

PAPER_PAKISTAN = {
    "slug": "pakistan-provincial-equity",
    "title": "Pakistan Provincial Equity",
    "group": "pakistan-deep-dive",
    "paper_num": 1,
    "query": {"condition": None, "countries": ["Pakistan"]},
    "stats": ["hhi_index", "gini_coefficient", "bootstrap_ci"],
    "context": "Pakistan's research capacity is concentrated in Punjab and Sindh, leaving Balochistan and tribal areas as clinical research deserts.",
}


# ---------------------------------------------------------------------------
# Helper function tests
# ---------------------------------------------------------------------------

class TestWordCount:
    def test_simple(self):
        assert _word_count("hello world") == 2

    def test_empty(self):
        assert _word_count("") == 0

    def test_multiword(self):
        assert _word_count("one two three four five") == 5


class TestSentenceCount:
    def test_simple_two(self):
        assert _sentence_count("First sentence. Second sentence.") == 2

    def test_single(self):
        assert _sentence_count("One sentence only.") == 1

    def test_question(self):
        assert _sentence_count("Is this a question? Yes it is.") == 2

    def test_abbreviation_gov(self):
        # ClinicalTrials.gov should NOT be counted as sentence boundary
        text = "Registered on ClinicalTrials.gov through April 2026."
        assert _sentence_count(text) == 1

    def test_decimal(self):
        text = "The Gini coefficient was 0.872. This is high."
        assert _sentence_count(text) == 2


class TestTrimToLimit:
    def test_under_limit(self):
        sentences = ["One two three.", "Four five."]
        result = _trim_to_limit(sentences, max_words=10)
        assert sum(_word_count(s) for s in result) <= 10

    def test_over_limit_trimmed(self):
        sentences = [
            "A " * 30 + "end.",
            "B " * 30 + "end.",
        ]
        result = _trim_to_limit(sentences, max_words=20)
        total = sum(_word_count(s) for s in result)
        assert total <= 20

    def test_preserves_count(self):
        sentences = ["S1.", "S2.", "S3.", "S4.", "S5.", "S6.", "S7."]
        result = _trim_to_limit(sentences, max_words=100)
        assert len(result) == 7


class TestFmt:
    def test_integer(self):
        assert _fmt(28500) == "28,500"

    def test_float(self):
        assert _fmt(0.872, 3) == "0.872"

    def test_none(self):
        assert _fmt(None) == "N/A"

    def test_whole_float(self):
        assert _fmt(100.0) == "100"


class TestPickEstimand:
    def test_gini(self):
        result = _pick_estimand(["gini_coefficient"])
        assert "Gini" in result

    def test_rate_ratio(self):
        result = _pick_estimand(["rate_ratio"])
        assert "rate ratio" in result

    def test_empty(self):
        result = _pick_estimand([])
        assert result == "trial disparity index"

    def test_unknown(self):
        result = _pick_estimand(["unknown_stat"])
        assert result == "trial disparity index"


# ---------------------------------------------------------------------------
# Core E156 body tests
# ---------------------------------------------------------------------------

class TestBodyHas7Sentences:
    """Every generated body must have exactly 7 sentences."""

    def test_geo_group(self):
        body = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        assert _sentence_count(body) == 7

    def test_health_group(self):
        body = generate_body(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        assert _sentence_count(body) == 7

    def test_gov_group(self):
        body = generate_body(PAPER_GOV, MOCK_DATA_GOV, MOCK_STATS_HHI)
        assert _sentence_count(body) == 7

    def test_methods_group(self):
        body = generate_body(PAPER_METHODS, MOCK_DATA_METHODS, MOCK_STATS_EMPTY)
        assert _sentence_count(body) == 7

    def test_pakistan_group(self):
        body = generate_body(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI)
        assert _sentence_count(body) == 7


class TestBodyUnder157Words:
    """Every generated body must have at most 156 words."""

    def test_geo_group(self):
        body = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        assert _word_count(body) <= 156, f"Word count {_word_count(body)} exceeds 156"

    def test_health_group(self):
        body = generate_body(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        assert _word_count(body) <= 156, f"Word count {_word_count(body)} exceeds 156"

    def test_gov_group(self):
        body = generate_body(PAPER_GOV, MOCK_DATA_GOV, MOCK_STATS_HHI)
        assert _word_count(body) <= 156, f"Word count {_word_count(body)} exceeds 156"

    def test_methods_group(self):
        body = generate_body(PAPER_METHODS, MOCK_DATA_METHODS, MOCK_STATS_EMPTY)
        assert _word_count(body) <= 156, f"Word count {_word_count(body)} exceeds 156"

    def test_pakistan_group(self):
        body = generate_body(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI)
        assert _word_count(body) <= 156, f"Word count {_word_count(body)} exceeds 156"


class TestBodyIsSingleParagraph:
    """Body must be a single paragraph -- no double newlines."""

    def test_geo_no_double_newline(self):
        body = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        assert "\n\n" not in body
        assert "\n" not in body

    def test_health_no_double_newline(self):
        body = generate_body(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        assert "\n\n" not in body
        assert "\n" not in body

    def test_pakistan_no_double_newline(self):
        body = generate_body(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI)
        assert "\n\n" not in body
        assert "\n" not in body


class TestBodyDeterministic:
    """Same inputs must produce same output."""

    def test_geo_deterministic(self):
        body1 = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        body2 = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        assert body1 == body2

    def test_health_deterministic(self):
        body1 = generate_body(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        body2 = generate_body(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        assert body1 == body2

    def test_pakistan_deterministic(self):
        body1 = generate_body(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI)
        body2 = generate_body(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI)
        assert body1 == body2


class TestBodyDiffersByGroup:
    """Different groups must produce different bodies."""

    def test_geo_vs_health(self):
        body_geo = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        body_health = generate_body(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        assert body_geo != body_health

    def test_gov_vs_methods(self):
        body_gov = generate_body(PAPER_GOV, MOCK_DATA_GOV, MOCK_STATS_HHI)
        body_methods = generate_body(PAPER_METHODS, MOCK_DATA_METHODS, MOCK_STATS_EMPTY)
        assert body_gov != body_methods

    def test_pakistan_vs_geo(self):
        body_pak = generate_body(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI)
        body_geo = generate_body(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        assert body_pak != body_geo


class TestAllFiveGroupsGenerate:
    """All five groups must produce valid, non-empty bodies."""

    ALL_PAPERS = [
        (PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI),
        (PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO),
        (PAPER_GOV, MOCK_DATA_GOV, MOCK_STATS_HHI),
        (PAPER_METHODS, MOCK_DATA_METHODS, MOCK_STATS_EMPTY),
        (PAPER_PAKISTAN, MOCK_DATA_PAKISTAN, MOCK_STATS_HHI),
    ]

    def test_all_nonempty(self):
        for paper, data, stats in self.ALL_PAPERS:
            body = generate_body(paper, data, stats)
            assert len(body) > 50, f"{paper['group']} produced too-short body"

    def test_all_7_sentences(self):
        for paper, data, stats in self.ALL_PAPERS:
            body = generate_body(paper, data, stats)
            sc = _sentence_count(body)
            assert sc == 7, (
                f"{paper['group']} has {sc} sentences, expected 7: {body[:100]}..."
            )

    def test_all_under_157_words(self):
        for paper, data, stats in self.ALL_PAPERS:
            body = generate_body(paper, data, stats)
            wc = _word_count(body)
            assert wc <= 156, (
                f"{paper['group']} has {wc} words, exceeds 156"
            )

    def test_all_single_paragraph(self):
        for paper, data, stats in self.ALL_PAPERS:
            body = generate_body(paper, data, stats)
            assert "\n" not in body, f"{paper['group']} contains newline"


# ---------------------------------------------------------------------------
# Sentence generator unit tests
# ---------------------------------------------------------------------------

class TestSentenceGenerators:
    """Unit tests for individual sentence generators."""

    def test_s1_geo_contains_saarc(self):
        s1 = _gen_s1(PAPER_GEO, MOCK_DATA_GEO)
        assert "SAARC" in s1 or "South Asia" in s1

    def test_s1_pakistan_contains_pakistan(self):
        s1 = _gen_s1(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN)
        assert "Pakistan" in s1

    def test_s1_health_with_condition(self):
        s1 = _gen_s1(PAPER_HEALTH, MOCK_DATA_HEALTH)
        assert "Cardiovascular" in s1

    def test_s2_contains_count(self):
        s2 = _gen_s2(PAPER_GEO, MOCK_DATA_GEO)
        assert "28,500" in s2

    def test_s2_contains_saarc(self):
        s2 = _gen_s2(PAPER_GEO, MOCK_DATA_GEO)
        assert "South Asian" in s2 or "SAARC" in s2 or "interventional" in s2

    def test_s3_contains_estimand(self):
        s3 = _gen_s3(["gini_coefficient"])
        assert "Gini" in s3

    def test_s4_gini_result(self):
        s4 = _gen_s4(PAPER_GEO, MOCK_DATA_GEO, MOCK_STATS_GINI)
        assert "0.87" in s4  # Gini value present

    def test_s4_ratio_result(self):
        s4 = _gen_s4(PAPER_HEALTH, MOCK_DATA_HEALTH, MOCK_STATS_RATIO)
        assert "Cardiovascular" in s4  # Condition-specific text

    def test_s5_entropy(self):
        s5 = _gen_s5(MOCK_STATS_GINI, MOCK_DATA_GEO)
        assert "1.45" in s5 or "entropy" in s5.lower()

    def test_s5_fallback(self):
        s5 = _gen_s5(MOCK_STATS_EMPTY, MOCK_DATA_GEO)
        assert "Sensitivity" in s5

    def test_s6_geo_interpretation(self):
        s6 = _gen_s6(PAPER_GEO, MOCK_DATA_GEO)
        assert "monopoly" in s6 or "invisible" in s6 or "SAARC" in s6

    def test_s6_pakistan_interpretation(self):
        s6 = _gen_s6(PAPER_PAKISTAN, MOCK_DATA_PAKISTAN)
        # Should use paper context, mentioning Balochistan or provincial
        assert "balochistan" in s6.lower() or "provincial" in s6.lower() or "concentrated" in s6.lower()

    def test_s7_variants(self):
        variants = _gen_s7_variants()
        assert len(variants) == 3
        for v in variants:
            assert "limited" in v.lower() or "constrained" in v.lower()

    def test_s7_saarc_context(self):
        variants = _gen_s7_variants()
        # At least one variant should mention South Asian or SAARC
        texts = ' '.join(variants)
        assert "South Asian" in texts or "SAARC" in texts


# ---------------------------------------------------------------------------
# Edge case tests
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Edge cases: empty data, zero counts, missing stats."""

    def test_zero_saarc_total(self):
        data = {"saarc_total": 0, "country_counts": {}}
        body = generate_body(PAPER_GEO, data, MOCK_STATS_EMPTY)
        assert _sentence_count(body) == 7
        assert _word_count(body) <= 156

    def test_empty_stats(self):
        body = generate_body(PAPER_GEO, MOCK_DATA_GEO, {})
        assert _sentence_count(body) == 7
        assert _word_count(body) <= 156

    def test_minimal_paper_def(self):
        paper = {
            "slug": "test-minimal",
            "title": "Test Paper",
            "group": "geographic-equity",
            "stats": [],
            "query": {},
        }
        body = generate_body(paper, MOCK_DATA_GEO, {})
        assert _sentence_count(body) == 7
        assert _word_count(body) <= 156
