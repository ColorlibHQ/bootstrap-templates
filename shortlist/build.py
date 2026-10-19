#!/usr/bin/env python3
"""
Generates Shortlist: a job board homepage and a job detail page.

The job data lives here once and is rendered by both pages, so the listing and
the detail can never disagree about a salary — which is the one thing a job
board must never get wrong.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

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
<body{bodyattr}>
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

PIN = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
       'aria-hidden="true"><path d="M8 14s5-3.2 5-7a5 5 0 0 0-10 0c0 3.8 5 7 5 7" stroke-linejoin="round"/>'
       '<circle cx="8" cy="7" r="1.9"/></svg>')


def combobox(name, placeholder, options, search=False, multiple=False):
    attrs = 'data-bs-toggle="combobox"'
    if search:
        attrs += ' data-bs-search="true"'
    if multiple:
        attrs += ' data-bs-multiple="true"'
    items = "\n          ".join(
        f'<button class="menu-item" type="button" data-bs-value="{v}">{l}</button>' for v, l in options)
    return f"""<button class="form-control combobox-toggle" type="button" {attrs} data-bs-name="{name}" data-bs-placeholder="{placeholder}">
          <span class="combobox-value">{placeholder}</span>
          {CARET}
        </button>
        <div class="menu">
          {items}
        </div>"""


# (id, title, company, initials, location, mode, type, pay, tags, new)
JOBS = [
    ("j1", "Senior Frontend Engineer", "Northwind Trading", "NT", "Leeds", "Hybrid", "Permanent",
     "&pound;65,000 — &pound;78,000", ["TypeScript", "React", "Design systems"], True),
    ("j2", "Product Designer", "Lumen Studio", "LS", "Remote (UK)", "Remote", "Permanent",
     "&pound;52,000 — &pound;62,000", ["Figma", "Research", "Design systems"], True),
    ("j3", "Data Engineer", "Kestrel Logistics", "KL", "Manchester", "Hybrid", "Permanent",
     "&pound;58,000 — &pound;70,000", ["Python", "dbt", "Snowflake"], False),
    ("j4", "Engineering Manager", "Fieldstone Group", "FG", "Sheffield", "On-site", "Permanent",
     "&pound;80,000 — &pound;95,000", ["Leadership", "Go", "Platform"], False),
    ("j5", "Customer Success Lead", "Ardent Works", "AW", "Bristol", "Hybrid", "Permanent",
     None, ["SaaS", "B2B"], False),
    ("j6", "Junior Developer", "Halden &amp; Co", "HC", "Leeds", "On-site", "Permanent",
     "&pound;28,000 — &pound;34,000", ["JavaScript", "Graduate welcome"], False),
    ("j7", "Contract QA Engineer", "Pemberton Civils", "PC", "Remote (UK)", "Remote", "Contract",
     "&pound;450 — &pound;525 / day", ["Playwright", "6 months"], False),
    ("j8", "Head of Marketing", "Sable Interiors", "SI", "London", "Hybrid", "Permanent",
     "&pound;72,000 — &pound;85,000", ["B2C", "Brand", "Team of 6"], False),
]


def job_row(j, href="job.html"):
    (jid, title, co, ini, loc, mode, jtype, pay, tags, new) = j
    pay_html = (f'<span class="job-pay">{pay}</span>' if pay
                else '<span class="job-pay job-pay-hidden">Salary not disclosed</span>')
    tag_html = "".join(f'<span class="chip">{t}</span>' for t in tags)
    new_html = '<span class="job-new">New</span> ' if new else ""
    return f"""      <a class="job" href="{href}">
        <div class="job-head">
          <span class="job-logo" aria-hidden="true">{ini}</span>
          <div class="me-auto">
            <p class="job-title mb-1">{new_html}{title}</p>
            <p class="job-co mb-0">{co} &middot; {loc} &middot; {mode}</p>
          </div>
          <div class="text-end">
            {pay_html}
            <p class="fg-3 fs-xs mb-0 mt-1">{jtype}</p>
          </div>
        </div>
        <div class="job-tags">{tag_html}</div>
      </a>"""


def chrome_header(active_home=True):
    prefix = "" if active_home else "index.html"
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#main">Skip to main content</a>

<header class="site-header">
  <nav class="navbar lg:navbar-expand" aria-label="Main">
    <div class="container">
      <a class="navbar-brand fw-bold" href="index.html" style="letter-spacing:-.02em">Shortlist</a>

      <dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
        <div class="drawer-header">
          <h5 class="drawer-title" id="navDrawerLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
        </div>
        <div class="drawer-body mb-2 lg:mb-0">
          <ul class="nav navbar-nav ms-auto lg:gap-3">
            <li class="nav-item"><a class="nav-link" href="{prefix}#jobs">Browse jobs</a></li>
            <li class="nav-item"><a class="nav-link" href="{prefix}#sectors">Sectors</a></li>
            <li class="nav-item"><a class="nav-link" href="{prefix}#companies">Companies</a></li>
            <li class="nav-item"><a class="nav-link" href="{prefix}#post">For employers</a></li>
          </ul>
        </div>
      </dialog>

      <div class="d-flex align-items-center gap-2 ms-auto">
        {TOGGLE}
        <a class="btn-solid theme-primary d-none md:d-inline-flex" href="{prefix}#post">Post a job</a>
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
        <p class="fw-bold fs-lg mb-3" style="letter-spacing:-.02em">Shortlist</p>
        <p class="fg-3 fs-sm mb-0">Every job on this board shows a salary range. It is a condition of listing, not a preference.</p>
      </div>
      <div class="md:col-2">
        <p class="fw-semibold fs-sm mb-3">Candidates</p>
        <ul class="list-unstyled fs-sm fg-3 mb-0">
          <li class="mb-2"><a href="index.html#jobs">Browse jobs</a></li>
          <li class="mb-2"><a href="index.html#sectors">By sector</a></li>
          <li class="mb-2"><a href="job.html">Example listing</a></li>
        </ul>
      </div>
      <div class="md:col-2">
        <p class="fw-semibold fs-sm mb-3">Employers</p>
        <ul class="list-unstyled fs-sm fg-3 mb-0">
          <li class="mb-2"><a href="index.html#post">Post a job</a></li>
          <li class="mb-2"><a href="index.html#companies">Companies</a></li>
        </ul>
      </div>
      <div class="md:col-4">
        <p class="fw-semibold fs-sm mb-3">Job alerts</p>
        <p class="fs-sm fg-3 mb-0">One email a week, only roles matching your filters. Unsubscribe in one click.</p>
      </div>
    </div>
    <hr class="my-5">
    <p class="fs-xs fg-3 mb-0">&copy; <span data-year></span> Shortlist. A free Bootstrap 6 template — every role here is fictional.</p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


# ------------------------------------------------------------------ homepage

def page_index():
    rows = "\n".join(job_row(j) for j in JOBS)
    return HEAD.format(
        title="Shortlist — Free Bootstrap 6 Job Board Website Template",
        desc="Shortlist is a free Bootstrap 6 job board template — filter rail with a salary floor, listings that all show a real salary range, sectors, companies and a job detail page.",
        bodyattr="",
    ) + chrome_header() + f"""
<section class="find">
  <div class="container">
    <div class="row justify-content-center text-center mb-4">
      <div class="lg:col-8">
        <h1 class="find-title mb-3">Jobs that tell you what they pay</h1>
        <p class="fs-lg fg-2 mb-0">
          1,284 open roles across the north of England. Every one shows a real
          salary range, because a listing without one wastes everybody's afternoon.
        </p>
      </div>
    </div>

    <form class="find-bar" role="search" onsubmit="return false">
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">{SEARCH}</div>
        <input type="search" class="form-ghost" placeholder="Job title, skill or company" aria-label="Search jobs">
      </div>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">{PIN}</div>
        <input type="search" class="form-ghost" placeholder="Town, city or remote" aria-label="Location">
      </div>
      <button class="btn-solid theme-primary btn-lg" type="submit">Search</button>
    </form>

    <div class="d-flex flex-wrap justify-content-center gap-2 mt-4">
      <span class="fs-sm fg-3 me-1">Popular:</span>
      <a class="chip" href="#jobs">Remote</a>
      <a class="chip" href="#jobs">Frontend</a>
      <a class="chip" href="#jobs">Four-day week</a>
      <a class="chip" href="#jobs">Graduate</a>
    </div>
  </div>
</section>

<main id="main">

  <section class="section" id="jobs">
    <div class="container">
      <div class="board">

        <aside class="rail">
          <form onsubmit="return false">
            <div class="rail-group">
              <p class="rail-label mb-2">Salary floor</p>
              <div class="form-range" data-bs-bubble>
                <input type="range" class="form-range-input" id="payFloor" min="20000" max="120000" step="5000" value="45000"
                       data-range-out="payOut" data-range-prefix="&pound;" aria-label="Minimum salary">
              </div>
              <p class="fs-sm mb-0">From <strong id="payOut">&pound;45000</strong></p>
            </div>

            <div class="rail-group">
              <p class="rail-label">Working pattern</p>
              <div class="form-field mb-2"><input type="checkbox" class="check" id="fRemote" checked><label for="fRemote">Remote</label></div>
              <div class="form-field mb-2"><input type="checkbox" class="check" id="fHybrid" checked><label for="fHybrid">Hybrid</label></div>
              <div class="form-field mb-0"><input type="checkbox" class="check" id="fOnsite"><label for="fOnsite">On-site</label></div>
            </div>

            <div class="rail-group">
              <p class="rail-label">Contract</p>
              <div class="form-field mb-2"><input type="checkbox" class="check" id="fPerm" checked><label for="fPerm">Permanent</label></div>
              <div class="form-field mb-0"><input type="checkbox" class="check" id="fCon"><label for="fCon">Contract</label></div>
            </div>

            <div class="rail-group">
              <p class="rail-label">Sector</p>
              {combobox("sector", "Any sector", [("eng", "Engineering"), ("design", "Design"), ("data", "Data"), ("mkt", "Marketing"), ("ops", "Operations")], search=True, multiple=True)}
            </div>

            <div class="rail-group">
              <div class="form-field mb-0">
                <div class="switch"><input type="checkbox" id="fPaid" role="switch" switch checked></div>
                <label for="fPaid">Only show jobs with a salary</label>
              </div>
            </div>
          </form>
        </aside>

        <div>
          <div class="d-flex flex-wrap align-items-center gap-3 mb-3">
            <p class="fw-semibold mb-0">{len(JOBS)} roles</p>
            <div class="d-flex flex-wrap gap-2">
              <span class="chip">Remote <button type="button" class="chip-dismiss" aria-label="Remove remote filter"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="4" x2="12" y2="12"/><line x1="12" y1="4" x2="4" y2="12"/></svg></button></span>
              <span class="chip">&pound;45k+ <button type="button" class="chip-dismiss" aria-label="Remove salary filter"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="4" x2="12" y2="12"/><line x1="12" y1="4" x2="4" y2="12"/></svg></button></span>
            </div>
            <div class="ms-auto" style="min-width:11rem">
              {combobox("sort", "Newest first", [("new", "Newest first"), ("pay", "Highest paid"), ("rel", "Most relevant")])}
            </div>
          </div>

{rows}

          <div class="d-flex justify-content-center mt-4">
            <nav aria-label="Job pages">
              <ul class="pagination mb-0">
                <li class="page-item disabled"><button class="page-link" type="button" disabled>&lsaquo;</button></li>
                <li class="page-item active"><button class="page-link" type="button" aria-current="page">1</button></li>
                <li class="page-item"><button class="page-link" type="button">2</button></li>
                <li class="page-item"><button class="page-link" type="button">3</button></li>
                <li class="page-item"><button class="page-link" type="button">&rsaquo;</button></li>
              </ul>
            </nav>
          </div>
        </div>

      </div>
    </div>
  </section>

  <!-- Sectors -->
  <section class="section bg-2" id="sectors">
    <div class="container">
      <h2 class="fs-3xl fw-bold mb-5" style="letter-spacing:-.03em">Browse by sector</h2>
      <div class="row g-3">
        <div class="sm:col-6 lg:col-4"><a class="cat-tile" href="#jobs"><span class="fw-semibold">Engineering</span><span class="cat-count">418</span></a></div>
        <div class="sm:col-6 lg:col-4"><a class="cat-tile" href="#jobs"><span class="fw-semibold">Design</span><span class="cat-count">162</span></a></div>
        <div class="sm:col-6 lg:col-4"><a class="cat-tile" href="#jobs"><span class="fw-semibold">Data &amp; analytics</span><span class="cat-count">204</span></a></div>
        <div class="sm:col-6 lg:col-4"><a class="cat-tile" href="#jobs"><span class="fw-semibold">Marketing</span><span class="cat-count">137</span></a></div>
        <div class="sm:col-6 lg:col-4"><a class="cat-tile" href="#jobs"><span class="fw-semibold">Operations</span><span class="cat-count">189</span></a></div>
        <div class="sm:col-6 lg:col-4"><a class="cat-tile" href="#jobs"><span class="fw-semibold">Customer</span><span class="cat-count">174</span></a></div>
      </div>
    </div>
  </section>

  <!-- Companies -->
  <section class="section" id="companies">
    <div class="container">
      <div class="d-flex flex-wrap justify-content-between align-items-end gap-3 mb-5">
        <h2 class="fs-3xl fw-bold mb-0" style="letter-spacing:-.03em">Hiring now</h2>
        <p class="fg-3 fs-sm mb-0">Companies that publish salaries on every role</p>
      </div>
      <div class="row g-3">
        <div class="col-6 md:col-4 lg:col-2"><div class="co-tile"><span class="job-logo">NT</span><span class="fs-sm fw-semibold">Northwind</span><span class="cat-count">12 roles</span></div></div>
        <div class="col-6 md:col-4 lg:col-2"><div class="co-tile"><span class="job-logo">LS</span><span class="fs-sm fw-semibold">Lumen</span><span class="cat-count">4 roles</span></div></div>
        <div class="col-6 md:col-4 lg:col-2"><div class="co-tile"><span class="job-logo">KL</span><span class="fs-sm fw-semibold">Kestrel</span><span class="cat-count">9 roles</span></div></div>
        <div class="col-6 md:col-4 lg:col-2"><div class="co-tile"><span class="job-logo">FG</span><span class="fs-sm fw-semibold">Fieldstone</span><span class="cat-count">6 roles</span></div></div>
        <div class="col-6 md:col-4 lg:col-2"><div class="co-tile"><span class="job-logo">SI</span><span class="fs-sm fw-semibold">Sable</span><span class="cat-count">3 roles</span></div></div>
        <div class="col-6 md:col-4 lg:col-2"><div class="co-tile"><span class="job-logo">PC</span><span class="fs-sm fw-semibold">Pemberton</span><span class="cat-count">7 roles</span></div></div>
      </div>
    </div>
  </section>

  <!-- Post a job -->
  <section class="section bg-2" id="post">
    <div class="container">
      <div class="row g-6 align-items-center">
        <div class="lg:col-5">
          <h2 class="fs-3xl fw-bold mb-3" style="letter-spacing:-.03em">Post a job</h2>
          <p class="fg-2 mb-4">
            &pound;180 for thirty days. One condition: the listing carries a
            salary range. We will not publish "competitive" and we will not make
            an exception for you.
          </p>
          <div class="spec-row"><span class="fg-3 fs-sm">Single listing</span><span class="fs-sm">&pound;180 &middot; 30 days</span></div>
          <div class="spec-row"><span class="fg-3 fs-sm">Five-pack</span><span class="fs-sm">&pound;720 &middot; 12 months to use</span></div>
          <div class="spec-row"><span class="fg-3 fs-sm">Featured slot</span><span class="fs-sm">+&pound;90</span></div>
          <div class="spec-row"><span class="fg-3 fs-sm">Median applications</span><span class="fs-sm">31 per listing</span></div>
        </div>
        <div class="lg:col-7">
          <div class="post-panel">
            <form data-demo-form data-bs-validate novalidate>
              <div class="row g-3">
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pjTitle">Job title</label>
                    <input type="text" class="form-control" id="pjTitle" required>
                    <div class="invalid-feedback">Required.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pjCo">Company</label>
                    <input type="text" class="form-control" id="pjCo" required>
                    <div class="invalid-feedback">Required.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pjMin">Salary from</label>
                    <input type="text" class="form-control" id="pjMin" placeholder="&pound;45,000" required>
                    <div class="invalid-feedback">A range is required to list.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pjMax">Salary to</label>
                    <input type="text" class="form-control" id="pjMax" placeholder="&pound;58,000" required>
                    <div class="invalid-feedback">A range is required to list.</div>
                  </div>
                </div>
                <div class="md:col-6">
                  <label class="form-label">Working pattern</label>
                  {combobox("pattern", "Choose one…", [("remote", "Remote"), ("hybrid", "Hybrid"), ("onsite", "On-site")])}
                </div>
                <div class="md:col-6">
                  <div class="form-field">
                    <label class="form-label" for="pjLive">Go live on</label>
                    <input type="text" class="form-control" id="pjLive" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date…">
                  </div>
                </div>
                <div class="col-12">
                  <button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Listing drafted ✓">Continue</button>
                  <p class="fs-xs fg-3 mt-3 mb-0">You will preview the listing before paying.</p>
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


# ------------------------------------------------------------------ job page

def page_job():
    j = JOBS[0]
    return HEAD.format(
        title="Senior Frontend Engineer at Northwind Trading — Shortlist",
        desc="Job listing page from the Shortlist Bootstrap 6 job board template — full description, requirements, salary range and a sticky apply rail.",
        bodyattr="",
    ) + chrome_header(active_home=False) + f"""
<div class="sub-head">
  <div class="container">
    <nav aria-label="Breadcrumb" class="mb-3">
      <ol class="breadcrumb mb-0">
        <li class="breadcrumb-item"><a class="breadcrumb-link" href="index.html">Shortlist</a></li>
        <li class="breadcrumb-item"><a class="breadcrumb-link" href="index.html#jobs">Engineering</a></li>
        <li class="breadcrumb-item active" aria-current="page">Senior Frontend Engineer</li>
      </ol>
    </nav>
    <div class="d-flex flex-wrap align-items-start gap-3">
      <span class="job-logo" aria-hidden="true">NT</span>
      <div>
        <h1 class="fs-3xl fw-bold mb-1" style="letter-spacing:-.03em">Senior Frontend Engineer</h1>
        <p class="fg-3 mb-0">Northwind Trading &middot; Leeds &middot; Hybrid &middot; Permanent</p>
      </div>
    </div>
  </div>
</div>

<main id="main">
  <section class="section">
    <div class="container">
      <div class="row g-6">
        <div class="lg:col-8">
          <div class="prose">
            <h2 class="fs-2xl fw-bold mb-3" style="letter-spacing:-.02em">The role</h2>
            <p class="fg-2">
              You would be the fourth engineer on a team that owns the customer-facing
              side of a logistics platform used by about 4,000 people a day. Most of
              the work is in TypeScript and React, with a design system we maintain
              ourselves rather than pulling off the shelf.
            </p>

            <h2 class="fs-2xl fw-bold mb-3 mt-6">What you would actually do</h2>
            <ul class="fg-2">
              <li class="mb-2">Own features end to end, from the design conversation to the deploy</li>
              <li class="mb-2">Maintain and extend the design system — roughly a day a week</li>
              <li class="mb-2">Pair with the two mid-level engineers, deliberately and often</li>
              <li>Take part in the on-call rota, one week in six, rarely called</li>
            </ul>

            <h2 class="fs-2xl fw-bold mb-3 mt-6">What we are looking for</h2>
            <p class="fg-2">
              Several years building production front-ends, comfort with TypeScript,
              and an opinion about accessibility that you can defend. We do not
              require a degree and we do not run a take-home test.
            </p>

            <h2 class="fs-2xl fw-bold mb-3 mt-6">Process</h2>
            <p class="fg-2 mb-0">
              A 30-minute call, then a two-hour paired session on our actual codebase
              (paid at day rate), then a conversation with the team you would join.
              Three stages, two weeks, and we tell you either way.
            </p>
          </div>
        </div>

        <div class="lg:col-4">
          <div class="apply-rail">
            <p class="job-pay fs-2xl mb-1">&pound;65,000 — &pound;78,000</p>
            <p class="fg-3 fs-sm mb-4">Plus 8% pension and a &pound;1,500 annual learning budget.</p>

            <button class="btn-solid theme-primary w-100 mb-2" type="button" data-bs-toggle="dialog" data-bs-target="#applyDialog">Apply now</button>
            <button class="btn-outline theme-secondary w-100 mb-4" type="button">Save for later</button>

            <div class="spec-row"><span class="fg-3 fs-sm">Location</span><span class="fs-sm">Leeds</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Pattern</span><span class="fs-sm">Hybrid, 2 days in</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Contract</span><span class="fs-sm">Permanent</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Holiday</span><span class="fs-sm">28 days + bank</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Posted</span><span class="fs-sm">2 days ago</span></div>
            <div class="spec-row"><span class="fg-3 fs-sm">Applications</span><span class="fs-sm">18 so far</span></div>
          </div>
        </div>
      </div>
    </div>
  </section>
</main>

<dialog class="dialog" id="applyDialog" aria-labelledby="applyLabel">
  <div class="dialog-header">
    <h2 class="dialog-title fs-lg" id="applyLabel">Apply — Senior Frontend Engineer</h2>
    <button type="button" class="btn-close" data-bs-dismiss="dialog" aria-label="Close"></button>
  </div>
  <form class="dialog-body vstack gap-3" id="applyForm" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="apName">Your name</label>
      <input type="text" class="form-control" id="apName" required>
      <div class="invalid-feedback">Required.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="apEmail">Email</label>
      <input type="email" class="form-control" id="apEmail" required>
      <div class="invalid-feedback">A valid email, please.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="apLink">Portfolio or GitHub</label>
      <input type="url" class="form-control" id="apLink" placeholder="https://">
    </div>
    <div class="form-field">
      <label class="form-label" for="apNote">Anything you want us to know</label>
      <textarea class="form-control" id="apNote" rows="4" placeholder="Optional. A cover letter is not required and we do not score them."></textarea>
    </div>
  </form>
  <div class="dialog-footer">
    <button type="button" class="btn-text" data-bs-dismiss="dialog">Cancel</button>
    <button type="submit" form="applyForm" class="btn-solid theme-primary" data-done-text="Applied ✓">Send application</button>
  </div>
</dialog>
""" + FOOTER


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "job.html").write_text(page_job(), encoding="utf-8")
print("wrote index.html + job.html")
