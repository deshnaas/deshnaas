"""Generate the static (animated) SVG artwork used by README.md.

Run:  python scripts/build_assets.py
Edit the data blocks below (ACHIEVEMENTS, CONTACTS, SECTIONS) and re-run.
All motion is CSS/SMIL inside the SVGs, so it plays on GitHub with no scripts,
and is switched off for visitors who prefer reduced motion.
"""
import random

from theme import (BLUE, GOLD, GOLD_LIGHT, LINE, MUTED, PANEL, SERIF, VIOLET, WHITE,
                   save, shimmer, svg, text, waves)

# ----------------------------------------------------------------------------- data
ACHIEVEMENTS = [
    # file, kind, badge, headline, competition, description
    ("award-iot-day", "award", "1", "First Prize", "IOT DAY",
     "Placed first among the competing teams."),
    ("award-hackwith-bangalore", "award", "2", "Runner-Up", "HACKWITH BANGALORE",
     "Hosted at the Microsoft Bengaluru office."),
    ("recognition-guvi-buildathon", BLUE, None, "Top 2%", "GUVI INDIA AI IMPACT BUILDATHON",
     "Among 48,000 participants."),
    ("recognition-national-finalist", VIOLET, None, "2×", "NATIONAL HACKATHON FINALIST",
     "Two-time finalist at national-level hackathons."),
    ("recognition-mumbai-hacks", BLUE, None, "Top 3,000", "MUMBAI HACKS",
     "Selected from 30,000 applicants."),
    ("recognition-sih", VIOLET, None, "Top 15", "SMART INDIA HACKATHON",
     "Top 15 teams in the college internal round."),
]

CONTACTS = [
    # key, label, display value
    ("linkedin", "LINKEDIN", "in/deshnaa-suresh"),
    ("email", "EMAIL", "spdeshnaa@gmail.com"),
    ("portfolio", "PORTFOLIO", "personal-website-portfolio-umber.vercel.app"),
    ("github", "GITHUB", "github.com/deshnaas"),
]

SECTIONS = [
    ("achievements", "01", "ACHIEVEMENTS", "AWARDS & RECOGNITION"),
    ("about", "02", "ABOUT", "ENGINEERING PHILOSOPHY"),
    ("projects", "03", "FEATURED PROJECTS", "SELECTED WORK"),
    ("expertise", "04", "TECHNICAL EXPERTISE", "TOOLS OF THE TRADE"),
    ("analytics", "05", "GITHUB ANALYTICS", "ACTIVITY"),
]

ICONS = {
    "linkedin": '<rect x="2.5" y="2.5" width="19" height="19" rx="4"/><circle cx="7.6" cy="7.7" r="0.9" fill="currentColor"/>'
                '<path d="M7.6 10.8V17M11.6 17v-6.2M11.6 13.4c0-1.6 1.1-2.7 2.6-2.7s2.5 1 2.5 2.7V17"/>',
    "email": '<rect x="2.5" y="5" width="19" height="14" rx="2.5"/><path d="M3.4 6.6 12 13l8.6-6.4"/>',
    "portfolio": '<circle cx="12" cy="12" r="9.5"/><ellipse cx="12" cy="12" rx="4.2" ry="9.5"/><path d="M2.5 12h19"/>',
    "github": '<circle cx="7" cy="5.5" r="2.3"/><circle cx="7" cy="18.5" r="2.3"/><circle cx="17" cy="8" r="2.3"/>'
              '<path d="M7 7.8v8.4M17 10.3c0 4-10 2.2-10 5.9"/>',
}
STAR = "M0 -7 L1.6 -1.6 L7 0 L1.6 1.6 L0 7 L-1.6 1.6 L-7 0 L-1.6 -1.6Z"


def icon(key, x, y, size, color=GOLD_LIGHT):
    s = size / 24
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" color="{color}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</g>')


def up(delay):
    return f'class="up" style="animation-delay:{delay}s"'


GLOWS = f"""
  <radialGradient id="g1" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.30"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="g2" cx="0.5" cy="0.5" r="0.5">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.26"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1.1" fill="#FFFFFF" fill-opacity="0.045"/>
  </pattern>
"""


def atmosphere(w, h, r=18):
    """Dot grid plus two slowly drifting colour glows, clipped to the card."""
    return (f'<g clip-path="url(#frame)"><rect width="{w}" height="{h}" fill="url(#dots)"/>'
            f'<ellipse class="float" cx="{w * 0.86:.0f}" cy="{h * 0.08:.0f}" rx="{w * 0.42:.0f}" ry="{h * 0.75:.0f}" fill="url(#g1)"/>'
            f'<ellipse class="float" style="animation-duration:18s;animation-direction:alternate-reverse" '
            f'cx="{w * 0.1:.0f}" cy="{h:.0f}" rx="{w * 0.4:.0f}" ry="{h * 0.7:.0f}" fill="url(#g2)"/></g>')


def constellation(w, h, n=26, seed=7, link=210):
    """A drifting network of twinkling nodes — a nod to neural nets."""
    rnd = random.Random(seed)
    pts = [(rnd.uniform(30, w - 30), rnd.uniform(24, h - 24)) for _ in range(n)]
    out = '<g clip-path="url(#frame)"><g class="float" style="animation-duration:22s">'
    for i, (x1, y1) in enumerate(pts):
        for x2, y2 in pts[i + 1:]:
            if (x1 - x2) ** 2 + (y1 - y2) ** 2 < link ** 2:
                out += (f'<path d="M{x1:.0f} {y1:.0f}L{x2:.0f} {y2:.0f}" stroke="{BLUE}" stroke-width="0.8" '
                        f'class="breathe" style="animation-delay:{rnd.uniform(0, 4):.1f}s" stroke-opacity="0.22"/>')
    for x, y in pts:
        c = rnd.choice([BLUE, GOLD_LIGHT, VIOLET, WHITE])
        out += (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(1.4, 2.8):.1f}" fill="{c}" class="tw" '
                f'style="animation-delay:{rnd.uniform(0, 3.2):.1f}s;animation-duration:{rnd.uniform(2.4, 4.6):.1f}s"/>')
    return out + "</g></g>"


# ----------------------------------------------------------------------------- hero
def hero():
    w, h = 1200, 460
    defs = GLOWS + shimmer("shineW", WHITE, GOLD, w, dur=6, band=320)
    body = atmosphere(w, h) + constellation(w, h) + "".join([
        f'<g clip-path="url(#frame)">{waves(w, 432, GOLD, amp=12, opacity=0.3)}</g>',
        text(64, 70, "ENGINEERING PORTFOLIO", 14, GOLD, weight=600, spacing=6, extra=up(0)),
        text(1136, 70, "AI / ML  ·  VOICE AI  ·  IoT", 14, MUTED, weight=500, spacing=4, anchor="end", extra=up(0)),
        text(600, 212, "DESHNAA SURESH", 82, "url(#shineW)", SERIF, spacing=10, anchor="middle", extra=up(0.2)),
        f'<g {up(0.7)}><rect x="520" y="249" width="160" height="2" rx="1" fill="url(#gold)"/>'
        f'<circle r="3.2" cy="250" fill="{GOLD_LIGHT}"><animate attributeName="cx" values="520;680;520" dur="4s" '
        f'repeatCount="indefinite"/></circle></g>',
        text(600, 300, "AI/ML ENGINEER   |   TECHNOLOGY BUILDER   |   INNOVATION ENTHUSIAST", 17,
             GOLD_LIGHT, weight=600, spacing=3.5, anchor="middle", extra=up(1.0)),
        text(600, 362, "Building intelligent systems and practical AI-powered solutions", 25, "#C9CFDC",
             SERIF, anchor="middle", extra='font-style="italic" ' + up(1.4)),
        text(600, 398, "that solve real-world problems.", 25, "#C9CFDC", SERIF, anchor="middle",
             extra='font-style="italic" ' + up(1.7)),
    ])
    save("hero.svg", svg(w, h, body, "Deshnaa Suresh — AI/ML Engineer, Technology Builder, Innovation Enthusiast. "
                         "Building intelligent systems and practical AI-powered solutions that solve real-world problems.",
                         defs, stroke=GOLD, stroke_opacity=0.35, light=GOLD_LIGHT, light_dur=9))


# ----------------------------------------------------------------------------- section headers
def section(key, num, title, tag):
    w, h = 1200, 104
    body = "".join([
        text(44, 62, num, 30, GOLD, SERIF, extra='font-style="italic" class="breathe"'),
        text(104, 62, title, 32, "url(#shineW)", SERIF, spacing=5, extra=up(0.1)),
        text(1156, 58, tag, 13, MUTED, weight=600, spacing=4, anchor="end", extra=up(0.4)),
        '<rect x="44" y="84" width="1112" height="1.5" fill="url(#fade)"/>',
        f'<path d="M44 84.75H1156" stroke="{GOLD_LIGHT}" stroke-width="2.5" stroke-linecap="round" pathLength="100" '
        f'stroke-dasharray="5 95" class="run" style="animation-duration:5s"/>',
    ])
    save(f"section-{key}.svg", svg(w, h, body, f"{num} — {title.title()}",
                                   shimmer("shineW", WHITE, GOLD, w, dur=7), radius=14))


# ----------------------------------------------------------------------------- achievements
def award(name, badge, headline, competition, desc):
    w, h = 600, 360
    rnd = random.Random(name)
    sparkles = "".join(
        f'<path d="{STAR}" transform="translate({rnd.uniform(400, 566):.0f} {rnd.choice([rnd.uniform(108, 140), rnd.uniform(226, 330)]):.0f}) '
        f'scale({rnd.uniform(0.5, 1.1):.2f})" fill="{GOLD_LIGHT}" class="tw" '
        f'style="animation-delay:{rnd.uniform(0, 3):.1f}s;animation-duration:{rnd.uniform(2.2, 4):.1f}s"/>'
        for _ in range(9))
    body = "".join([
        f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#aw)" class="breathe"/>',
        f'<rect x="11" y="11" width="{w-22}" height="{h-22}" rx="11" fill="none" stroke="{GOLD}" stroke-opacity="0.22"/>',
        sparkles,
        text(46, 66, "AWARD", 14, GOLD, weight=700, spacing=6, extra=up(0)),
        f'<circle cx="528" cy="60" r="24" fill="{PANEL}" stroke="url(#gold)" stroke-width="1.5"/>',
        f'<circle cx="528" cy="60" r="31" fill="none" stroke="{GOLD}" stroke-opacity="0.7" stroke-width="1.2" '
        f'stroke-dasharray="2 7" stroke-linecap="round" class="spin"/>',
        text(528, 69, badge, 26, GOLD_LIGHT, SERIF, anchor="middle"),
        text(44, 190, headline, 80, "url(#shineG)", SERIF, extra=up(0.2)),
        text(46, 244, competition, 21, WHITE, weight=700, spacing=4.5, extra=up(0.5)),
        f'<rect x="46" y="266" width="64" height="2" fill="url(#gold)" {up(0.7)}/>',
        text(46, 308, desc, 18, "#B4BCCB", extra=up(0.8)),
    ])
    defs = (f'<radialGradient id="aw" cx="0.9" cy="0" r="0.9"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.2"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>'
            + shimmer("shineG", GOLD, "#FFF6DA", w, dur=4.5, band=220))
    save(f"{name}.svg", svg(w, h, body, f"Award: {headline}, {competition.title()}. {desc}", defs,
                            stroke=GOLD, stroke_opacity=0.8, light="#FFF1C4", light_dur=6))


def recognition(name, accent, headline, competition, desc):
    w, h = 600, 290
    body = "".join([
        f'<rect x="1" y="46" width="4" height="64" rx="2" fill="{accent}" class="breathe"/>',
        f'<circle cx="536" cy="56" r="5" fill="{accent}"/>',
        f'<circle cx="536" cy="56" r="5" fill="none" stroke="{accent}" stroke-width="1.5" class="ping" '
        f'style="animation-duration:3.2s"/>',
        text(46, 62, "RECOGNITION", 13, accent, weight=700, spacing=6, extra=up(0)),
        text(44, 158, headline, 66, "url(#shineW)", SERIF, extra=up(0.2)),
        text(46, 204, competition, 17, WHITE, weight=700, spacing=2.4, extra=up(0.5)),
        f'<rect x="46" y="222" width="48" height="2" fill="{accent}" {up(0.7)}/>',
        text(46, 258, desc, 17, MUTED, extra=up(0.8)),
    ])
    save(f"{name}.svg", svg(w, h, body, f"Recognition: {headline}, {competition.title()}. {desc}",
                            shimmer("shineW", WHITE, accent, w, dur=5.5, band=220), light=accent, light_dur=8))


# ----------------------------------------------------------------------------- voxera
def voxera():
    w, h = 1200, 440
    steps = ["Call", "Language", "Triage", "Safety check", "Care & referral", "Follow-up"]
    xs = [110 + i * 196 for i in range(6)]
    y = 340
    rnd = random.Random(3)
    # voice equaliser, top right
    eq = ""
    for i in range(34):
        bh = 18 + 62 * abs(rnd.gauss(0, 0.55)) + (26 if 10 < i < 24 else 0)
        bh = min(bh, 118)
        eq += (f'<rect x="{770 + i * 11}" y="{176 - bh / 2:.0f}" width="5" height="{bh:.0f}" rx="2.5" fill="url(#eqg)" '
               f'class="eq" style="animation-delay:{-rnd.uniform(0, 1.2):.2f}s;animation-duration:{rnd.uniform(0.7, 1.5):.2f}s"/>')
    nodes = f'<path d="M{xs[0]} {y}H{xs[-1]}" stroke="{LINE}" stroke-width="2"/>'
    nodes += (f'<path d="M{xs[0]} {y}H{xs[-1]}" stroke="{BLUE}" stroke-width="2" stroke-linecap="round" pathLength="100" '
              f'stroke-dasharray="6 94" stroke-dashoffset="100"><animate attributeName="stroke-dashoffset" '
              f'values="100;0" dur="7s" repeatCount="indefinite"/></path>')
    for i, (x, label) in enumerate(zip(xs, steps)):
        c = GOLD if label == "Safety check" else BLUE
        nodes += (f'<circle cx="{x}" cy="{y}" r="23" fill="none" stroke="{c}" stroke-width="2" class="ping" '
                  f'style="animation-delay:{i * 1.4:.1f}s"/>')
        nodes += f'<circle cx="{x}" cy="{y}" r="23" fill="{PANEL}" stroke="{c}" stroke-width="1.5"/>'
        nodes += text(x, y + 6, f"{i+1:02d}", 15, c, weight=600, anchor="middle")
        nodes += text(x, y + 58, label, 16, WHITE, weight=500, anchor="middle", extra=up(0.9 + i * 0.15))
    defs = (GLOWS + shimmer("shineW", WHITE, GOLD, 700, dur=5, band=260)
            + f'<linearGradient id="eqg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}"/>'
              f'<stop offset="1" stop-color="{VIOLET}"/></linearGradient>')
    body = atmosphere(w, h) + "".join([
        text(64, 72, "FLAGSHIP PROJECT", 14, GOLD, weight=700, spacing=6, extra=up(0)),
        text(1136, 72, "HEALTHCARE  ·  VOICE AI", 14, MUTED, weight=600, spacing=4, anchor="end", extra=up(0)),
        eq,
        text(60, 172, "VOXERA", 92, "url(#shineW)", SERIF, spacing=10, extra=up(0.2)),
        text(64, 222, "No app. No typing. No smartphone. Just a phone call.", 27, GOLD_LIGHT, SERIF,
             extra='font-style="italic" ' + up(0.5)),
        text(64, 260, "Multilingual, voice-first AI for rural healthcare navigation and care coordination.", 18,
             "#B4BCCB", extra=up(0.7)),
        nodes,
    ])
    save("voxera.svg", svg(w, h, body, "Voxera — multilingual, voice-first AI rural healthcare and care-coordination "
                           "platform. Call, language, triage, safety check, care and referral, follow-up.",
                           defs, stroke=GOLD, stroke_opacity=0.55, light=BLUE, light_dur=8))


# ----------------------------------------------------------------------------- contact
def pill(key, label):
    w, h = 216, 52
    body = icon(key, 24, 14, 24) + text(60, 31.5, label, 14, WHITE, weight=700, spacing=3.2)
    save(f"btn-{key}.svg", svg(w, h, body, label.title(), radius=26, stroke=GOLD, stroke_opacity=0.55,
                               light=GOLD_LIGHT, light_dur=4))


def contact_card(key, label, value):
    w, h = 600, 130
    body = "".join([
        f'<circle cx="76" cy="65" r="31" fill="{PANEL}" stroke="url(#gold)" stroke-width="1.5"/>',
        f'<circle cx="76" cy="65" r="38" fill="none" stroke="{GOLD}" stroke-opacity="0.65" stroke-width="1.2" '
        f'stroke-dasharray="2 8" stroke-linecap="round" class="spin"/>',
        icon(key, 61, 50, 30),
        text(132, 56, label, 14, GOLD, weight=700, spacing=5.5),
        text(132, 87, value, 18, WHITE),
        f'<path class="nudge" d="M544 65h18m-7-7 7 7-7 7" fill="none" stroke="{GOLD_LIGHT}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
    ])
    save(f"contact-{key}.svg", svg(w, h, body, f"{label.title()}: {value}", stroke=GOLD, stroke_opacity=0.4,
                                   light=GOLD_LIGHT, light_dur=6))


def contact_banner():
    w, h = 1200, 250
    defs = GLOWS + shimmer("shineW", WHITE, GOLD, w, dur=6) + shimmer("shineG", GOLD, "#FFF6DA", w, dur=6)
    body = atmosphere(w, h) + constellation(w, h, n=18, seed=11) + "".join([
        f'<g clip-path="url(#frame)">{waves(w, 226, GOLD, amp=10, opacity=0.28)}</g>',
        text(600, 66, "06  ·  CONTACT", 14, GOLD, weight=700, spacing=6, anchor="middle", extra=up(0)),
        text(600, 134, "LET’S CONNECT & BUILD", 46, "url(#shineW)", SERIF, spacing=6, anchor="middle", extra=up(0.2)),
        text(600, 194, "SOMETHING MEANINGFUL.", 46, "url(#shineG)", SERIF, spacing=6, anchor="middle", extra=up(0.5)),
    ])
    save("section-contact.svg", svg(w, h, body, "Let's connect & build something meaningful.", defs,
                                    stroke=GOLD, stroke_opacity=0.35, light=GOLD_LIGHT, light_dur=9))


if __name__ == "__main__":
    hero()
    for s in SECTIONS:
        section(*s)
    for name, kind, badge, headline, comp, desc in ACHIEVEMENTS:
        if kind == "award":
            award(name, badge, headline, comp, desc)
        else:
            recognition(name, kind, headline, comp, desc)
    voxera()
    for key, label, value in CONTACTS:
        pill(key, label)
        contact_card(key, label, value)
    contact_banner()
