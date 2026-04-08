"""Tests for index_updater.py — validates HTML assembly for group and landing pages."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from html import escape

from lib.index_updater import make_paper_card, make_group_page, make_landing_page
from lib.paper_manifest import PAPERS, GROUPS


# ── Sample fixtures ───────────────────────────────────────

SAMPLE_PAPER = PAPERS[0]  # First paper from manifest
SAMPLE_BODY = "This is a sample E156 body text with seven sentences for testing purposes."


# ── Paper card tests ──────────────────────────────────────

def test_paper_card_html():
    """Card contains title, slug-based links, and paper-card class."""
    html = make_paper_card(SAMPLE_PAPER, 1, SAMPLE_BODY)
    assert 'class="paper-card"' in html
    assert SAMPLE_PAPER["title"] in html
    assert SAMPLE_PAPER["slug"] in html
    assert 'id="paper-1"' in html


def test_paper_card_has_sent_strip():
    """Card contains the 7-segment sentence colour strip."""
    html = make_paper_card(SAMPLE_PAPER, 1, SAMPLE_BODY)
    assert 'class="sent-strip"' in html
    assert html.count('class="seg"') == 7


def test_paper_card_has_actions():
    """Card contains dashboard, code download, and paper download buttons."""
    html = make_paper_card(SAMPLE_PAPER, 1, SAMPLE_BODY)
    assert "View Dashboard" in html
    assert "Download Code" in html
    assert "Download Paper" in html
    slug = SAMPLE_PAPER["slug"]
    assert f"dashboards/{slug}.html" in html
    assert f"code/{slug}.py" in html


def test_paper_card_has_note_block():
    """Card contains metadata note block with estimand, data source, certainty."""
    html = make_paper_card(SAMPLE_PAPER, 1, SAMPLE_BODY)
    assert "Estimand" in html
    assert "ClinicalTrials.gov API v2" in html
    assert "MODERATE" in html


def test_paper_card_has_refs():
    """Card contains suggested references."""
    html = make_paper_card(SAMPLE_PAPER, 1, SAMPLE_BODY)
    assert "Suggested References" in html
    assert "<ol>" in html


def test_paper_card_escapes_body():
    """Card escapes HTML entities in body text."""
    dangerous_body = '<script>alert("xss")</script>'
    html = make_paper_card(SAMPLE_PAPER, 1, dangerous_body)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_paper_card_placeholder_when_empty():
    """Card shows placeholder when body is empty."""
    html = make_paper_card(SAMPLE_PAPER, 1, "")
    assert "Body text will appear" in html


# ── Group page tests ──────────────────────────────────────

def _get_group_papers(group_id):
    """Get papers for a specific group."""
    return [p for p in PAPERS if p["group"] == group_id]


def test_group_page_contains_instructions():
    """Group page has Ziauddin workflow instructions."""
    papers = _get_group_papers("geographic-equity")
    html = make_group_page("geographic-equity", papers, {})
    assert "Ziauddin" in html
    assert "instructions" in html.lower()
    assert "Student Workflow" in html


def test_group_page_valid_html():
    """Group page has doctype and closing html tag."""
    papers = _get_group_papers("health-disease")
    html = make_group_page("health-disease", papers, {})
    assert html.strip().startswith("<!doctype html>")
    assert "</html>" in html


def test_group_page_has_og_meta():
    """Group page has Open Graph meta tags."""
    papers = _get_group_papers("governance-justice")
    html = make_group_page("governance-justice", papers, {})
    assert 'property="og:title"' in html
    assert 'property="og:description"' in html


def test_group_page_has_e156_rules():
    """Group page has collapsible E156 format rules."""
    papers = _get_group_papers("methods-systems")
    html = make_group_page("methods-systems", papers, {})
    assert "<details>" in html
    assert "E156 Format Rules" in html


def test_group_page_has_download_js():
    """Group page includes downloadMd JavaScript function."""
    papers = _get_group_papers("geographic-equity")
    html = make_group_page("geographic-equity", papers[:2], {})
    assert "function downloadMd" in html


def test_group_page_has_group_color():
    """Group page uses the group accent colour."""
    papers = _get_group_papers("pakistan-deep-dive")
    html = make_group_page("pakistan-deep-dive", papers[:2], {})
    assert "#4a235a" in html


def test_group_page_no_external_cdn():
    """Group page has no external CDN links."""
    papers = _get_group_papers("geographic-equity")
    html = make_group_page("geographic-equity", papers[:2], {})
    assert "cdn." not in html.lower()
    assert "unpkg.com" not in html.lower()


def test_group_page_uses_body_data():
    """Group page renders body text from all_paper_data dict."""
    papers = _get_group_papers("geographic-equity")[:1]
    slug = papers[0]["slug"]
    data = {slug: {"body": "Specific test body text for validation."}}
    html = make_group_page("geographic-equity", papers, data)
    assert "Specific test body text for validation." in html


def test_group_page_all_five_groups():
    """Every group can produce a valid group page."""
    for gid in GROUPS:
        papers = _get_group_papers(gid)
        html = make_group_page(gid, papers[:1], {})
        assert "<!doctype html>" in html
        assert escape(GROUPS[gid]["name"]) in html


# ── Landing page tests ────────────────────────────────────

def test_landing_page_has_5_groups():
    """Landing page has all 5 group titles."""
    html = make_landing_page()
    for gid, ginfo in GROUPS.items():
        assert escape(ginfo["name"]) in html, f"Missing group: {ginfo['name']}"


def test_landing_page_valid_html():
    """Landing page has doctype and closing html tag."""
    html = make_landing_page()
    assert html.strip().startswith("<!doctype html>")
    assert "</html>" in html


def test_landing_page_mentions_190_papers():
    """Landing page references 190 papers."""
    html = make_landing_page()
    assert "190" in html


def test_landing_page_mentions_ziauddin():
    """Landing page references Ziauddin Medical University."""
    html = make_landing_page()
    assert "Ziauddin" in html


def test_landing_page_mentions_saarc():
    """Landing page references SAARC."""
    html = make_landing_page()
    assert "SAARC" in html


def test_landing_page_mentions_8_nations():
    """Landing page references 8 SAARC nations."""
    html = make_landing_page()
    assert "8 SAARC nations" in html


def test_landing_page_mentions_pakistan():
    """Landing page references Pakistan emphasis."""
    html = make_landing_page()
    assert "Pakistan" in html


def test_landing_page_has_group_links():
    """Landing page has links to each group index."""
    html = make_landing_page()
    for gid in GROUPS:
        assert f'{gid}/index.html' in html


def test_landing_page_has_github_link():
    """Landing page has a GitHub repository link."""
    html = make_landing_page()
    assert "github.com" in html.lower()


def test_landing_page_has_paper_counts():
    """Landing page shows paper count for each group."""
    html = make_landing_page()
    for gid, ginfo in GROUPS.items():
        expected = f'{ginfo["paper_count"]} papers'
        assert expected in html, f"Missing count for {gid}: {expected}"


def test_landing_page_responsive_grid():
    """Landing page uses responsive grid CSS."""
    html = make_landing_page()
    assert "repeat(auto-fit, minmax(280px, 1fr))" in html


def test_landing_page_hover_effect():
    """Landing page group cards have hover transform."""
    html = make_landing_page()
    assert "translateY(-4px)" in html


def test_landing_page_group_card_borders():
    """Each group card has a coloured top border."""
    html = make_landing_page()
    assert "border-top:4px solid" in html
