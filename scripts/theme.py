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


ANIM = """<style>
.up{opacity:0;animation:up .9s cubic-bezier(.2,.7,.2,1) forwards}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.tw{animation:tw 3.2s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.12}50%{opacity:.95}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 16s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.run{animation:run 7s linear infinite}
@keyframes run{from{stroke-dashoffset:100}to{stroke-dashoffset:0}}
.eq{transform-box:fill-box;transform-origin:center;animation:eq 1.1s ease-in-out infinite alternate}
@keyframes eq{from{transform:scaleY(.18)}to{transform:scaleY(1)}}
.nudge{animation:nudge 1.8s ease-in-out infinite}
@keyframes nudge{0%,100%{transform:translateX(0)}50%{transform:translateX(7px)}}
.float{animation:float 14s ease-in-out infinite alternate}
@keyframes float{to{transform:translate(36px,-22px)}}
.wave{animation:wave 10s linear infinite}
@keyframes wave{to{transform:translateX(-600px)}}
.breathe{animation:breathe 4s ease-in-out infinite}
@keyframes breathe{0%,100%{opacity:.45}50%{opacity:1}}
.ping{transform-box:fill-box;transform-origin:center;opacity:0;animation:ping 7s ease-out infinite}
@keyframes ping{0%{opacity:.9;transform:scale(1)}14%{opacity:0;transform:scale(2.1)}100%{opacity:0;transform:scale(2.1)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.up{opacity:1}}
</style>"""


def shimmer(gid, base, hi, span, dur=5, band=280):
    """A highlight that sweeps left-to-right across anything filled with url(#gid)."""
    anim = (f'<animate attributeName="{{a}}" values="{{v0}};{{v1}};{{v1}}" keyTimes="0;0.55;1" '
            f'dur="{dur}s" repeatCount="indefinite"/>')
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{-band}" y1="0" x2="0" y2="0">'
            f'<stop offset="0" stop-color="{base}"/><stop offset="0.5" stop-color="{hi}"/>'
            f'<stop offset="1" stop-color="{base}"/>'
            + anim.format(a="x1", v0=-band, v1=span) + anim.format(a="x2", v0=0, v1=span + band)
            + "</linearGradient>")


def border_light(w, h, radius, color, dur=7, dash=9):
    """A soft light that travels around the card border."""
    rect = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{radius}" fill="none" stroke="{color}" '
            f'pathLength="100" stroke-dasharray="{dash} {100 - dash}" stroke-linecap="round" class="run" '
            f'style="animation-duration:{dur}s" ')
    return rect + 'stroke-width="5" stroke-opacity="0.18"/>' + rect + 'stroke-width="1.8"/>'


def waves(w, y, color, amp=14, opacity=0.35, dur=10, count=2):
    """Slow flowing sine lines; tile every 600px so the loop is seamless."""
    out = ""
    for i in range(count):
        a, yy = amp * (1 - 0.35 * i), y + 16 * i
        d = f"M0 {yy} q 75 {-a} 150 0" + " t 150 0" * ((w + 600) // 150)
        out += (f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity="{opacity * (1 - 0.4 * i):.2f}" '
                f'stroke-width="1.4" class="wave" style="animation-duration:{dur + 4 * i}s"/>')
    return out


def svg(w, h, body, label, defs="", radius=18, stroke=LINE, stroke_opacity=1.0, light=None, light_dur=7):
    glow = border_light(w, h, radius, light, light_dur) if light else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
        f'role="img" aria-label="{escape(label)}">' + "\n"
        f"<title>{escape(label)}</title>" + "\n"
        f'<defs>{DEFS}{defs}<clipPath id="frame"><rect x="1" y="1" width="{w - 2}" height="{h - 2}" '
        f'rx="{radius}"/></clipPath></defs>' + "\n" + ANIM + "\n"
        f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="{radius}" fill="url(#bg)" '
        f'stroke="{stroke}" stroke-opacity="{stroke_opacity}" stroke-width="1.5"/>' + "\n"
        + body + "\n" + glow + "\n</svg>\n"
    )


def save(name, content):
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / name).write_text(content, encoding="utf-8", newline="\n")
    print("wrote", name)
