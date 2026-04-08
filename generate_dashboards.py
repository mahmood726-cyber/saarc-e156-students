"""Regenerate all 190 HTML dashboards from cached data."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.paper_manifest import PAPERS
from lib.data_fetcher import _read_cache
from lib.body_generator import generate_body
from lib.dashboard_generator import generate_dashboard
from build import compute_stats, GROUP_DIRS

def main():
    count = 0
    for paper_def in PAPERS:
        slug = paper_def["slug"]
        data = _read_cache(slug)
        if not data:
            print(f"SKIP (no cache): {slug}")
            continue
        stats = compute_stats(paper_def, data)
        body = generate_body(paper_def, data, stats)
        html = generate_dashboard(paper_def, data, stats, body)
        group_dir = GROUP_DIRS[paper_def["group"]]
        path = group_dir / "dashboards" / f"{slug}.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        count += 1
        print(f"[{count:>3}] {slug}")
    print(f"\nDone: {count} dashboards regenerated")

if __name__ == "__main__":
    main()
