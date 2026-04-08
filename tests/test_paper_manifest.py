"""Tests for paper_manifest.py — validates schema integrity for all 190 papers."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from lib.paper_manifest import (
    MANIFEST, GEO_PAPERS, HEALTH_PAPERS, GOV_PAPERS, METHODS_PAPERS,
    PAKISTAN_PAPERS, PAK_PROVINCIAL, PAK_INSTITUTIONAL, PAK_DISEASE,
    PAK_SPONSOR, PAK_WORKFORCE, PAK_KARACHI,
    SAARC_COUNTRIES, PAKISTAN_PROVINCES, PAKISTAN_CITIES, PAKISTAN_INSTITUTIONS,
    LANDLOCKED_SAARC, ISLAND_SAARC, CONFLICT_SAARC,
    CHART_TYPES, GROUPS, ROLE_COLORS,
)

# Valid stat method names
VALID_STATS = {
    "gini_coefficient", "bootstrap_ci", "poisson_rate", "rate_ratio",
    "shannon_entropy", "hhi_index", "theil_index", "chi_squared",
    "bayesian_rate", "morans_i", "permutation_test", "spearman_correlation",
    "linear_regression", "network_centrality", "kaplan_meier_survival",
    "odds_ratio", "cohens_d", "kl_divergence", "concentration_index",
    "lorenz_area", "atkinson_index",
}

VALID_GROUPS = {
    "geographic-equity", "health-disease", "governance-justice",
    "methods-systems", "pakistan-deep-dive",
}


class TestManifestCounts:
    """Test total and group paper counts."""

    def test_total_count(self):
        assert len(MANIFEST) == 190

    def test_geo_count(self):
        assert len(GEO_PAPERS) == 35

    def test_health_count(self):
        assert len(HEALTH_PAPERS) == 35

    def test_gov_count(self):
        assert len(GOV_PAPERS) == 35

    def test_methods_count(self):
        assert len(METHODS_PAPERS) == 35

    def test_pakistan_count(self):
        assert len(PAKISTAN_PAPERS) == 50

    def test_pakistan_subgroups(self):
        assert len(PAK_PROVINCIAL) == 10
        assert len(PAK_INSTITUTIONAL) == 8
        assert len(PAK_DISEASE) == 12
        assert len(PAK_SPONSOR) == 8
        assert len(PAK_WORKFORCE) == 7
        assert len(PAK_KARACHI) == 5

    def test_manifest_is_sum_of_groups(self):
        total = len(GEO_PAPERS) + len(HEALTH_PAPERS) + len(GOV_PAPERS) + len(METHODS_PAPERS) + len(PAKISTAN_PAPERS)
        assert total == 190
        assert total == len(MANIFEST)


class TestSlugs:
    """Test slug uniqueness and format."""

    def test_all_slugs_unique(self):
        slugs = [p["slug"] for p in MANIFEST]
        assert len(slugs) == len(set(slugs)), f"Duplicate slugs: {[s for s in slugs if slugs.count(s) > 1]}"

    def test_slug_format(self):
        """Slugs should be kebab-case."""
        for p in MANIFEST:
            slug = p["slug"]
            assert slug == slug.lower(), f"Slug not lowercase: {slug}"
            assert " " not in slug, f"Slug has spaces: {slug}"
            assert slug == slug.strip("-"), f"Slug has leading/trailing hyphens: {slug}"


class TestRequiredFields:
    """Test that every paper has all required fields."""

    REQUIRED = {"slug", "title", "group", "paper_num", "query", "stats", "charts", "context", "refs"}

    def test_all_fields_present(self):
        for i, p in enumerate(MANIFEST):
            missing = self.REQUIRED - set(p.keys())
            assert not missing, f"Paper {i} ({p.get('slug', '?')}): missing fields {missing}"

    def test_query_has_condition_and_countries(self):
        for p in MANIFEST:
            q = p["query"]
            assert "condition" in q, f"Paper {p['slug']}: query missing 'condition'"
            assert "countries" in q, f"Paper {p['slug']}: query missing 'countries'"


class TestStats:
    """Test stat method assignments."""

    def test_at_least_5_stats(self):
        for p in MANIFEST:
            assert len(p["stats"]) >= 5, f"Paper {p['slug']}: only {len(p['stats'])} stats (need 5+)"

    def test_stats_are_valid(self):
        for p in MANIFEST:
            for stat in p["stats"]:
                assert stat in VALID_STATS, f"Paper {p['slug']}: invalid stat '{stat}'"


class TestCharts:
    """Test chart assignments."""

    def test_exactly_8_charts(self):
        for p in MANIFEST:
            assert len(p["charts"]) == 8, f"Paper {p['slug']}: has {len(p['charts'])} charts (need 8)"

    def test_charts_are_valid(self):
        for p in MANIFEST:
            for chart in p["charts"]:
                assert chart in CHART_TYPES, f"Paper {p['slug']}: invalid chart '{chart}'"


class TestGroups:
    """Test group assignments."""

    def test_group_keys_valid(self):
        for p in MANIFEST:
            assert p["group"] in VALID_GROUPS, f"Paper {p['slug']}: invalid group '{p['group']}'"

    def test_groups_dict_has_5_entries(self):
        assert len(GROUPS) == 5
        assert set(GROUPS.keys()) == VALID_GROUPS

    def test_geo_papers_group(self):
        for p in GEO_PAPERS:
            assert p["group"] == "geographic-equity"

    def test_health_papers_group(self):
        for p in HEALTH_PAPERS:
            assert p["group"] == "health-disease"

    def test_gov_papers_group(self):
        for p in GOV_PAPERS:
            assert p["group"] == "governance-justice"

    def test_methods_papers_group(self):
        for p in METHODS_PAPERS:
            assert p["group"] == "methods-systems"

    def test_pakistan_papers_group(self):
        for p in PAKISTAN_PAPERS:
            assert p["group"] == "pakistan-deep-dive"


class TestPaperNums:
    """Test paper numbering within groups."""

    def test_geo_paper_nums(self):
        nums = sorted(p["paper_num"] for p in GEO_PAPERS)
        assert nums == list(range(1, 36))

    def test_health_paper_nums(self):
        nums = sorted(p["paper_num"] for p in HEALTH_PAPERS)
        assert nums == list(range(1, 36))

    def test_gov_paper_nums(self):
        nums = sorted(p["paper_num"] for p in GOV_PAPERS)
        assert nums == list(range(1, 36))

    def test_methods_paper_nums(self):
        nums = sorted(p["paper_num"] for p in METHODS_PAPERS)
        assert nums == list(range(1, 36))

    def test_pakistan_paper_nums(self):
        nums = sorted(p["paper_num"] for p in PAKISTAN_PAPERS)
        assert nums == list(range(1, 51))

    def test_pakistan_provincial_range(self):
        """Provincial Inequity: papers 1-10."""
        nums = sorted(p["paper_num"] for p in PAK_PROVINCIAL)
        assert nums == list(range(1, 11))

    def test_pakistan_institutional_range(self):
        """Institutional Concentration: papers 11-18."""
        nums = sorted(p["paper_num"] for p in PAK_INSTITUTIONAL)
        assert nums == list(range(11, 19))

    def test_pakistan_disease_range(self):
        """Disease-Specific Gaps: papers 19-30."""
        nums = sorted(p["paper_num"] for p in PAK_DISEASE)
        assert nums == list(range(19, 31))

    def test_pakistan_sponsor_range(self):
        """Sponsor & Sovereignty: papers 31-38."""
        nums = sorted(p["paper_num"] for p in PAK_SPONSOR)
        assert nums == list(range(31, 39))

    def test_pakistan_workforce_range(self):
        """Workforce & Methods: papers 39-45."""
        nums = sorted(p["paper_num"] for p in PAK_WORKFORCE)
        assert nums == list(range(39, 46))

    def test_pakistan_karachi_range(self):
        """Karachi Lens: papers 46-50."""
        nums = sorted(p["paper_num"] for p in PAK_KARACHI)
        assert nums == list(range(46, 51))


class TestConstants:
    """Test constant definitions."""

    def test_saarc_countries_count(self):
        assert len(SAARC_COUNTRIES) == 8

    def test_saarc_countries_content(self):
        expected = {"India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal", "Afghanistan", "Bhutan", "Maldives"}
        assert set(SAARC_COUNTRIES) == expected

    def test_pakistan_provinces_count(self):
        assert len(PAKISTAN_PROVINCES) == 7

    def test_pakistan_cities_map(self):
        assert len(PAKISTAN_CITIES) > 0
        for city, province in PAKISTAN_CITIES.items():
            assert province in PAKISTAN_PROVINCES, f"City {city} maps to unknown province {province}"

    def test_pakistan_institutions_not_empty(self):
        assert len(PAKISTAN_INSTITUTIONS) >= 10

    def test_landlocked_saarc(self):
        for c in LANDLOCKED_SAARC:
            assert c in SAARC_COUNTRIES

    def test_island_saarc(self):
        for c in ISLAND_SAARC:
            assert c in SAARC_COUNTRIES

    def test_conflict_saarc(self):
        for c in CONFLICT_SAARC:
            assert c in SAARC_COUNTRIES

    def test_chart_types_count(self):
        assert len(CHART_TYPES) == 16

    def test_choropleth_pakistan_in_chart_types(self):
        assert "choropleth_pakistan" in CHART_TYPES

    def test_role_colors_count(self):
        assert len(ROLE_COLORS) == 7


class TestPakistanDeepDive:
    """Pakistan deep-dive specific tests."""

    def test_pakistan_papers_have_pakistan_country(self):
        """All Pakistan deep-dive papers should query Pakistan."""
        for p in PAKISTAN_PAPERS:
            assert "Pakistan" in p["query"]["countries"], f"Paper {p['slug']}: Pakistan not in countries"

    def test_provincial_papers_use_choropleth_pakistan(self):
        """Provincial papers (1-10) should use choropleth_pakistan chart."""
        for p in PAK_PROVINCIAL:
            assert "choropleth_pakistan" in p["charts"], \
                f"Paper {p['slug']}: missing choropleth_pakistan chart"


class TestRefs:
    """Test reference assignments."""

    def test_refs_not_empty(self):
        for p in MANIFEST:
            assert len(p["refs"]) >= 2, f"Paper {p['slug']}: only {len(p['refs'])} refs (need 2+)"

    def test_refs_at_most_3(self):
        for p in MANIFEST:
            assert len(p["refs"]) <= 3, f"Paper {p['slug']}: has {len(p['refs'])} refs (max 3)"


class TestContext:
    """Test context descriptions."""

    def test_context_not_empty(self):
        for p in MANIFEST:
            assert len(p["context"]) > 20, f"Paper {p['slug']}: context too short"

    def test_context_is_string(self):
        for p in MANIFEST:
            assert isinstance(p["context"], str), f"Paper {p['slug']}: context is not a string"


class TestChartDiversity:
    """Test that chart combinations vary across papers within each group."""

    def test_no_duplicate_chart_combos_within_group(self):
        """Within each group, chart combinations should not all be identical."""
        for group_name, papers in [
            ("geographic-equity", GEO_PAPERS),
            ("health-disease", HEALTH_PAPERS),
            ("governance-justice", GOV_PAPERS),
            ("methods-systems", METHODS_PAPERS),
            ("pakistan-deep-dive", PAKISTAN_PAPERS),
        ]:
            chart_tuples = [tuple(p["charts"]) for p in papers]
            unique_combos = set(chart_tuples)
            # At least 50% of papers should have unique chart combinations
            assert len(unique_combos) >= len(papers) * 0.5, \
                f"Group {group_name}: only {len(unique_combos)} unique chart combos for {len(papers)} papers"
