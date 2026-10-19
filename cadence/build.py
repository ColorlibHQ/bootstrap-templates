#!/usr/bin/env python3
"""
Generates Cadence: a CRM dashboard.

STAGES and DEALS are declared once and drive the board, the overview figures,
the reports and the deal page — so the pipeline total on one screen can never
disagree with the pipeline total on another.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
TITLE = "Cadence"

# key, label, win probability %, days a deal is expected to sit here
#
# The probability is what makes a weighted forecast possible, and the expected
# age is what lets the board flag a deal as stalled rather than just old.
STAGES = [
    ("lead", "Lead", 10, 14),
    ("qualified", "Qualified", 25, 21),
    ("proposal", "Proposal", 50, 21),
    ("negotiation", "Negotiation", 75, 14),
    ("won", "Closed won", 100, 0),
]

# company, contact, value (£), stage, days in stage, owner initials
#
# Days-in-stage rather than a fixed date on purpose: a hardcoded 2026 date makes
# every deal in the demo look years stale the moment the year turns, whereas
# "9 days in this stage" stays plausible forever.
DEALS = [
    ("Northwind Logistics", "Priya Raman", 48000, "negotiation", 6, "DA"),
    ("Palisade Health", "Tom Beckwith", 126000, "negotiation", 19, "RW"),
    ("Kettle & Co", "Rae Whitcombe", 18500, "proposal", 4, "DA"),
    ("Brightsea Marine", "Josephine Marr", 74000, "proposal", 27, "JM"),
    ("Ordinal Systems", "Wes Tremayne", 32000, "proposal", 11, "RW"),
    ("Meridian Labs", "Nadia Osei", 96000, "qualified", 8, "DA"),
    ("Halden Brewing", "Ivan Kazlouski", 12750, "qualified", 30, "JM"),
    ("Fenwick Partners", "Marit Halvorsen", 55000, "qualified", 3, "RW"),
    ("Cobalt Interiors", "Dilan Aksoy", 21000, "lead", 2, "JM"),
    ("Ashgrove Schools", "Anna Oyelaran", 39500, "lead", 17, "DA"),
    ("Trent & Vale", "Sofia Marchetti", 8400, "lead", 1, "RW"),
    ("Latimer Retail", "Gregor Fyfe", 64000, "lead", 9, "JM"),
    ("Silverbrook Foods", "Elena Popova", 87000, "won", 2, "DA"),
    ("Windmill Studios", "Casey Nolan", 29000, "won", 5, "RW"),
]

OWNERS = {"DA": "Dilan Aksoy", "RW": "Rae Whitcombe", "JM": "Josephine Marr"}

CONTACTS = [
    ("Priya Raman", "Head of Ops", "Northwind Logistics", "priya@northwind.example", "+44 161 496 0118", "Customer", "DA"),
    ("Tom Beckwith", "CTO", "Palisade Health", "tom@palisade.example", "+44 20 7946 0332", "Opportunity", "RW"),
    ("Rae Whitcombe", "Founder", "Kettle & Co", "rae@kettleco.example", "+44 113 496 0771", "Opportunity", "DA"),
    ("Josephine Marr", "Procurement", "Brightsea Marine", "j.marr@brightsea.example", "+44 1752 496 220", "Opportunity", "JM"),
    ("Wes Tremayne", "Product Lead", "Ordinal Systems", "wes@ordinal.example", "+44 131 496 0904", "Opportunity", "RW"),
    ("Nadia Osei", "Design Lead", "Meridian Labs", "nadia@meridianlabs.example", "+44 20 7946 0518", "Lead", "DA"),
    ("Ivan Kazlouski", "Owner", "Halden Brewing", "ivan@halden.example", "+44 191 496 0663", "Lead", "JM"),
    ("Marit Halvorsen", "Finance Director", "Fenwick Partners", "marit@fenwick.example", "+44 20 7946 0140", "Opportunity", "RW"),
    ("Dilan Aksoy", "Studio Manager", "Cobalt Interiors", "dilan@cobalt.example", "+44 161 496 0287", "Lead", "JM"),
    ("Anna Oyelaran", "Business Manager", "Ashgrove Schools", "a.oyelaran@ashgrove.example", "+44 121 496 0455", "Lead", "DA"),
    ("Sofia Marchetti", "Buyer", "Trent & Vale", "sofia@trentvale.example", "+44 115 496 0910", "Lead", "RW"),
    ("Gregor Fyfe", "Head of Retail", "Latimer Retail", "gregor@latimer.example", "+44 141 496 0362", "Lead", "JM"),
]

ACTIVITY = [
    ("call", "Rae Whitcombe", "Kettle & Co", "Walked through the proposal. Wants the annual option costed before Thursday.", "12 minutes ago"),
    ("email", "Tom Beckwith", "Palisade Health", "Sent revised terms — legal has the redlines back.", "1 hour ago"),
    ("stage", "Nadia Osei", "Meridian Labs", "Moved from Lead to Qualified.", "3 hours ago"),
    ("note", "Josephine Marr", "Brightsea Marine", "Budget confirmed but the decision slips to next quarter.", "Yesterday"),
    ("meeting", "Marit Halvorsen", "Fenwick Partners", "Discovery call booked for Tuesday, 30 minutes.", "Yesterday"),
    ("won", "Elena Popova", "Silverbrook Foods", "Closed won — £87,000, 24-month term.", "2 days ago"),
]

TASKS = [
    ("Cost the annual option for Kettle & Co", "Today, 4:00pm", True),
    ("Chase legal on Palisade redlines", "Today, 5:30pm", True),
    ("Discovery call — Fenwick Partners", "Tomorrow, 10:00am", False),
    ("Send case study to Ashgrove", "Thursday", False),
    ("Quarterly review with Northwind", "Friday, 2:00pm", False),
]

NAV = [
    ("index.html", "Overview", "grid"),
    ("pipeline.html", "Pipeline", "board"),
    ("contacts.html", "Contacts", "people"),
    ("reports.html", "Reports", "chart"),
    ("settings.html", "Settings", "cog"),
]

ICON = {
    "grid": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="2" width="5" height="5" rx="1"/><rect x="9" y="2" width="5" height="5" rx="1"/><rect x="2" y="9" width="5" height="5" rx="1"/><rect x="9" y="9" width="5" height="5" rx="1"/></svg>',
    "board": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="2.5" width="3.5" height="11" rx="1"/><rect x="6.5" y="2.5" width="3.5" height="7" rx="1"/><rect x="11" y="2.5" width="3" height="9" rx="1"/></svg>',
    "people": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="6" cy="5.5" r="2.5"/><path d="M1.5 14a4.5 4.5 0 0 1 9 0"/><path d="M11 3.2a2.5 2.5 0 0 1 0 4.6M12 14a4.5 4.5 0 0 0-1.6-3.4"/></svg>',
    "chart": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M2 13.5V9M6 13.5V4M10 13.5V7M14 13.5V2.5"/></svg>',
    "cog": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="8" cy="8" r="2.25"/><path d="M8 1.5v1.6M8 12.9v1.6M14.5 8h-1.6M3.1 8H1.5m10.1-4.6-1.1 1.1M5.5 10.5l-1.1 1.1m0-8.2 1.1 1.1m5 5 1.1 1.1"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5 14 14" stroke-linecap="round"/></svg>',
    "bell": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 6.5a4 4 0 0 1 8 0c0 3 1 4 1 4H3s1-1 1-4Z"/><path d="M6.5 13a1.6 1.6 0 0 0 3 0"/></svg>',
    "plus": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M8 3.5v9M3.5 8h9"/></svg>',
    "call": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 3.5c0-.6.4-1 1-1h1.6c.4 0 .8.3.9.7l.6 2c.1.4 0 .8-.4 1l-1 .7a8 8 0 0 0 3.4 3.4l.7-1c.2-.3.6-.5 1-.4l2 .6c.4.1.7.5.7.9V12c0 .6-.4 1-1 1A10 10 0 0 1 3 3.5Z"/></svg>',
    "email": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="1.5" y="3.5" width="13" height="9" rx="1.5"/><path d="m2 4.5 6 4 6-4"/></svg>',
    "stage": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M2 8h9M8 4.5 11.5 8 8 11.5M13 4v8"/></svg>',
    "note": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M3 2.5h7L13 5.5v8H3z"/><path d="M5.5 8h5M5.5 10.5h3"/></svg>',
    "meeting": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="3" width="12" height="11" rx="1.5"/><path d="M2 6.5h12M5.5 1.5v3M10.5 1.5v3"/></svg>',
    "won": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="m3 8.5 3.5 3.5L13 5"/></svg>',
}

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""


def gbp(n):
    return f"£{n:,.0f}"


def short(n):
    return f"£{n / 1000:.0f}k" if n < 1_000_000 else f"£{n / 1_000_000:.2f}m"


HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Bootstrap 6, bundled in assets/vendor/bootstrap6 (version in the JS bundle header). To load it from jsDelivr instead, replace both paths below with https://cdn.jsdelivr.net/npm/bootstrap@VERSION/dist/... -->
<link rel="stylesheet" href="assets/vendor/bootstrap6/css/bootstrap.min.css">
<script type="importmap">{{"imports": {{"bootstrap": "./assets/vendor/bootstrap6/js/bootstrap.bundle.min.js"}}}}</script>
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
"""


def nav_links(current, drawer=False):
    cls = "drawer-link" if drawer else "side-link"
    out = []
    for href, label, icon in NAV:
        active = " is-active" if href == current else ""
        aria = ' aria-current="page"' if href == current else ""
        out.append(f'<a class="{cls}{active}" href="{href}"{aria}>{ICON[icon]}<span>{label}</span></a>')
    return "\n      ".join(out)


def shell(current, title, subtitle, body, *, actions=""):
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-3" href="#main">Skip to main content</a>

<div class="app">

  <aside class="side" id="side">
    <a class="side-brand" href="index.html">
      <span class="side-mark" aria-hidden="true">C</span><span>{TITLE}</span>
    </a>
    <p class="side-label mb-0">Sell</p>
      {nav_links(current)}
    <div class="side-foot">
      <span class="avatar avatar-sm"><span class="avatar-initials">DA</span></span>
      <span class="side-who"><strong>Dilan Aksoy</strong><small>Account executive</small></span>
    </div>
  </aside>

  <div class="main-col">
    <header class="topbar">
      <button class="btn-icon lg:d-none" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
        <span class="navbar-toggler-icon" aria-hidden="true"></span>
      </button>
      <button class="btn-icon d-none lg:d-inline-flex" type="button" id="railToggle" aria-label="Collapse sidebar" aria-pressed="false">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="3" width="12" height="10" rx="1.5"/><path d="M6.5 3v10"/></svg>
      </button>

      <div class="form-control form-adorn search-field d-none md:d-flex">
        <div class="form-adorn-icon">{ICON['search']}</div>
        <input type="search" class="form-ghost" placeholder="Search deals, companies, people…" aria-label="Search">
      </div>

      <div class="d-flex align-items-center gap-3 ms-auto">
        {TOGGLE}
        <button class="btn-icon" type="button" aria-label="Notifications">{ICON['bell']}</button>
        <button class="btn-icon p-0" type="button" data-bs-toggle="menu" aria-expanded="false" aria-label="Account menu">
          <span class="avatar avatar-sm"><span class="avatar-initials">DA</span></span>
        </button>
        <div class="menu">
          <a class="menu-item" href="settings.html">Settings</a>
          <a class="menu-item" href="reports.html">My reports</a>
          <hr class="menu-divider">
          <a class="menu-item" href="index.html">Sign out</a>
        </div>
      </div>
    </header>

    <main id="main" class="page">
      <div class="page-head">
        <div>
          <h1 class="page-title">{title}</h1>
          <p class="page-sub mb-0">{subtitle}</p>
        </div>
        <div class="page-actions">{actions}</div>
      </div>
{body}
    </main>
  </div>
</div>

<dialog class="drawer drawer-start" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
  <div class="drawer-header">
    <h5 class="drawer-title" id="navDrawerLabel">{TITLE}</h5>
    <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
  </div>
  <div class="drawer-body">
      {nav_links(current, drawer=True)}
  </div>
</dialog>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page(current, file, title, subtitle, body, *, actions="", desc=""):
    html = HEAD.format(title=f"{title} — {TITLE} Bootstrap 6 CRM Dashboard", desc=desc) \
        + shell(current, title, subtitle, body, actions=actions)
    (ROOT / file).write_text(html, encoding="utf-8")


# ------------------------------------------------------------------ pieces

def stat(label, figure, delta, direction, note):
    arrow = "▲" if direction == "up" else "▼"
    return f"""      <article class="kpi">
        <p class="kpi-label mb-1">{label}</p>
        <p class="kpi-figure mb-1">{figure}</p>
        <p class="kpi-delta mb-0 is-{direction}"><span aria-hidden="true">{arrow}</span> {delta} <span class="fg-3">{note}</span></p>
      </article>"""


def deal_card(company, contact, value, stage, days, owner, idx):
    """One board card. Everything the maths needs travels on the element, so the
    script never keeps a parallel copy of the data that could drift."""
    expected = dict((s[0], s[3]) for s in STAGES)[stage]
    stalled = expected and days > expected
    return f"""          <article class="deal" draggable="true" tabindex="0" data-deal="d{idx}" data-value="{value}" data-days="{days}" aria-label="{company}, {gbp(value)}">
            <div class="deal-top">
              <h3 class="deal-co">{company}</h3>
              <span class="avatar avatar-xs" title="{OWNERS[owner]}"><span class="avatar-initials">{owner}</span></span>
            </div>
            <p class="deal-value mb-3">{gbp(value)}</p>
            <p class="deal-contact mb-0">{contact}</p>
            <div class="deal-foot">
              <span class="deal-age{' is-stalled' if stalled else ''}">{days}d in stage</span>
              <span class="deal-move">
                <button class="deal-btn" type="button" data-move="-1" aria-label="Move {company} back a stage">&larr;</button>
                <button class="deal-btn" type="button" data-move="1" aria-label="Move {company} forward a stage">&rarr;</button>
              </span>
            </div>
          </article>"""


def board():
    cols = []
    for key, label, prob, expected in STAGES:
        cards = [deal_card(*d, i) for i, d in enumerate(DEALS) if d[3] == key]
        # The closed column is a destination, not part of open pipeline — the
        # totals above the board must not count money already banked.
        closed = ' data-closed' if key == "won" else ''
        cols.append(f"""      <section class="col-stage{' is-closed' if key == 'won' else ''}" data-stage="{key}" data-prob="{prob}" data-expected="{expected}"{closed}>
        <header class="stage-head">
          <div>
            <h2 class="stage-name">{label}</h2>
            <p class="stage-meta mb-0"><span data-stage-count>0</span> deals &middot; <span data-stage-sum>—</span></p>
          </div>
          <span class="stage-prob" title="Win probability applied to this stage">{prob}%</span>
        </header>
        <div class="stage-drop" data-drop>
{chr(10).join(cards)}
        </div>
      </section>""")
    return "\n".join(cols)


def area_chart(points, *, w=620, h=180, pad=6):
    lo, hi = min(points), max(points)
    span = (hi - lo) or 1
    step = (w - pad * 2) / (len(points) - 1)
    xy = [(pad + i * step, h - pad - ((v - lo) / span) * (h - pad * 2.4)) for i, v in enumerate(points)]
    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(xy))
    area = line + f" L{xy[-1][0]:.1f},{h} L{xy[0][0]:.1f},{h} Z"
    return f"""<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Weighted pipeline over the last twelve weeks" preserveAspectRatio="none">
        <defs><linearGradient id="cadFill" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="var(--bs-primary-base)" stop-opacity=".28"/>
          <stop offset="100%" stop-color="var(--bs-primary-base)" stop-opacity="0"/>
        </linearGradient></defs>
        <path d="{area}" fill="url(#cadFill)"/>
        <path d="{line}" fill="none" stroke="var(--bs-primary-base)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke"/>
      </svg>"""


def funnel():
    """Stage-by-stage conversion, drawn as nested bars rather than a chart
    library. Widths come from the deal data, so it cannot disagree with the board."""
    rows = []
    for key, label, prob, _ in STAGES:
        ds = [d for d in DEALS if d[3] == key]
        total = sum(d[2] for d in ds)
        rows.append((label, len(ds), total, prob))
    peak = max(r[2] for r in rows) or 1
    out = []
    for label, n, total, prob in rows:
        pct = round(total / peak * 100)
        out.append(f"""        <div class="funnel-row">
          <p class="funnel-label mb-0">{label}<span class="fg-3"> · {n}</span></p>
          <div class="funnel-track"><div class="funnel-bar" style="--w:{pct}%"></div></div>
          <p class="funnel-value mb-0">{short(total)}</p>
          <p class="funnel-prob mb-0 fg-3">{prob}%</p>
        </div>""")
    return "\n".join(out)


def activity_feed(limit=None):
    out = []
    for kind, who, co, text, when in ACTIVITY[:limit]:
        out.append(f"""        <li class="act">
          <span class="act-icon act-{kind}" aria-hidden="true">{ICON[kind]}</span>
          <div>
            <p class="act-head mb-1"><strong>{who}</strong> <span class="fg-3">· {co}</span></p>
            <p class="act-text mb-1">{text}</p>
            <p class="act-when mb-0">{when}</p>
          </div>
        </li>""")
    return "\n".join(out)


# ------------------------------------------------------------------- pages

def page_index():
    open_deals = [d for d in DEALS if d[3] != "won"]
    total = sum(d[2] for d in open_deals)
    weighted = sum(d[2] * dict((s[0], s[2]) for s in STAGES)[d[3]] / 100 for d in open_deals)
    won = sum(d[2] for d in DEALS if d[3] == "won")

    body = f"""
      <div class="kpi-row">
{stat("Open pipeline", short(total), "8.2%", "up", "vs last month")}
{stat("Weighted forecast", short(weighted), "3.1%", "up", "at current stage odds")}
{stat("Closed this month", short(won), "12.4%", "up", "2 deals")}
{stat("Average cycle", "38 days", "4 days", "down", "lead to close")}
      </div>

      <div class="grid-2">
        <section class="card">
          <header class="card-head">
            <div><h2 class="card-title">Weighted pipeline</h2><p class="card-sub mb-0">Last twelve weeks</p></div>
            <span class="chip">Rolling</span>
          </header>
          <div class="card-body">
            {area_chart([382, 401, 396, 428, 447, 439, 462, 488, 471, 503, 528, 541])}
            <div class="chart-axis"><span>12w ago</span><span>8w</span><span>4w</span><span>Now</span></div>
          </div>
        </section>

        <section class="card">
          <header class="card-head">
            <div><h2 class="card-title">Pipeline by stage</h2><p class="card-sub mb-0">Value and win probability</p></div>
            <a class="btn-text theme-secondary btn-sm" href="pipeline.html">Open board</a>
          </header>
          <div class="card-body">
            <div class="funnel">
{funnel()}
            </div>
          </div>
        </section>
      </div>

      <div class="grid-2">
        <section class="card">
          <header class="card-head">
            <div><h2 class="card-title">Recent activity</h2><p class="card-sub mb-0">Across your accounts</p></div>
          </header>
          <div class="card-body">
            <ul class="act-list">
{activity_feed(5)}
            </ul>
          </div>
        </section>

        <section class="card">
          <header class="card-head">
            <div><h2 class="card-title">Today and next</h2><p class="card-sub mb-0"><span data-task-open>0</span> still open</p></div>
            <button class="btn-outline theme-secondary btn-sm" type="button">{ICON['plus']} Task</button>
          </header>
          <div class="card-body">
            <ul class="task-list" data-tasks>
{chr(10).join(f'''              <li class="task">
                <input type="checkbox" class="check" id="t{i}">
                <label for="t{i}"><span class="task-text">{t}</span><span class="task-when{' is-due' if due else ''}">{when}</span></label>
              </li>''' for i, (t, when, due) in enumerate(TASKS))}
            </ul>
          </div>
        </section>
      </div>
"""
    page("index.html", "index.html", "Overview", "Your pipeline at a glance, Monday 28 July.", body,
         actions=f'<button class="btn-solid theme-primary" type="button">{ICON["plus"]} New deal</button>',
         desc="Cadence is a free Bootstrap 6 CRM dashboard template with a weighted pipeline board, contacts, reports and settings.")


def page_pipeline():
    body = f"""
      <div class="board-bar">
        <div class="board-figs">
          <div><p class="bf-k mb-0">Open pipeline</p><p class="bf-v mb-0" data-board-total>—</p></div>
          <div><p class="bf-k mb-0">Weighted forecast</p><p class="bf-v is-brand mb-0" data-board-weighted>—</p></div>
          <div><p class="bf-k mb-0">Open deals</p><p class="bf-v mb-0" data-board-count>—</p></div>
          <div><p class="bf-k mb-0">Stalled</p><p class="bf-v is-warn mb-0" data-board-stalled>—</p></div>
        </div>
        <p class="board-hint mb-0">
          Drag a deal between stages, or focus one and use <kbd>&larr;</kbd> <kbd>&rarr;</kbd>.
          Every figure above recalculates as it moves.
        </p>
      </div>

      <div class="board" data-board>
{board()}
      </div>
"""
    page("pipeline.html", "pipeline.html", "Pipeline", "Five stages, weighted by the odds of each one closing.", body,
         actions=f'<button class="btn-solid theme-primary" type="button">{ICON["plus"]} New deal</button>',
         desc="A weighted CRM pipeline board: drag or keyboard-move a deal and the forecast recalculates from each stage's win probability.")


def page_contacts():
    rows = "\n".join(f"""            <tr>
              <th scope="row">
                <span class="cell-who">
                  <span class="avatar avatar-sm"><span class="avatar-initials">{n.split()[0][0]}{n.split()[-1][0]}</span></span>
                  <span><strong>{n}</strong><small class="fg-3 d-block">{role}</small></span>
                </span>
              </th>
              <td data-cell="Company">{co}</td>
              <td data-cell="Email"><a href="mailto:{email}">{email}</a></td>
              <td data-cell="Phone" class="tabular">{phone}</td>
              <td data-cell="Status"><span class="chip chip-{status.lower()}">{status}</span></td>
              <td data-cell="Owner"><span class="avatar avatar-xs" title="{OWNERS[owner]}"><span class="avatar-initials">{owner}</span></span></td>
            </tr>""" for n, role, co, email, phone, status, owner in CONTACTS)

    body = f"""
      <section class="card">
        <header class="card-head">
          <div class="form-control form-adorn" style="max-width:20rem">
            <div class="form-adorn-icon">{ICON['search']}</div>
            <input type="search" class="form-ghost" placeholder="Filter contacts…" aria-label="Filter contacts" data-filter="#contactTable">
          </div>
          <div class="d-flex gap-3">
            <button class="btn-outline theme-secondary btn-sm" type="button">Export</button>
            <button class="btn-solid theme-primary btn-sm" type="button">{ICON['plus']} Contact</button>
          </div>
        </header>
        <div class="table-responsive">
          <table class="table lg:table-stacked align-middle" id="contactTable">
            <thead>
              <tr><th scope="col">Name</th><th scope="col">Company</th><th scope="col">Email</th><th scope="col">Phone</th><th scope="col">Status</th><th scope="col">Owner</th></tr>
            </thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <footer class="card-foot">
          <p class="fs-sm fg-3 mb-0"><span data-filter-count>{len(CONTACTS)}</span> of {len(CONTACTS)} contacts</p>
        </footer>
      </section>
"""
    page("contacts.html", "contacts.html", "Contacts", f"{len(CONTACTS)} people across {len(set(c[2] for c in CONTACTS))} companies.", body,
         desc="A filterable CRM contacts table that stacks properly on small screens.")


def page_reports():
    owner_totals = {}
    for co, ct, v, st, d, ow in DEALS:
        if st != "won":
            owner_totals[ow] = owner_totals.get(ow, 0) + v
    peak = max(owner_totals.values())
    owner_rows = "\n".join(f"""          <div class="funnel-row">
            <p class="funnel-label mb-0">{OWNERS[o]}</p>
            <div class="funnel-track"><div class="funnel-bar" style="--w:{round(v / peak * 100)}%"></div></div>
            <p class="funnel-value mb-0">{short(v)}</p>
            <p class="funnel-prob mb-0 fg-3">{len([d for d in DEALS if d[5] == o and d[3] != 'won'])} deals</p>
          </div>""" for o, v in sorted(owner_totals.items(), key=lambda x: -x[1]))

    body = f"""
      <div class="kpi-row">
{stat("Win rate", "31%", "2.4pts", "up", "trailing 90 days")}
{stat("Average deal", short(sum(d[2] for d in DEALS) / len(DEALS)), "6.1%", "up", "all stages")}
{stat("Deals stalled", "3", "1", "down", "past expected stage age")}
{stat("Forecast accuracy", "88%", "5pts", "up", "vs closed actuals")}
      </div>

      <div class="grid-2">
        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Weighted pipeline</h2><p class="card-sub mb-0">Twelve weeks</p></div></header>
          <div class="card-body">
            {area_chart([382, 401, 396, 428, 447, 439, 462, 488, 471, 503, 528, 541])}
            <div class="chart-axis"><span>12w ago</span><span>8w</span><span>4w</span><span>Now</span></div>
          </div>
        </section>

        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Open pipeline by owner</h2><p class="card-sub mb-0">Excludes closed won</p></div></header>
          <div class="card-body"><div class="funnel">
{owner_rows}
          </div></div>
        </section>
      </div>

      <section class="card">
        <header class="card-head"><div><h2 class="card-title">Stage conversion</h2><p class="card-sub mb-0">Value held at each step, and the odds applied to it</p></div></header>
        <div class="card-body"><div class="funnel">
{funnel()}
        </div></div>
      </section>
"""
    page("reports.html", "reports.html", "Reports", "Where the pipeline actually is, and who is carrying it.", body,
         desc="CRM reporting: weighted pipeline over time, pipeline by owner, and stage conversion — all drawn in SVG with no chart library.")


def page_settings():
    body = f"""
      <div class="grid-2">
        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Pipeline stages</h2><p class="card-sub mb-0">Probability drives the weighted forecast</p></div></header>
          <div class="card-body">
            <form data-demo-form novalidate>
{chr(10).join(f'''              <div class="stage-row">
                <span class="stage-grip" aria-hidden="true">⠿</span>
                <input class="form-control" type="text" value="{label}" aria-label="Stage {i + 1} name">
                <div class="form-adorn form-control" style="max-width:7rem">
                  <input type="number" class="form-ghost tabular" value="{prob}" min="0" max="100" aria-label="{label} win probability">
                  <span class="form-adorn-text">%</span>
                </div>
              </div>''' for i, (key, label, prob, exp) in enumerate(STAGES))}
              <button class="btn-solid theme-primary mt-4" type="submit" data-done-text="Saved ✓">Save stages</button>
            </form>
          </div>
        </section>

        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Your details</h2><p class="card-sub mb-0">Visible to your team</p></div></header>
          <div class="card-body">
            <form data-demo-form novalidate>
              <div class="row g-4">
                <div class="md:col-6">
                  <label class="form-label" for="sName">Full name</label>
                  <input class="form-control" type="text" id="sName" value="Dilan Aksoy" required>
                </div>
                <div class="md:col-6">
                  <label class="form-label" for="sEmail">Email</label>
                  <input class="form-control" type="email" id="sEmail" value="dilan@cadence.example" required>
                </div>
                <div class="col-12">
                  <label class="form-label" for="sRole">Role</label>
                  <select class="form-control form-control-caret" id="sRole">
                    <option selected>Account executive</option>
                    <option>Sales manager</option>
                    <option>Administrator</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label" for="sSig">Email signature</label>
                  <textarea class="form-control" id="sSig" rows="3">Dilan Aksoy — Cadence
+44 161 496 0100</textarea>
                </div>
                <div class="col-12">
                  <button class="btn-solid theme-primary" type="submit" data-done-text="Saved ✓">Save details</button>
                </div>
              </div>
            </form>
          </div>
        </section>
      </div>

      <section class="card">
        <header class="card-head"><div><h2 class="card-title">Notifications</h2><p class="card-sub mb-0">What reaches you, and how</p></div></header>
        <div class="card-body">
{chr(10).join(f'''          <div class="switch-row">
            <div><p class="mb-0 fw-semibold">{t}</p><p class="fg-3 fs-sm mb-0">{d}</p></div>
            <div class="switch"><input type="checkbox" role="switch" switch id="n{i}" {'checked' if on else ''} aria-label="{t}"></div>
          </div>''' for i, (t, d, on) in enumerate([
              ("A deal stalls", "When a deal passes the expected age for its stage.", True),
              ("Stage changes on my accounts", "Someone else moves one of your deals.", True),
              ("Weekly forecast summary", "Monday morning, weighted pipeline and what moved.", True),
              ("Mentions", "Someone @s you in a note.", False),
          ]))}
        </div>
      </section>
"""
    page("settings.html", "settings.html", "Settings", "Stages, your details, and what you get told about.", body,
         desc="Settings for a Bootstrap 6 CRM dashboard: editable pipeline stages, profile and notification switches.")


page_index()
page_pipeline()
page_contacts()
page_reports()
page_settings()
print(f"wrote 5 pages — {len(DEALS)} deals, {len(STAGES)} stages")
