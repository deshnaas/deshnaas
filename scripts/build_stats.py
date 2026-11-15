"""Generate the GitHub analytics SVGs from live public data (standard library only).

Run:  python scripts/build_stats.py
Uses the GraphQL API when GITHUB_TOKEN is set (as in the scheduled workflow); otherwise
reads the public contributions page. Nothing is estimated: every figure is computed from
the contribution calendar and the repository language statistics GitHub reports.
"""
import datetime as dt
import json
import os
import re
import urllib.request

from theme import BLUE, GOLD, GOLD_LIGHT, MUTED, SERIF, VIOLET, WHITE, save, svg, text

USER = os.environ.get("PROFILE_USER", "deshnaas")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
LEVELS = ["#121A2B", "#1D3566", "#2C56A6", "#4C8DFF", "#A9C8FF"]
LANG_COLORS = [BLUE, GOLD, VIOLET, GOLD_LIGHT, "#5B6B8C", "#A9C8FF"]


def http(url, data=None):
    headers = {"User-Agent": "profile-readme-stats", "Accept": "application/vnd.github+json"}
    if TOKEN and "api.github.com" in url:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8")


def calendar_graphql():
    q = ("query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{totalContributions "
         "weeks{contributionDays{date contributionCount}}}}}}")
    raw = http("https://api.github.com/graphql", json.dumps({"query": q, "variables": {"u": USER}}).encode())
    cal = json.loads(raw)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = {d["date"]: d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]}
    return days, cal["totalContributions"]


def calendar_html():
    page = http(f"https://github.com/users/{USER}/contributions")
    ids = dict(re.findall(r'<td[^>]*data-date="(\d{4}-\d\d-\d\d)"[^>]*id="([^"]+)"', page))
    tips = dict(re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>\s*([^<]*)', page))
    days = {}
    for date, cid in ids.items():
        m = re.match(r"(\d+) contribution", tips.get(cid, ""))
        days[date] = int(m.group(1)) if m else 0
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", page)
    total = int(m.group(1).replace(",", "")) if m else sum(days.values())
    return days, total


def calendar():
    if TOKEN:
        try:
            return calendar_graphql()
        except Exception as e:  # fall back to the public page
            print("graphql failed, using public page:", e)
    return calendar_html()


def active_days(days):
    return sum(1 for n in days.values() if n > 0)


def languages():
    repos = json.loads(http(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner"))
    totals = {}
    own = [r for r in repos if not r["fork"]]
    for r in own:
        for lang, n in json.loads(http(r["languages_url"])).items():
            totals[lang] = totals.get(lang, 0) + n
    return totals, len(repos)


def level(n, peak):
    if n == 0:
        return 0
    return min(4, 1 + int(3 * n / max(peak, 1) + 0.5)) if peak > 3 else min(4, n)


def contributions_svg(days, total):
    w, h = 1200, 300
    dates = sorted(dt.date.fromisoformat(d) for d in days)
    peak = max(days.values() or [0])
    first = dates[0] - dt.timedelta(days=(dates[0].weekday() + 1) % 7)  # back to Sunday
    cell, gap, x0, y0 = 15, 5, 96, 106
    body = [text(44, 56, f"{total:,}", 34, WHITE, SERIF),
            text(44 + 22 * len(f"{total:,}") + 8, 56, "contributions in the last year", 16, MUTED),
            ]
    seen_months = set()
    for d in dates:
        col, row = (d - first).days // 7, (d.weekday() + 1) % 7
        x, y = x0 + col * (cell + gap), y0 + row * (cell + gap)
        body.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3.5" '
                    f'class="up" style="animation-delay:{col * 0.03:.2f}s" '
                    f'fill="{LEVELS[level(days[d.isoformat()], peak)]}"/>')
        key = (d.year, d.month)
        if d.day <= 7 and row == 0 and key not in seen_months and col < 52:
            seen_months.add(key)
            body.append(text(x, y0 - 14, d.strftime("%b").upper(), 11, MUTED, weight=600, spacing=2))
    for row, name in ((1, "MON"), (3, "WED"), (5, "FRI")):
        body.append(text(44, y0 + row * (cell + gap) + 12, name, 11, MUTED, weight=600, spacing=2))
    lx = 1156 - 5 * 20 - 46
    body.append(text(lx - 10, 272, "LESS", 11, MUTED, weight=600, spacing=2, anchor="end"))
    for i, c in enumerate(LEVELS):
        body.append(f'<rect x="{lx + i * 20}" y="261" width="14" height="14" rx="3" fill="{c}"/>')
    body.append(text(lx + 5 * 20 + 4, 272, "MORE", 11, MUTED, weight=600, spacing=2))
    save("stats-contributions.svg", svg(w, h, "".join(body), f"{total} contributions in the last year",
                                        light=BLUE, light_dur=10))


def overview_svg(total, active, repos, langs):
    w, h = 600, 260
    items = [(f"{total:,}", "CONTRIBUTIONS · 12 MO"), (str(repos), "PUBLIC REPOSITORIES"),
             (str(active), "ACTIVE DAYS · 12 MO"), (str(langs), "LANGUAGES IN USE")]
    body = [text(44, 54, "ACTIVITY", 13, GOLD, weight=700, spacing=6)]
    for i, (value, label) in enumerate(items):
        x, y = 44 + (i % 2) * 270, 122 + (i // 2) * 84
        body.append(text(x, y, value, 40, WHITE, SERIF, extra=f'class="up" style="animation-delay:{0.2 + i * 0.2:.1f}s"'))
        body.append(text(x, y + 24, label, 11.5, MUTED, weight=600, spacing=2.2))
    save("stats-overview.svg", svg(w, h, "".join(body), "GitHub activity: " +
                                   ", ".join(f"{v} {l.lower()}" for v, l in items), light=GOLD_LIGHT, light_dur=8))


def languages_svg(totals):
    w, h = 600, 260
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    top, rest = ranked[:5], sum(n for _, n in ranked[5:])
    if rest:
        top.append(("Other", rest))
    grand = sum(n for _, n in top) or 1
    body = [text(44, 54, "LANGUAGES", 13, GOLD, weight=700, spacing=6),
            '<clipPath id="bar"><rect x="44" y="78" width="512" height="12" rx="6">'
            '<animate attributeName="width" from="0" to="512" dur="1.8s" fill="freeze"/></rect></clipPath>']
    x = 44.0
    for i, (lang, n) in enumerate(top):
        bw = 512 * n / grand
        body.append(f'<rect clip-path="url(#bar)" x="{x:.1f}" y="78" width="{bw + 0.5:.1f}" height="12" '
                    f'fill="{LANG_COLORS[i]}"/>')
        x += bw
        lx, ly = 44 + (i % 2) * 262, 134 + (i // 2) * 40
        body.append(f'<circle cx="{lx + 6}" cy="{ly - 5}" r="6" fill="{LANG_COLORS[i]}"/>')
        body.append(text(lx + 22, ly, lang, 16, WHITE, weight=500))
        body.append(text(lx + 222, ly, f"{100 * n / grand:.1f}%", 15, MUTED, anchor="end"))
    save("stats-languages.svg", svg(w, h, "".join(body), "Languages by code size: " +
                                    ", ".join(f"{l} {100 * n / grand:.1f}%" for l, n in top), light=BLUE, light_dur=8))


if __name__ == "__main__":
    days, total = calendar()
    if not days:
        raise SystemExit("no contribution data returned; keeping existing cards")
    active = active_days(days)
    totals, repos = languages()
    contributions_svg(days, total)
    overview_svg(total, active, repos, len(totals))
    languages_svg(totals)
    print(f"total={total} active_days={active} repos={repos} languages={len(totals)}")
