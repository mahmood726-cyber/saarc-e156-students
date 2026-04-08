"""
16 SVG chart generators for SAARC E156 HTML dashboards.

Pure Python, no external dependencies. Each function returns a complete
inline SVG string using NYT-style aesthetics (Georgia serif, muted palette).

Colors: Pakistan #006600, India #FF9933, SAARC #0d6b57.
"""
import math
from html import escape as _escape

# -- Palette constants -------------------------------------------------------
_PAKISTAN = "#006600"    # Pakistan green
_INDIA = "#FF9933"      # India saffron
_SAARC = "#0d6b57"      # Teal
_INK = "#1d2430"
_MUTED = "#4a5568"
_LINE = "#d8cfbf"
_BG = "#fffdf8"
_ACCENT_SOFT = "#dcefe8"
_FONT = "Georgia,'Times New Roman',serif"

# -- Helpers ------------------------------------------------------------------

def _fmt(v, decimals=1):
    """Format a number nicely."""
    if isinstance(v, int) or v == int(v):
        return str(int(v))
    return f"{v:.{decimals}f}"


def _lerp_color(t, lo=(230, 245, 230), hi=(0, 102, 0)):
    """Linear interpolate between two RGB colors, t in [0,1].
    Default: light green to Pakistan green."""
    t = max(0.0, min(1.0, t))
    r = int(lo[0] + (hi[0] - lo[0]) * t)
    g = int(lo[1] + (hi[1] - lo[1]) * t)
    b = int(lo[2] + (hi[2] - lo[2]) * t)
    return f"rgb({r},{g},{b})"


def _axis_ticks(lo, hi, n=5):
    """Return n nice axis tick values spanning lo..hi."""
    if hi <= lo:
        hi = lo + 1
    rng = hi - lo
    rough = rng / max(n - 1, 1)
    mag = 10 ** math.floor(math.log10(rough)) if rough > 0 else 1
    nice = rough / mag
    if nice <= 1.5:
        step = 1 * mag
    elif nice <= 3:
        step = 2 * mag
    elif nice <= 7:
        step = 5 * mag
    else:
        step = 10 * mag
    start = math.floor(lo / step) * step
    ticks = []
    v = start
    while v <= hi + step * 0.001:
        ticks.append(v)
        v += step
    return ticks


def _gaussian_kde(data, n_points=80, bw=None):
    """Simple Gaussian KDE. Returns list of (x, density) tuples."""
    if not data:
        return []
    mn, mx = min(data), max(data)
    rng = mx - mn if mx > mn else 1.0
    if bw is None:
        std = (sum((v - sum(data) / len(data)) ** 2 for v in data) / len(data)) ** 0.5
        bw = 1.06 * max(std, rng / 20) * len(data) ** (-0.2)
    bw = max(bw, rng / 100)
    pad = 3 * bw
    xs = [mn - pad + (rng + 2 * pad) * i / (n_points - 1) for i in range(n_points)]
    result = []
    coeff = 1.0 / (len(data) * bw * math.sqrt(2 * math.pi))
    for x in xs:
        d = sum(math.exp(-0.5 * ((x - v) / bw) ** 2) for v in data) * coeff
        result.append((x, d))
    return result


# -- CHART_TYPE_MAP -----------------------------------------------------------

CHART_TYPE_MAP = {
    "choropleth": "choropleth_saarc",
    "choropleth_pakistan": "choropleth_pakistan",
    "lorenz": "lorenz_chart",
    "forest": "forest_plot",
    "violin": "violin_plot",
    "heatmap": "heatmap_chart",
    "network": "network_graph",
    "timeseries": "timeseries_chart",
    "waterfall": "waterfall_chart",
    "sankey": "sankey_chart",
    "radar": "radar_chart",
    "bubble": "bubble_chart",
    "slope": "slope_chart",
    "ridge": "ridge_plot",
    "funnel": "funnel_plot",
    "kaplan_meier": "kaplan_meier_chart",
}


# -- Simplified SAARC SVG paths (8 nations) ----------------------------------
# Hand-simplified polygon outlines positioned for a 500x500 viewBox.
# ViewBox covers roughly 60E-100E, 0N-40N (South Asia region).
# Coordinates are approximate; recognizable but not cartographic.

_SAARC_PATHS = {
    "Afghanistan": (
        "M 55 65 L 85 50 L 120 55 L 135 75 L 130 100 L 110 115 "
        "L 85 110 L 65 95 Z",
        95, 82
    ),
    "Pakistan": (
        "M 110 115 L 130 100 L 135 75 L 155 70 L 175 85 L 185 110 "
        "L 180 140 L 175 170 L 165 200 L 155 220 L 140 230 L 125 215 "
        "L 120 190 L 115 160 L 110 135 Z",
        150, 155
    ),
    "India": (
        "M 175 85 L 200 75 L 230 70 L 260 80 L 290 75 L 315 85 "
        "L 330 100 L 340 120 L 345 145 L 340 175 L 330 205 "
        "L 310 235 L 290 270 L 275 300 L 265 330 L 255 355 "
        "L 245 365 L 235 355 L 240 325 L 245 295 L 240 265 "
        "L 225 240 L 210 220 L 195 200 L 185 175 L 180 140 "
        "L 185 110 Z",
        265, 200
    ),
    "Nepal": (
        "M 230 120 L 260 110 L 290 108 L 310 115 L 305 130 "
        "L 275 135 L 245 132 L 230 128 Z",
        270, 122
    ),
    "Bhutan": (
        "M 320 115 L 340 110 L 355 118 L 350 130 L 335 132 "
        "L 322 125 Z",
        337, 122
    ),
    "Bangladesh": (
        "M 330 145 L 345 135 L 360 140 L 365 160 L 360 180 "
        "L 345 185 L 335 175 L 330 160 Z",
        348, 160
    ),
    "Sri Lanka": (
        "M 260 380 L 275 370 L 285 380 L 283 400 L 270 410 "
        "L 258 400 Z",
        272, 392
    ),
    "Maldives": (
        "M 195 405 L 200 395 L 205 405 L 202 418 L 197 418 Z",
        200, 408
    ),
}

# -- SAARC country colors for multi-series charts ----------------------------
_SAARC_COLORS = {
    "Pakistan": _PAKISTAN,
    "India": _INDIA,
    "Bangladesh": "#006A4E",
    "Sri Lanka": "#8B0000",
    "Nepal": "#DC143C",
    "Afghanistan": "#000000",
    "Bhutan": "#FF8C00",
    "Maldives": "#D62828",
}


# -- Simplified Pakistan SVG paths (7 provinces/territories) -----------------
# ViewBox covers Pakistan only (~500x500).

_PAKISTAN_PATHS = {
    "Balochistan": (
        "M 30 200 L 70 150 L 120 130 L 170 140 L 200 175 "
        "L 210 220 L 200 280 L 170 340 L 130 380 L 80 390 "
        "L 40 350 L 25 290 Z",
        115, 270
    ),
    "Sindh": (
        "M 200 280 L 230 240 L 270 230 L 300 260 L 310 310 "
        "L 300 370 L 270 410 L 230 430 L 190 420 L 170 380 "
        "L 170 340 Z",
        245, 340
    ),
    "Punjab": (
        "M 200 175 L 230 140 L 270 120 L 320 115 L 360 130 "
        "L 380 165 L 370 210 L 340 240 L 300 260 L 270 230 "
        "L 230 240 Z",
        295, 190
    ),
    "KPK": (
        "M 170 70 L 210 50 L 250 55 L 270 80 L 270 120 "
        "L 230 140 L 200 130 L 170 140 L 155 115 Z",
        215, 95
    ),
    "ICT": (
        "M 280 108 L 295 102 L 305 110 L 300 120 L 285 118 Z",
        292, 112
    ),
    "Gilgit-Baltistan": (
        "M 220 10 L 270 5 L 320 15 L 350 40 L 340 70 "
        "L 300 80 L 260 65 L 230 45 Z",
        285, 40
    ),
    "AJK": (
        "M 310 80 L 340 70 L 360 85 L 360 110 L 340 120 "
        "L 320 115 L 310 95 Z",
        335, 97
    ),
}


# =============================================================================
# 1. Choropleth SAARC
# =============================================================================

def choropleth_saarc(country_values: dict, title: str, width=500, height=500) -> str:
    """SVG map of South Asia with 8 SAARC nations shaded by value."""
    if not country_values:
        return ""
    vals = [v for v in country_values.values() if v is not None]
    if not vals:
        return ""
    mn, mx = min(vals), max(vals)
    rng = mx - mn if mx > mn else 1.0

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="24" text-anchor="middle" font-size="15" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Draw all countries
    for country, (path_d, cx, cy) in _SAARC_PATHS.items():
        v = country_values.get(country)
        if v is not None:
            t = (v - mn) / rng
            fill = _lerp_color(t)
        else:
            fill = "#e8e4db"
        parts.append(f'<path d="{path_d}" fill="{fill}" stroke="#fff" stroke-width="1.5" '
                     f'opacity="0.9"><title>{_escape(country)}: '
                     f'{_fmt(v) if v is not None else "N/A"}</title></path>')

    # Label all countries at centroids
    for country, (path_d, cx, cy) in _SAARC_PATHS.items():
        v = country_values.get(country)
        # Use abbreviated names for small countries
        short_names = {
            "Afghanistan": "AFG", "Pakistan": "PAK", "India": "IND",
            "Nepal": "NPL", "Bhutan": "BTN", "Bangladesh": "BGD",
            "Sri Lanka": "LKA", "Maldives": "MDV",
        }
        abbr = short_names.get(country, country[:3].upper())
        parts.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="9" '
                     f'fill="{_INK}" font-weight="600">{abbr}</text>')
        if v is not None:
            parts.append(f'<text x="{cx}" y="{cy+11}" text-anchor="middle" font-size="8" '
                         f'fill="{_MUTED}">{_fmt(v)}</text>')

    # Color scale legend
    ly = height - 35
    for i in range(50):
        c = _lerp_color(i / 49)
        parts.append(f'<rect x="{width//2 - 75 + i*3}" y="{ly}" width="3" height="10" fill="{c}"/>')
    parts.append(f'<text x="{width//2 - 78}" y="{ly+9}" text-anchor="end" font-size="9" '
                 f'fill="{_MUTED}">{_fmt(mn)}</text>')
    parts.append(f'<text x="{width//2 + 78}" y="{ly+9}" text-anchor="start" font-size="9" '
                 f'fill="{_MUTED}">{_fmt(mx)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 2. Choropleth Pakistan
# =============================================================================

def choropleth_pakistan(province_values: dict, title: str, width=500, height=500) -> str:
    """SVG map of Pakistan with 7 provinces/territories shaded by value."""
    if not province_values:
        return ""
    vals = [v for v in province_values.values() if v is not None]
    if not vals:
        return ""
    mn, mx = min(vals), max(vals)
    rng = mx - mn if mx > mn else 1.0

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="24" text-anchor="middle" font-size="15" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Draw all provinces
    for province, (path_d, cx, cy) in _PAKISTAN_PATHS.items():
        v = province_values.get(province)
        if v is not None:
            t = (v - mn) / rng
            fill = _lerp_color(t)
        else:
            fill = "#e8e4db"
        parts.append(f'<path d="{path_d}" fill="{fill}" stroke="#fff" stroke-width="1.5" '
                     f'opacity="0.9"><title>{_escape(province)}: '
                     f'{_fmt(v) if v is not None else "N/A"}</title></path>')

    # Label all provinces at centroids
    for province, (path_d, cx, cy) in _PAKISTAN_PATHS.items():
        v = province_values.get(province)
        short_names = {
            "Balochistan": "BAL", "Sindh": "SND", "Punjab": "PJB",
            "KPK": "KPK", "ICT": "ICT",
            "Gilgit-Baltistan": "GB", "AJK": "AJK",
        }
        abbr = short_names.get(province, province[:3].upper())
        parts.append(f'<text x="{cx}" y="{cy}" text-anchor="middle" font-size="10" '
                     f'fill="{_INK}" font-weight="600">{abbr}</text>')
        if v is not None:
            parts.append(f'<text x="{cx}" y="{cy+12}" text-anchor="middle" font-size="9" '
                         f'fill="{_MUTED}">{_fmt(v)}</text>')

    # Color scale legend
    ly = height - 35
    for i in range(50):
        c = _lerp_color(i / 49)
        parts.append(f'<rect x="{width//2 - 75 + i*3}" y="{ly}" width="3" height="10" fill="{c}"/>')
    parts.append(f'<text x="{width//2 - 78}" y="{ly+9}" text-anchor="end" font-size="9" '
                 f'fill="{_MUTED}">{_fmt(mn)}</text>')
    parts.append(f'<text x="{width//2 + 78}" y="{ly+9}" text-anchor="start" font-size="9" '
                 f'fill="{_MUTED}">{_fmt(mx)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 3. Lorenz Chart
# =============================================================================

def lorenz_chart(values: list, title: str, width=400, height=280) -> str:
    """Lorenz curve with Gini coefficient annotation."""
    if not values or len(values) < 2:
        return ""
    vals = sorted(values)
    n = len(vals)
    total = sum(vals)
    if total == 0:
        return ""

    m = {"t": 35, "r": 20, "b": 35, "l": 50}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    # Build Lorenz points
    cum = 0.0
    lorenz_pts = [(0.0, 0.0)]
    for i, v in enumerate(vals):
        cum += v
        lorenz_pts.append(((i + 1) / n, cum / total))

    # Gini = 1 - 2*area_under_lorenz
    area = sum(0.5 * (lorenz_pts[i][1] + lorenz_pts[i + 1][1]) * (lorenz_pts[i + 1][0] - lorenz_pts[i][0])
               for i in range(len(lorenz_pts) - 1))
    gini = 1.0 - 2.0 * area

    def tx(frac):
        return m["l"] + frac * pw

    def ty(frac):
        return m["t"] + (1 - frac) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Diagonal (equality line)
    parts.append(f'<line x1="{tx(0)}" y1="{ty(0)}" x2="{tx(1)}" y2="{ty(1)}" '
                 f'stroke="{_LINE}" stroke-width="1.5" stroke-dasharray="5,3"/>')

    # Shaded area between diagonal and curve
    poly_pts = ' '.join(f'{tx(x):.1f},{ty(y):.1f}' for x, y in lorenz_pts)
    poly_pts += f' {tx(1):.1f},{ty(1):.1f}'
    parts.append(f'<polygon points="{poly_pts}" fill="{_SAARC}" opacity="0.15"/>')

    # Lorenz curve
    curve_d = f'M {tx(lorenz_pts[0][0]):.1f} {ty(lorenz_pts[0][1]):.1f}'
    for x, y in lorenz_pts[1:]:
        curve_d += f' L {tx(x):.1f} {ty(y):.1f}'
    parts.append(f'<path d="{curve_d}" fill="none" stroke="{_SAARC}" stroke-width="2"/>')

    # Axes
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]}" x2="{m["l"]}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]+ph}" x2="{m["l"]+pw}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')

    # Axis labels
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        x_pos = tx(frac)
        parts.append(f'<text x="{x_pos}" y="{m["t"]+ph+15}" text-anchor="middle" '
                     f'font-size="9" fill="{_MUTED}">{int(frac*100)}%</text>')
        y_pos = ty(frac)
        parts.append(f'<text x="{m["l"]-5}" y="{y_pos+3}" text-anchor="end" '
                     f'font-size="9" fill="{_MUTED}">{int(frac*100)}%</text>')

    # Gini annotation
    parts.append(f'<text x="{tx(0.55)}" y="{ty(0.25)}" font-size="13" '
                 f'font-weight="700" fill="{_SAARC}">Gini = {gini:.3f}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 4. Forest Plot
# =============================================================================

def forest_plot(effects: list, title: str, width=420, height=None) -> str:
    """Forest plot with squares for studies and diamond for summary."""
    if not effects:
        return ""
    n = len(effects)
    row_h = 28
    if height is None:
        height = 60 + n * row_h + 10
    m = {"t": 40, "r": 30, "b": 20, "l": 160}
    pw = width - m["l"] - m["r"]

    all_vals = []
    for e in effects:
        all_vals.extend([e.get("ci_lower", 0), e.get("ci_upper", 0), e.get("estimate", 0)])
    lo, hi = min(all_vals), max(all_vals)
    pad = (hi - lo) * 0.15 if hi > lo else 1
    lo -= pad
    hi += pad
    rng = hi - lo if hi > lo else 1

    # Determine null reference (1 for ratios, 0 for differences)
    null_ref = 1.0 if all(e.get("estimate", 0) > 0 for e in effects) else 0.0

    def tx(v):
        return m["l"] + (v - lo) / rng * pw

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Null reference line
    if lo <= null_ref <= hi:
        nx = tx(null_ref)
        parts.append(f'<line x1="{nx}" y1="{m["t"]}" x2="{nx}" y2="{height-m["b"]}" '
                     f'stroke="{_LINE}" stroke-width="1" stroke-dasharray="4,3"/>')

    # Studies
    for i, e in enumerate(effects):
        y = m["t"] + i * row_h + row_h // 2
        est = e.get("estimate", 0)
        ci_l = e.get("ci_lower", est)
        ci_u = e.get("ci_upper", est)
        label = e.get("label", f"Study {i+1}")

        # Label
        parts.append(f'<text x="{m["l"]-8}" y="{y+4}" text-anchor="end" font-size="10" '
                     f'fill="{_INK}">{_escape(label)}</text>')
        # CI line
        parts.append(f'<line x1="{tx(ci_l):.1f}" y1="{y}" x2="{tx(ci_u):.1f}" y2="{y}" '
                     f'stroke="{_INK}" stroke-width="1.5"/>')
        # Square at estimate
        sq = 5
        parts.append(f'<rect x="{tx(est)-sq:.1f}" y="{y-sq}" width="{sq*2}" height="{sq*2}" '
                     f'fill="{_SAARC}"/>')

    # Axis ticks
    ticks = _axis_ticks(lo, hi, 5)
    ya = height - m["b"]
    parts.append(f'<line x1="{m["l"]}" y1="{ya}" x2="{m["l"]+pw}" y2="{ya}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    for t in ticks:
        if lo <= t <= hi:
            xt = tx(t)
            parts.append(f'<text x="{xt}" y="{ya+14}" text-anchor="middle" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 5. Violin Plot
# =============================================================================

def violin_plot(groups: dict, title: str, width=400, height=280) -> str:
    """Violin plot with KDE, median line, and quartile markers."""
    if not groups:
        return ""
    valid = {k: v for k, v in groups.items() if v and len(v) >= 2}
    if not valid:
        return ""

    m = {"t": 40, "r": 20, "b": 35, "l": 50}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    all_vals = [v for vs in valid.values() for v in vs]
    g_min, g_max = min(all_vals), max(all_vals)
    rng = g_max - g_min if g_max > g_min else 1

    def ty(v):
        return m["t"] + (1 - (v - g_min) / rng) * ph

    n_groups = len(valid)
    band = pw / n_groups
    max_half = band * 0.4

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    for idx, (name, vals) in enumerate(valid.items()):
        cx = m["l"] + band * idx + band / 2
        color = _SAARC_COLORS.get(name, _SAARC)
        kde = _gaussian_kde(vals)
        if not kde:
            continue
        max_d = max(d for _, d in kde)
        if max_d == 0:
            continue

        # Build violin polygon (right half then left half mirrored)
        right = [(cx + (d / max_d) * max_half, ty(x)) for x, d in kde]
        left = [(cx - (d / max_d) * max_half, ty(x)) for x, d in kde]
        pts = right + list(reversed(left))
        poly = ' '.join(f'{px:.1f},{py:.1f}' for px, py in pts)
        parts.append(f'<polygon points="{poly}" fill="{color}" opacity="0.3" '
                     f'stroke="{color}" stroke-width="1"/>')

        # Median & quartiles
        s = sorted(vals)
        median = s[len(s) // 2]
        q1 = s[len(s) // 4]
        q3 = s[3 * len(s) // 4]

        parts.append(f'<line x1="{cx-max_half*0.4:.1f}" y1="{ty(q1):.1f}" '
                     f'x2="{cx+max_half*0.4:.1f}" y2="{ty(q1):.1f}" stroke="{color}" stroke-width="1"/>')
        parts.append(f'<line x1="{cx-max_half*0.4:.1f}" y1="{ty(q3):.1f}" '
                     f'x2="{cx+max_half*0.4:.1f}" y2="{ty(q3):.1f}" stroke="{color}" stroke-width="1"/>')
        parts.append(f'<line x1="{cx-max_half*0.6:.1f}" y1="{ty(median):.1f}" '
                     f'x2="{cx+max_half*0.6:.1f}" y2="{ty(median):.1f}" '
                     f'stroke="{color}" stroke-width="2.5"/>')

        # Group label
        parts.append(f'<text x="{cx}" y="{height-10}" text-anchor="middle" '
                     f'font-size="10" fill="{_INK}">{_escape(name)}</text>')

    # Y-axis
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]}" x2="{m["l"]}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    ticks = _axis_ticks(g_min, g_max, 5)
    for t in ticks:
        if g_min <= t <= g_max:
            yt = ty(t)
            parts.append(f'<text x="{m["l"]-5}" y="{yt+3}" text-anchor="end" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')
            parts.append(f'<line x1="{m["l"]}" y1="{yt}" x2="{m["l"]+pw}" y2="{yt}" '
                         f'stroke="{_LINE}" stroke-width="0.5" opacity="0.4"/>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 6. Heatmap Chart
# =============================================================================

def heatmap_chart(matrix: list, row_labels: list, col_labels: list,
                  title: str, width=420, height=320) -> str:
    """Color-coded heatmap with value annotations."""
    if not matrix or not matrix[0]:
        return ""
    n_rows = len(matrix)
    n_cols = len(matrix[0])

    m = {"t": 45, "r": 60, "b": 15, "l": 90}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]
    cw = pw / n_cols
    ch = ph / n_rows

    flat = [v for row in matrix for v in row if v is not None]
    if not flat:
        return ""
    mn, mx = min(flat), max(flat)
    rng = mx - mn if mx > mn else 1

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Column labels
    for j, cl in enumerate(col_labels[:n_cols]):
        x = m["l"] + j * cw + cw / 2
        parts.append(f'<text x="{x}" y="{m["t"]-5}" text-anchor="middle" '
                     f'font-size="9" fill="{_MUTED}">{_escape(str(cl))}</text>')

    # Cells
    for i, row in enumerate(matrix):
        y = m["t"] + i * ch
        # Row label
        if i < len(row_labels):
            parts.append(f'<text x="{m["l"]-5}" y="{y+ch/2+3}" text-anchor="end" '
                         f'font-size="9" fill="{_INK}">{_escape(str(row_labels[i]))}</text>')
        for j, v in enumerate(row):
            x = m["l"] + j * cw
            if v is None:
                fill = "#e8e4db"
            else:
                t = (v - mn) / rng
                fill = _lerp_color(t)
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{cw:.1f}" height="{ch:.1f}" '
                         f'fill="{fill}" stroke="#fff" stroke-width="1"/>')
            if v is not None:
                tx_c = x + cw / 2
                ty_c = y + ch / 2 + 3
                t_val = (v - mn) / rng
                txt_color = "#fff" if t_val > 0.6 else _INK
                parts.append(f'<text x="{tx_c:.1f}" y="{ty_c:.1f}" text-anchor="middle" '
                             f'font-size="9" fill="{txt_color}">{_fmt(v)}</text>')

    # Color scale legend (vertical, right side)
    lx = width - m["r"] + 15
    for i in range(30):
        c = _lerp_color(1 - i / 29)
        parts.append(f'<rect x="{lx}" y="{m["t"]+i*(ph/30):.1f}" width="10" '
                     f'height="{ph/30+1:.1f}" fill="{c}"/>')
    parts.append(f'<text x="{lx+14}" y="{m["t"]+8}" font-size="8" fill="{_MUTED}">{_fmt(mx)}</text>')
    parts.append(f'<text x="{lx+14}" y="{m["t"]+ph}" font-size="8" fill="{_MUTED}">{_fmt(mn)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 7. Network Graph
# =============================================================================

def network_graph(nodes: list, edges: list, title: str, width=400, height=300) -> str:
    """Simple network graph with circular layout and spring nudge."""
    if not nodes:
        return ""
    n = len(nodes)
    cx, cy = width / 2, height / 2 + 15
    radius = min(width, height) * 0.32

    # Circular initial positions
    positions = []
    for i in range(n):
        angle = 2 * math.pi * i / n - math.pi / 2
        positions.append([cx + radius * math.cos(angle), cy + radius * math.sin(angle)])

    # Simple spring adjustment (3 iterations)
    for _ in range(3):
        forces = [[0.0, 0.0] for _ in range(n)]
        for edge in edges:
            s, t = edge.get("source", 0), edge.get("target", 0)
            if 0 <= s < n and 0 <= t < n:
                dx = positions[t][0] - positions[s][0]
                dy = positions[t][1] - positions[s][1]
                dist = max(math.sqrt(dx * dx + dy * dy), 1)
                w = edge.get("weight", 1)
                f = (dist - radius * 0.5) * 0.02 * w
                forces[s][0] += dx / dist * f
                forces[s][1] += dy / dist * f
                forces[t][0] -= dx / dist * f
                forces[t][1] -= dy / dist * f
        for i in range(n):
            positions[i][0] += forces[i][0]
            positions[i][1] += forces[i][1]
            # Keep inside bounds
            positions[i][0] = max(30, min(width - 30, positions[i][0]))
            positions[i][1] = max(40, min(height - 20, positions[i][1]))

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Edges
    for edge in edges:
        s, t = edge.get("source", 0), edge.get("target", 0)
        if 0 <= s < n and 0 <= t < n:
            w = min(edge.get("weight", 1), 5)
            parts.append(f'<line x1="{positions[s][0]:.1f}" y1="{positions[s][1]:.1f}" '
                         f'x2="{positions[t][0]:.1f}" y2="{positions[t][1]:.1f}" '
                         f'stroke="{_LINE}" stroke-width="{max(0.5, w):.1f}" opacity="0.6"/>')

    # Nodes
    for i, node in enumerate(nodes):
        px, py = positions[i]
        sz = max(4, min(20, node.get("size", 8)))
        color = node.get("color", _SAARC)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sz}" '
                     f'fill="{color}" opacity="0.85"/>')
        nid = node.get("id", "")
        if nid:
            parts.append(f'<text x="{px:.1f}" y="{py-sz-3:.1f}" text-anchor="middle" '
                         f'font-size="8" fill="{_INK}">{_escape(str(nid))}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 8. Timeseries Chart
# =============================================================================

def timeseries_chart(series: dict, title: str, width=440, height=240,
                     changepoints: list = None) -> str:
    """Multi-series line chart with optional changepoint markers."""
    if not series:
        return ""
    valid_series = {k: v for k, v in series.items() if v and len(v) >= 1}
    if not valid_series:
        return ""

    m = {"t": 40, "r": 20, "b": 40, "l": 55}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    all_x = [pt[0] for vs in valid_series.values() for pt in vs]
    all_y = [pt[1] for vs in valid_series.values() for pt in vs]
    x_min, x_max = min(all_x), max(all_x)
    y_min, y_max = min(all_y), max(all_y)
    x_rng = x_max - x_min if x_max > x_min else 1
    y_rng = y_max - y_min if y_max > y_min else 1
    y_min_plot = y_min - y_rng * 0.05
    y_max_plot = y_max + y_rng * 0.05
    y_rng_plot = y_max_plot - y_min_plot if y_max_plot > y_min_plot else 1

    def tx(v):
        return m["l"] + (v - x_min) / x_rng * pw

    def ty(v):
        return m["t"] + (1 - (v - y_min_plot) / y_rng_plot) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Grid + axes
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]}" x2="{m["l"]}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]+ph}" x2="{m["l"]+pw}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')

    y_ticks = _axis_ticks(y_min, y_max, 5)
    for t in y_ticks:
        if y_min_plot <= t <= y_max_plot:
            yt = ty(t)
            parts.append(f'<line x1="{m["l"]}" y1="{yt:.1f}" x2="{m["l"]+pw}" y2="{yt:.1f}" '
                         f'stroke="{_LINE}" stroke-width="0.5" opacity="0.4"/>')
            parts.append(f'<text x="{m["l"]-5}" y="{yt+3:.1f}" text-anchor="end" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')

    # Changepoints
    if changepoints:
        for cp in changepoints:
            if x_min <= cp <= x_max:
                xc = tx(cp)
                parts.append(f'<line x1="{xc:.1f}" y1="{m["t"]}" x2="{xc:.1f}" y2="{m["t"]+ph}" '
                             f'stroke="{_SAARC}" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>')

    # Series lines + dots
    legend_y = m["t"] + 10
    series_colors = [_PAKISTAN, _INDIA, "#006A4E", "#DC143C", "#8B0000", "#FF8C00", _SAARC, _MUTED]
    for si, (name, pts) in enumerate(valid_series.items()):
        color = _SAARC_COLORS.get(name, series_colors[si % len(series_colors)])
        sorted_pts = sorted(pts, key=lambda p: p[0])
        path_d = f'M {tx(sorted_pts[0][0]):.1f} {ty(sorted_pts[0][1]):.1f}'
        for pt in sorted_pts[1:]:
            path_d += f' L {tx(pt[0]):.1f} {ty(pt[1]):.1f}'
        parts.append(f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="2"/>')
        for pt in sorted_pts:
            parts.append(f'<circle cx="{tx(pt[0]):.1f}" cy="{ty(pt[1]):.1f}" r="3" '
                         f'fill="{color}"/>')

        # Legend
        parts.append(f'<line x1="{m["l"]+5}" y1="{legend_y}" x2="{m["l"]+18}" y2="{legend_y}" '
                     f'stroke="{color}" stroke-width="2"/>')
        parts.append(f'<text x="{m["l"]+22}" y="{legend_y+3}" font-size="9" '
                     f'fill="{_INK}">{_escape(name)}</text>')
        legend_y += 14

    # X-axis labels
    x_ticks = _axis_ticks(x_min, x_max, 5)
    for t in x_ticks:
        if x_min <= t <= x_max:
            parts.append(f'<text x="{tx(t):.1f}" y="{m["t"]+ph+15}" text-anchor="middle" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t, 0)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 9. Waterfall Chart
# =============================================================================

def waterfall_chart(items: list, title: str, width=420, height=280) -> str:
    """Waterfall chart with running total, connector lines."""
    if not items:
        return ""
    m = {"t": 40, "r": 20, "b": 45, "l": 50}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    # Compute running totals
    running = []
    total = 0.0
    for item in items:
        v = item.get("value", 0)
        start = total
        total += v
        running.append((start, total, v, item))

    all_vals = [r[0] for r in running] + [r[1] for r in running]
    y_min = min(0, min(all_vals))
    y_max = max(all_vals)
    y_rng = y_max - y_min if y_max > y_min else 1

    n = len(items)
    bar_w = pw / n * 0.6
    gap = pw / n

    def ty(v):
        return m["t"] + (1 - (v - y_min) / y_rng) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Zero line
    if y_min < 0:
        parts.append(f'<line x1="{m["l"]}" y1="{ty(0):.1f}" x2="{m["l"]+pw}" y2="{ty(0):.1f}" '
                     f'stroke="{_LINE}" stroke-width="1"/>')

    for i, (start, end, v, item) in enumerate(running):
        x = m["l"] + i * gap + (gap - bar_w) / 2
        color = item.get("color", _PAKISTAN if v >= 0 else _INDIA)
        y_top = ty(max(start, end))
        y_bot = ty(min(start, end))
        bar_h = max(1, y_bot - y_top)

        parts.append(f'<rect x="{x:.1f}" y="{y_top:.1f}" width="{bar_w:.1f}" '
                     f'height="{bar_h:.1f}" fill="{color}" opacity="0.85" rx="1"/>')

        # Value label
        label_y = y_top - 5 if v >= 0 else y_bot + 12
        parts.append(f'<text x="{x+bar_w/2:.1f}" y="{label_y:.1f}" text-anchor="middle" '
                     f'font-size="8" fill="{_INK}">{_fmt(v)}</text>')

        # Connector line to next bar
        if i < n - 1:
            next_x = m["l"] + (i + 1) * gap + (gap - bar_w) / 2
            parts.append(f'<line x1="{x+bar_w:.1f}" y1="{ty(end):.1f}" '
                         f'x2="{next_x:.1f}" y2="{ty(end):.1f}" '
                         f'stroke="{_LINE}" stroke-width="1" stroke-dasharray="3,2"/>')

        # X label
        label_text = item.get("label", "")
        if label_text:
            parts.append(f'<text x="{x+bar_w/2:.1f}" y="{m["t"]+ph+14}" '
                         f'text-anchor="middle" font-size="8" fill="{_MUTED}" '
                         f'transform="rotate(-30 {x+bar_w/2:.1f} {m["t"]+ph+14})">'
                         f'{_escape(label_text[:12])}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 10. Sankey Chart
# =============================================================================

def sankey_chart(flows: list, title: str, width=440, height=300) -> str:
    """Two-column Sankey diagram with curved flow paths."""
    if not flows:
        return ""
    m = {"t": 40, "r": 20, "b": 15, "l": 20}
    ph = height - m["t"] - m["b"]

    # Collect unique sources and targets
    sources = list(dict.fromkeys(f["source"] for f in flows))
    targets = list(dict.fromkeys(f["target"] for f in flows))

    # Compute totals
    src_totals = {s: sum(f["value"] for f in flows if f["source"] == s) for s in sources}
    tgt_totals = {t: sum(f["value"] for f in flows if f["target"] == t) for t in targets}
    grand = max(sum(src_totals.values()), 1)

    node_w = 18
    col_left = m["l"] + 80
    col_right = width - m["r"] - 80 - node_w
    node_gap = 4

    # Position source nodes
    src_pos = {}
    y = m["t"]
    for s in sources:
        h = max(8, (src_totals[s] / grand) * ph)
        src_pos[s] = (y, h)
        y += h + node_gap

    # Position target nodes
    tgt_pos = {}
    y = m["t"]
    for t in targets:
        h = max(8, (tgt_totals[t] / grand) * ph)
        tgt_pos[t] = (y, h)
        y += h + node_gap

    colors = [_PAKISTAN, _INDIA, _SAARC, "#006A4E", "#8e44ad", "#e67e22", "#16a085"]

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Flow paths
    src_offsets = {s: 0.0 for s in sources}
    tgt_offsets = {t: 0.0 for t in targets}
    for fi, flow in enumerate(flows):
        s, t, v = flow["source"], flow["target"], flow["value"]
        if s not in src_pos or t not in tgt_pos:
            continue
        sy, sh = src_pos[s]
        ty_val, th = tgt_pos[t]
        flow_h_src = max(2, (v / max(src_totals[s], 1)) * sh)
        flow_h_tgt = max(2, (v / max(tgt_totals[t], 1)) * th)

        x1 = col_left + node_w
        y1 = sy + src_offsets[s]
        x2 = col_right
        y2 = ty_val + tgt_offsets[t]

        # Cubic bezier
        mid_x = (x1 + x2) / 2
        path_d = (f'M {x1} {y1} C {mid_x} {y1}, {mid_x} {y2}, {x2} {y2} '
                  f'L {x2} {y2+flow_h_tgt:.1f} '
                  f'C {mid_x} {y2+flow_h_tgt:.1f}, {mid_x} {y1+flow_h_src:.1f}, {x1} {y1+flow_h_src:.1f} Z')
        color = colors[fi % len(colors)]
        parts.append(f'<path d="{path_d}" fill="{color}" opacity="0.35"/>')

        src_offsets[s] += flow_h_src
        tgt_offsets[t] += flow_h_tgt

    # Source nodes + labels
    for i, s in enumerate(sources):
        sy, sh = src_pos[s]
        parts.append(f'<rect x="{col_left}" y="{sy:.1f}" width="{node_w}" height="{sh:.1f}" '
                     f'fill="{_PAKISTAN}" rx="2"/>')
        parts.append(f'<text x="{col_left-4}" y="{sy+sh/2+3:.1f}" text-anchor="end" '
                     f'font-size="9" fill="{_INK}">{_escape(str(s))}</text>')

    # Target nodes + labels
    for i, t in enumerate(targets):
        ty_val, th = tgt_pos[t]
        parts.append(f'<rect x="{col_right}" y="{ty_val:.1f}" width="{node_w}" height="{th:.1f}" '
                     f'fill="{_INDIA}" rx="2"/>')
        parts.append(f'<text x="{col_right+node_w+4}" y="{ty_val+th/2+3:.1f}" text-anchor="start" '
                     f'font-size="9" fill="{_INK}">{_escape(str(t))}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 11. Radar Chart
# =============================================================================

def radar_chart(dimensions: dict, title: str, width=300, height=300,
                max_val=1.0) -> str:
    """Radar/spider chart with polygon, grid rings, and axis labels."""
    if not dimensions:
        return ""
    keys = list(dimensions.keys())
    vals = [dimensions[k] for k in keys]
    n = len(keys)
    if n < 3:
        return ""

    cx, cy = width / 2, height / 2 + 12
    radius = min(width, height) * 0.33
    max_val = max(max_val, max(vals) if vals else 1)

    def polar(i, r):
        angle = 2 * math.pi * i / n - math.pi / 2
        return cx + r * math.cos(angle), cy + r * math.sin(angle)

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Grid rings at 25%, 50%, 75%, 100%
    for frac in [0.25, 0.5, 0.75, 1.0]:
        ring_pts = ' '.join(f'{polar(i, radius*frac)[0]:.1f},{polar(i, radius*frac)[1]:.1f}'
                            for i in range(n))
        parts.append(f'<polygon points="{ring_pts}" fill="none" stroke="{_LINE}" '
                     f'stroke-width="0.7" opacity="0.5"/>')

    # Axis lines
    for i in range(n):
        ex, ey = polar(i, radius)
        parts.append(f'<line x1="{cx}" y1="{cy}" x2="{ex:.1f}" y2="{ey:.1f}" '
                     f'stroke="{_LINE}" stroke-width="0.7" opacity="0.5"/>')

    # Data polygon
    data_pts = []
    for i, v in enumerate(vals):
        r = (v / max_val) * radius
        data_pts.append(polar(i, r))
    poly = ' '.join(f'{px:.1f},{py:.1f}' for px, py in data_pts)
    parts.append(f'<polygon points="{poly}" fill="{_SAARC}" opacity="0.2" '
                 f'stroke="{_SAARC}" stroke-width="2"/>')

    # Data points
    for px, py in data_pts:
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{_SAARC}"/>')

    # Axis labels
    for i, key in enumerate(keys):
        lx, ly = polar(i, radius + 18)
        anchor = "middle"
        if lx < cx - 10:
            anchor = "end"
        elif lx > cx + 10:
            anchor = "start"
        parts.append(f'<text x="{lx:.1f}" y="{ly+3:.1f}" text-anchor="{anchor}" '
                     f'font-size="9" fill="{_INK}">{_escape(str(key))}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 12. Bubble Chart
# =============================================================================

def bubble_chart(points: list, title: str, width=400, height=300) -> str:
    """Bubble chart with axis labels and size-proportional circles."""
    if not points:
        return ""
    m = {"t": 40, "r": 20, "b": 35, "l": 55}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    sizes = [p.get("size", 10) for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    s_max = max(sizes) if sizes else 1
    x_rng = x_max - x_min if x_max > x_min else 1
    y_rng = y_max - y_min if y_max > y_min else 1

    def tx(v):
        return m["l"] + (v - x_min) / x_rng * pw

    def ty(v):
        return m["t"] + (1 - (v - y_min) / y_rng) * ph

    max_r = 25

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Axes
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]}" x2="{m["l"]}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]+ph}" x2="{m["l"]+pw}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')

    # Axis ticks
    for t in _axis_ticks(x_min, x_max, 5):
        if x_min <= t <= x_max:
            parts.append(f'<text x="{tx(t):.1f}" y="{m["t"]+ph+15}" text-anchor="middle" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')
    for t in _axis_ticks(y_min, y_max, 5):
        if y_min <= t <= y_max:
            parts.append(f'<text x="{m["l"]-5}" y="{ty(t)+3:.1f}" text-anchor="end" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')

    # Bubbles (largest first so small ones render on top)
    sorted_pts = sorted(points, key=lambda p: -p.get("size", 10))
    for p in sorted_pts:
        bx = tx(p["x"])
        by = ty(p["y"])
        sz = p.get("size", 10)
        r = max(4, math.sqrt(sz / max(s_max, 1)) * max_r)
        color = p.get("color", _SAARC)
        parts.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r:.1f}" '
                     f'fill="{color}" opacity="0.6" stroke="{color}" stroke-width="1"/>')
        label = p.get("label", "")
        if label:
            parts.append(f'<text x="{bx:.1f}" y="{by-r-3:.1f}" text-anchor="middle" '
                         f'font-size="8" fill="{_INK}">{_escape(str(label)[:15])}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 13. Slope Chart
# =============================================================================

def slope_chart(pairs: list, title: str, width=360, height=280) -> str:
    """Slope chart: before/after columns with connecting lines."""
    if not pairs:
        return ""
    m = {"t": 40, "r": 30, "b": 30, "l": 30}
    ph = height - m["t"] - m["b"]

    all_vals = [p.get("before", 0) for p in pairs] + [p.get("after", 0) for p in pairs]
    v_min, v_max = min(all_vals), max(all_vals)
    v_rng = v_max - v_min if v_max > v_min else 1

    x_before = m["l"] + 80
    x_after = width - m["r"] - 80

    def ty(v):
        return m["t"] + (1 - (v - v_min) / v_rng) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Column headers
    parts.append(f'<text x="{x_before}" y="{m["t"]-8}" text-anchor="middle" '
                 f'font-size="10" font-weight="600" fill="{_MUTED}">Before</text>')
    parts.append(f'<text x="{x_after}" y="{m["t"]-8}" text-anchor="middle" '
                 f'font-size="10" font-weight="600" fill="{_MUTED}">After</text>')

    for pair in pairs:
        b = pair.get("before", 0)
        a = pair.get("after", 0)
        label = pair.get("label", "")
        color = _PAKISTAN if a >= b else _INDIA  # green if improved, saffron if worsened

        y1 = ty(b)
        y2 = ty(a)
        parts.append(f'<line x1="{x_before}" y1="{y1:.1f}" x2="{x_after}" y2="{y2:.1f}" '
                     f'stroke="{color}" stroke-width="2" opacity="0.7"/>')
        parts.append(f'<circle cx="{x_before}" cy="{y1:.1f}" r="4" fill="{color}"/>')
        parts.append(f'<circle cx="{x_after}" cy="{y2:.1f}" r="4" fill="{color}"/>')

        # Labels
        parts.append(f'<text x="{x_before-8}" y="{y1+3:.1f}" text-anchor="end" '
                     f'font-size="9" fill="{_INK}">{_escape(str(label)[:12])}</text>')
        parts.append(f'<text x="{x_before+8}" y="{y1+3:.1f}" text-anchor="start" '
                     f'font-size="8" fill="{_MUTED}">{_fmt(b)}</text>')
        parts.append(f'<text x="{x_after+8}" y="{y2+3:.1f}" text-anchor="start" '
                     f'font-size="8" fill="{_MUTED}">{_fmt(a)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 14. Ridge Plot
# =============================================================================

def ridge_plot(distributions: dict, title: str, width=400, height=300) -> str:
    """Overlapping density curves with vertical offset per group."""
    if not distributions:
        return ""
    valid = {k: v for k, v in distributions.items() if v and len(v) >= 2}
    if not valid:
        return ""

    m = {"t": 40, "r": 20, "b": 20, "l": 80}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    all_vals = [v for vs in valid.values() for v in vs]
    g_min, g_max = min(all_vals), max(all_vals)

    n_groups = len(valid)
    row_h = ph / n_groups
    max_curve_h = row_h * 0.8

    # Compute all KDEs
    kdes = {}
    global_max_d = 0
    for name, vals in valid.items():
        kde = _gaussian_kde(vals, n_points=60)
        kdes[name] = kde
        md = max((d for _, d in kde), default=0)
        if md > global_max_d:
            global_max_d = md

    if global_max_d == 0:
        return ""

    def tx(v):
        rng = g_max - g_min if g_max > g_min else 1
        return m["l"] + (v - g_min) / rng * pw

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    series_colors = [_PAKISTAN, _INDIA, "#006A4E", "#DC143C", "#8B0000", "#FF8C00", _SAARC, _MUTED]
    for idx, (name, kde) in enumerate(kdes.items()):
        color = _SAARC_COLORS.get(name, series_colors[idx % len(series_colors)])
        baseline_y = m["t"] + (idx + 1) * row_h

        # Build filled polygon
        pts_str = f'{tx(kde[0][0]):.1f},{baseline_y:.1f}'
        for x, d in kde:
            curve_y = baseline_y - (d / global_max_d) * max_curve_h
            pts_str += f' {tx(x):.1f},{curve_y:.1f}'
        pts_str += f' {tx(kde[-1][0]):.1f},{baseline_y:.1f}'

        parts.append(f'<polygon points="{pts_str}" fill="{color}" opacity="0.3" '
                     f'stroke="{color}" stroke-width="1.5"/>')

        # Group label
        parts.append(f'<text x="{m["l"]-5}" y="{baseline_y-row_h*0.3:.1f}" text-anchor="end" '
                     f'font-size="10" fill="{_INK}">{_escape(name)}</text>')

    # X-axis
    x_ticks = _axis_ticks(g_min, g_max, 5)
    ya = m["t"] + ph
    for t in x_ticks:
        if g_min <= t <= g_max:
            parts.append(f'<text x="{tx(t):.1f}" y="{ya+14}" text-anchor="middle" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 15. Funnel Plot
# =============================================================================

def funnel_plot(effects: list, title: str, width=400, height=300) -> str:
    """Inverted funnel plot with 95% CI bounds."""
    if not effects:
        return ""
    m = {"t": 40, "r": 20, "b": 35, "l": 55}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    effs = [e.get("effect", 0) for e in effects]
    ses = [e.get("se", 0.1) for e in effects]
    mean_eff = sum(effs) / len(effs)

    se_max = max(ses) if ses else 1
    eff_range = max(abs(e - mean_eff) for e in effs) + 1.96 * se_max
    x_min = mean_eff - eff_range * 1.2
    x_max = mean_eff + eff_range * 1.2
    x_rng = x_max - x_min if x_max > x_min else 1

    def tx(v):
        return m["l"] + (v - x_min) / x_rng * pw

    def ty(se):
        return m["t"] + (se / max(se_max * 1.1, 0.001)) * ph

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # 95% CI funnel triangle
    top_x = tx(mean_eff)
    top_y = ty(0)
    bot_l = tx(mean_eff - 1.96 * se_max * 1.1)
    bot_r = tx(mean_eff + 1.96 * se_max * 1.1)
    bot_y = ty(se_max * 1.1)
    parts.append(f'<polygon points="{top_x:.1f},{top_y:.1f} {bot_l:.1f},{bot_y:.1f} '
                 f'{bot_r:.1f},{bot_y:.1f}" fill="{_ACCENT_SOFT}" opacity="0.5" '
                 f'stroke="{_LINE}" stroke-width="1"/>')

    # Vertical center line
    parts.append(f'<line x1="{top_x:.1f}" y1="{top_y:.1f}" x2="{top_x:.1f}" y2="{bot_y:.1f}" '
                 f'stroke="{_LINE}" stroke-width="1" stroke-dasharray="4,3"/>')

    # Points
    for e in effects:
        eff = e.get("effect", 0)
        se = e.get("se", 0.1)
        label = e.get("label", "")
        color = _SAARC_COLORS.get(label, _INK)
        px = tx(eff)
        py = ty(se)
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" '
                     f'fill="{color}" opacity="0.8"/>')

    # Axes
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]}" x2="{m["l"]}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]+ph}" x2="{m["l"]+pw}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')

    # X-axis labels (effect)
    for t in _axis_ticks(x_min, x_max, 5):
        if x_min <= t <= x_max:
            parts.append(f'<text x="{tx(t):.1f}" y="{m["t"]+ph+15}" text-anchor="middle" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t)}</text>')

    # Y-axis labels (SE, inverted: 0 at top)
    for t in _axis_ticks(0, se_max, 4):
        yt = ty(t)
        parts.append(f'<text x="{m["l"]-5}" y="{yt+3:.1f}" text-anchor="end" '
                     f'font-size="9" fill="{_MUTED}">{_fmt(t, 2)}</text>')

    # Axis titles
    parts.append(f'<text x="{width//2}" y="{height-3}" text-anchor="middle" '
                 f'font-size="9" fill="{_MUTED}">Effect Size</text>')
    parts.append(f'<text x="12" y="{m["t"]+ph//2}" text-anchor="middle" '
                 f'font-size="9" fill="{_MUTED}" '
                 f'transform="rotate(-90 12 {m["t"]+ph//2})">Std Error</text>')

    parts.append('</svg>')
    return '\n'.join(parts)


# =============================================================================
# 16. Kaplan-Meier Chart
# =============================================================================

def kaplan_meier_chart(curves: dict, title: str, width=420, height=280) -> str:
    """KM survival curves with step functions and optional at-risk table."""
    if not curves:
        return ""
    valid = {k: v for k, v in curves.items() if v and len(v) >= 2}
    if not valid:
        return ""

    m = {"t": 40, "r": 20, "b": 55, "l": 55}
    pw = width - m["l"] - m["r"]
    ph = height - m["t"] - m["b"]

    all_t = [pt[0] for vs in valid.values() for pt in vs]
    t_min, t_max = min(all_t), max(all_t)
    t_rng = t_max - t_min if t_max > t_min else 1

    def tx(v):
        return m["l"] + (v - t_min) / t_rng * pw

    def ty(v):
        return m["t"] + (1 - v) * ph  # survival 0..1

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
             f'style="max-width:{width}px;font-family:{_FONT};">']
    parts.append(f'<rect width="{width}" height="{height}" fill="{_BG}" rx="4"/>')
    parts.append(f'<text x="{width//2}" y="22" text-anchor="middle" font-size="14" '
                 f'font-weight="700" fill="{_INK}">{_escape(title)}</text>')

    # Axes
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]}" x2="{m["l"]}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')
    parts.append(f'<line x1="{m["l"]}" y1="{m["t"]+ph}" x2="{m["l"]+pw}" y2="{m["t"]+ph}" '
                 f'stroke="{_LINE}" stroke-width="1"/>')

    # Y-axis (survival probability)
    for frac in [0, 0.25, 0.5, 0.75, 1.0]:
        yt = ty(frac)
        parts.append(f'<text x="{m["l"]-5}" y="{yt+3:.1f}" text-anchor="end" '
                     f'font-size="9" fill="{_MUTED}">{frac:.0%}</text>')
        parts.append(f'<line x1="{m["l"]}" y1="{yt:.1f}" x2="{m["l"]+pw}" y2="{yt:.1f}" '
                     f'stroke="{_LINE}" stroke-width="0.5" opacity="0.3"/>')

    # X-axis labels
    x_ticks = _axis_ticks(t_min, t_max, 5)
    for t in x_ticks:
        if t_min <= t <= t_max:
            parts.append(f'<text x="{tx(t):.1f}" y="{m["t"]+ph+15}" text-anchor="middle" '
                         f'font-size="9" fill="{_MUTED}">{_fmt(t, 0)}</text>')

    parts.append(f'<text x="{width//2}" y="{m["t"]+ph+28}" text-anchor="middle" '
                 f'font-size="9" fill="{_MUTED}">Time</text>')

    # Step function curves
    series_colors = [_PAKISTAN, _INDIA, "#006A4E", "#DC143C", "#8B0000", "#FF8C00", _SAARC, _MUTED]
    legend_y = m["t"] + 10
    for si, (name, pts) in enumerate(valid.items()):
        color = _SAARC_COLORS.get(name, series_colors[si % len(series_colors)])
        sorted_pts = sorted(pts, key=lambda p: p[0])

        # Build step path
        path_d = f'M {tx(sorted_pts[0][0]):.1f} {ty(sorted_pts[0][1]):.1f}'
        for i in range(1, len(sorted_pts)):
            prev_surv = sorted_pts[i - 1][1]
            curr_t = sorted_pts[i][0]
            curr_surv = sorted_pts[i][1]
            # Horizontal to current time at previous survival
            path_d += f' L {tx(curr_t):.1f} {ty(prev_surv):.1f}'
            # Vertical drop to current survival
            path_d += f' L {tx(curr_t):.1f} {ty(curr_surv):.1f}'

        parts.append(f'<path d="{path_d}" fill="none" stroke="{color}" stroke-width="2"/>')

        # Legend
        parts.append(f'<line x1="{width-m["r"]-80}" y1="{legend_y}" '
                     f'x2="{width-m["r"]-67}" y2="{legend_y}" '
                     f'stroke="{color}" stroke-width="2"/>')
        parts.append(f'<text x="{width-m["r"]-63}" y="{legend_y+3}" '
                     f'font-size="9" fill="{_INK}">{_escape(name)}</text>')
        legend_y += 14

    # At-risk table (simplified: show counts at select time points)
    at_risk_y = height - 15
    parts.append(f'<text x="{m["l"]-5}" y="{at_risk_y}" text-anchor="end" '
                 f'font-size="8" font-weight="600" fill="{_MUTED}">At risk</text>')
    check_times = [t for t in x_ticks if t_min <= t <= t_max][:5]
    for si, (name, pts) in enumerate(valid.items()):
        color = _SAARC_COLORS.get(name, series_colors[si % len(series_colors)])
        sorted_pts = sorted(pts, key=lambda p: p[0])
        for ct in check_times:
            # Find survival at this time
            surv = 1.0
            for pt in sorted_pts:
                if pt[0] <= ct:
                    surv = pt[1]
                else:
                    break
            n_risk = max(1, int(surv * 100))
            parts.append(f'<text x="{tx(ct):.1f}" y="{at_risk_y}" text-anchor="middle" '
                         f'font-size="7" fill="{color}">{n_risk}</text>')
        at_risk_y += 10

    parts.append('</svg>')
    return '\n'.join(parts)
