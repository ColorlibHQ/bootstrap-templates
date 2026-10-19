#!/usr/bin/env python3
"""
Generates Openhands: a charity homepage and an appeal page.

The donation tiers live here once — amount, and what that amount buys — and are
rendered into both the homepage widget and the appeal rail. A charity site where
the two disagree about what £50 pays for is worse than one that says nothing.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

# (value, label, what it buys)
TIERS = [
    (25, "&pound;25", "a food parcel for a family of four, for three days"),
    (50, "&pound;50", "a week of hot meals at the Kirkgate day centre"),
    (100, "&pound;100", "a night of emergency accommodation for two people"),
    (250, "&pound;250", "a caseworker&#8217;s time for a full week of appointments"),
]

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
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

TICK = ('<svg width="20" height="20" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
        '<path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1m3.2 5.2-4 4a.75.75 0 0 1-1.06 0l-2-2 1.06-1.06L7.67 8.6z"/></svg>')


def amount_buttons(prefix):
    """Radio group styled as buttons. Radios rather than buttons so the choice is
    a single form value with real keyboard semantics, which a row of <button>
    elements would not give you."""
    out = []
    for i, (v, label, buys) in enumerate(TIERS[:3]):
        checked = " checked" if i == 1 else ""
        out.append(
            f'<label class="btn-check btn-outline theme-primary">'
            f'<input type="radio" name="{prefix}amount" value="{v}" data-buys="{buys}"{checked}> {label}</label>')
    return "\n            ".join(out)


def chrome(home=True):
    p = "" if home else "index.html"
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#main">Skip to main content</a>

<header class="site-header">
  <nav class="navbar lg:navbar-expand" aria-label="Main">
    <div class="container">
      <a class="navbar-brand fw-bold" href="index.html" style="letter-spacing:-.02em">Openhands</a>

      <dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
        <div class="drawer-header">
          <h5 class="drawer-title" id="navDrawerLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
        </div>
        <div class="drawer-body mb-2 lg:mb-0">
          <ul class="nav navbar-nav ms-auto lg:gap-3">
            <li class="nav-item"><a class="nav-link" href="{p}#work">Our work</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#money">Where money goes</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#stories">Stories</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#help">Get involved</a></li>
          </ul>
        </div>
      </dialog>

      <div class="d-flex align-items-center gap-2 ms-auto">
        {TOGGLE}
        <a class="btn-solid theme-primary d-none md:d-inline-flex" href="{p}#give">Donate</a>
        <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
          <span class="navbar-toggler-icon" aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </nav>
</header>
"""


FOOTER = """
<footer class="site-footer section pb-5 bg-2">
  <div class="container">
    <div class="row g-5">
      <div class="md:col-4">
        <p class="fw-bold fs-lg mb-3" style="letter-spacing:-.02em">Openhands</p>
        <p class="fg-3 fs-sm mb-0">14 Kirkgate<br>Leeds LS1 6BY<br>United Kingdom</p>
      </div>
      <div class="md:col-2">
        <p class="fw-semibold fs-sm mb-3">About</p>
        <ul class="list-unstyled fs-sm fg-3 mb-0">
          <li class="mb-2"><a href="index.html#work">Our work</a></li>
          <li class="mb-2"><a href="index.html#money">Where money goes</a></li>
          <li class="mb-2"><a href="appeal.html">Winter appeal</a></li>
        </ul>
      </div>
      <div class="md:col-2">
        <p class="fw-semibold fs-sm mb-3">Support</p>
        <ul class="list-unstyled fs-sm fg-3 mb-0">
          <li class="mb-2"><a href="index.html#give">Donate</a></li>
          <li class="mb-2"><a href="index.html#help">Volunteer</a></li>
        </ul>
      </div>
      <div class="md:col-4">
        <p class="fw-semibold fs-sm mb-3">Registered charity</p>
        <p class="fs-xs fg-3 mb-0">
          Openhands is a registered charity in England and Wales, no. 1102938.
          Our annual report and accounts are published on the Charity Commission
          register and linked from this site every October.
        </p>
      </div>
    </div>
    <hr class="my-5">
    <p class="fs-xs fg-3 mb-0">&copy; <span data-year></span> Openhands. A free Bootstrap 6 template — the charity is fictional.</p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page_index():
    return HEAD.format(
        title="Openhands — Free Bootstrap 6 Charity &amp; NGO Website Template",
        desc="Openhands is a free Bootstrap 6 charity template — a donate widget that says what each amount buys, transparent fund allocation, programmes, stories and a volunteer form.",
    ) + chrome() + f"""
<section class="hero">
  <img class="hero-bg" src="img/hero.jpg" alt="" width="1800" height="1000" loading="eager">
  <div class="container">
    <div class="row g-6 align-items-center">
      <div class="lg:col-6">
        <p class="fs-sm fg-primary mb-3" style="letter-spacing:.14em;text-transform:uppercase">Leeds &middot; since 1998</p>
        <h1 class="hero-title mb-4">Nobody in this city should be hungry on a Tuesday</h1>
        <p class="fs-lg fg-2 mb-5" style="max-width:32rem">
          We run three day centres, a caseworker service and an emergency food
          programme across Leeds. Last year we supported 4,120 people.
        </p>
        <div class="d-flex flex-wrap gap-3">
          <a class="btn-solid theme-primary btn-lg" href="#give">Donate</a>
          <a class="btn-outline theme-secondary btn-lg" href="#money">See where money goes</a>
        </div>
      </div>

      <div class="lg:col-6" id="give">
        <div class="donate">
          <h2 class="fs-xl fw-bold mb-1">Give once, or monthly</h2>
          <p class="fg-3 fs-sm mb-4">Every donation is unrestricted unless you tell us otherwise.</p>

          <form id="donateForm" data-demo-form data-bs-validate novalidate>
            <div class="mb-3">
              <p class="form-label mb-2">How often?</p>
              <div class="d-flex flex-wrap gap-2">
                <label class="btn-check btn-outline theme-secondary"><input type="radio" name="freq" value="once" checked> Once</label>
                <label class="btn-check btn-outline theme-secondary"><input type="radio" name="freq" value="monthly"> Monthly</label>
              </div>
            </div>

            <div class="mb-3">
              <p class="form-label mb-2">Amount</p>
              <div class="amount-grid" id="amounts">
            {amount_buttons("")}
              </div>
            </div>

            <div class="form-field mb-3">
              <label class="form-label" for="custom">Or another amount</label>
              <input type="text" class="form-control" id="custom" placeholder="&pound;" inputmode="numeric">
            </div>

            <div class="buys mb-4" id="buysBox">
              <p class="mb-0 fs-sm"><span class="buys-amount" id="buysAmt">&pound;50</span> pays for <span id="buysWhat">a week of hot meals at the Kirkgate day centre</span>.</p>
            </div>

            <div class="form-field mb-3">
              <div class="switch"><input type="checkbox" id="giftaid" role="switch" switch checked></div>
              <label for="giftaid">Add Gift Aid — worth 25% more at no cost to you</label>
            </div>

            <button class="btn-solid theme-primary btn-lg w-100" type="submit" data-done-text="Thank you ✓">Continue to payment</button>
            <p class="fs-xs fg-3 mt-3 mb-0 text-center">Secure payment. We never sell or share your details.</p>
          </form>
        </div>
      </div>
    </div>
  </div>
</section>

<main id="main">

  <!-- Impact -->
  <section class="section">
    <div class="container">
      <div class="row g-4 text-center">
        <div class="sm:col-6 lg:col-3">
          <p class="impact-figure mb-2">4,120</p>
          <p class="fg-3 fs-sm mb-0">people supported last year</p>
        </div>
        <div class="sm:col-6 lg:col-3">
          <p class="impact-figure mb-2">61,400</p>
          <p class="fg-3 fs-sm mb-0">hot meals served</p>
        </div>
        <div class="sm:col-6 lg:col-3">
          <p class="impact-figure mb-2">892</p>
          <p class="fg-3 fs-sm mb-0">people helped into housing</p>
        </div>
        <div class="sm:col-6 lg:col-3">
          <p class="impact-figure mb-2">147</p>
          <p class="fg-3 fs-sm mb-0">volunteers on the rota</p>
        </div>
      </div>
    </div>
  </section>

  <!-- Where money goes -->
  <section class="section bg-2" id="money">
    <div class="container">
      <div class="row g-6">
        <div class="lg:col-5">
          <h2 class="fs-3xl fw-bold mb-3" style="letter-spacing:-.03em">Where your money goes</h2>
          <p class="fg-2 mb-4">
            Taken from our 2026 accounts, filed with the Charity Commission. We
            publish these figures because "the majority goes to the cause" is not
            a number.
          </p>
          <div class="reg-note fg-2">
            Our reserves policy holds three months of running costs. Anything
            above that is spent, not banked.
          </div>
        </div>

        <div class="lg:col-7">
          <div class="alloc-row">
            <div class="d-flex justify-content-between mb-1"><span class="fw-semibold">Front-line services</span><span class="fw-bold">78p</span></div>
            <div class="progress" role="progressbar" aria-label="Front-line services" aria-valuenow="78" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar" style="width:78%"></div></div>
            <p class="fg-3 fs-sm mb-0 mt-1">Meals, caseworkers, the day centres and emergency accommodation.</p>
          </div>
          <div class="alloc-row">
            <div class="d-flex justify-content-between mb-1"><span class="fw-semibold">Fundraising</span><span class="fw-bold">12p</span></div>
            <div class="progress" role="progressbar" aria-label="Fundraising" aria-valuenow="12" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar theme-warning" style="width:12%"></div></div>
            <p class="fg-3 fs-sm mb-0 mt-1">Raising the next pound costs something. Pretending otherwise would be dishonest.</p>
          </div>
          <div class="alloc-row">
            <div class="d-flex justify-content-between mb-1"><span class="fw-semibold">Governance &amp; admin</span><span class="fw-bold">10p</span></div>
            <div class="progress" role="progressbar" aria-label="Governance and admin" aria-valuenow="10" aria-valuemin="0" aria-valuemax="100"><div class="progress-bar theme-secondary" style="width:10%"></div></div>
            <p class="fg-3 fs-sm mb-0 mt-1">Audit, insurance, safeguarding training and the accounts you are reading.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Programmes -->
  <section class="section" id="work">
    <div class="container">
      <div class="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-5">
        <h2 class="fs-3xl fw-bold mb-0" style="letter-spacing:-.03em">What we run</h2>
        <a class="btn-outline theme-secondary" href="appeal.html">This winter's appeal</a>
      </div>
      <div class="row g-4">
        <div class="md:col-4">
          <a class="prog" href="appeal.html">
            <div class="ph"><img src="img/prog-1.jpg" alt="Volunteers serving hot meals" width="800" height="500" loading="lazy"></div>
            <div class="prog-body">
              <p class="fw-semibold mb-2">Emergency food</p>
              <p class="fg-2 fs-sm mb-3">Three day centres serving 1,200 hot meals a week, plus parcels for families referred by schools.</p>
              <p class="fs-sm fg-primary fw-semibold mb-0 mt-auto">Read more &rarr;</p>
            </div>
          </a>
        </div>
        <div class="md:col-4">
          <a class="prog" href="appeal.html">
            <div class="ph"><img src="img/prog-2.jpg" alt="A caseworker meeting" width="800" height="500" loading="lazy"></div>
            <div class="prog-body">
              <p class="fw-semibold mb-2">Casework &amp; advice</p>
              <p class="fg-2 fs-sm mb-3">Eleven caseworkers handling benefits, debt, housing applications and appeals.</p>
              <p class="fs-sm fg-primary fw-semibold mb-0 mt-auto">Read more &rarr;</p>
            </div>
          </a>
        </div>
        <div class="md:col-4">
          <a class="prog" href="appeal.html">
            <div class="ph"><img src="img/prog-3.jpg" alt="Emergency accommodation" width="800" height="500" loading="lazy"></div>
            <div class="prog-body">
              <p class="fw-semibold mb-2">Night shelter</p>
              <p class="fg-2 fs-sm mb-3">Eighteen beds from November to March, staffed overnight, no referral needed.</p>
              <p class="fs-sm fg-primary fw-semibold mb-0 mt-auto">Read more &rarr;</p>
            </div>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Stories -->
  <section class="section bg-2" id="stories">
    <div class="container">
      <div class="row g-6 align-items-center">
        <div class="lg:col-6">
          <div class="ph ph-4x3 rounded-4"><img src="img/story.jpg" alt="A volunteer and a visitor at the day centre" width="900" height="675" loading="lazy"></div>
        </div>
        <div class="lg:col-6">
          <div class="story">
            <p class="story-quote mb-4">
              "I came in for the food, honestly. It was six weeks before I let
              anyone help with the rest of it. Nobody pushed. That is why I came
              back."
            </p>
            <p class="fw-semibold mb-1">Denise</p>
            <p class="fg-3 fs-sm mb-0">Kirkgate day centre, now volunteering on Thursdays</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Get involved -->
  <section class="section" id="help">
    <div class="container">
      <div class="row g-6">
        <div class="lg:col-5">
          <h2 class="fs-3xl fw-bold mb-3" style="letter-spacing:-.03em">Other ways to help</h2>
          <p class="fg-2 mb-4">
            Money is the most useful thing, but it is not the only thing. We are
            always short of Thursday drivers.
          </p>
          <div class="trust-row">{TICK}<div><p class="fw-semibold mb-1">Volunteer</p><p class="fg-3 fs-sm mb-0">Three-hour shifts, DBS check provided, training on your first day.</p></div></div>
          <div class="trust-row">{TICK}<div><p class="fw-semibold mb-1">Corporate partnership</p><p class="fg-3 fs-sm mb-0">Match funding, payroll giving, or lending us a van in December.</p></div></div>
          <div class="trust-row">{TICK}<div><p class="fw-semibold mb-1">Leave a gift in your will</p><p class="fg-3 fs-sm mb-0">Legacies funded the night shelter's entire first year.</p></div></div>
        </div>

        <div class="lg:col-7">
          <div class="donate">
            <h3 class="fs-xl fw-bold mb-4">Volunteer enquiry</h3>
            <form data-demo-form data-bs-validate novalidate>
              <div class="row g-3">
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="vName">Your name</label>
                    <input type="text" class="form-control" id="vName" required>
                    <div class="invalid-feedback">Required.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="vEmail">Email</label>
                    <input type="email" class="form-control" id="vEmail" required>
                    <div class="invalid-feedback">A valid email, please.</div>
                  </div>
                </div>
                <div class="col-12">
                  <label class="form-label">Which would suit you?</label>
                  <button class="form-control combobox-toggle" type="button" data-bs-toggle="combobox" data-bs-search="true" data-bs-multiple="true" data-bs-name="roles" data-bs-placeholder="Select one or more…">
                    <span class="combobox-value">Select one or more…</span>
                    <svg class="combobox-caret" width="10" height="16" viewBox="0 0 10 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M0.46967 5.46967C0.762563 5.17678 1.23744 5.17678 1.53033 5.46967L5 8.93934L8.46967 5.46967C8.76256 5.17678 9.23744 5.17678 9.53033 5.46967C9.82322 5.76256 9.82322 6.23744 9.53033 6.53033L5.53033 10.5303C5.23744 10.8232 4.76256 10.8232 4.46967 10.5303L0.46967 6.53033C0.176777 6.23744 0.176777 5.76256 0.46967 5.46967Z" fill="currentcolor"/></svg>
                  </button>
                  <div class="menu">
                    <button class="menu-item" type="button" data-bs-value="kitchen">Kitchen &amp; serving</button>
                    <button class="menu-item" type="button" data-bs-value="driving">Driving &amp; collections</button>
                    <button class="menu-item" type="button" data-bs-value="admin">Admin &amp; reception</button>
                    <button class="menu-item" type="button" data-bs-value="night">Night shelter</button>
                    <button class="menu-item" type="button" data-bs-value="trustee">Trustee or committee</button>
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="vStart">Earliest you could start</label>
                    <input type="text" class="form-control" id="vStart" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date…">
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <div class="switch"><input type="checkbox" id="vDbs" role="switch" switch></div>
                    <label for="vDbs">I already hold an enhanced DBS</label>
                  </div>
                </div>
                <div class="col-12">
                  <button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Thank you ✓">Send enquiry</button>
                  <p class="fs-xs fg-3 mt-3 mb-0">Our volunteer coordinator replies within a week.</p>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>
""" + FOOTER


def page_appeal():
    tiers = "\n".join(
        f'            <div class="spec-row"><span class="fs-sm">{label}</span>'
        f'<span class="fg-3 fs-sm text-end" style="max-width:14rem">{buys}</span></div>'
        for v, label, buys in TIERS)
    return HEAD.format(
        title="Winter appeal — Openhands | Free Bootstrap 6 Charity Template",
        desc="Appeal page from the Openhands Bootstrap 6 charity template — target progress, what each amount buys, and a sticky donate rail.",
    ) + chrome(home=False) + f"""
<div class="sub-head">
  <div class="container">
    <nav aria-label="Breadcrumb" class="mb-3">
      <ol class="breadcrumb mb-0">
        <li class="breadcrumb-item"><a class="breadcrumb-link" href="index.html">Openhands</a></li>
        <li class="breadcrumb-item"><a class="breadcrumb-link" href="index.html#work">Our work</a></li>
        <li class="breadcrumb-item active" aria-current="page">Winter appeal</li>
      </ol>
    </nav>
    <p class="fs-sm fg-primary mb-2" style="letter-spacing:.14em;text-transform:uppercase">Appeal &middot; closes 28 February</p>
    <h1 class="fs-4xl fw-bold mb-3" style="letter-spacing:-.03em">Keep the night shelter open</h1>
    <p class="fs-lg fg-2 mb-0" style="max-width:42rem">
      Eighteen beds, November to March, staffed every night. It costs
      &pound;164,000 to run and we are &pound;38,000 short.
    </p>
  </div>
</div>

<main id="main">
  <section class="section">
    <div class="container">
      <div class="row g-6">
        <div class="lg:col-8">
          <div class="ph ph-16x9 rounded-4 mb-5">
            <img src="img/prog-3.jpg" alt="Inside the night shelter" width="1200" height="675" loading="eager">
          </div>

          <div class="prose">
            <h2 class="fs-2xl fw-bold mb-3">Why this appeal</h2>
            <p class="fg-2">
              The shelter opened in 2019 as a six-week pilot with twelve camp beds
              in a church hall. It now runs five months a year with eighteen proper
              beds, two staff overnight and a caseworker attached, because a bed
              on its own does not change anything by March.
            </p>
            <p class="fg-2">
              Local authority funding covered 62% of last winter. This year it
              covers 39%. Nothing about the need has changed — only the funding.
            </p>

            <h2 class="fs-2xl fw-bold mb-3 mt-6">What the money does</h2>
            <p class="fg-2">
              Roughly two thirds is staffing. It is a legal requirement to have two
              awake staff overnight and it is the single thing that makes the
              shelter safe enough for people to actually sleep.
            </p>
            <div class="spec-row"><span class="fs-sm">Overnight staffing</span><span class="fs-sm">&pound;104,000</span></div>
            <div class="spec-row"><span class="fs-sm">Building, heat and light</span><span class="fs-sm">&pound;28,000</span></div>
            <div class="spec-row"><span class="fs-sm">Food and bedding</span><span class="fs-sm">&pound;19,000</span></div>
            <div class="spec-row"><span class="fs-sm">Caseworker time</span><span class="fs-sm">&pound;13,000</span></div>

            <h2 class="fs-2xl fw-bold mb-3 mt-6">What happens if we fall short</h2>
            <p class="fg-2 mb-0">
              We open in November regardless and close early. Last time that
              happened it was the third week of February, which is the coldest
              fortnight of the year in this city.
            </p>
          </div>
        </div>

        <div class="lg:col-4">
          <div class="appeal-rail">
            <p class="impact-figure mb-1">&pound;126,000</p>
            <p class="fg-3 fs-sm mb-3">raised of &pound;164,000</p>
            <div class="progress mb-4" role="progressbar" aria-label="Appeal progress" aria-valuenow="77" aria-valuemin="0" aria-valuemax="100">
              <div class="progress-bar" style="width:77%"></div>
            </div>

            <p class="form-label mb-2">What your gift buys</p>
{tiers}

            <a class="btn-solid theme-primary btn-lg w-100 mt-4" href="index.html#give">Donate to this appeal</a>
            <p class="fs-xs fg-3 mt-3 mb-0 text-center">1,847 people have given so far.</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>
""" + FOOTER


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "appeal.html").write_text(page_appeal(), encoding="utf-8")
print("wrote index.html + appeal.html")
