"""Regenerate all 190 E156 bodies from cached data."""
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from lib.paper_manifest import PAPERS
from lib.data_fetcher import _read_cache
from lib.body_generator import generate_body
from build import compute_stats

def main():
    count = 0
    bodies = {}
    for paper_def in PAPERS:
        slug = paper_def["slug"]
        data = _read_cache(slug)
        if not data:
            print(f"SKIP (no cache): {slug}")
            continue
        stats = compute_stats(paper_def, data)
        body = generate_body(paper_def, data, stats)
        bodies[slug] = body
        wc = len(body.split())
        count += 1
        print(f"[{count:>3}] {slug} ({wc}w)")
    with open("data_cache/all_bodies.json", "w", encoding="utf-8") as f:
        json.dump(bodies, f, indent=2)
    print(f"\nDone: {count} bodies generated, saved to data_cache/all_bodies.json")

if __name__ == "__main__":
    main()
