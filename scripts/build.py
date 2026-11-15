"""Regenerates the profile graphics in assets/.

    python scripts/build.py

- stack.svg, journey.svg, portrait.svg and contact.svg are generated here.
- hero.svg and deliver.svg are hand-written.
- Every graphic also gets a *-dark.svg twin for GitHub's dark theme.

Colour convention in the light files: text that should turn coral on dark
backgrounds uses the upper-case hex #C9151E; shapes use lower-case #c9151e.
"""
import base64
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "font-family:'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
SERIF = "font-family:'Instrument Serif',Georgia,'Times New Roman',serif;font-style:italic"

# light -> dark replacements for the substitution-based dark twins
DARK = {
    "#f2ecea": "#1b1113",  # card background
    "#241a1b": "#f6eeec",  # ink
    "#6d5f61": "#b7a6a8",  # muted text
    "#C9151E": "#ff7a80",  # brand-coloured text
    "#fdeeec": "#5a1a1f",  # big backdrop sphere
    "#f0cfcb": "#3d0f13",
    "#dba9a4": "#2a0a0d",
}

GRADS = """    <radialGradient id="red" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ef4a52"/><stop offset=".55" stop-color="#c9151e"/><stop offset="1" stop-color="#8f0d14"/></radialGradient>
    <radialGradient id="coral" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffa3a6"/><stop offset=".6" stop-color="#ff6b70"/><stop offset="1" stop-color="#e0444a"/></radialGradient>
    <radialGradient id="blush" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff3f1"/><stop offset=".6" stop-color="#f3d3cf"/><stop offset="1" stop-color="#d9a5a0"/></radialGradient>
    <linearGradient id="ring" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff9a9d"/><stop offset="1" stop-color="#e8474d"/></linearGradient>
    <radialGradient id="sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#5e0a10" stop-opacity=".24"/><stop offset="1" stop-color="#5e0a10" stop-opacity="0"/></radialGradient>"""

MOTION = """    .drift{animation:drift 9s ease-in-out infinite}
    .drift.x{animation-duration:12s;animation-delay:-5s}
    .bob{animation:bob 6s ease-in-out infinite}
    .flow{stroke-dasharray:4 9;animation:flow 1.4s linear infinite}
    @keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(6px,-12px)}}
    @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
    @keyframes flow{to{stroke-dashoffset:-26}}
    @keyframes tilt{0%,100%{transform:rotate(-8deg)}50%{transform:rotate(10deg) translateY(-8px)}}
    @media (prefers-reduced-motion:reduce){*{animation:none!important}}"""


def torus(cx, cy, rx=30, ry=19, w=20):
    return f"""<g style="animation:tilt 14s ease-in-out infinite;transform-origin:{cx}px {cy}px">
      <ellipse cx="{cx}" cy="{cy + 4}" rx="{rx}" ry="{ry}" fill="none" stroke="#b9353b" stroke-width="{w}" opacity=".35"/>
      <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="url(#ring)" stroke-width="{w}"/>
      <path d="M{cx - rx + 4},{cy - ry / 2:.0f} A{rx},{ry} 0 0 1 {cx + rx / 2:.0f},{cy - ry + 2}" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".55"/>
    </g>"""


def card(w, h, title, desc, body, defs=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="t d">
  <title id="t">{title}</title>
  <desc id="d">{desc}</desc>
  <defs>
    <clipPath id="card"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="28"/></clipPath>
{GRADS}
{defs}
  </defs>
  <style>
    .sans{{{SANS}}}
    .serif{{{SERIF}}}
{MOTION}
  </style>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="28" fill="#f2ecea"/>
{body}
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="28" fill="none" stroke="#241a1b" stroke-opacity=".14" stroke-width="2"/>
</svg>
"""


# ---------------------------------------------------------------- stack
def stack(dark=False):
    HW, HH, T, SX, SY, X0, Y0 = 96, 48, 16, 104, 52, 600, 96
    pal = {
        "sap": ("#e8373f", "#c9151e", "#9c0f16", "#6f0a10", "#ffffff"),
        "back": ("#ffa3a6", "#ff6b70", "#e04a50", "#b9353b", "#3d080c"),
        "mobile": ("#fffaf9", "#f1d6d2", "#dcb4af", "#c08f8a", "#3d080c"),
        "data": ("#4a3839", "#2a1e1f", "#1a1213", "#0e0909", "#fbf8f7"),
        "tools": ("#ffffff", "#f6efed", "#ddd0cd", "#c4b3b0", "#2a1e1f"),
    }
    if dark:
        pal["data"] = ("#8a676b", "#5f4447", "#463134", "#332325", "#fbf8f7")
    rows = [
        [("SAP ABAP", "sap"), ("Laravel", "back"), ("PHP", "back"), ("CodeIgniter", "back")],
        [("Node.js", "back"), ("REST APIs", "back"), ("Flutter", "mobile"), ("Dart", "mobile")],
        [("Vue.js", "mobile"), ("Ionic", "mobile"), ("MySQL", "data"), ("PostgreSQL", "data")],
        [("MariaDB", "data"), ("MongoDB", "data"), ("Linux", "tools"), ("Git", "tools")],
    ]
    legend = [("Enterprise &amp; SAP", "sap", 285), ("Backend", "back", 465), ("Mobile &amp; frontend", "mobile", 580),
              ("Data", "data", 770), ("Tools", "tools", 860)]
    bg, ink, muted = ("#1b1113", "#f6eeec", "#b7a6a8") if dark else ("#f2ecea", "#241a1b", "#6d5f61")
    names = ", ".join(n for r in rows for n, _ in r)
    o = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 560" width="1200" height="560" role="img" aria-labelledby="t d">',
         '  <title id="t">Tech stack of Md. Sazzadul Islam</title>',
         f'  <desc id="d">Isometric 3D grid of the technologies I work with: {names}.</desc>', '  <defs>']
    for k, (a, b, *_r) in pal.items():
        o.append(f'    <linearGradient id="{k}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')
    shade = "#000000" if dark else "#5e0a10"
    o.append(f'    <radialGradient id="sh" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{shade}" stop-opacity=".25"/><stop offset="1" stop-color="{shade}" stop-opacity="0"/></radialGradient>')
    o += ['  </defs>', '  <style>', f'    .sans{{{SANS}}}', '    .w{animation:w 5s ease-in-out infinite}']
    o += [f'    .w{d}{{animation-delay:{-5 + d * 0.4:.1f}s}}' for d in range(7)]
    o += ['    @keyframes w{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}',
          '    @media (prefers-reduced-motion:reduce){.w{animation:none}}', '  </style>',
          f'  <rect x="1" y="1" width="1198" height="558" rx="28" fill="{bg}" stroke="{ink}" stroke-opacity=".14" stroke-width="2"/>',
          f'  <ellipse cx="{X0}" cy="{Y0 + 3 * SY + 40}" rx="470" ry="230" fill="url(#sh)"/>']
    tiles = sorted((i + j, i, j, n, c) for j, row in enumerate(rows) for i, (n, c) in enumerate(row))
    for d, i, j, name, cat in tiles:
        cx, cy = X0 + (i - j) * SX, Y0 + (i + j) * SY
        _, _, left, right, tink = pal[cat]
        o += [f'  <g class="w w{d}"><g transform="translate({cx},{cy})">',
              f'    <path d="M{-HW},0 L0,{HH} L0,{HH + T} L{-HW},{T}Z" fill="{left}"/>',
              f'    <path d="M{HW},0 L0,{HH} L0,{HH + T} L{HW},{T}Z" fill="{right}"/>',
              f'    <path d="M0,{-HH} L{HW},0 L0,{HH} L{-HW},0Z" fill="url(#{cat})"/>',
              f'    <text class="sans" transform="matrix(.894,.447,-.894,.447,0,0)" text-anchor="middle" dy=".35em" font-size="17" font-weight="700" fill="{tink}">{name}</text>',
              '  </g></g>']
    o.append(f'  <g class="sans" font-size="14" fill="{muted}">')
    for label, cat, x in legend:
        o += [f'    <rect x="{x}" y="517" width="14" height="14" rx="4" fill="url(#{cat})" stroke="{ink}" stroke-opacity=".2"/>',
              f'    <text x="{x + 22}" y="529">{label}</text>']
    o += ['  </g>', '</svg>']
    return "\n".join(o) + "\n"


# -------------------------------------------------------------- journey
def journey():
    roles = [
        (2015.75, 2017.33, "Oct 2015 – Apr 2017", "Jr. Web Developer", "Ronova-it Ltd.", 26),
        (2017.33, 2019.25, "May 2017 – Mar 2019", "Software Developer", "ABH World", 36),
        (2019.25, 2021.58, "Apr 2019 – Jul 2021", "Sr. Executive, Software Engineer", "Super Star Group", 46),
        (2021.58, 2022.50, "Aug 2021 – Jul 2022", "Sr. Executive, Software Engineer", "Gemcon Group", 56),
        (2022.50, 2026.90, "Jul 2022 – now", "Deputy Manager (Project Manager)", "Super Star Group", 70),
    ]
    cols = [
        ("#fbe4e1", "#ecc5c0", "#dcb4af", "#c08f8a"),
        ("#ffc2c4", "#ff9397", "#f07075", "#cf4f55"),
        ("#ff8a8e", "#f2545a", "#d9363d", "#ae2228"),
        ("#f25a61", "#dc2f37", "#b81b23", "#8f1219"),
        ("#e8373f", "#c9151e", "#9c0f16", "#6f0a10"),
    ]
    T0, DX, DY = 2015.75, -46, 25

    def P(t):
        return 150 + 84 * (t - T0), 372 - 18 * (t - T0)

    defs = "\n".join(
        f'    <linearGradient id="j{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c[0]}"/><stop offset="1" stop-color="{c[1]}"/></linearGradient>'
        for i, c in enumerate(cols))
    b = []
    # ground shadow
    (sx0, sy0), (sx1, sy1) = P(T0), P(2026.9)
    b.append(f'  <path d="M{sx0 + DX:.0f},{sy0 + DY + 10:.0f} L{sx1 + DX:.0f},{sy1 + DY + 10:.0f}" stroke="#5e0a10" stroke-opacity=".07" stroke-width="26" stroke-linecap="round"/>')
    labels = []
    for i, (t0, t1, when, role, org, H) in enumerate(roles):
        t0g = t0 + (0.05 if i else 0)
        (ax, ay), (bx, by) = P(t0g), P(t1)
        _, _, front, end = cols[i]
        pts = lambda *p: " ".join(f"{x:.1f},{y:.1f}" for x, y in p)
        top = pts((ax, ay - H), (bx, by - H), (bx + DX, by + DY - H), (ax + DX, ay + DY - H))
        fr = pts((ax + DX, ay + DY - H), (bx + DX, by + DY - H), (bx + DX, by + DY), (ax + DX, ay + DY))
        en = pts((ax, ay - H), (ax + DX, ay + DY - H), (ax + DX, ay + DY), (ax, ay))
        b.append(f'  <g><polygon points="{en}" fill="{end}"/><polygon points="{fr}" fill="{front}"/><polygon points="{top}" fill="url(#j{i})"/></g>')
        mx, my = (ax + bx) / 2 + DX / 2, (ay + by) / 2 + DY / 2
        if i % 2 == 0:  # label above
            x, y = mx - (44 if i == len(roles) - 1 else 0), my - H - 18
            labels.append(f'  <path class="flow" d="M{x:.0f},{my - H:.0f} V{y + 4:.0f}" stroke="#C9151E" stroke-width="2" stroke-linecap="round"/>')
            y0 = y - 50
        else:  # label below
            x, y = (ax + bx) / 2 + DX, (ay + by) / 2 + DY
            labels.append(f'  <path class="flow" d="M{x:.0f},{y + 4:.0f} V{y + 40:.0f}" stroke="#C9151E" stroke-width="2" stroke-linecap="round"/>')
            y0 = y + 62
        labels.append(f'''  <g class="sans" text-anchor="middle" transform="translate({x:.0f},{y0:.0f})">
    <text class="serif" font-size="17" fill="#C9151E">{when}</text>
    <text y="21" font-size="15.5" font-weight="700" fill="#241a1b">{role}</text>
    <text y="40" font-size="13.5" fill="#6d5f61">{org}</text>
  </g>''')
    # "now" marker on the last bar
    (nx, ny) = P(2026.55)
    nx, ny = nx + DX / 2, ny + DY / 2 - roles[-1][5]
    b.append(f'  <ellipse cx="{nx:.0f}" cy="{ny:.0f}" rx="16" ry="6" fill="#3d080c" opacity=".3"/>')
    b.append(f'  <g class="bob"><circle cx="{nx:.0f}" cy="{ny - 24:.0f}" r="17" fill="url(#blush)"/><ellipse cx="{nx - 6:.0f}" cy="{ny - 31:.0f}" rx="5" ry="3" fill="#fff" opacity=".7" transform="rotate(-30 {nx - 6:.0f} {ny - 31:.0f})"/></g>')
    deco = f'''  <g clip-path="url(#card)">
    <circle class="drift x" cx="1180" cy="430" r="90" fill="url(#red)"/>
    <circle class="drift" cx="60" cy="60" r="26" fill="url(#coral)"/>
    {torus(1110, 300, 24, 15, 16)}
  </g>'''
    desc = "Isometric timeline of my roles. " + " ".join(f"{w}: {r}, {o}." for _, _, w, r, o, _ in roles)
    return card(1200, 470, "Career of Md. Sazzadul Islam, 2015 to now", desc, deco + "\n" + "\n".join(b + labels), defs)


# ------------------------------------------------------------- portrait
def portrait():
    img = base64.b64encode((ASSETS / "portrait.webp").read_bytes()).decode()
    arch = "M70,600 V240 A170,170 0 0 1 410,240 V600 Z"
    defs = f'''    <linearGradient id="arch" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbe4e1"/><stop offset="1" stop-color="#ecc5c0"/></linearGradient>
    <clipPath id="archClip"><path d="{arch}"/></clipPath>'''
    body = f'''  <g clip-path="url(#card)">
    <circle class="drift x" cx="40" cy="70" r="74" fill="url(#red)"/>
    <path d="{arch}" fill="#c08f8a" transform="translate(14,12)" opacity=".55"/>
    <path d="{arch}" fill="url(#arch)"/>
    <g clip-path="url(#archClip)">
      <path d="{arch}" fill="url(#arch)"/>
      <image x="20" y="96" width="440" height="550" preserveAspectRatio="xMidYMin slice" style="mix-blend-mode:multiply" href="data:image/webp;base64,{img}"/>
    </g>
    <path d="{arch}" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="3"/>
    {torus(424, 150, 28, 18, 18)}
    <circle class="drift" cx="48" cy="420" r="20" fill="url(#coral)"/>
    <circle class="drift x" cx="440" cy="452" r="30" fill="url(#blush)"/>
    <g class="bob">
      <rect x="110" y="527" width="260" height="46" rx="23" fill="#6f0a10"/>
      <rect x="110" y="520" width="260" height="46" rx="23" fill="#c9151e"/>
      <text class="sans" x="240" y="549" text-anchor="middle" font-size="16.5" font-weight="700" fill="#fff">Sazzadul · Dhaka, Bangladesh</text>
    </g>
  </g>'''
    return card(480, 600, "Portrait of Md. Sazzadul Islam", "Md. Sazzadul Islam, software engineer and project manager, Dhaka, Bangladesh.", body, defs)


# -------------------------------------------------------------- contact
def contact():
    body = f'''  <g clip-path="url(#card)">
    <ellipse cx="1000" cy="226" rx="170" ry="20" fill="url(#sh)"/>
    <circle class="drift x" cx="1010" cy="118" r="82" fill="url(#red)"/>
    <ellipse cx="982" cy="84" rx="22" ry="12" fill="#fff" opacity=".28" transform="rotate(-30 982 84)"/>
    <circle class="drift" cx="1128" cy="176" r="40" fill="url(#blush)"/>
    <circle class="drift" cx="902" cy="188" r="22" fill="url(#coral)"/>
    {torus(1120, 62, 28, 18, 18)}
    <g class="bob"><g transform="translate(868,54)">
      <path d="M-26,0 L0,13 L0,43 L-26,30Z" fill="#e04a50"/>
      <path d="M26,0 L0,13 L0,43 L26,30Z" fill="#b9353b"/>
      <path d="M0,-13 L26,0 L0,13 L-26,0Z" fill="#ffa3a6"/>
    </g></g>
  </g>
  <text class="serif" x="64" y="98" font-size="40" fill="#C9151E">Have a process that should be software?</text>
  <text class="sans" x="64" y="134" font-size="16.5" fill="#6d5f61">ERP, SAP integration, sales automation or mobile apps. I'm glad to talk.</text>
  <g class="sans">
    <rect x="64" y="169" width="232" height="46" rx="23" fill="#6f0a10"/>
    <rect x="64" y="162" width="232" height="46" rx="23" fill="#c9151e"/>
    <text x="180" y="191" text-anchor="middle" font-size="16.5" font-weight="700" fill="#fff">Get in touch  →</text>
    <text x="318" y="191" font-size="15.5" fill="#241a1b">sazzadul.com</text>
  </g>'''
    return card(1200, 250, "Get in touch with Md. Sazzadul Islam",
                "Have a process that should be software? ERP, SAP integration, sales automation or mobile apps. Get in touch at sazzadul.com.", body)


def darken(svg):
    for a, b in DARK.items():
        svg = svg.replace(a, b)
    return svg


def write(name, text):
    (ASSETS / name).write_text(text, encoding="utf-8", newline="\n")
    print(f"{name:22} {len(text) / 1024:6.1f} KB")


if __name__ == "__main__":
    write("stack.svg", stack())
    write("stack-dark.svg", stack(dark=True))
    for name, make in (("journey", journey), ("portrait", portrait), ("contact", contact)):
        write(f"{name}.svg", make())
    for name in ("hero", "deliver", "journey", "portrait", "contact"):
        write(f"{name}-dark.svg", darken((ASSETS / f"{name}.svg").read_text(encoding="utf-8")))
