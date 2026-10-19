#!/usr/bin/env python3
"""
Generates Forecourt: a dealership homepage and a vehicle detail page.

Vehicle data lives here once and renders both pages. The monthly figures are
computed from the cash price by the same formula the page script uses at runtime,
so the static markup and the live calculator agree on load rather than jumping
the moment the script runs.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

# Finance assumptions used for the figures baked into the markup. The page
# script recalculates with the same numbers, so nothing shifts on first paint.
APR = 9.9
TERM = 48
DEPOSIT_PCT = 10

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="dark">
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

CARET = ('<svg class="combobox-caret" width="10" height="16" viewBox="0 0 10 16" fill="none" '
         'xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M0.46967 5.46967C0.762563 5.17678 '
         '1.23744 5.17678 1.53033 5.46967L5 8.93934L8.46967 5.46967C8.76256 5.17678 9.23744 5.17678 9.53033 '
         '5.46967C9.82322 5.76256 9.82322 6.23744 9.53033 6.53033L5.53033 10.5303C5.23744 10.8232 4.76256 '
         '10.8232 4.46967 10.5303L0.46967 6.53033C0.176777 6.23744 0.176777 5.76256 0.46967 5.46967Z" '
         'fill="currentcolor"/></svg>')

SEARCH = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
          'aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 4 4" stroke-linecap="round"/></svg>')

TICK = ('<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
        '<path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1m3.2 5.2-4 4a.75.75 0 0 1-1.06 0l-2-2 1.06-1.06L7.67 8.6z"/></svg>')


def monthly(cash, apr=APR, term=TERM, deposit_pct=DEPOSIT_PCT):
    """Flat-rate monthly figure. Deliberately simple and stated as such on the
    page — a real dealer quote is an APR calculation on a reducing balance, and
    pretending otherwise in a template would be misleading."""
    financed = cash * (1 - deposit_pct / 100)
    total = financed * (1 + (apr / 100) * (term / 12))
    return round(total / term)


def combobox(name, placeholder, options, search=False):
    attrs = 'data-bs-toggle="combobox"' + (' data-bs-search="true"' if search else "")
    items = "\n          ".join(
        f'<button class="menu-item" type="button" data-bs-value="{v}">{l}</button>' for v, l in options)
    return f"""<button class="form-control combobox-toggle" type="button" {attrs} data-bs-name="{name}" data-bs-placeholder="{placeholder}">
          <span class="combobox-value">{placeholder}</span>
          {CARET}
        </button>
        <div class="menu">
          {items}
        </div>"""


# (img, name, trim, year, mileage, fuel, gearbox, cash, flag)
CARS = [
    ("car-1", "Volvo XC40", "B4 Plus Dark", "2023", "18,400", "Mild hybrid", "Automatic", 27995, "Just in"),
    ("car-2", "Škoda Octavia", "1.5 TSI SE L", "2022", "31,200", "Petrol", "Manual", 17450, None),
    ("car-3", "BMW 3 Series", "320d M Sport", "2022", "27,850", "Diesel", "Automatic", 24990, None),
    ("car-4", "Kia EV6", "GT-Line S", "2024", "9,100", "Electric", "Automatic", 34495, "Low mileage"),
    ("car-5", "Ford Puma", "1.0 EcoBoost ST-Line", "2023", "22,600", "Petrol", "Manual", 16995, None),
    ("car-6", "Toyota Corolla", "1.8 Hybrid Design", "2023", "19,300", "Hybrid", "Automatic", 20950, None),
]


def car_card(c):
    (img, name, trim, year, miles, fuel, box, cash, flag) = c
    pm = monthly(cash)
    flag_html = f'<span class="car-flag">{flag}</span>' if flag else ""
    return f"""        <div class="sm:col-6 lg:col-4">
          <a class="car" href="vehicle.html">
            <div class="car-media">
              <div class="ph"><img src="img/{img}.jpg" alt="{name} {trim}" width="800" height="600" loading="lazy"></div>
              {flag_html}
            </div>
            <div class="car-body">
              <p class="car-name mb-1">{name}</p>
              <p class="car-trim mb-0">{trim}</p>
              <div class="car-specs">
                <span>{year}</span><span>{miles} mi</span><span>{box}</span>
              </div>
              <div class="mt-auto">
                <p class="car-pm mb-1" data-cash="{cash}">&pound;{pm}<span class="fs-xs fg-3 fw-normal">/mo</span></p>
                <p class="car-cash mb-0">&pound;{cash:,} cash &middot; {fuel}</p>
              </div>
            </div>
          </a>
        </div>"""


def chrome(home=True):
    p = "" if home else "index.html"
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-3" href="#main">Skip to main content</a>

<header class="site-header">
  <nav class="navbar lg:navbar-expand" aria-label="Main">
    <div class="container">
      <a class="navbar-brand fw-bold" href="index.html" style="letter-spacing:-.02em">Forecourt</a>

      <dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
        <div class="drawer-header">
          <h5 class="drawer-title" id="navDrawerLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
        </div>
        <div class="drawer-body mb-3 lg:mb-0">
          <ul class="nav navbar-nav ms-auto lg:gap-4">
            <li class="nav-item"><a class="nav-link" href="{p}#stock">Used cars</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#finance">Finance</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#partex">Part exchange</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#branches">Branches</a></li>
          </ul>
        </div>
      </dialog>

      <div class="d-flex align-items-center gap-3 ms-auto">
        {TOGGLE}
        <a class="btn-solid theme-primary d-none md:d-inline-flex" href="tel:01138000000">0113 800 0000</a>
        <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
          <span class="navbar-toggler-icon" aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </nav>
</header>
"""


FOOTER = """
<footer class="site-footer section pb-6 bg-2">
  <div class="container">
    <div class="row g-6">
      <div class="md:col-4">
        <p class="fw-bold fs-lg mb-4" style="letter-spacing:-.02em">Forecourt</p>
        <p class="fg-3 fs-sm mb-0">Three branches across West Yorkshire. Every car HPI-checked, every price the price.</p>
      </div>
      <div class="md:col-2">
        <p class="fw-semibold fs-sm mb-4">Buying</p>
        <ul class="list-unstyled fs-sm fg-3 mb-0">
          <li class="mb-3"><a href="index.html#stock">Used cars</a></li>
          <li class="mb-3"><a href="vehicle.html">Example listing</a></li>
          <li class="mb-3"><a href="index.html#finance">Finance</a></li>
        </ul>
      </div>
      <div class="md:col-2">
        <p class="fw-semibold fs-sm mb-4">Selling</p>
        <ul class="list-unstyled fs-sm fg-3 mb-0">
          <li class="mb-3"><a href="index.html#partex">Part exchange</a></li>
          <li class="mb-3"><a href="index.html#branches">Branches</a></li>
        </ul>
      </div>
      <div class="md:col-4">
        <p class="fw-semibold fs-sm mb-4">Regulatory</p>
        <p class="fs-xs fg-3 mb-0">
          Forecourt Motor Group is authorised and regulated by the Financial Conduct Authority.
          Finance subject to status. Figures shown are illustrative flat-rate estimates, not a quotation.
        </p>
      </div>
    </div>
    <hr class="my-6">
    <p class="fs-xs fg-3 mb-0">&copy; <span data-year></span> Forecourt. A free Bootstrap 6 template — the dealership is fictional.</p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page_index():
    cards = "\n".join(car_card(c) for c in CARS)
    sample = monthly(24990)
    return HEAD.format(
        title="Forecourt — Free Bootstrap 6 Car Dealership Website Template",
        desc="Forecourt is a free Bootstrap 6 car dealership template — vehicle cards led by the monthly payment, a live finance calculator with Range sliders, part exchange and a full vehicle page.",
    ) + chrome() + f"""
<section class="showroom">
  <img class="hero-bg" src="img/hero.jpg" alt="" width="1800" height="1000" loading="eager">
  <div class="container">
    <div class="row">
      <div class="lg:col-7">
        <p class="fs-sm fg-primary mb-4" style="letter-spacing:.14em;text-transform:uppercase">218 cars in stock</p>
        <h1 class="showroom-title mb-5">The price you see is the price you pay</h1>
        <p class="fs-lg fg-2 mb-6" style="max-width:34rem">
          No admin fee, no delivery fee, no "preparation" line appearing at
          signing. Every car HPI-checked and priced against the market weekly.
        </p>
      </div>
    </div>

    <form class="find-bar" role="search" onsubmit="return false">
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">{SEARCH}</div>
        <input type="search" class="form-ghost" placeholder="Make or model" aria-label="Make or model">
      </div>
      <div>
        {combobox("budget", "Monthly budget", [("150", "Up to &pound;150"), ("250", "Up to &pound;250"), ("400", "Up to &pound;400"), ("600", "Up to &pound;600"), ("any", "Any")])}
      </div>
      <div>
        {combobox("fuel", "Any fuel", [("petrol", "Petrol"), ("diesel", "Diesel"), ("hybrid", "Hybrid"), ("ev", "Electric")], search=True)}
      </div>
      <button class="btn-solid theme-primary btn-lg" type="submit">Search stock</button>
    </form>
  </div>
</section>

<main id="main">

  <!-- Stock -->
  <section class="section" id="stock">
    <div class="container">
      <div class="d-flex flex-wrap justify-content-between align-items-end gap-4 mb-5">
        <div>
          <h2 class="fs-3xl fw-bold mb-1" style="letter-spacing:-.03em">Latest arrivals</h2>
          <p class="fg-3 fs-sm mb-0">Monthly figures assume {DEPOSIT_PCT}% deposit over {TERM} months at {APR}% APR.</p>
        </div>
        <a class="btn-outline theme-secondary" href="#stock">View all 218</a>
      </div>

      <div class="row g-5">
{cards}
      </div>
    </div>
  </section>

  <!-- Finance calculator -->
  <section class="section bg-2" id="finance">
    <div class="container">
      <div class="row g-7 align-items-center">
        <div class="lg:col-5">
          <h2 class="fs-3xl fw-bold mb-4" style="letter-spacing:-.03em">What it actually costs</h2>
          <p class="fg-2 mb-5">
            Move the sliders and every monthly figure on this page updates with
            them — including the cards above. A calculator that does not change
            the listings is decoration.
          </p>
          <p class="fs-sm fg-3 mb-0">
            These are flat-rate illustrations for comparison, not a quotation. A
            real agreement is calculated on a reducing balance and depends on
            your credit profile.
          </p>
        </div>

        <div class="lg:col-7">
          <div class="calc">
            <div class="row g-5">
              <div class="md:col-7">
                <div class="mb-5">
                  <div class="d-flex justify-content-between mb-1">
                    <label class="form-label mb-0" for="cDep">Deposit</label>
                    <strong id="cDepOut">10%</strong>
                  </div>
                  <div class="form-range">
                    <input type="range" class="form-range-input" id="cDep" min="0" max="40" step="5" value="{DEPOSIT_PCT}" aria-label="Deposit percentage">
                  </div>
                </div>

                <div class="mb-5">
                  <div class="d-flex justify-content-between mb-1">
                    <label class="form-label mb-0" for="cTerm">Term</label>
                    <strong id="cTermOut">48 months</strong>
                  </div>
                  <div class="form-range">
                    <input type="range" class="form-range-input" id="cTerm" min="12" max="60" step="12" value="{TERM}" aria-label="Term in months">
                  </div>
                </div>

                <div>
                  <div class="d-flex justify-content-between mb-1">
                    <label class="form-label mb-0" for="cApr">APR</label>
                    <strong id="cAprOut">9.9%</strong>
                  </div>
                  <div class="form-range">
                    <input type="range" class="form-range-input" id="cApr" min="4.9" max="19.9" step="1" value="{APR}" aria-label="Annual percentage rate">
                  </div>
                </div>
              </div>

              <div class="md:col-5">
                <p class="fs-xs fg-3 mb-1" style="letter-spacing:.12em;text-transform:uppercase">BMW 3 Series, &pound;24,990</p>
                <p class="calc-figure mb-5" id="cMonthly" data-cash="24990">&pound;{sample}<span class="fs-sm fg-3 fw-normal">/mo</span></p>
                <div class="calc-row"><span class="fg-3 fs-sm">Deposit</span><span class="fs-sm" id="cDepAmt">&pound;2,499</span></div>
                <div class="calc-row"><span class="fg-3 fs-sm">Amount financed</span><span class="fs-sm" id="cFin">&pound;22,491</span></div>
                <div class="calc-row"><span class="fg-3 fs-sm">Total payable</span><span class="fs-sm" id="cTotal">&pound;31,388</span></div>
                <a class="btn-solid theme-primary w-100 mt-5" href="vehicle.html">See this car</a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Part exchange -->
  <section class="section" id="partex">
    <div class="container">
      <div class="row g-7">
        <div class="lg:col-5">
          <h2 class="fs-3xl fw-bold mb-4" style="letter-spacing:-.03em">Part exchange</h2>
          <p class="fg-2 mb-5">
            Give us the registration and we will come back with a figure inside
            two hours during opening times. If we cannot beat the online buyers
            we will tell you that too.
          </p>
          <div class="trust-cell">{TICK}<div><p class="fw-semibold mb-1">Valuation held for 7 days</p><p class="fg-3 fs-sm mb-0">Not "subject to inspection" and then dropped on the day.</p></div></div>
          <div class="trust-cell">{TICK}<div><p class="fw-semibold mb-1">Outstanding finance settled</p><p class="fg-3 fs-sm mb-0">We handle the settlement directly with your lender.</p></div></div>
          <div class="trust-cell">{TICK}<div><p class="fw-semibold mb-1">We will buy it outright</p><p class="fg-3 fs-sm mb-0">You do not have to buy a car from us to sell one to us.</p></div></div>
        </div>

        <div class="lg:col-7">
          <div class="calc">
            <form data-demo-form data-bs-validate novalidate>
              <div class="row g-4">
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pxReg">Registration</label>
                    <input type="text" class="form-control text-uppercase" id="pxReg" placeholder="AB12 CDE" required>
                    <div class="invalid-feedback">We need the reg to value it.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pxMiles">Mileage</label>
                    <input type="text" class="form-control" id="pxMiles" placeholder="42,000" required>
                    <div class="invalid-feedback">Roughly is fine.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <label class="form-label">Condition</label>
                  {combobox("cond", "Choose one…", [("ex", "Excellent"), ("good", "Good, a few marks"), ("fair", "Fair, needs work"), ("poor", "Poor")])}
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pxWhen">When are you looking to change?</label>
                    <input type="text" class="form-control" id="pxWhen" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date…">
                  </div>
                </div>
                <div class="col-12">
                  <div class="form-field">
                    <div class="switch"><input type="checkbox" id="pxFinance" role="switch" switch></div>
                    <label for="pxFinance">There is outstanding finance on the car</label>
                  </div>
                </div>
                <div class="col-12">
                  <button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Valuation requested ✓">Get a valuation</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Branches -->
  <section class="section bg-2" id="branches">
    <div class="container">
      <h2 class="fs-3xl fw-bold mb-6" style="letter-spacing:-.03em">Three branches</h2>
      <div class="row g-5">
        <div class="md:col-4">
          <div class="branch">
            <p class="fw-semibold mb-1">Leeds</p>
            <p class="fg-3 fs-sm mb-4">Kirkstall Road, LS4 2AZ</p>
            <div class="spec-row"><span class="fg-3 fs-sm">Mon — Fri</span><span class="fs-sm">08:30 — 18:00</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Saturday</span><span class="fs-sm">09:00 — 17:00</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Sunday</span><span class="fs-sm">11:00 — 16:00</span></div>
            <p class="fs-sm mt-4 mb-0"><a href="tel:01138000000">0113 800 0000</a></p>
          </div>
        </div>
        <div class="md:col-4">
          <div class="branch">
            <p class="fw-semibold mb-1">Bradford</p>
            <p class="fg-3 fs-sm mb-4">Canal Road, BD1 4SG</p>
            <div class="spec-row"><span class="fg-3 fs-sm">Mon — Fri</span><span class="fs-sm">08:30 — 18:00</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Saturday</span><span class="fs-sm">09:00 — 17:00</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Sunday</span><span class="fs-sm">Closed</span></div>
            <p class="fs-sm mt-4 mb-0"><a href="tel:01274000000">01274 000 000</a></p>
          </div>
        </div>
        <div class="md:col-4">
          <div class="branch">
            <p class="fw-semibold mb-1">Wakefield</p>
            <p class="fg-3 fs-sm mb-4">Denby Dale Road, WF2 7AW</p>
            <div class="spec-row"><span class="fg-3 fs-sm">Mon — Fri</span><span class="fs-sm">09:00 — 18:00</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Saturday</span><span class="fs-sm">09:00 — 17:00</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Sunday</span><span class="fs-sm">11:00 — 16:00</span></div>
            <p class="fs-sm mt-4 mb-0"><a href="tel:01924000000">01924 000 000</a></p>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>
""" + FOOTER


def page_vehicle():
    cash = 24990
    pm = monthly(cash)
    return HEAD.format(
        title="BMW 3 Series 320d M Sport — Forecourt | Free Bootstrap 6 Dealership Template",
        desc="Vehicle listing page from the Forecourt Bootstrap 6 car dealership template — gallery, full specification, history and a sticky finance rail.",
    ) + chrome(home=False) + f"""
<div class="sub-head">
  <div class="container">
    <nav aria-label="Breadcrumb" class="mb-4">
      <ol class="breadcrumb mb-0">
        <li class="breadcrumb-item"><a class="breadcrumb-link" href="index.html">Forecourt</a></li>
        <li class="breadcrumb-item"><a class="breadcrumb-link" href="index.html#stock">Used cars</a></li>
        <li class="breadcrumb-item active" aria-current="page">BMW 3 Series</li>
      </ol>
    </nav>
    <h1 class="fs-3xl fw-bold mb-1" style="letter-spacing:-.03em">BMW 3 Series 320d M Sport</h1>
    <p class="fg-3 mb-0">2022 &middot; 27,850 miles &middot; Diesel &middot; Automatic &middot; Leeds</p>
  </div>
</div>

<main id="main">
  <section class="section">
    <div class="container">
      <div class="row g-7">
        <div class="lg:col-8">
          <div class="ph ph-16x9 rounded-4">
            <img src="img/car-3.jpg" alt="BMW 3 Series 320d M Sport" width="1200" height="675" loading="eager">
          </div>
          <div class="gallery-strip">
            <div class="ph"><img src="img/car-1.jpg" alt="Interior" width="300" height="225" loading="lazy"></div>
            <div class="ph"><img src="img/car-2.jpg" alt="Rear three-quarter" width="300" height="225" loading="lazy"></div>
            <div class="ph"><img src="img/car-4.jpg" alt="Dashboard" width="300" height="225" loading="lazy"></div>
            <div class="ph"><img src="img/car-5.jpg" alt="Boot space" width="300" height="225" loading="lazy"></div>
          </div>

          <div class="prose mt-7">
            <h2 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">About this car</h2>
            <p class="fg-2">
              One owner from new, full BMW service history with the last stamp at
              24,900 miles. Bought and part-exchanged at our Leeds branch, so we
              know the car rather than the auction description of it.
            </p>
            <p class="fg-2">
              Two scuffs on the nearside alloy and a small stone chip on the
              bonnet, both photographed rather than described. Everything else is
              as you would expect for the mileage.
            </p>

            <h2 class="fs-2xl fw-bold mb-4 mt-7">Specification</h2>
            <div class="row g-0 lg:gx-6">
              <div class="md:col-6">
                <div class="spec-row"><span class="fg-3 fs-sm">Registered</span><span class="fs-sm">March 2022</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Mileage</span><span class="fs-sm">27,850</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Engine</span><span class="fs-sm">2.0 diesel</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Gearbox</span><span class="fs-sm">8-speed automatic</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Body</span><span class="fs-sm">Saloon, 4 doors</span></div>
              </div>
              <div class="md:col-6">
                <div class="spec-row"><span class="fg-3 fs-sm">Owners</span><span class="fs-sm">1</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Service history</span><span class="fs-sm">Full, main dealer</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">MOT</span><span class="fs-sm">Until Feb 2027</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Road tax</span><span class="fs-sm">&pound;190 / year</span></div>
                <div class="spec-row"><span class="fg-3 fs-sm">Combined mpg</span><span class="fs-sm">58.9</span></div>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-4">
          <div class="buy-rail">
            <p class="calc-figure mb-1" id="cMonthly" data-cash="{cash}">&pound;{pm}<span class="fs-sm fg-3 fw-normal">/mo</span></p>
            <p class="fg-3 fs-sm mb-5">&pound;{cash:,} cash &middot; {DEPOSIT_PCT}% deposit, {TERM} months, {APR}% APR</p>

            <button class="btn-solid theme-primary w-100 mb-3" type="button" data-bs-toggle="dialog" data-bs-target="#bookDialog">Book a viewing</button>
            <button class="btn-outline theme-secondary w-100 mb-5" type="button">Reserve for &pound;99</button>

            <div class="spec-row"><span class="fg-3 fs-sm">Location</span><span class="fs-sm">Leeds</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Stock number</span><span class="fs-sm">FC-4821</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">HPI check</span><span class="fs-sm">Clear</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Warranty</span><span class="fs-sm">12 months</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Part exchange</span><span class="fs-sm">Welcome</span></div>

            <p class="fs-xs fg-3 mt-5 mb-0">Illustrative flat-rate figure, not a quotation. Finance subject to status.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

<dialog class="dialog" id="bookDialog" aria-labelledby="bookLabel">
  <div class="dialog-header">
    <h2 class="dialog-title fs-lg" id="bookLabel">Book a viewing</h2>
    <button type="button" class="btn-close" data-bs-dismiss="dialog" aria-label="Close"></button>
  </div>
  <form class="dialog-body vstack gap-4" id="bookForm" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="bkName">Your name</label>
      <input type="text" class="form-control" id="bkName" required>
      <div class="invalid-feedback">Required.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="bkPhone">Phone</label>
      <input type="tel" class="form-control" id="bkPhone" required>
      <div class="invalid-feedback">We will call to confirm.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="bkDate">Preferred day</label>
      <input type="text" class="form-control" id="bkDate" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date…" required>
      <div class="invalid-feedback">Pick a day.</div>
    </div>
    <div class="form-field">
      <div class="switch"><input type="checkbox" id="bkPx" role="switch" switch></div>
      <label for="bkPx">I have a car to part exchange</label>
    </div>
  </form>
  <div class="dialog-footer">
    <button type="button" class="btn-text" data-bs-dismiss="dialog">Cancel</button>
    <button type="submit" form="bookForm" class="btn-solid theme-primary" data-done-text="Booked ✓">Book viewing</button>
  </div>
</dialog>
""" + FOOTER


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "vehicle.html").write_text(page_vehicle(), encoding="utf-8")
print("wrote index.html + vehicle.html")
