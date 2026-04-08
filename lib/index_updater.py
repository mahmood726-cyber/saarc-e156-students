"""
Assemble group index pages and the landing page HTML.

Handles:
- make_paper_card: single paper card HTML block
- make_group_page: complete HTML page for one group
- make_landing_page: root landing page with 5 group cards
"""
from html import escape

from lib.paper_manifest import GROUPS, ROLE_COLORS, PAPERS

# Group accent colours (not in manifest — defined here for page rendering)
GROUP_COLORS = {
    "geographic-equity": "#1b4f72",
    "health-disease": "#922b21",
    "governance-justice": "#7e5109",
    "methods-systems": "#0b5345",
    "pakistan-deep-dive": "#4a235a",
}

# Shared CSS root variables — NYT editorial palette
_CSS_VARS = """\
:root {
    --bg: #f8f6f1;
    --paper: #fffdf8;
    --ink: #1d2430;
    --muted: #5f6b7a;
    --line: #d8cfbf;
    --accent: #0d6b57;
    --serif: Georgia,'Times New Roman',serif;
    --mono: Consolas,SFMono-Regular,Menlo,monospace;
}"""

# ───────────────────────────────────────────────────────────
#  Shared CSS
# ───────────────────────────────────────────────────────────

_SHARED_CSS = f"""
{_CSS_VARS}
*, *::before, *::after {{ box-sizing: border-box; }}
body {{
    margin: 0; padding: 0;
    font-family: var(--serif);
    background: var(--bg);
    color: var(--ink);
    line-height: 1.6;
}}
.container {{ max-width: 960px; margin: 0 auto; padding: 2rem 1.5rem; }}
h1, h2, h3, h4 {{ margin-top: 0; }}
a {{ color: var(--accent); text-decoration: none; }}
a:hover {{ text-decoration: underline; }}

/* Paper card */
.paper-card {{
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 1.8rem;
    position: relative;
}}
.paper-card .num {{
    display: inline-block;
    width: 2rem; height: 2rem;
    line-height: 2rem;
    text-align: center;
    border-radius: 50%;
    background: var(--accent);
    color: #fff;
    font-size: 0.85rem;
    font-weight: 700;
    margin-right: 0.6rem;
    vertical-align: middle;
}}
.paper-card h3 {{
    display: inline; vertical-align: middle;
    font-size: 1.15rem;
}}
.sent-strip {{
    display: flex; gap: 2px;
    margin: 0.8rem 0;
    height: 8px; border-radius: 3px; overflow: hidden;
}}
.sent-strip .seg {{ flex: 1; }}
.paper-body {{
    font-size: 0.95rem;
    color: var(--ink);
    margin-bottom: 1rem;
}}
.actions {{
    display: flex; gap: 0.5rem; flex-wrap: wrap;
    margin-bottom: 1rem;
}}
.btn {{
    display: inline-block;
    padding: 0.4rem 1rem;
    border: 1px solid var(--line);
    border-radius: 4px;
    background: var(--paper);
    color: var(--ink);
    font-size: 0.85rem;
    cursor: pointer;
    font-family: var(--serif);
}}
.btn:hover {{ background: #f0ede5; text-decoration: none; }}
.refs {{ margin-bottom: 1rem; }}
.refs h4 {{ font-size: 0.9rem; margin-bottom: 0.3rem; }}
.refs ol {{ margin: 0; padding-left: 1.4rem; font-size: 0.85rem; color: var(--muted); }}
.note-block {{
    background: #f4f1ea;
    border-left: 3px solid var(--accent);
    padding: 0.6rem 1rem;
    font-size: 0.85rem;
    border-radius: 0 4px 4px 0;
}}
.note-block .row {{
    display: flex; gap: 0.4rem; padding: 0.15rem 0;
}}
.note-block .key {{
    font-weight: 700; min-width: 90px;
}}

/* Masthead */
.masthead {{
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
    border-bottom: 2px solid var(--line);
    margin-bottom: 2rem;
}}
.masthead h1 {{ font-size: 2rem; margin-bottom: 0.3rem; }}
.masthead p {{ color: var(--muted); font-size: 1.05rem; max-width: 640px; margin: 0 auto; }}

/* Instructions panel */
.instructions {{
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 1.5rem;
    margin-bottom: 2rem;
}}
.instructions h2 {{ font-size: 1.15rem; margin-bottom: 0.5rem; }}
.instructions ol {{ padding-left: 1.4rem; font-size: 0.95rem; }}
.instructions li {{ margin-bottom: 0.3rem; }}

/* E156 rules collapsible */
details {{
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 1rem 1.5rem;
    margin: 2rem 0;
}}
details summary {{
    cursor: pointer;
    font-weight: 700;
    font-size: 1rem;
}}
details ol {{ font-size: 0.9rem; padding-left: 1.4rem; }}
"""

# CSS specific to the landing page grid
_LANDING_CSS = """
.group-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}
.group-card {
    background: var(--paper);
    border: 1px solid var(--line);
    border-radius: 6px;
    padding: 1.5rem;
    transition: transform 0.2s, box-shadow 0.2s;
}
.group-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 6px 18px rgba(0,0,0,0.10);
}
.group-card h2 { font-size: 1.2rem; margin-bottom: 0.4rem; }
.group-card p { color: var(--muted); font-size: 0.92rem; margin-bottom: 0.8rem; }
.group-card .paper-count {
    font-weight: 700; font-size: 1.1rem; color: var(--ink);
}
footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--muted);
    font-size: 0.85rem;
    border-top: 1px solid var(--line);
    margin-top: 2rem;
}
"""


# ───────────────────────────────────────────────────────────
#  Helpers
# ───────────────────────────────────────────────────────────

_INSTRUCTIONS_HTML = """\
<div class="instructions">
  <h2>Student Workflow — Ziauddin Medical University</h2>
  <ol>
    <li>Read the AI-drafted abstract carefully (the grey body text).</li>
    <li>Open the interactive dashboard to explore charts and numbers.</li>
    <li>Download the Python code to reproduce the analysis yourself.</li>
    <li>Write your own 7-sentence, at-most-156-word E156 micro-paper.</li>
    <li>Compare your version against the AI draft — where do they diverge?</li>
    <li>Review the suggested references and add any you find relevant.</li>
    <li>Submit your final E156 via the course portal before the deadline.</li>
  </ol>
</div>"""

_E156_RULES_HTML = """\
<details>
  <summary>E156 Format Rules (click to expand)</summary>
  <ol>
    <li>Exactly 7 sentences (S1-S7), at most 156 words, single paragraph.</li>
    <li>No citations, links, or metadata inside the body text.</li>
    <li>S1 = Question (population, intervention, endpoint).</li>
    <li>S2 = Dataset (studies, participants, scope).</li>
    <li>S3 = Method (synthesis model, effect scale).</li>
    <li>S4 = Result (lead estimate + confidence interval).</li>
    <li>S5 = Robustness (heterogeneity, sensitivity).</li>
    <li>S6 = Interpretation (plain-language meaning).</li>
    <li>S7 = Boundary (main limitation).</li>
  </ol>
</details>"""

_DOWNLOAD_JS = """\
<script>
function downloadMd(slug, title) {
  var card = document.getElementById('paper-' + slug) ||
             event.target.closest('.paper-card');
  var body = card ? card.querySelector('.paper-body').textContent : '';
  var md = '# ' + (title || slug) + '\\n\\n' + body.trim() + '\\n';
  var blob = new Blob([md], {type: 'text/markdown'});
  var url = URL.createObjectURL(blob);
  var a = document.createElement('a');
  a.href = url; a.download = slug + '.md';
  document.body.appendChild(a); a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
<""" + """/script>"""


# ───────────────────────────────────────────────────────────
#  make_paper_card
# ───────────────────────────────────────────────────────────

def make_paper_card(paper_def, card_num, body):
    """Return HTML string for one paper card.

    Parameters
    ----------
    paper_def : dict
        Paper definition from PAPERS list (slug, title, stats, refs, ...).
    card_num : int
        Sequential number to display on the card badge.
    body : str
        The E156 body text (may be empty placeholder).
    """
    slug = paper_def["slug"]
    title = escape(paper_def["title"])
    refs = paper_def.get("refs", [])
    stats = paper_def.get("stats", [])
    first_stat = stats[0].replace("_", " ").title() if stats else "N/A"

    # Sentence role colour strip (7 segments)
    strip = '<div class="sent-strip">'
    for c in ROLE_COLORS:
        strip += f'<div class="seg" style="background:{c};" title=""></div>'
    strip += "</div>"

    # References
    refs_html = '<div class="refs"><h4>Suggested References</h4><ol>'
    for r in refs:
        refs_html += f"<li>{escape(r)}</li>"
    refs_html += "</ol></div>"

    body_escaped = escape(body) if body else "<em>Body text will appear after generation.</em>"

    return f"""\
<article class="paper-card" id="paper-{card_num}">
  <span class="num" aria-hidden="true">{card_num}</span>
  <h3>{title}</h3>
  {strip}
  <div class="paper-body">{body_escaped}</div>
  <div class="actions">
    <a href="dashboards/{escape(slug)}.html" class="btn">View Dashboard</a>
    <a href="code/{escape(slug)}.py" class="btn" download>Download Code</a>
    <button class="btn" onclick="downloadMd('{escape(slug)}','{title}')">Download Paper</button>
  </div>
  {refs_html}
  <div class="note-block">
    <div class="row"><span class="key">Estimand</span><span>{first_stat}</span></div>
    <div class="row"><span class="key">Data</span><span>ClinicalTrials.gov API v2</span></div>
    <div class="row"><span class="key">Certainty</span><span>LOW\u2013MODERATE</span></div>
  </div>
</article>"""


# ───────────────────────────────────────────────────────────
#  make_group_page
# ───────────────────────────────────────────────────────────

def make_group_page(group_id, papers, all_paper_data):
    """Return complete HTML page for a group.

    Parameters
    ----------
    group_id : str
        Key into GROUPS dict (e.g. 'geographic-equity').
    papers : list of dict
        Paper definitions belonging to this group.
    all_paper_data : dict
        Mapping {slug: {"body": str, ...}}. May be empty — cards use placeholder.
    """
    group = GROUPS[group_id]
    color = GROUP_COLORS.get(group_id, "#0d6b57")
    title = escape(group["name"])
    desc = escape(group["description"])
    count = len(papers)

    cards_html = ""
    for i, pdef in enumerate(papers):
        card_num = i + 1
        slug = pdef["slug"]
        body = all_paper_data.get(slug, {}).get("body", "")
        cards_html += make_paper_card(pdef, card_num, body) + "\n"

    return f"""\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — SAARC E156</title>
<meta property="og:title" content="{title} — SAARC Clinical Trial Equity">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<style>
{_SHARED_CSS}
.masthead {{ border-bottom-color: {color}; }}
.paper-card .num {{ background: {color}; }}
.note-block {{ border-left-color: {color}; }}
</style>
</head>
<body>
<div class="container">

<div class="masthead">
  <h1 style="color:{color}">{title}</h1>
  <p>{desc}</p>
  <p style="margin-top:0.5rem;font-size:0.9rem;color:var(--muted)">
    {count} papers &middot; SAARC Clinical Trial Equity &middot; 8 SAARC nations
  </p>
</div>

{_INSTRUCTIONS_HTML}

{cards_html}

{_E156_RULES_HTML}

</div>
{_DOWNLOAD_JS}
</body>
</html>"""


# ───────────────────────────────────────────────────────────
#  make_landing_page
# ───────────────────────────────────────────────────────────

def make_landing_page():
    """Return complete HTML landing page with 5 group cards."""

    group_cards = ""
    for gid, ginfo in GROUPS.items():
        color = GROUP_COLORS.get(gid, "#0d6b57")
        name = escape(ginfo["name"])
        desc = escape(ginfo["description"])
        pcount = ginfo["paper_count"]
        group_cards += f"""\
<a href="{gid}/index.html" class="group-card" style="border-top:4px solid {color};">
  <h2 style="color:{color}">{name}</h2>
  <p>{desc}</p>
  <div class="paper-count">{pcount} papers</div>
</a>
"""

    return f"""\
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>SAARC Clinical Trial Equity — E156 Micro-Papers</title>
<meta property="og:title" content="SAARC Clinical Trial Equity — E156 Micro-Papers">
<meta property="og:description" content="190 structured analyses for Ziauddin Medical University examining clinical trial equity across 8 SAARC nations with Pakistan emphasis.">
<meta property="og:type" content="website">
<style>
{_SHARED_CSS}
{_LANDING_CSS}
</style>
</head>
<body>
<div class="container">

<div class="masthead">
  <h1>SAARC Clinical Trial Equity</h1>
  <p>190 Structured Analyses for Ziauddin Medical University</p>
  <p style="margin-top:0.5rem;font-size:0.9rem;color:var(--muted)">
    E156 micro-papers examining clinical trial distribution, disease burden alignment,
    governance, and research systems across 8 SAARC nations with Pakistan emphasis.
  </p>
</div>

<div class="group-grid">
{group_cards}
</div>

<footer>
  <p>SAARC Clinical Trial Equity &mdash; E156 Micro-Paper Platform</p>
  <p><a href="https://github.com/mahmood789/saarc-e156-students">GitHub Repository</a></p>
</footer>

</div>
</body>
</html>"""
