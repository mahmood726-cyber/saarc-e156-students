"""Tests for build.py — master build orchestrator."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def test_build_imports():
    """build module imports ok."""
    import build
    assert hasattr(build, "compute_stats")
    assert hasattr(build, "build_paper")
    assert hasattr(build, "build_group")
    assert hasattr(build, "build_all")
    assert hasattr(build, "main")
    assert hasattr(build, "STAT_FUNCTIONS")
    assert hasattr(build, "GROUP_DIRS")
    assert hasattr(build, "OUT")


def test_build_has_group_dirs():
    """GROUP_DIRS has 5 groups."""
    import build
    assert len(build.GROUP_DIRS) == 5
    expected = {
        "geographic-equity",
        "health-disease",
        "governance-justice",
        "methods-systems",
        "pakistan-deep-dive",
    }
    assert set(build.GROUP_DIRS.keys()) == expected


def test_build_output_path():
    """OUT contains 'saarc-e156-students'."""
    import build
    assert "saarc-e156-students" in str(build.OUT)
    assert isinstance(build.OUT, Path)


def test_compute_stats_basic():
    """compute_stats returns dict with expected keys for a simple paper."""
    import build

    # Minimal paper definition
    paper_def = {
        "slug": "test-paper",
        "stats": ["gini_coefficient", "shannon_entropy"],
    }
    # Minimal data dict
    data = {
        "country_counts": {
            "India": 5000,
            "Pakistan": 500,
            "Bangladesh": 300,
            "Sri Lanka": 200,
            "Nepal": 100,
            "Afghanistan": 50,
            "Bhutan": 5,
            "Maldives": 2,
        },
        "saarc_total": 6157,
        "metrics": {},
    }

    results = build.compute_stats(paper_def, data)
    assert isinstance(results, dict)
    assert "gini_coefficient" in results
    assert "shannon_entropy" in results
    # Each result should be a dict (from stats_library)
    assert isinstance(results["gini_coefficient"], dict)
    assert isinstance(results["shannon_entropy"], dict)


def test_stat_functions_all_present():
    """All 21 stat names used in the manifest are in STAT_FUNCTIONS."""
    import build
    from lib.paper_manifest import PAPERS

    # Collect all stat names from the manifest
    manifest_stats = set()
    for p in PAPERS:
        for s in p.get("stats", []):
            manifest_stats.add(s)

    assert len(manifest_stats) == 21, f"Expected 21 stat names, got {len(manifest_stats)}"

    missing = manifest_stats - set(build.STAT_FUNCTIONS.keys())
    assert len(missing) == 0, f"Missing stats in STAT_FUNCTIONS: {missing}"
