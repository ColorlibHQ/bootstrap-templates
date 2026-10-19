#!/usr/bin/env python3
"""
Generates Helm, a Bootstrap 6 admin dashboard.

Eight pages share one shell — sidebar, topbar, mobile drawer — so the chrome is
written once here rather than copy-pasted eight times and drifting. Auth and
error pages deliberately opt out of the shell.

Charts are inline SVG and CSS. No chart library: a dashboard template that
depends on Chart.js is really a Chart.js template, and the first thing most
people do is swap it for whatever their stack already uses.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
TITLE = "Helm"

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

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""

ICON = {
    "grid": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="2" width="5" height="5" rx="1"/><rect x="9" y="2" width="5" height="5" rx="1"/><rect x="2" y="9" width="5" height="5" rx="1"/><rect x="9" y="9" width="5" height="5" rx="1"/></svg>',
    "chart": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M2 13h12M4 11V7M8 11V4M12 11V9"/></svg>',
    "table": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="3" width="12" height="10" rx="1.5"/><path d="M2 6.5h12M6.5 6.5V13"/></svg>',
    "form": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M3 4.5h10M3 8h10M3 11.5h6"/></svg>',
    "user": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="8" cy="5.5" r="2.75"/><path d="M2.75 13.5a5.25 5.25 0 0 1 10.5 0" stroke-linecap="round"/></svg>',
    "cog": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="8" cy="8" r="2.25"/><path d="M8 1.5v1.75M8 12.75v1.75M14.5 8h-1.75M3.25 8H1.5m11-4.6-1.25 1.25M4.75 11.25 3.5 12.5m0-9 1.25 1.25m6.5 6.5 1.25 1.25" stroke-linecap="round"/></svg>',
    "lock": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="7" width="10" height="7" rx="1.5"/><path d="M5.5 7V5a2.5 2.5 0 0 1 5 0v2"/></svg>',
    "bell": '<svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 6.5a4 4 0 0 1 8 0c0 3 1 4 1 4H3s1-1 1-4" stroke-linejoin="round"/><path d="M6.5 13a1.5 1.5 0 0 0 3 0"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 4 4" stroke-linecap="round"/></svg>',
    "up": '<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="m8 3 5 6H3z"/></svg>',
    "down": '<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="m8 13 5-6H3z"/></svg>',
}

# (file, nav label, icon, badge)
NAV = [
    ("index.html", "Overview", "grid", None),
    ("analytics.html", "Analytics", "chart", None),
    ("orders.html", "Orders", "table", "24"),
    ("forms.html", "Forms", "form", None),
    ("profile.html", "Profile", "user", None),
    ("settings.html", "Settings", "cog", None),
]


def nav_links(current, in_drawer=False):
    out = []
    for href, label, icon, badge in NAV:
        active = " active" if href == current and not in_drawer else ""
        count = f'<span class="count">{badge}</span>' if badge else ""
        out.append(f'<a class="side-link{active}" href="{href}">{ICON[icon]}<span>{label}</span>{count}</a>')
    return "\n        ".join(out)


def shell(current, title, subtitle, body, *, actions=""):
    """Wraps page content in the sidebar + topbar chrome."""
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-3" href="#main">Skip to main content</a>

<div class="app" id="app">

  <aside class="side" id="side">
    <a class="side-brand" href="index.html">
      <span class="side-mark" aria-hidden="true">H</span><span>{TITLE}</span>
    </a>
    <p class="side-label mb-0">Workspace</p>
    {nav_links(current)}
    <p class="side-label mb-0">Account</p>
    <a class="side-link" href="login.html">{ICON['lock']}<span>Sign out</span></a>
  </aside>

  <div>
    <header class="topbar">
      <button class="btn-icon lg:d-none" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
        <span class="navbar-toggler-icon" aria-hidden="true"></span>
      </button>
      <button class="btn-icon d-none lg:d-inline-flex" type="button" id="railToggle" aria-label="Collapse sidebar" aria-pressed="false">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="2" y="3" width="12" height="10" rx="1.5"/><path d="M6.5 3v10"/></svg>
      </button>

      <div class="form-control form-adorn search-field d-none md:d-flex">
        <div class="form-adorn-icon">{ICON['search']}</div>
        <input type="search" class="form-ghost" placeholder="Search orders, customers…" aria-label="Search">
      </div>

      <div class="d-flex align-items-center gap-3 ms-auto">
        {TOGGLE}
        <button class="btn-icon" type="button" aria-label="Notifications">{ICON['bell']}</button>
        <button class="btn-icon p-0" type="button" data-bs-toggle="menu" aria-expanded="false" aria-label="Account menu">
          <span class="avatar avatar-sm"><span class="avatar-initials">PN</span></span>
        </button>
        <div class="menu">
          <a class="menu-item" href="profile.html">Profile</a>
          <a class="menu-item" href="settings.html">Settings</a>
          <hr class="menu-divider">
          <a class="menu-item" href="login.html">Sign out</a>
        </div>
      </div>
    </header>

    <main class="content" id="main">
      <div class="d-flex flex-wrap align-items-end justify-content-between gap-4 mb-5">
        <div>
          <h1 class="page-title mb-1">{title}</h1>
          <p class="fg-3 fs-sm mb-0">{subtitle}</p>
        </div>
        <div class="d-flex flex-wrap gap-3">{actions}</div>
      </div>
{body}
    </main>
  </div>
</div>

<dialog class="drawer drawer-start" id="navDrawer" aria-labelledby="navDrawerLabel">
  <div class="drawer-header">
    <h2 class="drawer-title fs-lg" id="navDrawerLabel">{TITLE}</h2>
    <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
  </div>
  <div class="drawer-body">
    <div class="d-grid gap-1">
        {nav_links(current, in_drawer=True)}
      <hr>
      <a class="side-link" href="login.html">{ICON['lock']}<span>Sign out</span></a>
    </div>
  </div>
</dialog>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def area_chart(points, *, w=560, h=170, second=None):
    """Line + area chart as inline SVG. Values are 0-100."""
    step = w / (len(points) - 1)
    def path(vals):
        return " ".join(
            f"{'M' if i == 0 else 'L'}{round(i * step, 1)},{round(h - (v / 100) * h, 1)}"
            for i, v in enumerate(vals))
    line = path(points)
    area = f"{line} L{w},{h} L0,{h} Z"
    dots = "".join(
        f'<circle class="dot" cx="{round(i * step, 1)}" cy="{round(h - (v / 100) * h, 1)}" r="3"/>'
        for i, v in enumerate(points) if i % 3 == 0)
    grid = "".join(
        f'<line class="grid-line" x1="0" y1="{round(h * f, 1)}" x2="{w}" y2="{round(h * f, 1)}"/>'
        for f in (0, 0.25, 0.5, 0.75, 1))
    second_path = f'<path class="series series-2" d="{path(second)}"/>' if second else ""
    return f"""<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-label="Revenue over the last twelve weeks">
        <defs>
          <linearGradient id="helmArea" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="var(--bs-primary-base)" stop-opacity=".28"/>
            <stop offset="100%" stop-color="var(--bs-primary-base)" stop-opacity="0"/>
          </linearGradient>
        </defs>
        {grid}
        <path class="area" d="{area}"/>
        {second_path}
        <path class="series" d="{line}"/>
        {dots}
      </svg>"""


def bars(values, labels, highlight=-1):
    cells = []
    peak = max(values)
    for i, (v, lab) in enumerate(zip(values, labels)):
        cls = "bar" if i == highlight or highlight == -1 else "bar bar-muted"
        cells.append(f'<div><span class="{cls}" style="height:{round(v / peak * 100)}%"></span>'
                     f'<span class="tick">{lab}</span></div>')
    return f'<div class="bars">{"".join(cells)}</div>'


def stat(label, figure, delta, direction, note):
    arrow = ICON["up"] if direction == "up" else ICON["down"]
    return f"""<div class="sm:col-6 xl:col-3">
          <div class="panel"><div class="panel-body">
            <p class="stat-label mb-3">{label}</p>
            <p class="stat-figure mb-1">{figure}</p>
            <p class="stat-delta {direction} mb-0">{arrow} {delta} <span class="fg-3 fw-normal">{note}</span></p>
          </div></div>
        </div>"""


ORDERS = [
    ("#4821", "Northwind Trading", "Paid", "success", "2026-07-22", 4820.00),
    ("#4822", "Kestrel Logistics", "Refunded", "danger", "2026-07-22", 1240.50),
    ("#4823", "Lumen Studio", "Paid", "success", "2026-07-21", 1750.00),
    ("#4824", "Fieldstone Group", "Pending", "warning", "2026-07-21", 8960.25),
    ("#4825", "Ardent Works", "Paid", "success", "2026-07-20", 2310.75),
    ("#4826", "Halden & Co", "Draft", "secondary", "2026-07-20", 640.00),
    ("#4827", "Pemberton Civils", "Pending", "warning", "2026-07-19", 19875.00),
    ("#4828", "Sable Interiors", "Paid", "success", "2026-07-19", 3405.60),
]


def order_rows(limit=None, checkbox=False):
    rows = ORDERS[:limit] if limit else ORDERS
    out = []
    for ref, who, status, theme, date, amt in rows:
        cb = ('<td><input type="checkbox" class="check" data-row-check '
              f'aria-label="Select {ref}"></td>') if checkbox else ""
        out.append(f"""<tr>{cb}
              <th scope="row" class="fw-normal">{ref}</th>
              <td data-cell="Customer">{who}</td>
              <td data-cell="Status"><span class="badge badge-subtle theme-{theme}">{status}</span></td>
              <td data-cell="Date" class="fg-3">{date}</td>
              <td data-cell="Total" class="num">&pound;{amt:,.2f}</td>
            </tr>""")
    return "\n            ".join(out)


# ------------------------------------------------------------------ pages

def page_index():
    return shell("index.html", "Overview", "Trading summary for the last twelve weeks.", f"""
      <div class="row g-4 xl:g-5 mb-5">
        {stat("Revenue", "&pound;48,204", "12.4%", "up", "vs last month")}
        {stat("Orders", "1,284", "4.1%", "up", "vs last month")}
        {stat("Refund rate", "2.1%", "0.4pp", "down", "vs last month")}
        {stat("Avg. order", "&pound;37.54", "1.8%", "up", "vs last month")}
      </div>

      <div class="row g-4 xl:g-5 mb-5">
        <div class="xl:col-8">
          <div class="panel">
            <div class="panel-head">
              <h2 class="fs-lg fw-semibold mb-0">Revenue</h2>
              <span class="fs-xs fg-3">Solid: this year &middot; dashed: last year</span>
              <div class="ms-auto d-flex gap-1">
                <button class="btn-outline theme-secondary btn-sm" type="button">Week</button>
                <button class="btn-solid theme-primary btn-sm" type="button">Quarter</button>
                <button class="btn-outline theme-secondary btn-sm" type="button">Year</button>
              </div>
            </div>
            <div class="panel-body">
              {area_chart([28, 34, 30, 42, 39, 51, 47, 58, 54, 66, 71, 78],
                          second=[24, 27, 26, 31, 30, 36, 34, 40, 38, 45, 47, 51])}
            </div>
          </div>
        </div>
        <div class="xl:col-4">
          <div class="panel">
            <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Conversion</h2></div>
            <div class="panel-body text-center">
              <div class="donut" style="--value:68" role="img" aria-label="68 percent of sessions converted">
                <span class="donut-value">68%</span>
              </div>
              <p class="fg-3 fs-sm mt-4 mb-0">2,184 of 3,212 sessions reached checkout.</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4 xl:g-5">
        <div class="xl:col-7">
          <div class="panel">
            <div class="panel-head">
              <h2 class="fs-lg fw-semibold mb-0">Recent orders</h2>
              <a class="btn-text btn-sm ms-auto" href="orders.html">View all</a>
            </div>
            <div class="panel-body panel-body-flush">
              <div class="table-responsive">
                <table class="table sm:table-stacked mb-0">
                  <thead>
                    <tr>
                      <th scope="col">Order</th><th scope="col">Customer</th>
                      <th scope="col">Status</th><th scope="col">Date</th>
                      <th scope="col" class="num">Total</th>
                    </tr>
                  </thead>
                  <tbody class="table-group-divider">
            {order_rows(limit=5)}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
        <div class="xl:col-5">
          <div class="panel">
            <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Orders by weekday</h2></div>
            <div class="panel-body">
              {bars([42, 55, 61, 58, 74, 39, 24], ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], highlight=4)}
              <p class="fg-3 fs-sm mt-4 mb-0">Friday is consistently the strongest day; weekends are worth staffing lower.</p>
            </div>
          </div>
        </div>
      </div>
""", actions='<button class="btn-outline theme-secondary" type="button">Export</button>'
              '<button class="btn-solid theme-primary" type="button">New order</button>')


def page_analytics():
    return shell("analytics.html", "Analytics", "Traffic, acquisition and behaviour.", f"""
      <div class="row g-4 xl:g-5 mb-5">
        {stat("Sessions", "82,410", "6.2%", "up", "vs last month")}
        {stat("Bounce rate", "38.4%", "2.1pp", "down", "vs last month")}
        {stat("Avg. session", "3m 12s", "14s", "up", "vs last month")}
        {stat("New visitors", "61.8%", "3.4pp", "up", "vs last month")}
      </div>

      <div class="row g-4 xl:g-5 mb-5">
        <div class="xl:col-7">
          <div class="panel">
            <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Sessions</h2></div>
            <div class="panel-body">
              {area_chart([40, 44, 41, 52, 49, 58, 55, 62, 60, 68, 72, 80])}
            </div>
          </div>
        </div>
        <div class="xl:col-5">
          <div class="panel">
            <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Acquisition</h2></div>
            <div class="panel-body">
              <div class="d-flex justify-content-between mb-1"><span class="fs-sm">Organic search</span><span class="fs-sm fw-semibold">46%</span></div>
              <div class="progress mb-4" role="progressbar" aria-label="Organic search" aria-valuenow="46" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar" style="width:46%"></div></div>
              <div class="d-flex justify-content-between mb-1"><span class="fs-sm">Direct</span><span class="fs-sm fw-semibold">24%</span></div>
              <div class="progress mb-4" role="progressbar" aria-label="Direct" aria-valuenow="24" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar theme-success" style="width:24%"></div></div>
              <div class="d-flex justify-content-between mb-1"><span class="fs-sm">Referral</span><span class="fs-sm fw-semibold">18%</span></div>
              <div class="progress mb-4" role="progressbar" aria-label="Referral" aria-valuenow="18" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar theme-warning" style="width:18%"></div></div>
              <div class="d-flex justify-content-between mb-1"><span class="fs-sm">Social</span><span class="fs-sm fw-semibold">12%</span></div>
              <div class="progress mb-0" role="progressbar" aria-label="Social" aria-valuenow="12" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar theme-secondary" style="width:12%"></div></div>
            </div>
          </div>
        </div>
      </div>

      <div class="panel">
        <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Top pages</h2></div>
        <div class="panel-body panel-body-flush">
          <div class="table-responsive">
            <table class="table sm:table-stacked mb-0">
              <thead><tr><th scope="col">Page</th><th scope="col" class="num">Views</th><th scope="col" class="num">Avg. time</th><th scope="col" class="num">Bounce</th></tr></thead>
              <tbody class="table-group-divider">
                <tr><th scope="row" class="fw-normal">/</th><td class="num">24,118</td><td class="num">2m 41s</td><td class="num">32.1%</td></tr>
                <tr><th scope="row" class="fw-normal">/pricing</th><td class="num">11,904</td><td class="num">3m 18s</td><td class="num">28.7%</td></tr>
                <tr><th scope="row" class="fw-normal">/docs/getting-started</th><td class="num">9,442</td><td class="num">5m 02s</td><td class="num">19.4%</td></tr>
                <tr><th scope="row" class="fw-normal">/blog/shipping-on-fridays</th><td class="num">6,731</td><td class="num">4m 27s</td><td class="num">61.2%</td></tr>
                <tr><th scope="row" class="fw-normal">/changelog</th><td class="num">4,015</td><td class="num">1m 54s</td><td class="num">44.8%</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
""")


def page_orders():
    return shell("orders.html", "Orders", "1,284 orders in the selected period.", f"""
      <div class="panel" data-selectable>
        <div class="panel-head">
          <div class="form-control form-adorn" style="flex:1 1 14rem;max-width:20rem">
            <div class="form-adorn-icon">{ICON['search']}</div>
            <input type="search" class="form-ghost" data-filter-text placeholder="Search orders…" aria-label="Search orders">
          </div>
          <span class="fs-sm fg-3" data-filter-count>8 of 8</span>
          <div class="ms-auto d-flex gap-3">
            <button class="btn-outline theme-secondary btn-sm" type="button">Filters</button>
            <button class="btn-outline theme-secondary btn-sm" type="button">Export</button>
          </div>
        </div>
        <div class="bulk-bar" data-bulk-bar hidden>
          <strong class="fs-sm" data-bulk-count>0 selected</strong>
          <div class="d-flex flex-wrap gap-3 ms-auto">
            <button class="btn-outline theme-secondary btn-sm" type="button">Mark paid</button>
            <button class="btn-solid theme-danger btn-sm" type="button">Refund</button>
          </div>
        </div>
        <div class="panel-body panel-body-flush">
          <div class="table-responsive">
            <table class="table table-hover sm:table-stacked mb-0">
              <thead>
                <tr>
                  <th scope="col" style="width:2.5rem"><input type="checkbox" class="check" id="checkAll" aria-label="Select all orders"></th>
                  <th scope="col">Order</th><th scope="col">Customer</th>
                  <th scope="col">Status</th><th scope="col">Date</th>
                  <th scope="col" class="num">Total</th>
                </tr>
              </thead>
              <tbody class="table-group-divider">
            {order_rows(checkbox=True)}
              </tbody>
            </table>
          </div>
          <p class="p-5 mb-0 fg-3 text-center" data-filter-empty hidden>No order matches that search.</p>
        </div>
      </div>
""", actions='<button class="btn-solid theme-primary" type="button">New order</button>')


def page_forms():
    return shell("forms.html", "Forms", "Every Bootstrap 6 form control, in one place.", """
      <div class="row g-4 xl:g-5">
        <div class="lg:col-6">
          <div class="panel"><div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Customer details</h2></div>
            <form class="panel-body vstack gap-4" data-demo-form data-bs-validate novalidate>
              <div class="form-field">
                <label class="form-label" for="fName">Full name</label>
                <input type="text" class="form-control" id="fName" required>
                <div class="invalid-feedback">Required.</div>
              </div>
              <div class="form-field">
                <label class="form-label" for="fEmail">Email</label>
                <input type="email" class="form-control" id="fEmail" required>
                <div class="invalid-feedback">A valid email, please.</div>
              </div>
              <div>
                <label class="form-label">Plan</label>
                <button class="form-control combobox-toggle" type="button" data-bs-toggle="combobox" data-bs-search="true" data-bs-name="plan" data-bs-placeholder="Choose a plan…">
                  <span class="combobox-value">Choose a plan…</span>
                  <svg class="combobox-caret" width="10" height="16" viewBox="0 0 10 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M0.46967 5.46967C0.762563 5.17678 1.23744 5.17678 1.53033 5.46967L5 8.93934L8.46967 5.46967C8.76256 5.17678 9.23744 5.17678 9.53033 5.46967C9.82322 5.76256 9.82322 6.23744 9.53033 6.53033L5.53033 10.5303C5.23744 10.8232 4.76256 10.8232 4.46967 10.5303L0.46967 6.53033C0.176777 6.23744 0.176777 5.76256 0.46967 5.46967Z" fill="currentcolor"/></svg>
                </button>
                <div class="menu">
                  <button class="menu-item" type="button" data-bs-value="starter">Starter</button>
                  <button class="menu-item" type="button" data-bs-value="team">Team</button>
                  <button class="menu-item" type="button" data-bs-value="scale">Scale</button>
                </div>
              </div>
              <div class="form-field">
                <label class="form-label" for="fStart">Start date</label>
                <input type="text" class="form-control" id="fStart" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date…">
              </div>
              <div class="form-field">
                <label class="form-label" for="fNotes">Notes</label>
                <textarea class="form-control" id="fNotes" rows="3"></textarea>
              </div>
              <div><button class="btn-solid theme-primary" type="submit" data-done-text="Saved &#10003;">Save customer</button></div>
            </form>
          </div>
        </div>

        <div class="lg:col-6">
          <div class="panel mb-4 xl:mb-5"><div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Choices</h2></div>
            <div class="panel-body vstack gap-4">
              <div class="form-field">
                <input type="checkbox" class="check" id="cA" checked>
                <label for="cA">Send order confirmations</label>
              </div>
              <div class="form-field">
                <input type="checkbox" class="check" id="cB">
                <label for="cB">Send weekly summaries</label>
              </div>
              <div class="form-field">
                <div class="switch"><input type="checkbox" id="sA" role="switch" switch checked></div>
                <label for="sA">Two-factor authentication</label>
              </div>
              <div class="form-field">
                <input type="radio" class="radio" name="tier" id="rA" checked>
                <label for="rA">Monthly billing</label>
              </div>
              <div class="form-field">
                <input type="radio" class="radio" name="tier" id="rB">
                <label for="rB">Annual billing &mdash; two months free</label>
              </div>
            </div>
          </div>

          <div class="panel"><div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Security</h2></div>
            <div class="panel-body vstack gap-4">
              <div class="form-field">
                <label class="form-label" for="pw">New password</label>
                <input type="password" class="form-control" id="pw" data-bs-strength>
              </div>
              <div>
                <label class="form-label d-block">Verification code</label>
                <div data-bs-otp data-bs-length="6"></div>
              </div>
              <div class="form-field">
                <label class="form-label" for="rng">Monthly budget</label>
                <div class="form-range" data-bs-bubble>
                  <input type="range" class="form-range-input" id="rng" min="0" max="5000" step="100" value="1800" aria-label="Monthly budget">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
""")


def page_profile():
    return shell("profile.html", "Profile", "Priya Nandakumar &middot; Administrator", """
      <div class="row g-4 xl:g-5">
        <div class="lg:col-4">
          <div class="panel"><div class="panel-body text-center">
            <span class="avatar avatar-lg mb-4"><span class="avatar-initials">PN</span></span>
            <h2 class="fs-xl fw-semibold mb-1">Priya Nandakumar</h2>
            <p class="fg-3 fs-sm mb-4">Administrator &middot; joined March 2021</p>
            <div class="d-flex flex-wrap justify-content-center gap-3 mb-5">
              <span class="chip">Billing</span><span class="chip">Support</span><span class="chip">Deploys</span>
            </div>
            <button class="btn-solid theme-primary w-100" type="button">Edit profile</button>
          </div></div>
        </div>
        <div class="lg:col-8">
          <div class="panel mb-4 xl:mb-5">
            <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Details</h2></div>
            <div class="panel-body">
              <div class="d-flex justify-content-between py-3" style="border-bottom:1px solid var(--bs-border-color)"><span class="fg-3 fs-sm">Email</span><span class="fs-sm">priya@example.com</span></div>
              <div class="d-flex justify-content-between py-3" style="border-bottom:1px solid var(--bs-border-color)"><span class="fg-3 fs-sm">Role</span><span class="fs-sm">Administrator</span></div>
              <div class="d-flex justify-content-between py-3" style="border-bottom:1px solid var(--bs-border-color)"><span class="fg-3 fs-sm">Two-factor</span><span class="fs-sm"><span class="badge badge-subtle theme-success">Enabled</span></span></div>
              <div class="d-flex justify-content-between py-3"><span class="fg-3 fs-sm">Last sign-in</span><span class="fs-sm">Today at 08:12 from Manchester</span></div>
            </div>
          </div>
          <div class="panel">
            <div class="panel-head"><h2 class="fs-lg fw-semibold mb-0">Recent activity</h2></div>
            <div class="panel-body">
              <div class="activity"><span class="activity-dot"></span><div><p class="fs-sm mb-0">Refunded order <strong>#4822</strong> for Kestrel Logistics</p><p class="fs-xs fg-3 mb-0">Today at 09:41</p></div></div>
              <div class="activity"><span class="activity-dot"></span><div><p class="fs-sm mb-0">Invited <strong>marcus@example.com</strong> as an editor</p><p class="fs-xs fg-3 mb-0">Yesterday at 16:03</p></div></div>
              <div class="activity"><span class="activity-dot"></span><div><p class="fs-sm mb-0">Changed the refund policy from 14 to 30 days</p><p class="fs-xs fg-3 mb-0">Monday at 11:20</p></div></div>
              <div class="activity"><span class="activity-dot"></span><div><p class="fs-sm mb-0">Enabled two-factor authentication</p><p class="fs-xs fg-3 mb-0">12 July</p></div></div>
            </div>
          </div>
        </div>
      </div>
""")


def page_settings():
    return shell("settings.html", "Settings", "Workspace configuration.", """
      <div class="panel">
        <div class="panel-head p-0 px-4">
          <ul class="nav nav-underline" role="tablist">
            <li class="nav-item" role="presentation"><button class="nav-link active" data-bs-toggle="tab" data-bs-target="#tabGeneral" type="button" role="tab" aria-selected="true">General</button></li>
            <li class="nav-item" role="presentation"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tabBilling" type="button" role="tab" aria-selected="false">Billing</button></li>
            <li class="nav-item" role="presentation"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tabTeam" type="button" role="tab" aria-selected="false">Team</button></li>
            <li class="nav-item" role="presentation"><button class="nav-link" data-bs-toggle="tab" data-bs-target="#tabDanger" type="button" role="tab" aria-selected="false">Danger zone</button></li>
          </ul>
        </div>
        <div class="panel-body">
          <div class="tab-content">
            <div class="tab-pane active" id="tabGeneral" role="tabpanel">
              <form class="vstack gap-4" style="max-width:32rem" data-demo-form data-bs-validate novalidate>
                <div class="form-field">
                  <label class="form-label" for="wsName">Workspace name</label>
                  <input type="text" class="form-control" id="wsName" value="Northwind Trading">
                </div>
                <div class="form-field">
                  <label class="form-label" for="wsUrl">Public URL</label>
                  <input type="text" class="form-control" id="wsUrl" value="northwind.example.com">
                </div>
                <div class="form-field">
                  <div class="switch"><input type="checkbox" id="wsPublic" role="switch" switch checked></div>
                  <label for="wsPublic">Allow public order tracking</label>
                </div>
                <div><button class="btn-solid theme-primary" type="submit" data-done-text="Saved &#10003;">Save changes</button></div>
              </form>
            </div>
            <div class="tab-pane" id="tabBilling" role="tabpanel">
              <p class="fg-2 mb-4">You are on the <strong>Team</strong> plan at &pound;29 per month, renewing on 1 August 2026.</p>
              <div class="d-flex flex-wrap gap-3"><button class="btn-outline theme-secondary" type="button">Change plan</button><button class="btn-text" type="button">Download invoices</button></div>
            </div>
            <div class="tab-pane" id="tabTeam" role="tabpanel">
              <div class="table-responsive">
                <table class="table sm:table-stacked mb-0">
                  <thead><tr><th scope="col">Member</th><th scope="col">Role</th><th scope="col">Last active</th></tr></thead>
                  <tbody class="table-group-divider">
                    <tr><th scope="row" class="fw-normal">Priya Nandakumar</th><td>Administrator</td><td class="fg-3">Today</td></tr>
                    <tr><th scope="row" class="fw-normal">Marcus Levy</th><td>Editor</td><td class="fg-3">Yesterday</td></tr>
                    <tr><th scope="row" class="fw-normal">Dana Reyes</th><td>Viewer</td><td class="fg-3">3 days ago</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="tab-pane" id="tabDanger" role="tabpanel">
              <div class="alert theme-danger" role="alert">
                <h3 class="alert-heading fs-lg">Delete this workspace</h3>
                <p class="mb-4">This removes all 1,284 orders and cannot be undone.</p>
                <button class="btn-solid theme-danger" type="button" data-bs-toggle="dialog" data-bs-target="#delDialog">Delete workspace</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <dialog class="dialog dialog-sm" id="delDialog" aria-labelledby="delLabel" data-bs-static="true">
        <div class="dialog-header">
          <h2 class="dialog-title fs-lg" id="delLabel">Delete this workspace?</h2>
          <button type="button" class="btn-close" data-bs-dismiss="dialog" aria-label="Close"></button>
        </div>
        <div class="dialog-body">
          <p class="fg-2 mb-0">Type the workspace name to confirm. All 1,284 orders will be removed permanently.</p>
        </div>
        <div class="dialog-footer">
          <button type="button" class="btn-text" data-bs-dismiss="dialog">Keep it</button>
          <button type="button" class="btn-solid theme-danger" data-bs-dismiss="dialog">Delete permanently</button>
        </div>
      </dialog>
""")


def page_login():
    return HEAD.format(title=f"Sign in — {TITLE} | Free Bootstrap 6 Admin Dashboard",
                       desc="Sign-in page from the Helm Bootstrap 6 admin dashboard template.") + """
<main class="auth-stage">
  <div class="auth-card">
    <div class="text-center mb-5">
      <span class="side-mark mx-auto mb-4" aria-hidden="true">H</span>
      <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Sign in to Helm</h1>
      <p class="fg-3 fs-sm mb-0">Welcome back. Use your work account.</p>
    </div>
    <div class="panel"><form class="panel-body vstack gap-4" data-demo-form data-bs-validate novalidate>
      <div class="form-field">
        <label class="form-label" for="liEmail">Email</label>
        <input type="email" class="form-control" id="liEmail" required>
        <div class="invalid-feedback">A valid email, please.</div>
      </div>
      <div class="form-field">
        <label class="form-label" for="liPass">Password</label>
        <input type="password" class="form-control" id="liPass" required>
        <div class="invalid-feedback">Required.</div>
      </div>
      <div class="d-flex align-items-center justify-content-between">
        <div class="form-field mb-0">
          <input type="checkbox" class="check" id="liRemember" checked>
          <label for="liRemember">Remember me</label>
        </div>
        <a class="fs-sm" href="#">Forgot password?</a>
      </div>
      <button class="btn-solid theme-primary w-100" type="submit" data-done-text="Signed in &#10003;">Sign in</button>
    </form></div>
    <p class="text-center fs-sm fg-3 mt-5 mb-0">Not registered? <a href="#">Create an account</a></p>
    <p class="text-center fs-sm mt-4 mb-0"><a href="index.html">&#8592; Back to the dashboard</a></p>
  </div>
</main>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page_404():
    return HEAD.format(title=f"Page not found — {TITLE} | Free Bootstrap 6 Admin Dashboard",
                       desc="404 page from the Helm Bootstrap 6 admin dashboard template.") + """
<main class="auth-stage text-center">
  <div style="max-width:26rem">
    <p class="fg-primary fw-bold mb-3" style="font-size:4rem;letter-spacing:-.04em;line-height:1">404</p>
    <h1 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">We cannot find that page</h1>
    <p class="fg-2 mb-5">It may have been moved, or the link that brought you here may be out of date.</p>
    <div class="d-flex flex-wrap justify-content-center gap-3">
      <a class="btn-solid theme-primary" href="index.html">Back to the dashboard</a>
      <a class="btn-outline theme-secondary" href="orders.html">View orders</a>
    </div>
  </div>
</main>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


PAGES = {
    "index.html": ("Helm — Free Bootstrap 6 Admin Dashboard Template",
                   "Helm is a free Bootstrap 6 admin dashboard template — collapsible sidebar, SVG charts with no chart library, data tables, forms, profile, settings, auth and 404 pages.",
                   page_index),
    "analytics.html": ("Analytics — Helm | Free Bootstrap 6 Admin Dashboard",
                       "Analytics page from the Helm Bootstrap 6 admin dashboard — sessions chart, acquisition breakdown and top pages.",
                       page_analytics),
    "orders.html": ("Orders — Helm | Free Bootstrap 6 Admin Dashboard",
                    "Orders table from the Helm Bootstrap 6 admin dashboard — searchable, selectable rows with bulk actions.",
                    page_orders),
    "forms.html": ("Forms — Helm | Free Bootstrap 6 Admin Dashboard",
                   "Form controls from the Helm Bootstrap 6 admin dashboard — Combobox, Datepicker, OTP, password strength and range.",
                   page_forms),
    "profile.html": ("Profile — Helm | Free Bootstrap 6 Admin Dashboard",
                     "Profile page from the Helm Bootstrap 6 admin dashboard template.",
                     page_profile),
    "settings.html": ("Settings — Helm | Free Bootstrap 6 Admin Dashboard",
                      "Tabbed settings page from the Helm Bootstrap 6 admin dashboard template.",
                      page_settings),
}

for name, (title, desc, fn) in PAGES.items():
    (ROOT / name).write_text(HEAD.format(title=title, desc=desc) + fn(), encoding="utf-8")

(ROOT / "login.html").write_text(page_login(), encoding="utf-8")
(ROOT / "404.html").write_text(page_404(), encoding="utf-8")

print(f"wrote {len(PAGES) + 2} pages")
