"""Generate the static SVG artwork used by README.md.

Run:  python scripts/build_assets.py
Edit the data blocks below (ACHIEVEMENTS, CONTACTS, SECTIONS) and re-run.
"""
from theme import (BLUE, GOLD, GOLD_LIGHT, LINE, MUTED, PANEL, SANS, SERIF, VIOLET, WHITE,
                   save, svg, text)

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


def icon(key, x, y, size, color=GOLD_LIGHT):
    s = size / 24
    return (f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{color}" color="{color}" '
            f'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">{ICONS[key]}</g>')


GLOWS = f"""
  <radialGradient id="g1" cx="0.88" cy="0.05" r="0.7">
    <stop offset="0" stop-color="{BLUE}" stop-opacity="0.24"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="g2" cx="0.08" cy="1" r="0.7">
    <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.2"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
  </radialGradient>
  <pattern id="dots" width="30" height="30" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1.1" fill="#FFFFFF" fill-opacity="0.045"/>
  </pattern>
"""


def atmosphere(w, h, r=18):
    return (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#dots)"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#g1)"/>'
            f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r}" fill="url(#g2)"/>')


# ----------------------------------------------------------------------------- hero
def hero():
    w, h = 1200, 460
    style = """<style>
      .rule{stroke-dasharray:160;stroke-dashoffset:160;animation:draw 1.6s ease-out .3s forwards}
      @keyframes draw{to{stroke-dashoffset:0}}
      @media (prefers-reduced-motion:reduce){.rule{animation:none;stroke-dashoffset:0}}
    </style>"""
    body = atmosphere(w, h) + style + "".join([
        text(64, 70, "ENGINEERING PORTFOLIO", 14, GOLD, weight=600, spacing=6),
        text(1136, 70, "AI / ML  ·  VOICE AI  ·  IoT", 14, MUTED, weight=500, spacing=4, anchor="end"),
        text(600, 212, "DESHNAA SURESH", 82, WHITE, SERIF, spacing=10, anchor="middle"),
        f'<path class="rule" d="M520 250h160" stroke="url(#gold)" stroke-width="2" fill="none"/>',
        text(600, 300, "AI/ML ENGINEER   |   TECHNOLOGY BUILDER   |   INNOVATION ENTHUSIAST", 17,
             GOLD_LIGHT, weight=600, spacing=3.5, anchor="middle"),
        text(600, 362, "Building intelligent systems and practical AI-powered solutions", 25, "#C9CFDC",
             SERIF, anchor="middle", extra='font-style="italic"'),
        text(600, 398, "that solve real-world problems.", 25, "#C9CFDC", SERIF, anchor="middle",
             extra='font-style="italic"'),
    ])
    save("hero.svg", svg(w, h, body, "Deshnaa Suresh — AI/ML Engineer, Technology Builder, Innovation Enthusiast. "
                         "Building intelligent systems and practical AI-powered solutions that solve real-world problems.",
                         GLOWS, stroke=GOLD, stroke_opacity=0.35))


# ----------------------------------------------------------------------------- section headers
def section(key, num, title, tag):
    w, h = 1200, 104
    body = "".join([
        text(44, 62, num, 30, GOLD, SERIF, extra='font-style="italic"'),
        text(104, 62, title, 32, WHITE, SERIF, spacing=5),
        text(1156, 58, tag, 13, MUTED, weight=600, spacing=4, anchor="end"),
        '<rect x="44" y="84" width="1112" height="1.5" fill="url(#fade)"/>',
    ])
    save(f"section-{key}.svg", svg(w, h, body, f"{num} — {title.title()}", radius=14))


# ----------------------------------------------------------------------------- achievements
def award(name, badge, headline, competition, desc):
    w, h = 600, 360
    body = "".join([
        f'<rect x="11" y="11" width="{w-22}" height="{h-22}" rx="11" fill="none" stroke="{GOLD}" stroke-opacity="0.22"/>',
        text(46, 66, "AWARD", 14, GOLD, weight=700, spacing=6),
        f'<circle cx="528" cy="60" r="24" fill="none" stroke="url(#gold)" stroke-width="1.5"/>',
        text(528, 69, badge, 26, GOLD_LIGHT, SERIF, anchor="middle"),
        text(44, 190, headline, 80, "url(#gold)", SERIF),
        text(46, 244, competition, 21, WHITE, weight=700, spacing=4.5),
        f'<rect x="46" y="266" width="64" height="2" fill="url(#gold)"/>',
        text(46, 308, desc, 18, "#B4BCCB"),
    ])
    defs = (f'<radialGradient id="aw" cx="0.9" cy="0" r="0.9"><stop offset="0" stop-color="{GOLD}" stop-opacity="0.16"/>'
            f'<stop offset="1" stop-color="{GOLD}" stop-opacity="0"/></radialGradient>')
    body = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="18" fill="url(#aw)"/>' + body
    save(f"{name}.svg", svg(w, h, body, f"Award: {headline}, {competition.title()}. {desc}", defs,
                            stroke=GOLD, stroke_opacity=0.8))


def recognition(name, accent, headline, competition, desc):
    w, h = 600, 290
    body = "".join([
        f'<rect x="1" y="46" width="4" height="64" rx="2" fill="{accent}"/>',
        text(46, 62, "RECOGNITION", 13, accent, weight=700, spacing=6),
        text(44, 158, headline, 66, WHITE, SERIF),
        text(46, 204, competition, 17, WHITE, weight=700, spacing=2.4),
        f'<rect x="46" y="222" width="48" height="2" fill="{accent}"/>',
        text(46, 258, desc, 17, MUTED),
    ])
    save(f"{name}.svg", svg(w, h, body, f"Recognition: {headline}, {competition.title()}. {desc}"))


# ----------------------------------------------------------------------------- voxera
def voxera():
    w, h = 1200, 440
    steps = ["Call", "Language", "Triage", "Safety check", "Care & referral", "Follow-up"]
    xs = [110 + i * 196 for i in range(6)]
    y = 340
    style = """<style>
      .pulse{animation:run 7s linear infinite}
      @keyframes run{from{transform:translateX(0)}to{transform:translateX(980px)}}
      @media (prefers-reduced-motion:reduce){.pulse{animation:none;opacity:0}}
    </style>"""
    nodes = f'<path d="M{xs[0]} {y}H{xs[-1]}" stroke="{LINE}" stroke-width="2"/>'
    nodes += f'<circle class="pulse" cx="{xs[0]}" cy="{y}" r="4" fill="{BLUE}"/>'
    for i, (x, label) in enumerate(zip(xs, steps)):
        c = GOLD if label == "Safety check" else BLUE
        nodes += f'<circle cx="{x}" cy="{y}" r="23" fill="{PANEL}" stroke="{c}" stroke-width="1.5"/>'
        nodes += text(x, y + 6, f"{i+1:02d}", 15, c, weight=600, anchor="middle")
        nodes += text(x, y + 58, label, 16, WHITE, weight=500, anchor="middle")
    body = atmosphere(w, h) + style + "".join([
        text(64, 72, "FLAGSHIP PROJECT", 14, GOLD, weight=700, spacing=6),
        text(1136, 72, "HEALTHCARE  ·  VOICE AI", 14, MUTED, weight=600, spacing=4, anchor="end"),
        text(60, 172, "VOXERA", 92, WHITE, SERIF, spacing=10),
        text(64, 222, "No app. No typing. No smartphone. Just a phone call.", 27, GOLD_LIGHT, SERIF,
             extra='font-style="italic"'),
        text(64, 260, "Multilingual, voice-first AI for rural healthcare navigation and care coordination.", 18,
             "#B4BCCB"),
        nodes,
    ])
    save("voxera.svg", svg(w, h, body, "Voxera — multilingual, voice-first AI rural healthcare and care-coordination "
                           "platform. Call, language, triage, safety check, care and referral, follow-up.",
                           GLOWS, stroke=GOLD, stroke_opacity=0.55))


# ----------------------------------------------------------------------------- contact
def pill(key, label):
    w, h = 216, 52
    body = icon(key, 24, 14, 24) + text(60, 31.5, label, 14, WHITE, weight=700, spacing=3.2)
    save(f"btn-{key}.svg", svg(w, h, body, label.title(), radius=26, stroke=GOLD, stroke_opacity=0.55))


def contact_card(key, label, value):
    w, h = 600, 130
    body = "".join([
        f'<circle cx="76" cy="65" r="31" fill="{PANEL}" stroke="url(#gold)" stroke-width="1.5"/>',
        icon(key, 61, 50, 30),
        text(132, 56, label, 14, GOLD, weight=700, spacing=5.5),
        text(132, 87, value, 18, WHITE),
        f'<path d="M548 65h18m-7-7 7 7-7 7" fill="none" stroke="{GOLD_LIGHT}" stroke-width="1.6" '
        f'stroke-linecap="round" stroke-linejoin="round"/>',
    ])
    save(f"contact-{key}.svg", svg(w, h, body, f"{label.title()}: {value}", stroke=GOLD, stroke_opacity=0.4))


def contact_banner():
    w, h = 1200, 250
    body = atmosphere(w, h) + "".join([
        text(600, 66, "06  ·  CONTACT", 14, GOLD, weight=700, spacing=6, anchor="middle"),
        text(600, 134, "LET’S CONNECT & BUILD", 46, WHITE, SERIF, spacing=6, anchor="middle"),
        text(600, 194, "SOMETHING MEANINGFUL.", 46, "url(#gold)", SERIF, spacing=6, anchor="middle"),
    ])
    save("section-contact.svg", svg(w, h, body, "Let's connect & build something meaningful.", GLOWS,
                                    stroke=GOLD, stroke_opacity=0.35))


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
