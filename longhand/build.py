#!/usr/bin/env python3
"""
Generates Longhand: a personal site and CV.

ROLES, PROJECTS and SKILLS are declared once and rendered into both the screen
layout and the print layout, so the CV somebody prints can never fall behind the
site they read.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

ME = {
    "name": "Marit Halvorsen",
    "role": "Interface engineer",
    "where": "Manchester, UK",
    "email": "marit@longhand.example",
    "phone": "+44 161 496 0100",
    "site": "longhand.example",
}

ROLES = [
    ("2022", "Present", "Principal engineer", "Palisade Health", "Manchester",
     "Own the design system and the front end of a banking-grade patient portal used by 9 million people.",
     ["Cut first-contentful paint from 4.1s to 1.2s on the slowest tenth of devices, which is where the users actually are.",
      "Wrote the type and spacing layer three teams now build against, and the migration guide that got them there.",
      "Took the portal from a 61 to a 98 on axe with no visual redesign — most of it was heading order and focus management."]),
    ("2019", "2022", "Senior front-end engineer", "Ordinal Systems", "Remote",
     "Built the reporting product from an internal tool into something sold separately.",
     ["Replaced a 340KB charting dependency with 6KB of SVG, and nobody noticed except the bundle.",
      "Introduced visual regression tests that caught 40-odd layout breaks before release in the first year."]),
    ("2016", "2019", "Front-end engineer", "Kettle & Co", "Leeds",
     "Second engineer at a twelve-person retailer. Did whatever the week needed.",
     ["Rebuilt checkout; completion went from 61% to 74% over two quarters.",
      "Ran the move off jQuery a page at a time, with no freeze and no rewrite."]),
    ("2014", "2016", "Junior developer", "Trent & Vale", "Nottingham",
     "Agency work: brochure sites, campaign pages, occasional emergency CMS surgery.", []),
]

PROJECTS = [
    ("Squint", "A browser extension that blurs a page so you can judge its typographic colour without reading it.",
     "TypeScript, CSS Houdini", "4,100 users"),
    ("Hairline", "A 2KB CSS layer that makes 1px borders behave the same on every display density.",
     "CSS", "MIT, 1.2k stars"),
    ("Set in Stone", "A weekly newsletter pulling apart the typography of one real interface.",
     "Writing", "2,800 subscribers"),
]

SKILLS = [
    ("Languages", ["TypeScript", "JavaScript", "CSS", "HTML", "Python", "SQL"]),
    ("Practice", ["Design systems", "Accessibility (WCAG 2.2)", "Performance budgets", "Progressive enhancement"]),
    ("Tooling", ["Vite", "Playwright", "Storybook", "Figma", "Git"]),
]

WRITING = [
    ("Line height is a ratio, not a number", "Why the CSS you inherited breaks at 13px", "12 min"),
    ("Everything I know about optical sizing", "And the two places it genuinely matters", "9 min"),
    ("The accessibility work that is actually typography", "Contrast is about strokes, not boxes", "15 min"),
]

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
<!-- Bootstrap 6, bundled in assets/vendor/bootstrap6 (version in the JS bundle header). To load it from jsDelivr instead, replace both paths below with https://cdn.jsdelivr.net/npm/bootstrap@VERSION/dist/... -->
<link rel="stylesheet" href="assets/vendor/bootstrap6/css/bootstrap.min.css">
<script type="importmap">{{"imports": {{"bootstrap": "./assets/vendor/bootstrap6/js/bootstrap.bundle.min.js"}}}}</script>
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/print.css" media="print">
</head>
<body>
"""


def chrome(current):
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-3" href="#main">Skip to main content</a>

<header class="site-header no-print">
  <div class="wrap head-in">
    <a class="wordmark" href="index.html">{ME['name']}</a>
    <nav class="head-nav" aria-label="Main">
      <a class="head-link{' is-active' if current == 'index.html' else ''}" href="index.html#work">Work</a>
      <a class="head-link{' is-active' if current == 'index.html' else ''}" href="index.html#writing">Writing</a>
      <a class="head-link{' is-active' if current == 'project.html' else ''}" href="project.html">Case study</a>
      <a class="head-link" href="index.html#contact">Contact</a>
    </nav>
    <div class="d-flex align-items-center gap-3">
      {TOGGLE}
      <button class="btn-solid theme-primary btn-sm" type="button" data-print>Print CV</button>
    </div>
  </div>
</header>
"""


FOOTER = """
<footer class="site-footer no-print">
  <div class="wrap">
    <p class="fs-sm fg-3 mb-0">
      &copy; <span data-year>2026</span> """ + ME["name"] + """ &mdash; a free Bootstrap 6 template.
      The person, the roles and every project here are fictional.
    </p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def roles_html():
    out = []
    for start, end, title, org, place, blurb, bullets in ROLES:
        items = "".join(f"<li>{b}</li>" for b in bullets)
        out.append(f"""        <article class="role">
          <p class="role-when mb-0"><span>{start}</span><span class="role-dash" aria-hidden="true">–</span><span>{end}</span></p>
          <div class="role-body">
            <h3 class="role-title mb-1">{title}</h3>
            <p class="role-org mb-3">{org}<span class="fg-3"> · {place}</span></p>
            <p class="fg-2 mb-{'3' if bullets else '0'}">{blurb}</p>
            {f'<ul class="role-points mb-0">{items}</ul>' if bullets else ''}
          </div>
        </article>""")
    return "\n".join(out)


def page_index():
    skills = "\n".join(f"""          <div class="skill-group">
            <p class="skill-k mb-3">{group}</p>
            <ul class="skill-list mb-0">{''.join(f'<li>{s}</li>' for s in items)}</ul>
          </div>""" for group, items in SKILLS)

    projects = "\n".join(f"""          <li class="proj">
            <div>
              <h3 class="proj-name mb-1"><a href="project.html">{name}</a></h3>
              <p class="fg-2 fs-sm mb-0">{what}</p>
            </div>
            <p class="proj-meta mb-0">{tech}<span class="fg-3 d-block">{stat}</span></p>
          </li>""" for name, what, tech, stat in PROJECTS)

    writing = "\n".join(f"""          <li class="post">
            <a class="post-title" href="project.html">{title}</a>
            <p class="fg-2 fs-sm mb-0">{sub}</p>
            <span class="post-time fg-3">{mins}</span>
          </li>""" for title, sub, mins in WRITING)

    return HEAD.format(
        title=f"{ME['name']} — Free Bootstrap 6 Personal &amp; CV Website Template",
        desc="Longhand is a free Bootstrap 6 personal site and CV template with a print stylesheet that produces a real one-page résumé, not a screenshot of a web page.",
    ) + chrome("index.html") + f"""
<main id="main">

  <!-- Identity. Doubles as the CV letterhead when printed. -->
  <section class="intro">
    <div class="wrap">
      <div class="intro-grid">
        <div>
          <h1 class="intro-name mb-3">{ME['name']}</h1>
          <p class="intro-role mb-5">{ME['role']} &middot; {ME['where']}</p>
          <p class="intro-lede mb-5">
            Twelve years making interfaces that hold up: type that stays readable
            at 13px, layouts that survive 400% zoom, and front ends that load on
            the phone somebody actually owns.
          </p>
          <p class="intro-lede mb-0 no-print">
            Currently at Palisade Health. Not looking, but always glad to talk
            about typography, performance budgets, or why your line height is
            wrong.
          </p>
        </div>
        <ul class="vcard mb-0">
          <li><span class="vcard-k">Email</span><a href="mailto:{ME['email']}">{ME['email']}</a></li>
          <li><span class="vcard-k">Phone</span><a href="tel:{ME['phone'].replace(' ', '')}">{ME['phone']}</a></li>
          <li><span class="vcard-k">Site</span><a href="index.html">{ME['site']}</a></li>
          <li><span class="vcard-k">Based</span>{ME['where']}</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- Experience -->
  <section class="band" id="work">
    <div class="wrap">
      <h2 class="band-title">Experience</h2>
      <div class="roles">
{roles_html()}
      </div>
    </div>
  </section>

  <!-- Skills -->
  <section class="band band-alt" id="skills">
    <div class="wrap">
      <h2 class="band-title">What I actually use</h2>
      <div class="skills">
{skills}
      </div>
    </div>
  </section>

  <!-- Projects -->
  <section class="band" id="projects">
    <div class="wrap">
      <h2 class="band-title">Things I made on my own time</h2>
      <ul class="proj-list">
{projects}
      </ul>
    </div>
  </section>

  <!-- Writing. Screen only: a CV is not the place for a reading list. -->
  <section class="band band-alt no-print" id="writing">
    <div class="wrap">
      <h2 class="band-title">Writing</h2>
      <ul class="post-list">
{writing}
      </ul>
    </div>
  </section>

  <!-- Contact -->
  <section class="band no-print" id="contact">
    <div class="wrap contact">
      <h2 class="band-title mb-4">Say hello</h2>
      <p class="fg-2 mb-5" style="max-width:34rem">
        The fastest way to reach me is email. I reply to everything that is not
        a recruiter template, and to about half of those.
      </p>
      <div class="d-flex flex-wrap gap-4">
        <a class="btn-solid theme-primary btn-lg" href="mailto:{ME['email']}">{ME['email']}</a>
        <button class="btn-outline theme-secondary btn-lg" type="button" data-print>Print this as a CV</button>
      </div>
      <p class="fs-sm fg-3 mt-5 mb-0">
        That button opens your browser's print dialogue. The page has a print
        stylesheet, so what comes out is a one-page CV — not a screenshot of a
        website with a navigation bar across the top.
      </p>
    </div>
  </section>

</main>
""" + FOOTER


def page_project():
    return HEAD.format(
        title="Rebuilding checkout — " + ME["name"] + " Bootstrap 6 Personal Template",
        desc="A worked case study page for a personal site: the problem, what changed, what it moved, and what did not work.",
    ) + chrome("project.html") + f"""
<main id="main" class="case">
  <div class="wrap">
    <p class="eyebrow fs-xs mb-4"><a href="index.html">{ME['name']}</a> &middot; Case study</p>
    <h1 class="case-title mb-4">Rebuilding checkout without a freeze</h1>
    <p class="case-sub mb-6">Kettle &amp; Co &middot; 2017 &middot; Completion 61% &rarr; 74%</p>

    <dl class="case-facts mb-6">
      <div><dt>Role</dt><dd>Front-end engineer, and for four months the only one</dd></div>
      <div><dt>Team</dt><dd>Me, a designer two days a week, one back-end engineer</dd></div>
      <div><dt>Constraint</dt><dd>No code freeze. The shop took orders throughout.</dd></div>
      <div><dt>Stack</dt><dd>Vanilla JS over a Rails monolith, jQuery being removed underneath</dd></div>
    </dl>

    <div class="prose">
      <p class="fs-lg">
        Checkout converted at 61%, which everybody knew, and the accepted plan
        was a rewrite behind a feature flag over two quarters. That plan had
        already failed once.
      </p>

      <h2>What was actually wrong</h2>
      <p>
        Session recordings put the drop almost entirely in one place: the address
        step, on phones. Not the payment step, where everyone assumed it was.
        Three separate things were happening there, and none of them needed a
        rewrite to fix.
      </p>
      <p>
        The postcode lookup blocked the whole form while it ran. Validation fired
        on every keystroke, so a half-typed postcode was permanently red. And the
        keyboard covered the continue button on any phone under 700px tall,
        which nobody on the team had because we all had new phones.
      </p>

      <h2>What changed</h2>
      <p>
        The lookup became optional and asynchronous — type the address manually
        and nothing waits. Validation moved to <code>:user-invalid</code>, so a
        field only goes red once you have left it. The continue button became
        sticky to the bottom of the viewport on short screens.
      </p>
      <p>
        Three changes, about 200 lines, shipped over five weeks one at a time so
        each could be measured on its own.
      </p>

      <h2>What it moved</h2>
      <p>
        Completion went 61% → 68% on the validation change alone, which was the
        cheapest of the three and the one I had argued hardest against. It
        finished at 74% two quarters later. The rewrite never happened and the
        flag was deleted.
      </p>

      <h2>What did not work</h2>
      <p>
        A progress indicator across the top of the steps tested flat and I kept
        it anyway because it looked finished. It came out a year later and
        nothing moved, which is the correct outcome and a fair thing to admit.
      </p>
    </div>

    <div class="case-foot">
      <a class="btn-outline theme-secondary" href="index.html">&larr; Back to everything else</a>
      <a class="btn-solid theme-primary" href="mailto:{ME['email']}">Get in touch</a>
    </div>
  </div>
</main>
""" + FOOTER


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "project.html").write_text(page_project(), encoding="utf-8")
print("wrote index.html, project.html")
