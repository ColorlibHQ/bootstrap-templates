#!/usr/bin/env python3
"""
Generates Cornerstone: a corporate site with an information architecture that
does not fall over.

MENU is declared once and rendered into both the desktop mega menu and the
mobile nested drawer, so the two can never offer different navigation — which is
the usual failure once a real company's IA outgrows a five-item navbar.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
TITLE = "Keystone"

# Real corporate IA: several columns per menu, each with a heading and links.
# This is the shape almost every Bootstrap template refuses to accommodate.
MENU = [
    ("Services", [
        ("By discipline", [
            ("Strategy &amp; transformation", "Where you are going, and whether it is worth going there"),
            ("Operations", "Making the thing you already do cost less to do"),
            ("Technology", "Systems, migrations, and the ones you cannot switch off"),
            ("Risk &amp; assurance", "Controls, audit readiness, and the regulator's questions"),
        ]),
        ("By need", [
            ("Cost reduction", ""),
            ("Post-merger integration", ""),
            ("Regulatory response", ""),
            ("Growth planning", ""),
        ]),
    ]),
    ("Industries", [
        ("Sectors we know", [
            ("Financial services", "Retail banking, payments, insurance"),
            ("Healthcare", "Providers, payers, and everything between"),
            ("Manufacturing", "Discrete and process, and their supply chains"),
            ("Public sector", "Central and local government"),
        ]),
        ("Recently", [
            ("Energy transition", ""),
            ("Logistics", ""),
            ("Higher education", ""),
        ]),
    ]),
    ("Insights", [
        ("Reading", [
            ("Reports", "Long-form research, four or five a year"),
            ("Articles", "Shorter pieces, roughly weekly"),
            ("Case studies", "What we did and what it moved"),
        ]),
        ("Events", [
            ("Webinars", ""),
            ("Roundtables", ""),
            ("Annual conference", ""),
        ]),
    ]),
    ("About", [
        ("The firm", [
            ("Who we are", "310 people across four offices"),
            ("How we work", "Fixed fee wherever we honestly can"),
            ("Leadership", ""),
            ("Careers", "We are hiring in Manchester and Leeds"),
        ]),
    ]),
]

STATS = [("310", "People"), ("4", "Offices"), ("1998", "Founded"), ("74%", "Repeat clients")]

SERVICES = [
    ("Strategy &amp; transformation",
     "Six to twelve weeks, usually. We start by testing whether the thing you have decided to do is the right thing, which occasionally ends the engagement early.",
     ["Market and competitor assessment", "Operating model design", "Business case and board pack", "Benefits tracking after we leave"]),
    ("Operations",
     "The unglamorous work: process mapping, capacity modelling, and finding the four handoffs that cause most of the delay.",
     ["Process and value-stream mapping", "Capacity and demand modelling", "Supplier and contract review", "Continuous improvement handover"]),
    ("Technology",
     "Systems that have to keep running while they change. We do the migration planning nobody wants to own.",
     ["Architecture and platform review", "Migration planning and sequencing", "Vendor selection, without a kickback", "Post-go-live stabilisation"]),
    ("Risk &amp; assurance",
     "Controls that survive an audit and a regulator's follow-up question, written so the people who have to follow them can.",
     ["Control design and testing", "Audit readiness", "Regulatory gap analysis", "Policy rewriting in plain English"]),
]

CASES = [
    ("A retail bank cut onboarding from 11 days to 2", "Financial services", "Operations",
     "Eleven days was four days of work and seven of waiting. We removed three handoffs and the waiting went with them."),
    ("A hospital trust released 34 beds without building any", "Healthcare", "Operations",
     "Discharge was the constraint, not capacity. Moving pharmacy sign-off earlier in the day did most of it."),
    ("A manufacturer avoided a £4m ERP replacement", "Manufacturing", "Technology",
     "The business case rested on a reporting problem that turned out to be a data quality problem. We fixed the data."),
]

PRINCIPLES = [
    ("Fixed fee wherever we honestly can",
     "Time and materials rewards us for being slow. We quote fixed where the scope is knowable and say so plainly where it is not."),
    ("The team that pitches is the team that works",
     "No partner-and-vanish. The people in the room at the pitch are the people on the engagement, named in the proposal."),
    ("We will tell you not to do it",
     "Roughly one engagement in six ends at the assessment because the answer was no. We would rather lose the fee than the relationship."),
    ("Your people can run it after we go",
     "Every engagement includes handover as a deliverable, not a courtesy. If it only works while we are there, it does not work."),
]

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""

CARET = '<svg class="mega-caret" width="10" height="10" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="m4 6 4 4 4-4"/></svg>'

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Bootstrap 6, bundled in assets/vendor/bootstrap6 (version in the CSS file header). To load it from jsDelivr instead, replace both paths below with https://cdn.jsdelivr.net/npm/bootstrap@VERSION/dist/... -->
<link rel="stylesheet" href="assets/vendor/bootstrap6/css/bootstrap.min.css">
<script type="importmap">{{"imports": {{"bootstrap": "./assets/vendor/bootstrap6/js/bootstrap.bundle.min.js"}}}}</script>
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
"""


def mega():
    """Desktop mega menu. Each top-level item is a button that owns a panel;
    the panel is a real element in the DOM rather than being built on hover, so
    it is reachable by keyboard and readable by a screen reader."""
    out = []
    for i, (label, columns) in enumerate(MENU):
        cols = []
        for heading, links in columns:
            items = "".join(
                f'<li><a href="services.html"><span class="mega-link">{name}</span>'
                + (f'<span class="mega-note">{note}</span>' if note else '')
                + '</a></li>' for name, note in links)
            cols.append(f"""            <div class="mega-col">
              <p class="mega-head">{heading}</p>
              <ul class="mega-list">{items}</ul>
            </div>""")
        out.append(f"""      <li class="mega-item">
        <button class="mega-toggle" type="button" data-mega="{i}" aria-expanded="false" aria-controls="mega{i}">{label}{CARET}</button>
        <div class="mega-panel" id="mega{i}" data-mega-panel="{i}" hidden>
          <div class="mega-in">
{chr(10).join(cols)}
            <div class="mega-aside">
              <p class="mega-head">Talk to someone</p>
              <p class="fs-sm fg-2 mb-4">Every enquiry reaches a named person, not a form queue.</p>
              <a class="btn-solid theme-primary btn-sm" href="contact.html">Contact us</a>
            </div>
          </div>
        </div>
      </li>""")
    return "\n".join(out)


def drawer_nav():
    """Mobile. The same MENU rendered as nested <details>, which is a genuine
    disclosure widget with no JavaScript behind it at all."""
    out = []
    for label, columns in MENU:
        groups = []
        for heading, links in columns:
            items = "".join(f'<li><a href="services.html">{name}</a></li>' for name, _ in links)
            groups.append(f'<p class="drawer-head">{heading}</p><ul class="drawer-list">{items}</ul>')
        out.append(f"""      <details class="drawer-group">
        <summary>{label}</summary>
        <div class="drawer-sub">{''.join(groups)}</div>
      </details>""")
    return "\n".join(out)


def chrome(current):
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-3" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="wrap head-in">
    <a class="wordmark" href="index.html">
      <span class="wordmark-mark" aria-hidden="true"></span>{TITLE}
    </a>

    <nav class="mega d-none lg:d-block" aria-label="Main">
      <ul class="mega-bar">
{mega()}
      </ul>
    </nav>

    <div class="d-flex align-items-center gap-3 ms-auto">
      {TOGGLE}
      <a class="btn-solid theme-primary btn-sm d-none md:d-inline-flex" href="contact.html">Contact us</a>
      <button class="btn-icon lg:d-none" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
        <span class="navbar-toggler-icon" aria-hidden="true"></span>
      </button>
    </div>
  </div>
</header>

<dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
  <div class="drawer-header">
    <h5 class="drawer-title" id="navDrawerLabel">{TITLE}</h5>
    <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
  </div>
  <div class="drawer-body">
{drawer_nav()}
    <a class="btn-solid theme-primary w-100 mt-4" href="contact.html">Contact us</a>
  </div>
</dialog>
"""


FOOTER = """
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <p class="wordmark mb-4"><span class="wordmark-mark" aria-hidden="true"></span>""" + TITLE + """</p>
        <p class="fg-2 fs-sm mb-0" style="max-width:20rem">
          A 310-person advisory firm working with organisations that cannot
          simply stop while they change.
        </p>
      </div>
""" + "\n".join(f"""      <div>
        <p class="foot-head">{label}</p>
        <ul class="foot-list">{''.join(f'<li><a href="services.html">{n}</a></li>' for n, _ in cols[0][1][:4])}</ul>
      </div>""" for label, cols in MENU[:3]) + """
    </div>
    <hr class="my-5">
    <p class="fs-xs fg-3 mb-0">
      &copy; <span data-year>2026</span> """ + TITLE + """ &mdash; a free Bootstrap 6 template.
      The firm, its people and every engagement described here are fictional.
    </p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page(file, title, desc, body, current="index.html"):
    (ROOT / file).write_text(
        HEAD.format(title=title, desc=desc) + chrome(current) + body + FOOTER, encoding="utf-8")


def page_index():
    stats = "".join(f'<div class="figure"><p class="figure-v mb-0">{v}</p><p class="figure-k mb-0">{k}</p></div>' for v, k in STATS)

    services = "\n".join(f"""        <article class="svc">
          <h3 class="svc-name mb-3">{name}</h3>
          <p class="fg-2 mb-4">{blurb}</p>
          <ul class="svc-list mb-0">{''.join(f'<li>{p}</li>' for p in points)}</ul>
        </article>""" for name, blurb, points in SERVICES)

    cases = "\n".join(f"""        <li class="case">
          <p class="case-tags mb-3"><span class="tag">{sector}</span><span class="tag">{disc}</span></p>
          <h3 class="case-name mb-3"><a href="services.html">{name}</a></h3>
          <p class="fg-2 fs-sm mb-0">{blurb}</p>
        </li>""" for name, sector, disc, blurb in CASES)

    principles = "\n".join(f"""        <div class="prin">
          <h3 class="prin-name mb-3">{name}</h3>
          <p class="fg-2 mb-0">{blurb}</p>
        </div>""" for name, blurb in PRINCIPLES)

    body = f"""
<main id="main">

  <section class="hero">
    <div class="wrap">
      <p class="eyebrow-rule mb-5">Advisory since 1998</p>
      <h1 class="hero-title mb-5">The work that has to happen<br>while the lights stay on.</h1>
      <p class="hero-lede fg-2 mb-6">
        We advise organisations that cannot pause to change — banks, hospitals,
        manufacturers, government. Fixed fee wherever we honestly can, and about
        one engagement in six ends early because the answer was no.
      </p>
      <div class="d-flex flex-wrap gap-4">
        <a class="btn-solid theme-primary btn-lg" href="services.html">What we do</a>
        <a class="btn-outline theme-secondary btn-lg" href="contact.html">Talk to someone</a>
      </div>
    </div>
  </section>

  <div class="figure-band"><div class="wrap figures">{stats}</div></div>

  <section class="band" id="services">
    <div class="wrap">
      <div class="band-head">
        <div>
          <p class="eyebrow-rule mb-4">Services</p>
          <h2 class="band-title mb-0">Four disciplines, and the honest length of each</h2>
        </div>
        <p class="fg-2 mb-0">
          Most engagements draw on two of these. Nobody has ever needed all four
          at once, whatever the proposal said.
        </p>
      </div>
      <div class="svc-grid">
{services}
      </div>
    </div>
  </section>

  <section class="band band-alt">
    <div class="wrap">
      <div class="band-head">
        <div>
          <p class="eyebrow-rule mb-4">Selected work</p>
          <h2 class="band-title mb-0">Three engagements, described plainly</h2>
        </div>
        <p class="fg-2 mb-0">Named clients on request. These are the numbers their finance teams agreed to.</p>
      </div>
      <ul class="case-list">
{cases}
      </ul>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <div class="band-head">
        <div>
          <p class="eyebrow-rule mb-4">How we work</p>
          <h2 class="band-title mb-0">Four things we commit to in writing</h2>
        </div>
        <p class="fg-2 mb-0">They are in the engagement letter, not just on this page.</p>
      </div>
      <div class="prin-grid">
{principles}
      </div>
    </div>
  </section>

  <section class="cta-band">
    <div class="wrap cta-in">
      <div>
        <h2 class="band-title mb-3">Start with a conversation, not a proposal</h2>
        <p class="fg-2 mb-0">Thirty minutes, no deck, and a straight answer on whether we are the right firm.</p>
      </div>
      <a class="btn-solid theme-primary btn-lg" href="contact.html">Contact us</a>
    </div>
  </section>

</main>
"""
    page("index.html", f"{TITLE} — Free Bootstrap 6 Corporate &amp; Business Website Template",
         "Keystone is a free Bootstrap 6 corporate template with a real mega menu — keyboard-navigable on desktop, a nested drawer on mobile, both from one declaration.", body)


def page_services():
    services = "\n".join(f"""      <article class="svc-full" id="s{i}">
        <div class="svc-full-head">
          <h2 class="band-title mb-0">{name}</h2>
          <a class="btn-outline theme-secondary btn-sm" href="contact.html">Enquire</a>
        </div>
        <p class="fg-2 mb-5" style="max-width:44rem">{blurb}</p>
        <ul class="svc-list mb-0">{''.join(f'<li>{p}</li>' for p in points)}</ul>
      </article>""" for i, (name, blurb, points) in enumerate(SERVICES))

    body = f"""
<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow fs-xs mb-4"><a href="index.html">{TITLE}</a> &middot; Services</p>
      <h1 class="hero-title mb-5">What we do, and how long it takes.</h1>
      <p class="hero-lede fg-2 mb-0">
        Four disciplines. Each one lists what you actually receive, because
        “strategic support” is not a deliverable.
      </p>
    </div>
  </section>

  <div class="wrap svc-page">
{services}
  </div>
</main>
"""
    page("services.html", f"Services — {TITLE} Bootstrap 6 Corporate Template",
         "A corporate services page listing concrete deliverables for each discipline rather than abstractions.", body, "services.html")


def page_contact():
    body = f"""
<main id="main">
  <section class="page-head">
    <div class="wrap">
      <p class="eyebrow fs-xs mb-4"><a href="index.html">{TITLE}</a> &middot; Contact</p>
      <h1 class="hero-title mb-5">Every enquiry reaches a person.</h1>
      <p class="hero-lede fg-2 mb-0">Not a queue, not a chatbot. Usually within one working day.</p>
    </div>
  </section>

  <div class="wrap contact-grid">
    <form class="contact-form" data-demo-form novalidate>
      <div class="row g-4">
        <div class="md:col-6">
          <label class="form-label" for="cName">Your name</label>
          <input class="form-control" type="text" id="cName" required>
          <div class="invalid-feedback">Please tell us who you are.</div>
        </div>
        <div class="md:col-6">
          <label class="form-label" for="cOrg">Organisation</label>
          <input class="form-control" type="text" id="cOrg">
        </div>
        <div class="md:col-6">
          <label class="form-label" for="cEmail">Email</label>
          <input class="form-control" type="email" id="cEmail" required>
          <div class="invalid-feedback">We need an address to reply to.</div>
        </div>
        <div class="md:col-6">
          <label class="form-label" for="cTopic">What is it about?</label>
          <select class="form-control form-control-caret" id="cTopic">
            <option>Strategy &amp; transformation</option>
            <option>Operations</option>
            <option>Technology</option>
            <option>Risk &amp; assurance</option>
            <option>Careers</option>
            <option>Something else</option>
          </select>
        </div>
        <div class="col-12">
          <label class="form-label" for="cMsg">Roughly what is going on?</label>
          <textarea class="form-control" id="cMsg" rows="5" required></textarea>
          <div class="invalid-feedback">A paragraph is plenty.</div>
        </div>
        <div class="col-12">
          <button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Thank you — we'll be in touch ✓">Send enquiry</button>
          <p class="fs-xs fg-3 mt-4 mb-0">Frontend-only demo form — nothing is sent anywhere.</p>
        </div>
      </div>
    </form>

    <aside class="contact-side">
      <div class="side-card">
        <p class="foot-head">Offices</p>
        <ul class="office-list">
          <li><strong>Manchester</strong><span class="fg-3">Head office &middot; 14 King Street, M2 6AZ</span></li>
          <li><strong>Leeds</strong><span class="fg-3">2 Wellington Place, LS1 4AP</span></li>
          <li><strong>Edinburgh</strong><span class="fg-3">40 Princes Street, EH2 2BY</span></li>
          <li><strong>London</strong><span class="fg-3">Fitzroy House, W1T 5HF</span></li>
        </ul>
      </div>
      <div class="side-card">
        <p class="foot-head">Direct</p>
        <p class="fg-2 fs-sm mb-3"><a href="tel:+441614960100">+44 161 496 0100</a></p>
        <p class="fg-2 fs-sm mb-0"><a href="mailto:hello@keystone.example">hello@keystone.example</a></p>
      </div>
      <div class="side-card">
        <p class="foot-head">Press</p>
        <p class="fg-2 fs-sm mb-0">Rae Whitcombe &middot; <a href="mailto:press@keystone.example">press@keystone.example</a></p>
      </div>
    </aside>
  </div>
</main>
"""
    page("contact.html", f"Contact — {TITLE} Bootstrap 6 Corporate Template",
         "A corporate contact page with a validating enquiry form, four office addresses and direct contacts.", body, "contact.html")


page_index()
page_services()
page_contact()
print(f"wrote 3 pages — {len(MENU)} mega menus, {sum(len(c) for _, c in MENU)} columns")
