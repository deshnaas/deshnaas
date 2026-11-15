"""Shared palette and SVG helpers for the profile README assets."""
from pathlib import Path
from xml.sax.saxutils import escape

ASSETS = Path(__file__).resolve().parent.parent / "assets"

NAVY = "#0C1424"
INK = "#060912"
PANEL = "#0E1626"
LINE = "#1E2A44"
GOLD = "#C9A961"
GOLD_LIGHT = "#E6D3A3"
GOLD_DEEP = "#A8873F"
BLUE = "#4C8DFF"
VIOLET = "#8B7CF6"
WHITE = "#F2F0EA"
MUTED = "#8D97AB"

SERIF = "Georgia, 'Times New Roman', Times, serif"
SANS = "'Segoe UI', -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif"

DEFS = f"""
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{NAVY}"/><stop offset="1" stop-color="{INK}"/>
  </linearGradient>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD_LIGHT}"/><stop offset="0.55" stop-color="{GOLD}"/><stop offset="1" stop-color="{GOLD_DEEP}"/>
  </linearGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="{GOLD}" stop-opacity="0.9"/><stop offset="1" stop-color="{GOLD}" stop-opacity="0"/>
  </linearGradient>
"""


def text(x, y, s, size, fill=WHITE, font=SANS, weight=400, spacing=0, anchor="start", extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
        f'fill="{fill}" letter-spacing="{spacing}" text-anchor="{anchor}" {extra}>{escape(s)}</text>'
    )


def svg(w, h, body, label, defs="", radius=18, stroke=LINE, stroke_opacity=1.0):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(label)}">\n<title>{escape(label)}</title>\n'
        f"<defs>{DEFS}{defs}</defs>\n"
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{radius}" fill="url(#bg)" '
        f'stroke="{stroke}" stroke-opacity="{stroke_opacity}" stroke-width="1.5"/>\n'
        f"{body}\n</svg>\n"
    )


def save(name, content):
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")
    print("wrote", name)
