#!/usr/bin/env python3
"""
Build orchestrator for 190 SAARC E156 Student Papers.

Pipeline: fetch data -> compute stats -> generate bodies ->
          generate dashboards -> generate code scripts -> assemble pages.

All heavy lifting lives in lib/; this script coordinates.
"""

import argparse
import sys
from pathlib import Path

# ── Project imports ──
sys.path.insert(0, str(Path(__file__).resolve().parent))

from lib.paper_manifest import PAPERS, GROUPS
from lib.data_fetcher import fetch_paper_data
import lib.stats_library as sl
from lib.body_generator import generate_body
from lib.dashboard_generator import generate_dashboard
from lib.code_generator import generate_code_script

# index_updater may still be under construction — import defensively
try:
    from lib.index_updater import make_paper_card, make_group_page, make_landing_page
    HAS_INDEX_UPDATER = True
except ImportError:
    HAS_INDEX_UPDATER = False

# ═══════════════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════════════

OUT = Path("C:/saarc-e156-students")
GITHUB_PAGES = "https://mahmood789.github.io/saarc-e156-students"

GROUP_DIRS = {
    "geographic-equity": OUT / "geographic-equity",
    "health-disease": OUT / "health-disease",
    "governance-justice": OUT / "governance-justice",
    "methods-systems": OUT / "methods-systems",
    "pakistan-deep-dive": OUT / "pakistan-deep-dive",
}


# ═══════════════════════════════════════════════════════════
#  SAARC adjacency matrix (8 countries, border-sharing)
# ═══════════════════════════════════════════════════════════

def _saarc_adjacency():
    """Return 8x8 adjacency matrix for SAARC border-sharing.

    Order: India, Pakistan, Bangladesh, Sri Lanka,
           Nepal, Afghanistan, Bhutan, Maldives.

    Adjacency = 1 if countries share a land border (or very close maritime).
    Sri Lanka and Maldives are islands — Sri Lanka is close to India (Palk Strait),
    Maldives has no land neighbour.
    """
    # I=0, PK=1, BD=2, LK=3, NP=4, AF=5, BT=6, MV=7
    return [
        # I   PK  BD  LK  NP  AF  BT  MV
        [0, 1, 1, 1, 1, 0, 1, 0],  # India
        [1, 0, 0, 0, 0, 1, 0, 0],  # Pakistan
        [1, 0, 0, 0, 0, 0, 0, 0],  # Bangladesh
        [1, 0, 0, 0, 0, 0, 0, 0],  # Sri Lanka
        [1, 0, 0, 0, 0, 0, 1, 0],  # Nepal
        [0, 1, 0, 0, 0, 0, 0, 0],  # Afghanistan
        [1, 0, 0, 0, 1, 0, 0, 0],  # Bhutan
        [0, 0, 0, 0, 0, 0, 0, 0],  # Maldives
    ]


# ═══════════════════════════════════════════════════════════
#  Wrapper helpers for stats that need data reshaping
# ═══════════════════════════════════════════════════════════

def _permutation_wrapper(data):
    """Split country counts into high/low halves for permutation test."""
    vals = sorted(data.get("country_counts", {}).values())
    mid = len(vals) // 2
    group1 = vals[:mid] if mid > 0 else [0]
    group2 = vals[mid:] if mid < len(vals) else [0]
    return sl.permutation_test(group1, group2, n_perm=1000, seed=42)


def _odds_ratio_wrapper(data):
    """Construct 2x2 table from country counts: high-trial vs low-trial countries."""
    counts = list(data.get("country_counts", {}).values())
    if len(counts) < 2:
        return sl.odds_ratio(1, 1, 1, 1)
    total = sum(counts) if sum(counts) > 0 else 1
    median_val = sorted(counts)[len(counts) // 2]
    a = sum(1 for c in counts if c > median_val)
    b = sum(1 for c in counts if c <= median_val)
    c = max(1, sum(c for c in counts if c > median_val))
    d = max(1, sum(c for c in counts if c <= median_val))
    return sl.odds_ratio(a, b, c, d)


def _cohens_d_wrapper(data):
    """Compare top-half vs bottom-half country trial counts."""
    vals = sorted(data.get("country_counts", {}).values())
    mid = len(vals) // 2
    group1 = vals[:mid] if mid > 0 else [0, 0]
    group2 = vals[mid:] if mid < len(vals) else [0, 0]
    # cohens_d needs at least 2 values per group
    if len(group1) < 2:
        group1 = group1 + [0]
    if len(group2) < 2:
        group2 = group2 + [0]
    return sl.cohens_d(group1, group2)


def _kl_wrapper(data):
    """KL divergence: observed distribution vs uniform."""
    vals = list(data.get("country_counts", {}).values())
    n = len(vals)
    if n == 0:
        return sl.kl_divergence([1], [1])
    total = sum(vals) if sum(vals) > 0 else 1
    p_vals = [v / total for v in vals]
    q_vals = [1.0 / n] * n
    return sl.kl_divergence(p_vals, q_vals)


# ═══════════════════════════════════════════════════════════
#  STAT_FUNCTIONS: maps stat names -> callables(data) -> dict
# ═══════════════════════════════════════════════════════════

STAT_FUNCTIONS = {
    "gini_coefficient": lambda data: sl.gini_coefficient(
        list(data["country_counts"].values())),
    "bootstrap_ci": lambda data: sl.bootstrap_ci(
        list(data["country_counts"].values()), seed=42),
    "shannon_entropy": lambda data: sl.shannon_entropy(
        list(data["country_counts"].values())),
    "hhi_index": lambda data: sl.herfindahl_hirschman_index(
        list(data["country_counts"].values())),
    "poisson_rate": lambda data: sl.poisson_rate(
        data.get("saarc_total", 0), 2_000_000_000),
    "rate_ratio": lambda data: sl.rate_ratio(
        data.get("country_counts", {}).get("Pakistan", 0), 220_000_000,
        data.get("country_counts", {}).get("India", 0), 1_400_000_000),
    "theil_index": lambda data: sl.theil_index(
        list(data["country_counts"].values())),
    "chi_squared": lambda data: sl.chi_squared(
        list(data["country_counts"].values()),
        [data.get("saarc_total", 1) / max(len(data.get("country_counts", {})), 1)]
        * len(data.get("country_counts", {}))),
    "bayesian_rate": lambda data: sl.bayesian_rate(
        data.get("saarc_total", 0), 500000),
    "morans_i": lambda data: sl.morans_i(
        list(data["country_counts"].values()), _saarc_adjacency()),
    "permutation_test": lambda data: _permutation_wrapper(data),
    "spearman_correlation": lambda data: sl.spearman_correlation(
        list(range(len(data["country_counts"]))),
        sorted(data["country_counts"].values())),
    "linear_regression": lambda data: sl.linear_regression(
        list(range(len(data["country_counts"]))),
        sorted(data["country_counts"].values())),
    "network_centrality": lambda data: sl.network_centrality(
        _saarc_adjacency()),
    "kaplan_meier_survival": lambda data: sl.kaplan_meier_survival(
        data.get("metrics", {}).get("start_years", [2020])),
    "odds_ratio": lambda data: _odds_ratio_wrapper(data),
    "cohens_d": lambda data: _cohens_d_wrapper(data),
    "kl_divergence": lambda data: _kl_wrapper(data),
    "concentration_index": lambda data: sl.concentration_index(
        list(data["country_counts"].values())),
    "lorenz_area": lambda data: sl.lorenz_area(
        list(data["country_counts"].values())),
    "atkinson_index": lambda data: sl.atkinson_index(
        list(data["country_counts"].values())),
}


# ═══════════════════════════════════════════════════════════
#  CORE BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════

def compute_stats(paper_def, data):
    """Run all assigned stats for a paper.

    Args:
        paper_def: dict from paper manifest (must have "stats" key).
        data: dict from fetch_paper_data (must have "country_counts" etc.).

    Returns:
        dict mapping stat_name -> result dict.
    """
    results = {}
    for stat_name in paper_def.get("stats", []):
        fn = STAT_FUNCTIONS.get(stat_name)
        if fn is None:
            results[stat_name] = {"error": f"Unknown stat: {stat_name}"}
            continue
        try:
            results[stat_name] = fn(data)
        except Exception as exc:
            results[stat_name] = {"error": str(exc)}
    return results


def build_paper(paper_def):
    """Build one paper: fetch data, compute stats, generate body, dashboard, code.

    Writes dashboard HTML and code .py to disk under the group directory.

    Returns:
        dict with keys: slug, group, body, dashboard_path, code_path, stats, ok.
    """
    slug = paper_def["slug"]
    group = paper_def["group"]
    group_dir = GROUP_DIRS.get(group, OUT / group)

    result = {
        "slug": slug,
        "group": group,
        "body": None,
        "dashboard_path": None,
        "code_path": None,
        "stats": {},
        "ok": False,
    }

    try:
        # 1. Fetch data
        data = fetch_paper_data(paper_def)

        # 2. Compute statistics
        stats_results = compute_stats(paper_def, data)
        result["stats"] = stats_results

        # 3. Generate E156 body
        body = generate_body(paper_def, data, stats_results)
        result["body"] = body

        # 4. Generate dashboard HTML
        dashboard_html = generate_dashboard(paper_def, data, stats_results, body)
        dash_dir = group_dir / "dashboards"
        dash_dir.mkdir(parents=True, exist_ok=True)
        dash_path = dash_dir / f"{slug}.html"
        dash_path.write_text(dashboard_html, encoding="utf-8")
        result["dashboard_path"] = str(dash_path)

        # 5. Generate code script
        code_text = generate_code_script(paper_def, data, stats_results)
        code_dir = group_dir / "code"
        code_dir.mkdir(parents=True, exist_ok=True)
        code_filename = slug.replace("_", "-") + ".py"
        code_path = code_dir / code_filename
        code_path.write_text(code_text, encoding="utf-8")
        result["code_path"] = str(code_path)

        result["ok"] = True

    except Exception as exc:
        result["error"] = str(exc)

    return result


def build_group(group_id):
    """Build all papers in a group, then generate group index page.

    Args:
        group_id: key from GROUPS dict (e.g. "geographic-equity").

    Returns:
        list of result dicts from build_paper.
    """
    group_papers = [p for p in PAPERS if p["group"] == group_id]
    results = []
    all_paper_data = {}

    print(f"\n--- Building group: {group_id} ({len(group_papers)} papers) ---")

    for i, paper_def in enumerate(group_papers, 1):
        slug = paper_def["slug"]
        print(f"  [{i}/{len(group_papers)}] {slug} ... ", end="", flush=True)
        r = build_paper(paper_def)
        results.append(r)
        all_paper_data[slug] = r
        status = "OK" if r["ok"] else f"FAIL: {r.get('error', '?')}"
        print(status)

    # Generate group index page if index_updater is available
    if HAS_INDEX_UPDATER:
        try:
            group_dir = GROUP_DIRS.get(group_id, OUT / group_id)
            group_dir.mkdir(parents=True, exist_ok=True)
            page_html = make_group_page(group_id, group_papers, all_paper_data)
            index_path = group_dir / "index.html"
            index_path.write_text(page_html, encoding="utf-8")
            print(f"  -> Group index: {index_path}")
        except Exception as exc:
            print(f"  -> Group index FAILED: {exc}")
    else:
        print("  -> Skipping group index (index_updater not available)")

    ok_count = sum(1 for r in results if r["ok"])
    print(f"  Summary: {ok_count}/{len(results)} papers built successfully")

    return results


def build_all():
    """Build all 5 groups + landing page. Print progress."""
    print("=" * 60)
    print("SAARC E156 Student Platform — Full Build")
    print(f"Output: {OUT}")
    print(f"Papers: {len(PAPERS)}")
    print(f"Groups: {len(GROUP_DIRS)}")
    print("=" * 60)

    all_results = []

    for group_id in GROUP_DIRS:
        results = build_group(group_id)
        all_results.extend(results)

    # Generate landing page
    if HAS_INDEX_UPDATER:
        try:
            landing_html = make_landing_page()
            landing_path = OUT / "index.html"
            landing_path.write_text(landing_html, encoding="utf-8")
            print(f"\nLanding page: {landing_path}")
        except Exception as exc:
            print(f"\nLanding page FAILED: {exc}")
    else:
        print("\nSkipping landing page (index_updater not available)")

    # Final summary
    total = len(all_results)
    ok = sum(1 for r in all_results if r["ok"])
    fail = total - ok
    print(f"\n{'=' * 60}")
    print(f"BUILD COMPLETE: {ok}/{total} papers OK, {fail} failures")
    print(f"{'=' * 60}")

    return all_results


# ═══════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════

def main():
    """CLI entry point with argparse."""
    parser = argparse.ArgumentParser(
        description="Build SAARC E156 student papers, dashboards, and code scripts."
    )
    parser.add_argument("--all", action="store_true",
                        help="Build all 5 groups + landing page")
    parser.add_argument("--group", type=str, metavar="GROUP_ID",
                        help="Build one group (e.g. geographic-equity)")
    parser.add_argument("--paper", type=str, metavar="SLUG",
                        help="Build one paper by slug")
    args = parser.parse_args()

    if args.paper:
        paper_def = next((p for p in PAPERS if p["slug"] == args.paper), None)
        if paper_def is None:
            print(f"ERROR: Paper slug '{args.paper}' not found in manifest.")
            sys.exit(1)
        print(f"Building paper: {args.paper}")
        r = build_paper(paper_def)
        if r["ok"]:
            print(f"  Body: {len(r['body'].split()) if r['body'] else 0} words")
            print(f"  Dashboard: {r['dashboard_path']}")
            print(f"  Code: {r['code_path']}")
        else:
            print(f"  FAILED: {r.get('error', '?')}")
            sys.exit(1)

    elif args.group:
        if args.group not in GROUP_DIRS:
            print(f"ERROR: Unknown group '{args.group}'.")
            print(f"  Valid groups: {', '.join(GROUP_DIRS.keys())}")
            sys.exit(1)
        build_group(args.group)

    elif args.all:
        build_all()

    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
