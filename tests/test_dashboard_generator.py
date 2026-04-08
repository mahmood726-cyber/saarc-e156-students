"""Tests for dashboard_generator — self-contained HTML dashboards with SVG charts."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.dashboard_generator import (
    generate_dashboard,
    _split_sentences,
    _word_count,
    _fmt,
    _safe,
    _prepare_chart_data,
    ROLE_NAMES,
)
from lib.paper_manifest import MANIFEST, ROLE_COLORS, GROUPS


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

_BODY = (
    "How many clinical trials are registered across SAARC nations on the US federal registry? "
    "We queried 28,500 studies spanning all eight SAARC countries from 2000 to 2025. "
    "Gini coefficients and Lorenz curves quantified geographic concentration. "
    "India hosted 24,500 trials (86%), followed by Pakistan with 1,800 at six percent. "
    "A Gini above ninety percent indicates extreme concentration across the region. "
    "Six of eight SAARC nations remain severely under-represented in global evidence. "
    "These findings exclude non-registered and retrospective studies."
)

_GEO_PAPER = {
    "slug": "saarc-trial-density-map",
    "title": "SAARC Trial Density Map",
    "group": "geographic-equity",
    "paper_num": 1,
    "query": {"condition": None, "countries": ["India", "Pakistan", "Bangladesh"]},
    "stats": ["gini_coefficient", "bootstrap_ci"],
    "charts": ["choropleth", "lorenz", "forest", "violin",
               "heatmap", "timeseries", "radar", "waterfall"],
    "context": "SAARC nations collectively host over 1.9 billion people.",
    "refs": [],
}

_PAKISTAN_PAPER = {
    "slug": "punjab-dominance-provincial",
    "title": "Punjab Dominance Provincial",
    "group": "pakistan-deep-dive",
    "paper_num": 1,
    "query": {"condition": None, "countries": ["Pakistan"]},
    "stats": ["hhi_index", "gini_coefficient"],
    "charts": ["choropleth_pakistan", "choropleth", "lorenz", "waterfall",
               "timeseries", "radar", "forest", "slope"],
    "context": "Punjab province hosts over 60% of Pakistan's clinical trials.",
    "refs": [],
}

_DATA = {
    "saarc_count": 28500,
    "india_count": 24500,
    "pakistan_count": 1800,
    "us_count": 190644,
    "total_saarc": 28500,
    "country_counts": {
        "India": 24500, "Pakistan": 1800, "Bangladesh": 900,
        "Sri Lanka": 450, "Nepal": 350, "Afghanistan": 80,
        "Bhutan": 12, "Maldives": 8,
    },
    "study_metrics": {"enrollment_values": [100, 200, 300, 50, 80, 150]},
}

_STATS = {
    "gini_coefficient": {"gini": 0.912, "ci_lower": 0.88, "ci_upper": 0.94},
}


# ---------------------------------------------------------------------------
# Helper tests
# ---------------------------------------------------------------------------

class TestHelpers:
    def test_word_count(self):
        assert _word_count("hello world") == 2
        assert _word_count("one") == 1
        assert _word_count("a b c d") == 4

    def test_fmt_int(self):
        assert _fmt(1000) == "1,000"
        assert _fmt(5) == "5"

    def test_fmt_float(self):
        assert _fmt(3.14159, 2) == "3.14"

    def test_fmt_none(self):
        assert _fmt(None) == "N/A"

    def test_safe(self):
        assert _safe(None, 42) == 42
        assert _safe(10) == 10
        assert _safe(0) == 0

    def test_split_sentences_seven(self):
        sents = _split_sentences(_BODY)
        assert len(sents) == 7

    def test_split_sentences_preserves_text(self):
        sents = _split_sentences(_BODY)
        rejoined = ' '.join(sents)
        assert "24,500" in rejoined
        assert "SAARC" in rejoined


# ---------------------------------------------------------------------------
# Dashboard structure tests
# ---------------------------------------------------------------------------

class TestDashboardStructure:
    def test_dashboard_is_valid_html(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert html.strip().startswith("<!doctype html")
        assert html.strip().endswith("</html>")

    def test_dashboard_contains_title(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "SAARC Trial Density Map" in html
        assert "<title>" in html
        assert "SAARC E156</title>" in html

    def test_dashboard_contains_svg_charts(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "<svg" in html
        # Should have multiple SVG charts
        svg_count = html.count("<svg")
        assert svg_count >= 4, f"Expected at least 4 SVGs, got {svg_count}"

    def test_dashboard_contains_body_text(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "24,500 trials" in html
        assert "body-text" in html

    def test_dashboard_has_sentence_breakdown(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "Sentence Structure" in html
        assert "role-tag" in html
        # Check at least some role names appear
        assert "Question" in html
        assert "Dataset" in html
        assert "Primary Result" in html
        assert "Boundary" in html

    def test_dashboard_no_external_dependencies(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        # Must not reference external CDN or unpkg
        assert "cdn." not in html.lower()
        assert "unpkg.com" not in html.lower()
        assert "cdnjs." not in html.lower()
        assert "googleapis.com" not in html.lower()
        # No external script or link tags
        for line in html.split('\n'):
            low = line.lower().strip()
            if low.startswith('<script') and 'src=' in low:
                assert 'http' not in low, f"External script found: {line}"
            if low.startswith('<link') and 'href=' in low and 'stylesheet' in low:
                assert 'http' not in low, f"External stylesheet found: {line}"

    def test_dashboard_has_open_graph(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert 'og:title' in html
        assert 'og:description' in html
        assert 'og:type' in html

    def test_dashboard_has_color_strip(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "color-strip" in html
        # 7 segments
        for color in ROLE_COLORS:
            assert color in html

    def test_dashboard_has_hero(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "hero" in html
        assert "SAARC Trials" in html or "SAARC Clinical Trials" in html

    def test_dashboard_has_finding(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "Key Finding" in html
        assert "finding" in html

    def test_dashboard_has_context(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "Why It Matters" in html
        assert "1.9 billion" in html

    def test_dashboard_has_footer(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "Mahmood Ahmad" in html
        assert "saarc-e156-students" in html

    def test_dashboard_is_responsive(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "viewport" in html
        assert "max-width:700px" in html

    def test_dashboard_word_badge(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, _BODY)
        assert "word-badge" in html
        assert "target 156" in html


# ---------------------------------------------------------------------------
# Pakistan deep-dive tests
# ---------------------------------------------------------------------------

class TestPakistanDeepDive:
    def test_dashboard_pakistan_deep_dive(self):
        html = generate_dashboard(_PAKISTAN_PAPER, _DATA, _STATS, _BODY)
        assert html.strip().startswith("<!doctype html")
        assert html.strip().endswith("</html>")
        assert "<svg" in html

    def test_pakistan_uses_green_accent(self):
        html = generate_dashboard(_PAKISTAN_PAPER, _DATA, _STATS, _BODY)
        assert "#006600" in html
        assert "pakistan-deep-dive" in html

    def test_pakistan_eyebrow(self):
        html = generate_dashboard(_PAKISTAN_PAPER, _DATA, _STATS, _BODY)
        assert "Pakistan Clinical Trials" in html

    def test_pakistan_province_metrics(self):
        html = generate_dashboard(_PAKISTAN_PAPER, _DATA, _STATS, _BODY)
        assert "Pakistan Trials" in html
        assert "Provinces" in html

    def test_pakistan_choropleth_present(self):
        """Pakistan papers should attempt choropleth_pakistan chart."""
        html = generate_dashboard(_PAKISTAN_PAPER, _DATA, _STATS, _BODY)
        # Should contain SVGs (charts rendered)
        assert "<svg" in html


# ---------------------------------------------------------------------------
# Chart preparation tests
# ---------------------------------------------------------------------------

class TestChartPreparation:
    def test_all_chart_types_produce_svg(self):
        """Each chart type should return a non-empty SVG string."""
        import random
        rng = random.Random(42)
        chart_types = [
            "choropleth", "lorenz", "forest", "violin", "heatmap",
            "network", "timeseries", "waterfall", "sankey", "radar",
            "bubble", "slope", "ridge", "funnel", "kaplan_meier",
            "choropleth_pakistan",
        ]
        for ct in chart_types:
            svg = _prepare_chart_data(ct, _GEO_PAPER, _DATA, _STATS, rng)
            assert svg, f"Chart type '{ct}' returned empty"
            assert "<svg" in svg, f"Chart type '{ct}' missing <svg tag"

    def test_unknown_chart_type_returns_empty(self):
        import random
        rng = random.Random(42)
        svg = _prepare_chart_data("nonexistent_type", _GEO_PAPER, _DATA, _STATS, rng)
        assert svg == ""

    def test_charts_with_empty_data(self):
        """Charts should still render with minimal/empty data."""
        import random
        rng = random.Random(42)
        empty_data = {}
        empty_stats = {}
        for ct in ["choropleth", "lorenz", "forest", "radar", "waterfall"]:
            svg = _prepare_chart_data(ct, _GEO_PAPER, empty_data, empty_stats, rng)
            assert isinstance(svg, str)
            # Even with empty data, defaults should produce SVGs
            if ct in ("choropleth", "forest", "waterfall", "radar"):
                assert "<svg" in svg, f"Chart '{ct}' should render with defaults"


# ---------------------------------------------------------------------------
# Manifest integration test
# ---------------------------------------------------------------------------

class TestManifestIntegration:
    def test_first_paper_renders(self):
        """First paper from the real manifest produces valid HTML."""
        paper = MANIFEST[0]
        html = generate_dashboard(paper, _DATA, _STATS, _BODY)
        assert html.strip().startswith("<!doctype html")
        assert html.strip().endswith("</html>")
        assert "<svg" in html

    def test_last_paper_renders(self):
        """Last paper from the real manifest produces valid HTML."""
        paper = MANIFEST[-1]
        html = generate_dashboard(paper, _DATA, _STATS, _BODY)
        assert html.strip().startswith("<!doctype html")
        assert html.strip().endswith("</html>")

    def test_pakistan_paper_from_manifest(self):
        """A real pakistan-deep-dive paper renders with green accent."""
        pak_papers = [p for p in MANIFEST if p["group"] == "pakistan-deep-dive"]
        assert len(pak_papers) > 0, "No pakistan-deep-dive papers in MANIFEST"
        html = generate_dashboard(pak_papers[0], _DATA, _STATS, _BODY)
        assert "#006600" in html
        assert "pakistan-deep-dive" in html


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_body(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, "")
        assert html.strip().startswith("<!doctype html")
        assert "0 words" in html

    def test_short_body(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, _STATS, "Just one sentence.")
        assert "Just one sentence." in html

    def test_no_gini_in_stats(self):
        html = generate_dashboard(_GEO_PAPER, _DATA, {}, _BODY)
        assert html.strip().startswith("<!doctype html")
        # Should still render without gini
        assert "Nations" in html or "SAARC" in html

    def test_minimal_paper_def(self):
        minimal = {
            "slug": "minimal-test",
            "title": "Minimal Test",
            "group": "geographic-equity",
            "paper_num": 999,
            "query": {},
            "stats": [],
            "charts": [],
            "context": "",
            "refs": [],
        }
        html = generate_dashboard(minimal, {}, {}, _BODY)
        assert html.strip().startswith("<!doctype html")
        assert "Minimal Test" in html

    def test_role_names_count(self):
        assert len(ROLE_NAMES) == 7
        assert len(ROLE_COLORS) == 7
