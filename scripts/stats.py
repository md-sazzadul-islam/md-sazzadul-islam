"""Renders assets/stats.svg and assets/stats-dark.svg from the public GitHub API.

    python scripts/stats.py            # GH_USER and GITHUB_TOKEN are optional env vars

With a token (as in the GitHub Action) language shares come from byte counts
per repository; without one they are estimated from each repository's main
language so the script stays inside the anonymous rate limit.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

USER = os.environ.get("GH_USER") or "md-sazzadul-islam"
TOKEN = os.environ.get("GITHUB_TOKEN")
ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "font-family:'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
SERIF = "font-family:'Instrument Serif',Georgia,'Times New Roman',serif;font-style:italic"
BARS = [
    ("#e8373f", "#c9151e", "#9c0f16", "#6f0a10"),
    ("#f25a61", "#dc2f37", "#b81b23", "#8f1219"),
    ("#ff8a8e", "#f2545a", "#d9363d", "#ae2228"),
    ("#ffc2c4", "#ff9397", "#f07075", "#cf4f55"),
    ("#fbe4e1", "#ecc5c0", "#dcb4af", "#c08f8a"),
    ("#ffffff", "#f6efed", "#ddd0cd", "#c4b3b0"),
]


def api(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "profile-stats"})
    if TOKEN:
        req.add_header("Authorization", f"Bearer {TOKEN}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def collect():
    user = api(f"https://api.github.com/users/{USER}")
    repos, page = [], 1
    while True:
        chunk = api(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&page={page}")
        repos += chunk
        if len(chunk) < 100:
            break
        page += 1
    own = [r for r in repos if not r["fork"]]
    langs = {}
    for r in own:
        if TOKEN:
            for name, size in api(r["languages_url"]).items():
                langs[name] = langs.get(name, 0) + size
        elif r["language"]:
            langs[r["language"]] = langs.get(r["language"], 0) + max(r["size"], 1)
    total = sum(langs.values()) or 1
    top = [kv for kv in sorted(langs.items(), key=lambda kv: -kv[1]) if kv[1] / total >= 0.005][:6]
    created = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
    years = (datetime.now(timezone.utc) - created).days // 365
    return {
        "numbers": [
            (user["public_repos"], "public repositories"),
            (sum(r["stargazers_count"] for r in own), "stars earned"),
            (user["followers"], "followers"),
            (years, "years on GitHub"),
        ],
        "langs": [(n, s / total) for n, s in top],
    }


def render(data, dark=False):
    bg, ink, muted, brand = ("#1b1113", "#f6eeec", "#b7a6a8", "#ff7a80") if dark else ("#f2ecea", "#241a1b", "#6d5f61", "#c9151e")
    shade = "#000000" if dark else "#5e0a10"
    o = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 430" width="1200" height="430" role="img" aria-labelledby="t d">
  <title id="t">GitHub in numbers for {USER}</title>
  <desc id="d">{"; ".join(f"{v} {l}" for v, l in data["numbers"])}. Top languages: {", ".join(f"{n} {s:.0%}" for n, s in data["langs"])}.</desc>
  <defs>''']
    for i, c in enumerate(BARS):
        o.append(f'    <linearGradient id="b{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>')
    o.append(f'''    <radialGradient id="sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{shade}" stop-opacity=".25"/><stop offset="1" stop-color="{shade}" stop-opacity="0"/></radialGradient>
  </defs>
  <style>
    .sans{{{SANS}}}
    .serif{{{SERIF}}}
    .bar{{animation:hop 6s ease-in-out infinite}}
    @keyframes hop{{0%,24%,100%{{transform:translateY(0)}}12%{{transform:translateY(-9px)}}}}
    @media (prefers-reduced-motion:reduce){{.bar{{animation:none}}}}
  </style>
  <rect x="1" y="1" width="1198" height="428" rx="28" fill="{bg}" stroke="{ink}" stroke-opacity=".14" stroke-width="2"/>
  <text class="serif" x="64" y="92" font-size="34" fill="{brand}">GitHub in numbers</text>
  <g class="sans">''')
    for k, (value, label) in enumerate(data["numbers"]):
        x, y = 64 + (k % 2) * 220, 180 + (k // 2) * 120
        o.append(f'    <text x="{x}" y="{y}" font-size="52" font-weight="700" fill="{ink}">{value}</text>')
        o.append(f'    <text x="{x}" y="{y + 28}" font-size="15" fill="{muted}">{label}</text>')
    o.append('  </g>')

    langs = data["langs"]
    if langs:
        HW, HH, STEP, BASE = 38, 19, 104, 318
        x0 = 870 - (len(langs) - 1) * STEP / 2
        peak = max(s for _, s in langs)
        o.append(f'  <text class="sans" x="{x0 - HW:.0f}" y="64" font-size="13" font-weight="700" letter-spacing="1.5" fill="{muted}">TOP LANGUAGES</text>')
        for i, (name, share) in enumerate(langs):
            cx, h = x0 + i * STEP, 24 + 190 * share / peak
            _, _, left, right = BARS[i % len(BARS)]
            o.append(f'''  <g transform="translate({cx:.0f},{BASE})">
    <ellipse cx="0" cy="12" rx="50" ry="10" fill="url(#sh)"/>
    <g class="bar" style="animation-delay:{i * 0.5:.1f}s">
      <path d="M{-HW},{-h:.0f} L0,{HH - h:.0f} L0,{HH} L{-HW},0Z" fill="{left}"/>
      <path d="M{HW},{-h:.0f} L0,{HH - h:.0f} L0,{HH} L{HW},0Z" fill="{right}"/>
      <path d="M0,{-HH - h:.0f} L{HW},{-h:.0f} L0,{HH - h:.0f} L{-HW},{-h:.0f}Z" fill="url(#b{i % len(BARS)})"/>
    </g>
    <text class="sans" y="52" text-anchor="middle" font-size="15" font-weight="700" fill="{ink}">{name}</text>
    <text class="serif" y="74" text-anchor="middle" font-size="16" fill="{brand}">{share:.0%}</text>
  </g>''')
    o.append('</svg>')
    return "\n".join(o) + "\n"


if __name__ == "__main__":
    data = collect()
    (ASSETS / "stats.svg").write_text(render(data), encoding="utf-8", newline="\n")
    (ASSETS / "stats-dark.svg").write_text(render(data, dark=True), encoding="utf-8", newline="\n")
    print(data)
