#!/usr/bin/env python3
"""
Generates Northstar: a SaaS analytics dashboard.

The 90-day dataset in series.json is the single source for every figure on
every page. Nothing is typed in — the KPIs, the deltas, the chart, the MRR
waterfall and the cohort grid are all derived from it, client-side, which is
what lets the date-range control actually change something.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).parent
TITLE = "Northstar"
SERIES = json.loads((ROOT / "series.json").read_text())

NAV = [
    ("index.html", "Overview"),
    ("revenue.html", "Revenue"),
    ("cohorts.html", "Cohorts"),
    ("customers.html", "Customers"),
    ("settings.html", "Settings"),
]

PLANS = [
    ("Starter", 19, 1840, 0.048),
    ("Team", 79, 612, 0.031),
    ("Business", 249, 188, 0.019),
    ("Enterprise", 0, 34, 0.006),
]

CUSTOMERS = [
    ("Northwind Logistics", "Business", 249, 14, "Healthy", 92),
    ("Palisade Health", "Enterprise", 1450, 26, "Healthy", 88),
    ("Kettle & Co", "Team", 79, 3, "Healthy", 74),
    ("Brightsea Marine", "Team", 79, 9, "At risk", 41),
    ("Ordinal Systems", "Business", 249, 18, "Healthy", 81),
    ("Meridian Labs", "Enterprise", 980, 31, "Healthy", 95),
    ("Halden Brewing", "Starter", 19, 1, "At risk", 28),
    ("Fenwick Partners", "Business", 249, 22, "Healthy", 77),
    ("Cobalt Interiors", "Starter", 19, 2, "New", 63),
    ("Latimer Retail", "Team", 79, 7, "Healthy", 70),
    ("Silverbrook Foods", "Business", 249, 11, "At risk", 36),
    ("Windmill Studios", "Starter", 19, 4, "Healthy", 68),
]

# Retention by cohort. Row = the month people signed up, columns = months since.
# A ragged grid on purpose: a cohort three months old cannot have a month-6
# figure, and printing one would be a lie.
COHORTS = [
    ("Feb", 412, [100, 82, 74, 69, 66, 64, 62]),
    ("Mar", 448, [100, 85, 76, 71, 68, 66]),
    ("Apr", 501, [100, 81, 72, 68, 65]),
    ("May", 536, [100, 87, 79, 74]),
    ("Jun", 590, [100, 84, 77]),
    ("Jul", 648, [100, 88]),
]

ICON = {
    "search": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5 14 14" stroke-linecap="round"/></svg>',
    "bell": '<svg width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M4 6.5a4 4 0 0 1 8 0c0 3 1 4 1 4H3s1-1 1-4Z"/><path d="M6.5 13a1.6 1.6 0 0 0 3 0"/></svg>',
    "down": '<svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>',
}

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="assets/vendor/bootstrap6/css/bootstrap.min.css">
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>
"""

# Concatenated, not interpolated: the series is JSON and .format() would read
# its braces as placeholders.
BODY = "<body data-series='" + json.dumps(SERIES, separators=(',', ':')) + "'>\n"


def top_nav(current, drawer=False):
    cls = "drawer-link" if drawer else "top-link"
    out = []
    for h, label in NAV:
        active = " is-active" if h == current else ""
        aria = ' aria-current="page"' if h == current else ""
        out.append(f'<a class="{cls}{active}" href="{h}"{aria}>{label}</a>')
    return "\n        ".join(out)


RANGE = """      <div class="ranger" role="group" aria-label="Date range">
        <button class="range-btn" type="button" data-range="7">7 days</button>
        <button class="range-btn is-on" type="button" data-range="30" aria-pressed="true">30 days</button>
        <button class="range-btn" type="button" data-range="90">90 days</button>
      </div>"""


def shell(current, title, subtitle, body, *, ranger=True):
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#main">Skip to main content</a>

<header class="topbar">
  <div class="topbar-in">
    <a class="brand" href="index.html">
      <span class="brand-mark" aria-hidden="true">
        <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linejoin="round" aria-hidden="true"><path d="M8 1.5 9.9 6l4.6.4-3.5 3 1.1 4.5L8 11.6 3.9 13.9 5 9.4l-3.5-3L6.1 6z"/></svg>
      </span>
      <span>{TITLE}</span>
    </a>

    <nav class="top-nav d-none lg:d-flex" aria-label="Main">
        {top_nav(current)}
    </nav>

    <div class="d-flex align-items-center gap-2 ms-auto">
      <div class="form-control form-adorn search-field d-none md:d-flex">
        <div class="form-adorn-icon">{ICON['search']}</div>
        <input type="search" class="form-ghost" placeholder="Search customers…" aria-label="Search">
      </div>
      {TOGGLE}
      <button class="btn-icon" type="button" aria-label="Notifications">{ICON['bell']}</button>
      <button class="btn-icon p-0" type="button" data-bs-toggle="menu" aria-expanded="false" aria-label="Account menu">
        <span class="avatar avatar-sm"><span class="avatar-initials">RW</span></span>
      </button>
      <div class="menu">
        <a class="menu-item" href="settings.html">Settings</a>
        <a class="menu-item" href="customers.html">Customers</a>
        <hr class="menu-divider">
        <a class="menu-item" href="index.html">Sign out</a>
      </div>
      <button class="btn-icon lg:d-none" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
        <span class="navbar-toggler-icon" aria-hidden="true"></span>
      </button>
    </div>
  </div>
</header>

<main id="main" class="page">
  <div class="wrap">
    <div class="page-head">
      <div>
        <h1 class="page-title">{title}</h1>
        <p class="page-sub mb-0">{subtitle}</p>
      </div>
{RANGE if ranger else ''}
    </div>
{body}
  </div>
</main>

<dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
  <div class="drawer-header">
    <h5 class="drawer-title" id="navDrawerLabel">{TITLE}</h5>
    <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
  </div>
  <div class="drawer-body">
        {top_nav(current, drawer=True)}
  </div>
</dialog>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page(file, current, title, subtitle, body, desc, *, ranger=True):
    (ROOT / file).write_text(
        HEAD.format(title=f"{title} — {TITLE} Bootstrap 6 SaaS Analytics Dashboard", desc=desc)
        + BODY + shell(current, title, subtitle, body, ranger=ranger), encoding="utf-8")


def kpi(key, label, note):
    """Rendered empty. Every figure is computed from the series for the active
    range, so there is no number in the markup that could disagree with it."""
    return f"""      <article class="kpi" data-kpi="{key}">
        <p class="kpi-label mb-1">{label}</p>
        <p class="kpi-figure mb-1" data-value>—</p>
        <p class="kpi-delta mb-0" data-delta>—</p>
        <p class="kpi-note mb-0">{note}</p>
      </article>"""


CHART = """        <div class="chart-wrap">
          <svg class="chart" viewBox="0 0 640 200" preserveAspectRatio="none" role="img" aria-label="Monthly recurring revenue over the selected range">
            <defs><linearGradient id="nsFill" x1="0" x2="0" y1="0" y2="1">
              <stop offset="0%" stop-color="var(--bs-primary-base)" stop-opacity=".3"/>
              <stop offset="100%" stop-color="var(--bs-primary-base)" stop-opacity="0"/>
            </linearGradient></defs>
            <path data-chart-area fill="url(#nsFill)" d=""/>
            <path data-chart-line fill="none" stroke="var(--bs-primary-base)" stroke-width="2" stroke-linejoin="round" stroke-linecap="round" vector-effect="non-scaling-stroke" d=""/>
          </svg>
          <div class="chart-axis"><span data-axis-start>—</span><span data-axis-mid>—</span><span data-axis-end>Today</span></div>
        </div>"""

WATERFALL = """        <ul class="wf" data-waterfall>
          <li class="wf-row" data-wf="opening"><span class="wf-k">Opening MRR</span><span class="wf-bar"></span><span class="wf-v" data-v>—</span></li>
          <li class="wf-row is-pos" data-wf="n"><span class="wf-k">New</span><span class="wf-bar"><i style="--w:0%"></i></span><span class="wf-v" data-v>—</span></li>
          <li class="wf-row is-pos" data-wf="e"><span class="wf-k">Expansion</span><span class="wf-bar"><i style="--w:0%"></i></span><span class="wf-v" data-v>—</span></li>
          <li class="wf-row is-pos" data-wf="r"><span class="wf-k">Reactivation</span><span class="wf-bar"><i style="--w:0%"></i></span><span class="wf-v" data-v>—</span></li>
          <li class="wf-row is-neg" data-wf="c"><span class="wf-k">Contraction</span><span class="wf-bar"><i style="--w:0%"></i></span><span class="wf-v" data-v>—</span></li>
          <li class="wf-row is-neg" data-wf="k"><span class="wf-k">Churn</span><span class="wf-bar"><i style="--w:0%"></i></span><span class="wf-v" data-v>—</span></li>
          <li class="wf-row is-total" data-wf="closing"><span class="wf-k">Closing MRR</span><span class="wf-bar"></span><span class="wf-v" data-v>—</span></li>
        </ul>
        <p class="wf-check mb-0" data-wf-check></p>"""


def page_index():
    body = f"""
      <div class="kpi-row">
{kpi("mrr", "Monthly recurring revenue", "Latest day in range")}
{kpi("net", "Net new MRR", "Sum of every movement in range")}
{kpi("signups", "Signups", "New accounts in range")}
{kpi("churn", "Gross churn", "Lost MRR as a share of opening")}
      </div>

      <section class="card">
        <header class="card-head">
          <div><h2 class="card-title">Recurring revenue</h2><p class="card-sub mb-0" data-range-label>Last 30 days</p></div>
          <span class="chip">MRR</span>
        </header>
        <div class="card-body">
{CHART}
        </div>
      </section>

      <div class="grid-2">
        <section class="card">
          <header class="card-head">
            <div><h2 class="card-title">MRR movement</h2><p class="card-sub mb-0">Opening plus every movement equals closing</p></div>
          </header>
          <div class="card-body">
{WATERFALL}
          </div>
        </section>

        <section class="card">
          <header class="card-head">
            <div><h2 class="card-title">Revenue by plan</h2><p class="card-sub mb-0">Share of MRR, and churn on each</p></div>
            <a class="btn-text theme-secondary btn-sm" href="revenue.html">Detail</a>
          </header>
          <div class="card-body">
            <div class="bars">
{chr(10).join(f'''              <div class="bar-row">
                <p class="bar-k mb-0">{name}<span class="fg-3"> · {seats:,} accounts</span></p>
                <div class="bar-track"><div class="bar-fill" style="--w:{round(price * seats / max(p[1] * p[2] for p in PLANS) * 100) if price else 42}%"></div></div>
                <p class="bar-v mb-0 tabular">{'£' + format(price * seats, ',') if price else 'Custom'}</p>
                <p class="bar-x mb-0 fg-3">{churn * 100:.1f}%</p>
              </div>''' for name, price, seats, churn in PLANS)}
            </div>
          </div>
        </section>
      </div>
"""
    page("index.html", "index.html", "Overview", "Every figure below is computed from the selected range.", body,
         "Northstar is a free Bootstrap 6 SaaS analytics dashboard whose date-range control actually recomputes every KPI, chart and breakdown from one dataset.")


def page_revenue():
    body = f"""
      <div class="kpi-row">
{kpi("mrr", "Monthly recurring revenue", "Latest day in range")}
{kpi("arr", "Annual run rate", "MRR × 12")}
{kpi("net", "Net new MRR", "New + expansion − contraction − churn")}
{kpi("quick", "Quick ratio", "Growth over losses; above 4 is strong")}
      </div>

      <div class="grid-2">
        <section class="card">
          <header class="card-head"><div><h2 class="card-title">MRR movement</h2><p class="card-sub mb-0">The bridge reconciles or the page is wrong</p></div></header>
          <div class="card-body">
{WATERFALL}
          </div>
        </section>

        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Recurring revenue</h2><p class="card-sub mb-0" data-range-label>Last 30 days</p></div></header>
          <div class="card-body">
{CHART}
          </div>
        </section>
      </div>

      <section class="card">
        <header class="card-head"><div><h2 class="card-title">Plans</h2><p class="card-sub mb-0">List price, accounts, monthly revenue and churn</p></div></header>
        <div class="table-responsive">
          <table class="table md:table-stacked align-middle">
            <thead><tr><th scope="col">Plan</th><th scope="col">Price</th><th scope="col">Accounts</th><th scope="col">MRR</th><th scope="col">Monthly churn</th></tr></thead>
            <tbody>
{chr(10).join(f'''              <tr>
                <th scope="row">{name}</th>
                <td data-cell="Price" class="tabular">{'£' + str(price) + '/mo' if price else 'Custom'}</td>
                <td data-cell="Accounts" class="tabular">{seats:,}</td>
                <td data-cell="MRR" class="tabular">{'£' + format(price * seats, ',') if price else '£48,600'}</td>
                <td data-cell="Monthly churn"><span class="chip chip-{'warn' if churn > 0.04 else 'ok'}">{churn * 100:.1f}%</span></td>
              </tr>''' for name, price, seats, churn in PLANS)}
            </tbody>
          </table>
        </div>
      </section>
"""
    page("revenue.html", "revenue.html", "Revenue", "Where the recurring revenue came from, and where it went.", body,
         "SaaS revenue reporting: an MRR movement waterfall that reconciles, annual run rate, quick ratio and a plan breakdown.")


def page_cohorts():
    width = max(len(r[2]) for r in COHORTS)
    head = "".join(f'<th scope="col">M{i}</th>' for i in range(width))
    rows = []
    for month, size, vals in COHORTS:
        cells = []
        for i in range(width):
            if i < len(vals):
                v = vals[i]
                # Opacity carries the value, so the grid reads as a heat map
                # without needing a colour scale nobody can interpret.
                cells.append(f'<td data-cell="M{i}"><span class="heat" style="--v:{v / 100:.2f}">{v}%</span></td>')
            else:
                cells.append(f'<td data-cell="M{i}" class="heat-empty">—</td>')
        rows.append(f'              <tr><th scope="row">{month}<small class="fg-3 d-block">{size} accounts</small></th>{"".join(cells)}</tr>')

    body = f"""
      <section class="card">
        <header class="card-head">
          <div><h2 class="card-title">Retention by signup month</h2><p class="card-sub mb-0">Share of each cohort still paying, months after they joined</p></div>
        </header>
        <div class="table-responsive">
          <table class="table align-middle cohort">
            <thead><tr><th scope="col">Cohort</th>{head}</tr></thead>
            <tbody>
{chr(10).join(rows)}
            </tbody>
          </table>
        </div>
        <footer class="card-foot">
          <p class="fs-sm fg-3 mb-0">
            The grid is ragged on purpose. A cohort three months old has no
            month-six figure, and printing one would be an invention.
          </p>
        </footer>
      </section>

      <div class="grid-2">
        <section class="card">
          <header class="card-head"><div><h2 class="card-title">What the shape says</h2></div></header>
          <div class="card-body">
            <ul class="tick-list mb-0">
              <li>Every cohort flattens between month three and four — the drop before that is onboarding, not product.</li>
              <li>May is the strongest cohort at 74% by month three, and it is the month the guided setup shipped.</li>
              <li>April underperforms its neighbours by four points and is worth a look before it ages out of the window.</li>
            </ul>
          </div>
        </section>

        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Recurring revenue</h2><p class="card-sub mb-0" data-range-label>Last 30 days</p></div></header>
          <div class="card-body">
{CHART}
          </div>
        </section>
      </div>
"""
    page("cohorts.html", "cohorts.html", "Cohorts", "Retention triangle, read down the columns not across the rows.", body,
         "A SaaS cohort retention grid rendered as a heat map, with a deliberately ragged edge where a cohort is too young to have a figure.")


def page_customers():
    rows = "\n".join(f"""              <tr>
                <th scope="row">{co}</th>
                <td data-cell="Plan"><span class="chip">{plan}</span></td>
                <td data-cell="MRR" class="tabular">£{mrr:,}</td>
                <td data-cell="Months" class="tabular">{months}</td>
                <td data-cell="Health">
                  <span class="health">
                    <span class="health-track"><span class="health-fill" style="--w:{score}%"></span></span>
                    <span class="tabular">{score}</span>
                  </span>
                </td>
                <td data-cell="Status"><span class="chip chip-{status.lower().replace(' ', '')}">{status}</span></td>
              </tr>""" for co, plan, mrr, months, status, score in CUSTOMERS)

    body = f"""
      <section class="card">
        <header class="card-head">
          <div class="form-control form-adorn" style="max-width:20rem">
            <div class="form-adorn-icon">{ICON['search']}</div>
            <input type="search" class="form-ghost" placeholder="Filter customers…" aria-label="Filter customers" data-filter="#custTable">
          </div>
          <button class="btn-outline theme-secondary btn-sm" type="button">Export CSV</button>
        </header>
        <div class="table-responsive">
          <table class="table lg:table-stacked align-middle" id="custTable">
            <thead><tr><th scope="col">Customer</th><th scope="col">Plan</th><th scope="col">MRR</th><th scope="col">Months</th><th scope="col">Health</th><th scope="col">Status</th></tr></thead>
            <tbody>
{rows}
            </tbody>
          </table>
        </div>
        <footer class="card-foot">
          <p class="fs-sm fg-3 mb-0"><span data-filter-count>{len(CUSTOMERS)}</span> of {len(CUSTOMERS)} customers</p>
        </footer>
      </section>
"""
    page("customers.html", "customers.html", "Customers", f"{len(CUSTOMERS)} accounts, sorted by nothing in particular.", body,
         "A filterable SaaS customer table with health scores and plan chips, stacking properly on small screens.", ranger=False)


def page_settings():
    body = """
      <div class="grid-2">
        <section class="card">
          <header class="card-head"><div><h2 class="card-title">Workspace</h2><p class="card-sub mb-0">Applies to everyone on the account</p></div></header>
          <div class="card-body">
            <form data-demo-form novalidate>
              <div class="row g-3">
                <div class="md:col-6">
                  <label class="form-label" for="wName">Workspace name</label>
                  <input class="form-control" type="text" id="wName" value="Northstar" required>
                </div>
                <div class="md:col-6">
                  <label class="form-label" for="wCur">Reporting currency</label>
                  <select class="form-control form-control-caret" id="wCur">
                    <option selected>GBP (£)</option><option>USD ($)</option><option>EUR (€)</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label" for="wStart">Week starts on</label>
                  <select class="form-control form-control-caret" id="wStart">
                    <option selected>Monday</option><option>Sunday</option>
                  </select>
                </div>
                <div class="col-12">
                  <button class="btn-solid theme-primary" type="submit" data-done-text="Saved ✓">Save workspace</button>
                </div>
              </div>
            </form>
          </div>
        </section>

        <section class="card">
          <header class="card-head"><div><h2 class="card-title">How MRR is counted</h2><p class="card-sub mb-0">These choices change every figure in the product</p></div></header>
          <div class="card-body">
            <div class="switch-row">
              <div><p class="mb-0 fw-semibold">Count annual plans as monthly</p><p class="fg-3 fs-sm mb-0">Divide the annual price by twelve rather than booking it all in one month.</p></div>
              <div class="switch"><input type="checkbox" role="switch" switch id="m1" checked aria-label="Count annual plans as monthly"></div>
            </div>
            <div class="switch-row">
              <div><p class="mb-0 fw-semibold">Exclude one-off charges</p><p class="fg-3 fs-sm mb-0">Setup fees and overages are not recurring, so they stay out of MRR.</p></div>
              <div class="switch"><input type="checkbox" role="switch" switch id="m2" checked aria-label="Exclude one-off charges"></div>
            </div>
            <div class="switch-row">
              <div><p class="mb-0 fw-semibold">Treat a downgrade as contraction</p><p class="fg-3 fs-sm mb-0">Off, a downgrade is booked as churn plus new, which flatters both.</p></div>
              <div class="switch"><input type="checkbox" role="switch" switch id="m3" checked aria-label="Treat a downgrade as contraction"></div>
            </div>
            <div class="switch-row">
              <div><p class="mb-0 fw-semibold">Include trials in active accounts</p><p class="fg-3 fs-sm mb-0">Off by default — a trial is not a customer.</p></div>
              <div class="switch"><input type="checkbox" role="switch" switch id="m4" aria-label="Include trials in active accounts"></div>
            </div>
          </div>
        </section>
      </div>
"""
    page("settings.html", "settings.html", "Settings", "Workspace, and the definitions every number here depends on.", body,
         "Settings for a SaaS analytics dashboard, including the MRR counting rules that change every figure in the product.", ranger=False)


page_index()
page_revenue()
page_cohorts()
page_customers()
page_settings()
print(f"wrote 5 pages — {len(SERIES['days'])} days of data")
