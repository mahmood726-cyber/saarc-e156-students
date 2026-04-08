"""Tests for chart_library — 16 SVG chart generators with SAARC and Pakistan maps."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from lib.chart_library import (
    CHART_TYPE_MAP,
    choropleth_saarc, choropleth_pakistan,
    lorenz_chart, forest_plot, violin_plot, heatmap_chart,
    network_graph, timeseries_chart, waterfall_chart, sankey_chart,
    radar_chart, bubble_chart, slope_chart, ridge_plot,
    funnel_plot, kaplan_meier_chart,
    _fmt, _lerp_color, _axis_ticks, _gaussian_kde,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_valid_svg(s):
    """Check string is a complete SVG element."""
    return isinstance(s, str) and s.startswith("<svg") and s.endswith("</svg>")


# ---------------------------------------------------------------------------
# CHART_TYPE_MAP
# ---------------------------------------------------------------------------

class TestChartTypeMap:
    def test_has_16_entries(self):
        assert len(CHART_TYPE_MAP) == 16

    def test_all_functions_callable(self):
        """Every value in CHART_TYPE_MAP refers to a callable in the module."""
        import lib.chart_library as mod
        for key, func_name in CHART_TYPE_MAP.items():
            fn = getattr(mod, func_name, None)
            assert callable(fn), f"CHART_TYPE_MAP['{key}'] -> '{func_name}' is not callable"

    def test_expected_keys(self):
        expected = {
            "choropleth", "choropleth_pakistan", "lorenz", "forest",
            "violin", "heatmap", "network", "timeseries", "waterfall",
            "sankey", "radar", "bubble", "slope", "ridge", "funnel",
            "kaplan_meier",
        }
        assert set(CHART_TYPE_MAP.keys()) == expected


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

class TestHelpers:
    def test_fmt_integer(self):
        assert _fmt(5) == "5"
        assert _fmt(5.0) == "5"

    def test_fmt_decimal(self):
        assert _fmt(3.14159, 2) == "3.14"

    def test_lerp_color_bounds(self):
        lo = _lerp_color(0.0)
        hi = _lerp_color(1.0)
        assert lo.startswith("rgb(")
        assert hi.startswith("rgb(")
        # Default: light green to Pakistan green
        assert lo == "rgb(230,245,230)"
        assert hi == "rgb(0,102,0)"

    def test_lerp_color_mid(self):
        mid = _lerp_color(0.5)
        assert mid.startswith("rgb(")

    def test_lerp_color_clamps(self):
        assert _lerp_color(-1.0) == _lerp_color(0.0)
        assert _lerp_color(2.0) == _lerp_color(1.0)

    def test_axis_ticks_basic(self):
        ticks = _axis_ticks(0, 100, 5)
        assert len(ticks) >= 3
        assert ticks[0] <= 0
        assert ticks[-1] >= 100

    def test_axis_ticks_equal(self):
        ticks = _axis_ticks(5, 5, 5)
        assert len(ticks) >= 2  # should handle lo == hi

    def test_gaussian_kde_empty(self):
        assert _gaussian_kde([]) == []

    def test_gaussian_kde_basic(self):
        kde = _gaussian_kde([1, 2, 3, 4, 5], n_points=20)
        assert len(kde) == 20
        assert all(isinstance(pt, tuple) and len(pt) == 2 for pt in kde)
        # All densities non-negative
        assert all(d >= 0 for _, d in kde)


# ---------------------------------------------------------------------------
# 1. Choropleth SAARC
# ---------------------------------------------------------------------------

class TestChoroplethSaarc:
    def test_valid_svg(self):
        vals = {"India": 100, "Pakistan": 50, "Bangladesh": 30}
        svg = choropleth_saarc(vals, "SAARC Trial Density")
        assert _is_valid_svg(svg)

    def test_contains_country_names(self):
        vals = {"India": 100, "Pakistan": 50, "Sri Lanka": 20}
        svg = choropleth_saarc(vals, "Test")
        assert "IND" in svg
        assert "PAK" in svg
        assert "LKA" in svg

    def test_all_eight_nations(self):
        vals = {
            "Afghanistan": 5, "Pakistan": 80, "India": 200,
            "Nepal": 10, "Bhutan": 2, "Bangladesh": 40,
            "Sri Lanka": 15, "Maldives": 1,
        }
        svg = choropleth_saarc(vals, "All SAARC")
        assert _is_valid_svg(svg)
        for abbr in ["AFG", "PAK", "IND", "NPL", "BTN", "BGD", "LKA", "MDV"]:
            assert abbr in svg, f"Missing country abbreviation: {abbr}"

    def test_empty_returns_empty(self):
        assert choropleth_saarc({}, "Test") == ""

    def test_none_values_handled(self):
        vals = {"India": None, "Pakistan": 50}
        svg = choropleth_saarc(vals, "Test")
        assert _is_valid_svg(svg)
        assert "N/A" in svg

    def test_single_country(self):
        svg = choropleth_saarc({"India": 42}, "Single")
        assert _is_valid_svg(svg)

    def test_title_escaped(self):
        svg = choropleth_saarc({"India": 1}, "Test <br> & Title")
        assert "&amp;" in svg
        assert "&lt;" in svg


# ---------------------------------------------------------------------------
# 2. Choropleth Pakistan
# ---------------------------------------------------------------------------

class TestChoroplethPakistan:
    def test_valid_svg(self):
        vals = {"Punjab": 100, "Sindh": 60, "KPK": 30, "Balochistan": 10}
        svg = choropleth_pakistan(vals, "Pakistan Provinces")
        assert _is_valid_svg(svg)

    def test_contains_province_names(self):
        vals = {"Punjab": 100, "Sindh": 60, "Balochistan": 10}
        svg = choropleth_pakistan(vals, "Test")
        assert "PJB" in svg
        assert "SND" in svg
        assert "BAL" in svg

    def test_all_seven_regions(self):
        vals = {
            "Balochistan": 10, "Sindh": 60, "Punjab": 100,
            "KPK": 40, "ICT": 5, "Gilgit-Baltistan": 3, "AJK": 8,
        }
        svg = choropleth_pakistan(vals, "All Pakistan")
        assert _is_valid_svg(svg)
        for abbr in ["BAL", "SND", "PJB", "KPK", "ICT", "GB", "AJK"]:
            assert abbr in svg, f"Missing province abbreviation: {abbr}"

    def test_empty_returns_empty(self):
        assert choropleth_pakistan({}, "Test") == ""

    def test_none_values(self):
        vals = {"Punjab": None, "Sindh": 50}
        svg = choropleth_pakistan(vals, "Test")
        assert _is_valid_svg(svg)

    def test_ict_small_territory(self):
        """ICT is a tiny territory — should still render."""
        svg = choropleth_pakistan({"ICT": 42}, "ICT Only")
        assert _is_valid_svg(svg)
        assert "ICT" in svg


# ---------------------------------------------------------------------------
# 3. Lorenz Chart
# ---------------------------------------------------------------------------

class TestLorenzChart:
    def test_valid_svg(self):
        svg = lorenz_chart([10, 20, 30, 40, 50], "Equity")
        assert _is_valid_svg(svg)

    def test_gini_annotation(self):
        svg = lorenz_chart([1, 1, 1, 1, 100], "Gini Test")
        assert "Gini" in svg

    def test_too_few_values(self):
        assert lorenz_chart([5], "One") == ""
        assert lorenz_chart([], "None") == ""

    def test_all_zeros(self):
        assert lorenz_chart([0, 0, 0], "Zeros") == ""

    def test_equal_values(self):
        svg = lorenz_chart([10, 10, 10, 10], "Equal")
        assert _is_valid_svg(svg)
        assert "0.000" in svg  # Gini should be 0


# ---------------------------------------------------------------------------
# 4. Forest Plot
# ---------------------------------------------------------------------------

class TestForestPlot:
    def test_valid_svg(self):
        effects = [
            {"label": "Study A", "estimate": 1.5, "ci_lower": 1.0, "ci_upper": 2.2},
            {"label": "Study B", "estimate": 0.8, "ci_lower": 0.5, "ci_upper": 1.1},
        ]
        svg = forest_plot(effects, "Forest")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert forest_plot([], "Empty") == ""

    def test_labels_present(self):
        effects = [{"label": "TOPCAT", "estimate": 1.0, "ci_lower": 0.8, "ci_upper": 1.2}]
        svg = forest_plot(effects, "Test")
        assert "TOPCAT" in svg


# ---------------------------------------------------------------------------
# 5. Violin Plot
# ---------------------------------------------------------------------------

class TestViolinPlot:
    def test_valid_svg(self):
        groups = {
            "Pakistan": [10, 20, 30, 25, 15],
            "India": [40, 50, 60, 55, 45],
        }
        svg = violin_plot(groups, "Distributions")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert violin_plot({}, "Empty") == ""

    def test_single_value_group_skipped(self):
        groups = {"A": [10], "B": [20, 30, 40]}
        svg = violin_plot(groups, "Test")
        assert _is_valid_svg(svg)


# ---------------------------------------------------------------------------
# 6. Heatmap Chart
# ---------------------------------------------------------------------------

class TestHeatmapChart:
    def test_valid_svg(self):
        matrix = [[10, 20, 30], [40, 50, 60]]
        svg = heatmap_chart(matrix, ["Row1", "Row2"], ["C1", "C2", "C3"], "Heat")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert heatmap_chart([], [], [], "Empty") == ""
        assert heatmap_chart([[]], ["R"], ["C"], "Empty") == ""

    def test_none_cells(self):
        matrix = [[10, None], [None, 50]]
        svg = heatmap_chart(matrix, ["A", "B"], ["X", "Y"], "Sparse")
        assert _is_valid_svg(svg)


# ---------------------------------------------------------------------------
# 7. Network Graph
# ---------------------------------------------------------------------------

class TestNetworkGraph:
    def test_valid_svg(self):
        nodes = [{"id": "A", "size": 10}, {"id": "B", "size": 8}, {"id": "C", "size": 6}]
        edges = [{"source": 0, "target": 1, "weight": 2}, {"source": 1, "target": 2, "weight": 1}]
        svg = network_graph(nodes, edges, "Network")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert network_graph([], [], "Empty") == ""

    def test_node_labels(self):
        nodes = [{"id": "Pakistan"}, {"id": "India"}]
        edges = [{"source": 0, "target": 1}]
        svg = network_graph(nodes, edges, "Test")
        assert "Pakistan" in svg
        assert "India" in svg


# ---------------------------------------------------------------------------
# 8. Timeseries Chart
# ---------------------------------------------------------------------------

class TestTimeseriesChart:
    def test_valid_svg(self):
        series = {
            "Pakistan": [(2000, 10), (2005, 20), (2010, 30)],
            "India": [(2000, 15), (2005, 25), (2010, 35)],
        }
        svg = timeseries_chart(series, "Trends")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert timeseries_chart({}, "Empty") == ""

    def test_changepoints(self):
        series = {"A": [(2000, 10), (2005, 20), (2010, 30)]}
        svg = timeseries_chart(series, "CP", changepoints=[2005])
        assert _is_valid_svg(svg)


# ---------------------------------------------------------------------------
# 9. Waterfall Chart
# ---------------------------------------------------------------------------

class TestWaterfallChart:
    def test_valid_svg(self):
        items = [
            {"label": "Base", "value": 100},
            {"label": "Add", "value": 50},
            {"label": "Loss", "value": -30},
        ]
        svg = waterfall_chart(items, "Waterfall")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert waterfall_chart([], "Empty") == ""


# ---------------------------------------------------------------------------
# 10. Sankey Chart
# ---------------------------------------------------------------------------

class TestSankeyChart:
    def test_valid_svg(self):
        flows = [
            {"source": "Pakistan", "target": "Cardiology", "value": 50},
            {"source": "India", "target": "Oncology", "value": 80},
            {"source": "Pakistan", "target": "Oncology", "value": 20},
        ]
        svg = sankey_chart(flows, "Flow")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert sankey_chart([], "Empty") == ""

    def test_labels_present(self):
        flows = [{"source": "Lahore", "target": "Cardio", "value": 10}]
        svg = sankey_chart(flows, "Test")
        assert "Lahore" in svg
        assert "Cardio" in svg


# ---------------------------------------------------------------------------
# 11. Radar Chart
# ---------------------------------------------------------------------------

class TestRadarChart:
    def test_valid_svg(self):
        dims = {"Equity": 0.7, "Access": 0.5, "Quality": 0.9, "Coverage": 0.6}
        svg = radar_chart(dims, "Radar")
        assert _is_valid_svg(svg)

    def test_too_few_dimensions(self):
        assert radar_chart({"A": 1, "B": 2}, "Two") == ""

    def test_empty(self):
        assert radar_chart({}, "Empty") == ""


# ---------------------------------------------------------------------------
# 12. Bubble Chart
# ---------------------------------------------------------------------------

class TestBubbleChart:
    def test_valid_svg(self):
        pts = [
            {"x": 10, "y": 20, "size": 30, "label": "PAK"},
            {"x": 40, "y": 50, "size": 60, "label": "IND"},
        ]
        svg = bubble_chart(pts, "Bubbles")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert bubble_chart([], "Empty") == ""


# ---------------------------------------------------------------------------
# 13. Slope Chart
# ---------------------------------------------------------------------------

class TestSlopeChart:
    def test_valid_svg(self):
        pairs = [
            {"label": "Punjab", "before": 30, "after": 50},
            {"label": "Sindh", "before": 40, "after": 35},
        ]
        svg = slope_chart(pairs, "Before/After")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert slope_chart([], "Empty") == ""

    def test_labels(self):
        pairs = [{"label": "KPK", "before": 10, "after": 20}]
        svg = slope_chart(pairs, "Test")
        assert "KPK" in svg


# ---------------------------------------------------------------------------
# 14. Ridge Plot
# ---------------------------------------------------------------------------

class TestRidgePlot:
    def test_valid_svg(self):
        dists = {
            "Pakistan": [10, 20, 30, 25, 15, 18, 22],
            "India": [40, 50, 60, 55, 45, 48, 52],
        }
        svg = ridge_plot(dists, "Ridges")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert ridge_plot({}, "Empty") == ""


# ---------------------------------------------------------------------------
# 15. Funnel Plot
# ---------------------------------------------------------------------------

class TestFunnelPlot:
    def test_valid_svg(self):
        effects = [
            {"effect": 0.5, "se": 0.1, "label": "Study 1"},
            {"effect": 0.3, "se": 0.2, "label": "Study 2"},
            {"effect": 0.7, "se": 0.15, "label": "Study 3"},
        ]
        svg = funnel_plot(effects, "Funnel")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert funnel_plot([], "Empty") == ""

    def test_contains_axis_labels(self):
        effects = [{"effect": 0.5, "se": 0.1}]
        svg = funnel_plot(effects, "Test")
        assert "Effect Size" in svg
        assert "Std Error" in svg


# ---------------------------------------------------------------------------
# 16. Kaplan-Meier Chart
# ---------------------------------------------------------------------------

class TestKaplanMeierChart:
    def test_valid_svg(self):
        curves = {
            "Treatment": [(0, 1.0), (6, 0.9), (12, 0.75), (18, 0.6), (24, 0.5)],
            "Control": [(0, 1.0), (6, 0.85), (12, 0.65), (18, 0.45), (24, 0.3)],
        }
        svg = kaplan_meier_chart(curves, "Survival")
        assert _is_valid_svg(svg)

    def test_empty(self):
        assert kaplan_meier_chart({}, "Empty") == ""

    def test_single_point_curve_skipped(self):
        curves = {"A": [(0, 1.0)], "B": [(0, 1.0), (12, 0.5)]}
        svg = kaplan_meier_chart(curves, "Test")
        assert _is_valid_svg(svg)

    def test_at_risk_table(self):
        curves = {"Arm": [(0, 1.0), (6, 0.8), (12, 0.6)]}
        svg = kaplan_meier_chart(curves, "Test")
        assert "At risk" in svg


# ---------------------------------------------------------------------------
# Cross-cutting: every chart function returns valid SVG or empty string
# ---------------------------------------------------------------------------

class TestAllChartsReturnValidSvg:
    """Smoke test that every chart function produces valid SVG."""

    def test_choropleth_saarc(self):
        svg = choropleth_saarc({"India": 100, "Pakistan": 50}, "T")
        assert _is_valid_svg(svg)

    def test_choropleth_pakistan(self):
        svg = choropleth_pakistan({"Punjab": 100, "Sindh": 50}, "T")
        assert _is_valid_svg(svg)

    def test_lorenz(self):
        svg = lorenz_chart([10, 20, 30], "T")
        assert _is_valid_svg(svg)

    def test_forest(self):
        svg = forest_plot([{"estimate": 1, "ci_lower": 0.5, "ci_upper": 1.5}], "T")
        assert _is_valid_svg(svg)

    def test_violin(self):
        svg = violin_plot({"G": [1, 2, 3, 4, 5]}, "T")
        assert _is_valid_svg(svg)

    def test_heatmap(self):
        svg = heatmap_chart([[1, 2], [3, 4]], ["R1", "R2"], ["C1", "C2"], "T")
        assert _is_valid_svg(svg)

    def test_network(self):
        svg = network_graph([{"id": "A"}, {"id": "B"}],
                            [{"source": 0, "target": 1}], "T")
        assert _is_valid_svg(svg)

    def test_timeseries(self):
        svg = timeseries_chart({"S": [(0, 1), (1, 2)]}, "T")
        assert _is_valid_svg(svg)

    def test_waterfall(self):
        svg = waterfall_chart([{"value": 10}, {"value": -5}], "T")
        assert _is_valid_svg(svg)

    def test_sankey(self):
        svg = sankey_chart([{"source": "A", "target": "B", "value": 10}], "T")
        assert _is_valid_svg(svg)

    def test_radar(self):
        svg = radar_chart({"X": 0.5, "Y": 0.7, "Z": 0.3}, "T")
        assert _is_valid_svg(svg)

    def test_bubble(self):
        svg = bubble_chart([{"x": 1, "y": 2, "size": 10}], "T")
        assert _is_valid_svg(svg)

    def test_slope(self):
        svg = slope_chart([{"before": 10, "after": 20}], "T")
        assert _is_valid_svg(svg)

    def test_ridge(self):
        svg = ridge_plot({"G": [1, 2, 3, 4]}, "T")
        assert _is_valid_svg(svg)

    def test_funnel(self):
        svg = funnel_plot([{"effect": 0.5, "se": 0.1}], "T")
        assert _is_valid_svg(svg)

    def test_kaplan_meier(self):
        svg = kaplan_meier_chart({"C": [(0, 1.0), (12, 0.5)]}, "T")
        assert _is_valid_svg(svg)
