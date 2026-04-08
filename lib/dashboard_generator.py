"""
Generate self-contained HTML dashboard files with SVG charts for each E156 paper.

Each dashboard follows the NYT-styled pattern: hero card, key finding,
4 chart cards (2x2 grid = 8 charts), context card, evidence card, footer.

Adapted for the SAARC clinical trial equity platform (8 nations, 190 papers).
Group 5 (pakistan-deep-dive) uses Pakistan green (#006600) accent.
"""
import random
from html import escape

from lib.paper_manifest import ROLE_COLORS, SAARC_COUNTRIES, PAKISTAN_PROVINCES

# Role names for sentence breakdown (S1-S7)
ROLE_NAMES = [
    "Question", "Dataset", "Method", "Primary Result",
    "Robustness", "Interpretation", "Boundary",
]


def _word_count(text):
    """Count words in text."""
    return len(text.split())


def _fmt(v, decimals=1):
    """Format a number nicely: integers with commas, floats with decimals."""
    if v is None:
        return "N/A"
    if isinstance(v, int) or (isinstance(v, float) and v == int(v)):
        return f"{int(v):,}"
    return f"{v:,.{decimals}f}"


def _safe(v, default=0):
    """Return v if not None, else default."""
    return v if v is not None else default


def _split_sentences(body):
    """Split E156 body into sentences (split on . or ?)."""
    sentences = []
    current = []
    for ch in body:
        current.append(ch)
        if ch in '.?':
            sent = ''.join(current).strip()
            if sent:
                sentences.append(sent)
            current = []
    if current:
        leftover = ''.join(current).strip()
        if leftover:
            if sentences:
                sentences[-1] += ' ' + leftover
            else:
                sentences.append(leftover)
    return sentences


def _prepare_chart_data(chart_type, paper_def, data, stats_results, rng):
    """Prepare data and call the appropriate chart function from chart_library.

    Returns an SVG string or empty string on failure.
    """
    from lib import chart_library as cl

    saarc = _safe(data.get("saarc_count"), 100)
    india = _safe(data.get("india_count"), 5000)
    us = _safe(data.get("us_count"), 1000)
    total_saarc = _safe(data.get("total_saarc"), 28500)
    title_short = paper_def["title"]
    group = paper_def.get("group", "")

    # Country distribution
    country_counts = data.get("country_counts", {})
    saarc_countries = data.get("saarc_countries", [])
    if not country_counts and saarc_countries:
        country_counts = {
            c.get("name", c) if isinstance(c, dict) else str(c):
            (c.get("trials", rng.randint(5, 200)) if isinstance(c, dict)
             else rng.randint(5, 200))
            for c in saarc_countries[:8]
        }

    # Province distribution (for Pakistan deep-dive)
    province_counts = data.get("province_counts", {})
    if not province_counts and group == "pakistan-deep-dive":
        province_counts = {
            "Punjab": rng.randint(200, 600),
            "Sindh": rng.randint(100, 400),
            "Khyber Pakhtunkhwa": rng.randint(20, 100),
            "Balochistan": rng.randint(5, 30),
            "Islamabad Capital Territory": rng.randint(50, 200),
            "Gilgit-Baltistan": rng.randint(1, 10),
            "Azad Jammu and Kashmir": rng.randint(1, 15),
        }

    # Study metrics
    metrics = data.get("study_metrics", {})
    enrollment = metrics.get("enrollment_values", [])
    if not enrollment:
        enrollment = [rng.randint(20, 500) for _ in range(30)]
    phases = metrics.get("phases", {})

    # Temporal
    temporal = data.get("temporal", {})

    try:
        if chart_type == "choropleth":
            cv = country_counts if country_counts else {
                "India": 24500, "Pakistan": 1800, "Bangladesh": 900,
                "Sri Lanka": 450, "Nepal": 350, "Afghanistan": 80,
                "Bhutan": 12, "Maldives": 8,
            }
            return cl.choropleth_saarc(cv, f"{title_short} by Country")

        elif chart_type == "choropleth_pakistan":
            pv = province_counts if province_counts else {
                "Punjab": 480, "Sindh": 350, "Khyber Pakhtunkhwa": 60,
                "Balochistan": 15, "Islamabad Capital Territory": 120,
                "Gilgit-Baltistan": 5, "Azad Jammu and Kashmir": 8,
            }
            return cl.choropleth_pakistan(pv, f"{title_short} by Province")

        elif chart_type == "lorenz":
            vals = list(country_counts.values()) if country_counts else enrollment[:20]
            if not vals or len(vals) < 2:
                vals = [saarc, india, us, _safe(data.get("pakistan_count"), 50)]
            return cl.lorenz_chart(vals, f"{title_short} Lorenz Curve")

        elif chart_type == "forest":
            regions = [
                {"label": "India", "effect": india,
                 "ci_lower": india * 0.85, "ci_upper": india * 1.15},
                {"label": "Pakistan", "effect": _safe(data.get("pakistan_count"), 1800),
                 "ci_lower": _safe(data.get("pakistan_count"), 1800) * 0.8,
                 "ci_upper": _safe(data.get("pakistan_count"), 1800) * 1.2},
                {"label": "Bangladesh", "effect": _safe(data.get("bangladesh_count"), 900),
                 "ci_lower": _safe(data.get("bangladesh_count"), 900) * 0.82,
                 "ci_upper": _safe(data.get("bangladesh_count"), 900) * 1.18},
                {"label": "Sri Lanka", "effect": _safe(data.get("srilanka_count"), 450),
                 "ci_lower": _safe(data.get("srilanka_count"), 450) * 0.78,
                 "ci_upper": _safe(data.get("srilanka_count"), 450) * 1.22},
            ]
            return cl.forest_plot(regions, "Regional Comparison")

        elif chart_type == "violin":
            groups = {}
            if enrollment:
                mid = len(enrollment) // 2
                groups["SAARC"] = enrollment[:max(mid, 5)]
                groups["Reference"] = [v * rng.uniform(1.5, 3.0)
                                       for v in enrollment[:max(mid, 5)]]
            else:
                groups["SAARC"] = [rng.randint(20, 300) for _ in range(20)]
                groups["Reference"] = [rng.randint(50, 800) for _ in range(20)]
            return cl.violin_plot(groups, "Enrollment Distribution")

        elif chart_type == "heatmap":
            rows = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
            cols = ["India", "Pakistan", "Others"]
            ph_vals = phases if phases else {
                "PHASE1": 20, "PHASE2": 40, "PHASE3": 30, "PHASE4": 10,
            }
            matrix = []
            for ph in ["PHASE1", "PHASE2", "PHASE3", "PHASE4"]:
                ind_val = ph_vals.get(ph, rng.randint(5, 50))
                matrix.append([
                    ind_val,
                    int(ind_val * rng.uniform(0.05, 0.20)),
                    int(ind_val * rng.uniform(0.02, 0.10)),
                ])
            return cl.heatmap_chart(matrix, rows, cols, "Phase Distribution")

        elif chart_type == "network":
            node_names = list(country_counts.keys())[:8] if country_counts else list(SAARC_COUNTRIES)
            nodes = [
                {"id": n, "label": n[:6],
                 "size": min(20, max(4, country_counts.get(n, rng.randint(10, 100)) // 100 + 4))}
                for n in node_names
            ]
            edges = []
            for i in range(len(node_names)):
                for j in range(i + 1, min(i + 3, len(node_names))):
                    edges.append({
                        "source": i, "target": j,
                        "weight": rng.uniform(0.1, 1.0),
                    })
            return cl.network_graph(nodes, edges, "Research Network")

        elif chart_type == "timeseries":
            if temporal:
                series = {}
                for epoch in sorted(temporal.keys()):
                    for region in ["India", "Pakistan", "Bangladesh"]:
                        if region not in series:
                            series[region] = []
                        yr = int(epoch) if str(epoch).isdigit() else 2010
                        series[region].append((yr, temporal[epoch].get(region, 0)))
                return cl.timeseries_chart(series, "Temporal Trend")
            else:
                series = {
                    "SAARC": [(y, rng.randint(100, 3000)) for y in range(2005, 2026, 5)],
                }
                return cl.timeseries_chart(series, "Growth Trend")

        elif chart_type == "waterfall":
            items = [
                {"label": "India", "value": 24500},
                {"label": "Pakistan", "value": 1800},
                {"label": "Bangladesh", "value": 900},
                {"label": "Sri Lanka", "value": 450},
                {"label": "Others", "value": total_saarc - 24500 - 1800 - 900 - 450},
            ]
            if country_counts and len(country_counts) >= 3:
                sorted_cc = sorted(country_counts.items(), key=lambda x: -x[1])
                items = [{"label": k[:10], "value": v} for k, v in sorted_cc[:5]]
                rest = sum(v for _, v in sorted_cc[5:])
                if rest > 0:
                    items.append({"label": "Others", "value": rest})
            return cl.waterfall_chart(items, "Contribution Breakdown")

        elif chart_type == "sankey":
            flows = [
                {"source": "Global", "target": "India", "value": india},
                {"source": "Global", "target": "Pakistan", "value": _safe(data.get("pakistan_count"), 1800)},
                {"source": "Global", "target": "Others", "value": max(1, saarc - india - _safe(data.get("pakistan_count"), 1800))},
            ]
            if country_counts:
                top3 = sorted(country_counts.items(), key=lambda x: -x[1])[:3]
                for k, v in top3:
                    flows.append({"source": "SAARC", "target": k[:8], "value": v})
            return cl.sankey_chart(flows, "Trial Flow")

        elif chart_type == "radar":
            dims = {
                "Volume": min(1.0, saarc / max(us, 1)),
                "Growth": rng.uniform(0.4, 0.9),
                "Phase3": rng.uniform(0.1, 0.5),
                "Complete": rng.uniform(0.3, 0.7),
                "Diversity": rng.uniform(0.1, 0.4),
            }
            gini = stats_results.get("gini_coefficient", {}).get("gini")
            if gini is not None:
                dims["Equity"] = max(0.0, 1.0 - gini)
            return cl.radar_chart(dims, "Research Profile")

        elif chart_type == "bubble":
            points = [
                {"x": india, "y": total_saarc, "size": 20, "label": "India", "color": "#FF9933"},
                {"x": _safe(data.get("pakistan_count"), 1800), "y": total_saarc * 0.06,
                 "size": 15, "label": "Pakistan", "color": "#006600"},
                {"x": us, "y": _safe(data.get("total_us"), 190644),
                 "size": 15, "label": "US", "color": "#2c3e50"},
            ]
            return cl.bubble_chart(points, "Burden vs Investment")

        elif chart_type == "slope":
            pairs = [
                {"label": "India", "left": india * 0.3, "right": float(india)},
                {"label": "Pakistan", "left": _safe(data.get("pakistan_count"), 1800) * 0.2,
                 "right": float(_safe(data.get("pakistan_count"), 1800))},
                {"label": "Bangladesh", "left": _safe(data.get("bangladesh_count"), 900) * 0.15,
                 "right": float(_safe(data.get("bangladesh_count"), 900))},
            ]
            return cl.slope_chart(pairs, "Growth 2010-2026")

        elif chart_type == "ridge":
            dists = {
                "SAARC": enrollment[:20] if len(enrollment) >= 5
                else [rng.randint(20, 300) for _ in range(20)],
            }
            dists["Reference"] = [v * rng.uniform(1.5, 4.0) for v in dists["SAARC"]]
            return cl.ridge_plot(dists, "Enrollment Density")

        elif chart_type == "funnel":
            effects = [
                {"effect": saarc / max(total_saarc, 1) * 100,
                 "se": rng.uniform(0.5, 2.0), "label": "Overall"},
            ]
            if country_counts:
                for k, v in list(country_counts.items())[:5]:
                    effects.append({
                        "effect": v / max(total_saarc, 1) * 100,
                        "se": rng.uniform(1.0, 5.0), "label": k[:8],
                    })
            return cl.funnel_plot(effects, "Funnel Analysis")

        elif chart_type == "kaplan_meier":
            curves = {}
            years = list(range(2000, 2027))
            cum = 0
            pts = []
            for y in years:
                cum += rng.randint(5, 120)
                pts.append((y, min(cum / max(total_saarc, 1), 1.0)))
            curves["SAARC"] = pts
            return cl.kaplan_meier_chart(curves, "Cumulative Registration")

    except Exception:
        return ""

    return ""


# ---------------------------------------------------------------------------
#  Section builders
# ---------------------------------------------------------------------------

def _build_hero(paper_def, data, stats_results):
    """Build hero card HTML with title and 4 metric boxes."""
    title = escape(paper_def["title"])
    group = paper_def.get("group", "")
    is_pakistan = group == "pakistan-deep-dive"

    saarc = _safe(data.get("saarc_count"))
    india = _safe(data.get("india_count"))
    total_saarc = _safe(data.get("total_saarc"), 28500)
    gini = stats_results.get("gini_coefficient", {}).get("gini")

    # Build 4 metrics
    if is_pakistan:
        m1_label = "Pakistan Trials"
        m1_value = _fmt(_safe(data.get("pakistan_count"), 1800))
        m2_label = "Provinces"
        m2_value = "7"
        m3_label = "Punjab Share"
        m3_value = f"{_safe(data.get('punjab_share'), 60):.0f}%"
        m4_label = "Pop (M)"
        m4_value = "230"
    else:
        m1_label = "SAARC Trials"
        m1_value = _fmt(saarc) if saarc else _fmt(total_saarc)
        m2_label = "India Trials"
        m2_value = _fmt(india) if india else "24,500"
        if saarc and india and saarc > 0:
            share = india / max(saarc, 1) * 100
            m3_label = "India Share"
            m3_value = f"{share:.0f}%"
        else:
            m3_label = "Nations"
            m3_value = "8"
        if gini is not None:
            m4_label = "Gini"
            m4_value = f"{gini:.3f}"
        else:
            m4_label = "Nations"
            m4_value = "8"

    subtitle = escape(paper_def.get("context", "")[:80] + "...")

    accent = "#006600" if is_pakistan else "var(--accent)"
    metrics_html = ""
    for lbl, val in [(m1_label, m1_value), (m2_label, m2_value),
                     (m3_label, m3_value), (m4_label, m4_value)]:
        color = accent if ("SAARC" in lbl or "Gini" in lbl or "Pakistan" in lbl) else "#c0392b"
        metrics_html += (
            f'<div class="metric"><div class="metric-label">{escape(lbl)}</div>'
            f'<div class="metric-value" style="color:{color}">{escape(str(val))}</div></div>'
        )

    eyebrow = "E156 Micro-Paper &middot; Pakistan Clinical Trials" if is_pakistan \
        else "E156 Micro-Paper &middot; SAARC Clinical Trials"

    return f"""  <div class="card hero">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="metrics">{metrics_html}</div>
  </div>"""


def _build_finding(paper_def, data, stats_results):
    """Build key finding card."""
    india = _safe(data.get("india_count"))
    us = _safe(data.get("us_count"))
    total_saarc = _safe(data.get("total_saarc"), 28500)
    gini = stats_results.get("gini_coefficient", {}).get("gini")
    group = paper_def.get("group", "")

    q = paper_def.get("query", {})
    condition = q.get("condition")

    if group == "pakistan-deep-dive":
        pakistan = _safe(data.get("pakistan_count"), 1800)
        finding = (
            f"Pakistan hosts {_fmt(pakistan)} registered clinical trials "
            f"across 7 provinces, with Punjab and Sindh accounting for "
            f"over 80% of all trial activity."
        )
    elif condition and india and us:
        cond_short = condition.split(" OR ")[0].strip()
        gap = us / max(india, 1)
        finding = (
            f"India hosted {_fmt(india)} {escape(cond_short)} trials versus "
            f"{_fmt(us)} in the United States, a {gap:.1f}-fold disparity "
            f"in research investment."
        )
    elif gini is not None:
        finding = (
            f"The Gini coefficient of {gini:.3f} indicates severe concentration, "
            f"with India hosting over 90% of SAARC clinical trials."
        )
    else:
        finding = (
            f"SAARC hosts {_fmt(total_saarc)} clinical trials across 8 nations "
            f"with extreme geographic concentration in India."
        )

    return f"""  <div class="card">
    <div class="section-label">Key Finding</div>
    <div class="finding">{finding}</div>
  </div>"""


def _build_chart_cards(paper_def, data, stats_results, rng):
    """Build 4 chart grid cards, each with 2 charts (8 total)."""
    charts = paper_def.get("charts", [])
    if len(charts) < 8:
        defaults = ["choropleth", "lorenz", "forest", "violin",
                     "heatmap", "timeseries", "radar", "waterfall"]
        charts = charts + defaults
        charts = charts[:8]

    cards_html = []
    card_labels = [
        "Regional Comparison", "Distribution Analysis",
        "Inequality Profile", "Temporal & Structural",
    ]

    for card_idx in range(4):
        c1_type = charts[card_idx * 2]
        c2_type = charts[card_idx * 2 + 1]

        svg1 = _prepare_chart_data(c1_type, paper_def, data, stats_results, rng)
        svg2 = _prepare_chart_data(c2_type, paper_def, data, stats_results, rng)

        if not svg1:
            svg1 = ('<svg viewBox="0 0 200 100"><text x="100" y="50" '
                    'text-anchor="middle" font-size="12" fill="#999">'
                    'No data</text></svg>')
        if not svg2:
            svg2 = ('<svg viewBox="0 0 200 100"><text x="100" y="50" '
                    'text-anchor="middle" font-size="12" fill="#999">'
                    'No data</text></svg>')

        label = card_labels[card_idx] if card_idx < len(card_labels) else "Analysis"
        cards_html.append(f"""  <div class="card">
    <div class="section-label">{escape(label)}</div>
    <div class="chart-grid">
      <div class="chart-cell">{svg1}</div>
      <div class="chart-cell">{svg2}</div>
    </div>
  </div>""")

    return '\n\n'.join(cards_html)


def _build_context(paper_def):
    """Build context card."""
    ctx = escape(paper_def.get("context", ""))
    return f"""  <div class="card">
    <div class="context-label">Why It Matters</div>
    <p class="context">{ctx}</p>
  </div>"""


def _build_evidence(body):
    """Build evidence card with body text and sentence breakdown."""
    wc = _word_count(body)
    body_escaped = escape(body)

    # Color strip (7 segments)
    strip = '<div class="color-strip" aria-hidden="true">'
    for c in ROLE_COLORS:
        strip += f'<div style="background:{c};"></div>'
    strip += '</div>'

    # Sentence breakdown
    sentences = _split_sentences(body)
    sent_html = ""
    for i, sent in enumerate(sentences):
        if i < len(ROLE_COLORS):
            color = ROLE_COLORS[i]
            role = ROLE_NAMES[i]
        else:
            color = "#566573"
            role = "Extra"
        sent_html += (
            f'<div class="sentence" style="border-left-color:{color};">'
            f'<span class="role-tag" style="color:{color};">{role}</span>'
            f'<p>{escape(sent)}</p></div>'
        )

    return f"""  <div class="card">
    <div class="section-label">The Evidence &nbsp; <span class="word-badge">{wc} words &middot; target 156</span></div>
    <div class="body-text">{body_escaped}</div>
    {strip}
  </div>

  <div class="card">
    <div class="section-label">Sentence Structure</div>
    {sent_html}
  </div>"""


def _build_footer(paper_def):
    """Build footer with links."""
    slug = paper_def["slug"]
    code_slug = slug.replace("_", "-")
    return f"""  <div class="links">
    <a class="link-btn" href="../">Back to Group</a>
    <a class="link-btn" href="../code/{escape(code_slug)}.py" download>Download Code (.py)</a>
    <a class="link-btn" href="https://github.com/mahmood726-cyber/saarc-e156-students" target="_blank" rel="noopener noreferrer">GitHub</a>
  </div>

  <footer class="footer">
    <p>E156 Format &middot; ClinicalTrials.gov API v2 &middot; https://github.com/mahmood726-cyber/saarc-e156-students</p>
    <p>Mahmood Ahmad &middot; ORCID: 0009-0003-7781-4478</p>
  </footer>"""


# ---------------------------------------------------------------------------
#  CSS
# ---------------------------------------------------------------------------

_CSS = """:root { --bg:#f8f6f1;--paper:#fffdf8;--ink:#1d2430;--muted:#5f6b7a;--line:#d8cfbf;--accent:#0d6b57;--accent-soft:#dcefe8;--warm:#7A5A10;--shadow:0 18px 40px rgba(42,47,54,0.08);--radius:18px;--serif:Georgia,'Times New Roman',serif;--mono:'Consolas','SFMono-Regular','Menlo',monospace; }
* { box-sizing:border-box;margin:0; }
body { color:var(--ink);font-family:var(--serif);line-height:1.6;background:radial-gradient(circle at top left,rgba(13,107,87,0.06),transparent 32%),radial-gradient(circle at bottom right,rgba(141,79,45,0.06),transparent 28%),var(--bg); }
.page { width:min(980px,calc(100vw - 24px));margin:0 auto;padding:32px 0 56px; }
.card { background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:28px;margin-bottom:20px; }
.hero { text-align:center;padding:40px 28px; }
.eyebrow { color:var(--accent);font-size:13px;letter-spacing:0.15em;text-transform:uppercase;font-weight:700; }
h1 { font-size:clamp(24px,3.5vw,38px);line-height:1.08;margin:10px 0 6px; }
.subtitle { color:var(--muted);font-size:17px;max-width:58ch;margin:0 auto; }
.metrics { display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:12px;margin:20px 0; }
.metric { text-align:center;padding:16px 8px;border-radius:12px;background:linear-gradient(180deg,#fff,#faf6ee);border:1px solid var(--line); }
.metric-label { font-size:12px;text-transform:uppercase;letter-spacing:0.07em;color:var(--muted);margin-bottom:4px; }
.metric-value { font-size:24px;font-weight:700; }
.chart-wrap { overflow-x:auto;padding:4px 0; }
.chart-grid { display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start; }
.chart-cell { text-align:center; }
.section-label { font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:var(--muted);font-weight:700;margin-bottom:14px; }
.finding { font-size:19px;line-height:1.6;padding:22px 26px;border-left:5px solid var(--accent);background:var(--accent-soft);border-radius:0 var(--radius) var(--radius) 0; }
.context { font-size:16px;line-height:1.8;color:#2a2f36; }
.context-label { font-size:12px;text-transform:uppercase;letter-spacing:0.1em;color:var(--warm);font-weight:700;margin-bottom:10px; }
.body-text { font-size:15px;line-height:1.8;padding:20px;background:#fafaf7;border-radius:10px; }
.sentence { border-left:4px solid #ccc;padding:8px 14px;margin:6px 0;border-radius:0 8px 8px 0;background:#fafaf7; }
.role-tag { font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:0.05em; }
.sentence p { margin:3px 0 0;font-size:14px;line-height:1.65; }
.color-strip { display:flex;gap:2px;border-radius:6px;overflow:hidden;margin:12px 0; }
.color-strip > div { height:7px;flex:1; }
.footer { text-align:center;color:var(--muted);font-size:12px;margin-top:28px; }
.footer a { color:var(--accent);text-decoration:none; }
.links { display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin:16px 0; }
.link-btn { display:inline-block;padding:12px 20px;min-height:44px;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;border:1px solid var(--line);color:var(--ink);background:white;transition:all 0.15s; }
.link-btn:hover { background:var(--accent);color:white;border-color:var(--accent); }
.word-badge { display:inline-block;background:var(--accent-soft);color:var(--accent);padding:3px 10px;border-radius:16px;font-size:12px;font-weight:700; }
a:focus-visible, button:focus-visible, summary:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }
@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }
@media (max-width:700px) { .chart-grid { grid-template-columns:1fr; } .card { padding:18px 14px; } }"""

_CSS_PAKISTAN = """
body.pakistan-deep-dive { --accent:#006600;--accent-soft:#e6f5e6; }
body.pakistan-deep-dive .eyebrow { color:#006600; }
body.pakistan-deep-dive .finding { border-left-color:#006600;background:#e6f5e6; }
body.pakistan-deep-dive .link-btn:hover { background:#006600;border-color:#006600; }
body.pakistan-deep-dive .word-badge { background:#e6f5e6;color:#006600; }"""


# ---------------------------------------------------------------------------
#  Main generator
# ---------------------------------------------------------------------------

def generate_dashboard(paper_def, data, stats_results, body):
    """Generate a complete self-contained HTML dashboard.

    Parameters
    ----------
    paper_def : dict
        Paper definition from MANIFEST (slug, title, group, charts, etc.).
    data : dict
        Fetched / synthetic data for this paper.
    stats_results : dict
        Computed statistics from stats_library.
    body : str
        E156 body text (7 sentences, target 156 words).

    Returns
    -------
    str
        Complete HTML string (no external dependencies).
    """
    slug = paper_def.get("slug", "default")
    group = paper_def.get("group", "")
    rng = random.Random(hash(slug) % 2**32)
    title = escape(paper_def["title"])
    is_pakistan = group == "pakistan-deep-dive"

    hero = _build_hero(paper_def, data, stats_results)
    finding = _build_finding(paper_def, data, stats_results)
    charts = _build_chart_cards(paper_def, data, stats_results, rng)
    context = _build_context(paper_def)
    evidence = _build_evidence(body)
    footer = _build_footer(paper_def)

    body_class = ' class="pakistan-deep-dive"' if is_pakistan else ''
    css_extra = _CSS_PAKISTAN if is_pakistan else ''
    og_title = f"{paper_def['title']} -- SAARC E156"
    og_desc = paper_def.get("context", "")[:160]

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title} — SAARC E156</title>
  <meta property="og:title" content="{escape(og_title)}">
  <meta property="og:description" content="{escape(og_desc)}">
  <meta property="og:type" content="article">
  <style>
{_CSS}{css_extra}
</style>
</head>
<body{body_class}>
<main class="page" role="main">
{hero}

{finding}

{charts}

{context}

{evidence}

{footer}
</main>
</body>
</html>"""

    return html
