#!/usr/bin/env python3
"""
Generates Syllabus: a course landing page and a lesson page.

The curriculum is declared once in MODULES and rendered into both — the landing
page as a tickable outline, the lesson page as a sidebar — so lesson counts,
durations and the total runtime are all derived rather than typed twice.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

# (module title, blurb, [(lesson title, minutes, kind)])
MODULES = [
    ("Reading type before you set it",
     "Before any of the craft, the part most courses skip: learning to actually see what a typeface is doing.",
     [("Why screen type is a different problem", 9, "video"),
      ("Anatomy without the vocabulary test", 14, "video"),
      ("Seeing rhythm, colour and texture", 17, "video"),
      ("Exercise: annotate three interfaces", 25, "task")]),

    ("Choosing, and defending the choice",
     "How to pick a typeface for a reason you can say out loud in a review.",
     [("What a brief actually constrains", 11, "video"),
      ("Superfamilies, and when you don't need one", 13, "video"),
      ("Testing a face against real content", 16, "video"),
      ("Licensing without the panic", 12, "video"),
      ("Exercise: shortlist and justify", 30, "task")]),

    ("Scale, rhythm and the vertical grid",
     "The module people come back to. Building a type scale that survives contact with a real product.",
     [("Modular scales, and their limits", 15, "video"),
      ("Line height is a ratio, not a number", 12, "video"),
      ("Optical sizing and why 14px lies", 18, "video"),
      ("Building the scale in code", 22, "video"),
      ("Exercise: retype a settings page", 35, "task"),
      ("Review: common scale failures", 14, "video")]),

    ("Setting long-form text",
     "Measure, hyphenation, widows, and the parts of CSS text layout nobody teaches.",
     [("Measure: the 45–75 myth, examined", 13, "video"),
      ("Hyphenation and justification on the web", 16, "video"),
      ("text-wrap: balance and pretty, in practice", 11, "video"),
      ("Quotes, dashes and the rest of the punctuation you are getting wrong", 19, "video"),
      ("Exercise: set a 2,000-word article", 40, "task")]),

    ("Interface type at small sizes",
     "Labels, tables, numerals and the dense screens where typography is load-bearing.",
     [("Tabular numerals and aligning money", 14, "video"),
      ("Labels, captions and the 12px floor", 12, "video"),
      ("Type in tables without a scrollbar", 17, "video"),
      ("Truncation is a design decision", 10, "video"),
      ("Exercise: a dense dashboard", 35, "task")]),

    ("Accessibility as typography",
     "Contrast, spacing and reflow — the accessibility work that is genuinely typographic.",
     [("Contrast is about the strokes, not the box", 15, "video"),
      ("Letter, word and line spacing requirements", 13, "video"),
      ("Reflow at 400% zoom", 14, "video"),
      ("Dyslexia-friendly: what the research says", 18, "video"),
      ("Exercise: audit your own product", 30, "task")]),

    ("Shipping and defending it",
     "Getting the work into production and keeping it there after you move on.",
     [("Variable fonts, subsetting and the byte budget", 21, "video"),
      ("Fallback stacks that don't shift the layout", 16, "video"),
      ("Writing the type section of a design system", 19, "video"),
      ("Final project: a complete type system", 90, "task")]),
]

REVIEWS = [
    ("The line-height module rewrote how I brief engineers. I had been asking for the wrong thing for six years.",
     "Nadia Osei", "Design lead, healthcare"),
    ("I came for the scale-building and stayed for the punctuation lesson, which I have now made three colleagues watch.",
     "Wes Tremayne", "Product designer"),
    ("It never once told me a rule without telling me when to break it. That is the whole difference.",
     "Priya Anand", "Front-end engineer"),
]

FAQ = [
    ("Do I need design training to take this?",
     "No. It assumes you can already build or design an interface and that nobody ever taught you type. Engineers take it as often as designers do, and the code sections use plain CSS."),
    ("How long does it actually take?",
     "Around eleven and a half hours of material, and most people finish in six to ten weeks. The planner above turns your available hours into a real date rather than making you guess."),
    ("Is there a deadline?",
     "No. Access does not expire, the exercises have no due dates, and nothing is drip-fed. If you disappear for four months your ticks are still here."),
    ("Will I get feedback on the exercises?",
     "On the final project, yes — a written critique within ten working days. The other exercises are self-directed with a worked example to compare against."),
    ("What if it isn't for me?",
     "Full refund within 30 days, no form and no conversation about it. Email once and it is done."),
]

TOTAL_MIN = sum(m for _, lessons in ((mod[0], mod[2]) for mod in MODULES) for _, m, _ in lessons)
TOTAL_LESSONS = sum(len(mod[2]) for mod in MODULES)


def hhmm(mins):
    h, m = divmod(int(mins), 60)
    if h and m:
        return f"{h}h {m}m"
    return f"{h}h" if h else f"{m}m"


# Lesson id -> minutes, for the whole course. Emitted on <body> because the
# lesson page only lists three modules in its sidebar: without the full map it
# would compute "time remaining" from whatever happened to be on screen.
LESSON_MIN = {}
_n = 0
for _mod in MODULES:
    for _t, _m, _k in _mod[2]:
        _n += 1
        LESSON_MIN[f"l{_n}"] = _m

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
"""

# Concatenated rather than interpolated: the map is JSON, and its braces would
# be read as .format() placeholders.
BODY = "<body data-lessons='" + str(LESSON_MIN).replace("'", '"') + "'>\n"

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""

MARK = """<svg class="brand-glyph" width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M2.5 5.5A2 2 0 0 1 4.5 3.5H11v17H4.5a2 2 0 0 1-2-2v-13Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M21.5 5.5a2 2 0 0 0-2-2H13v17h6.5a2 2 0 0 0 2-2v-13Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round" opacity=".45"/>
</svg>"""


def chrome(home=True):
    p = "" if home else "index.html"
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-3" href="#main">Skip to main content</a>

<header class="site-header">
  <nav class="navbar lg:navbar-expand" aria-label="Main">
    <div class="container">
      <a class="wordmark" href="index.html">{MARK}<span>Syllabus</span></a>

      <dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
        <div class="drawer-header">
          <h5 class="drawer-title" id="navDrawerLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
        </div>
        <div class="drawer-body mb-3 lg:mb-0">
          <ul class="nav navbar-nav ms-auto lg:gap-5">
            <li class="nav-item"><a class="nav-link" href="{p}#outcomes">What you'll learn</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#curriculum">Curriculum</a></li>
            <li class="nav-item"><a class="nav-link" href="lesson.html">Sample lesson</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#teacher">Who teaches it</a></li>
          </ul>
        </div>
      </dialog>

      <div class="d-flex align-items-center gap-3 ms-auto">
        {TOGGLE}
        <a class="btn-solid theme-primary" href="{p}#enrol">Enrol &mdash; &pound;180</a>
        <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
          <span class="navbar-toggler-icon" aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </nav>
</header>
"""


FOOTER = """
<footer class="site-footer section pb-6">
  <div class="container">
    <div class="row g-6">
      <div class="lg:col-5">
        <p class="wordmark mb-4">""" + MARK + """<span>Syllabus</span></p>
        <p class="fg-2 fs-sm mb-0" style="max-width:24rem">
          One course, taught properly, by someone who does the work. No cohort,
          no deadline, no expiry.
        </p>
      </div>
      <div class="md:col-6 lg:col-3">
        <p class="eyebrow fs-xs fg-3 mb-4">Course</p>
        <ul class="link-list"><li><a href="index.html#outcomes">What you'll learn</a></li><li><a href="index.html#curriculum">Curriculum</a></li><li><a href="lesson.html">Sample lesson</a></li><li><a href="index.html#faq">Questions</a></li></ul>
      </div>
      <div class="md:col-6 lg:col-4">
        <p class="eyebrow fs-xs fg-3 mb-4">Your progress</p>
        <p class="fg-2 fs-sm mb-0">
          Ticks are stored in this browser only — nothing is sent anywhere and
          there is no account. Clearing site data clears your progress, which is
          the honest trade for not asking you to sign up.
        </p>
      </div>
    </div>

    <hr class="my-6">

    <p class="fs-xs fg-3 mb-0">&copy; <span data-year>2026</span> Syllabus &mdash; a free Bootstrap 6 template. The course, its teacher and every review here are fictional.</p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def curriculum(interactive=True):
    """The tickable outline. Each lesson carries its own duration so the summary
    figures are computed rather than written down and left to rot."""
    out = []
    n = 0
    for mi, (title, blurb, lessons) in enumerate(MODULES):
        mins = sum(m for _, m, _ in lessons)
        rows = []
        for title_l, m, kind in lessons:
            n += 1
            lid = f"l{n}"
            rows.append(f"""            <li class="lesson">
              <input type="checkbox" class="check" id="{lid}" data-lesson="{lid}" data-min="{m}">
              <label for="{lid}">
                <span class="lesson-title">{title_l}</span>
                <span class="lesson-kind kind-{kind}">{kind}</span>
              </label>
              <span class="lesson-min">{m} min</span>
            </li>""")
        out.append(f"""        <details class="module" {'open' if mi == 0 else ''}>
          <summary>
            <span class="module-no">{mi + 1:02d}</span>
            <span class="module-head">
              <span class="module-title">{title}</span>
              <span class="module-meta">{len(lessons)} lessons &middot; {hhmm(mins)} &middot; <span data-module-done>0</span> done</span>
            </span>
          </summary>
          <div class="module-body">
            <p class="fg-2 fs-sm mb-4">{blurb}</p>
            <ul class="lesson-list">
{chr(10).join(rows)}
            </ul>
          </div>
        </details>""")
    return "\n".join(out)


def progress_panel():
    """Progress + pace planner. The two things a course page never tells you:
    how much is left, and when you would actually finish."""
    return f"""      <div class="tracker" data-tracker>
        <div class="tracker-top">
          <div>
            <p class="tracker-k mb-1">Your progress</p>
            <p class="tracker-v mb-0"><span data-done>0</span> of {TOTAL_LESSONS} lessons</p>
          </div>
          <div class="text-end">
            <p class="tracker-k mb-1">Left to watch</p>
            <p class="tracker-v mb-0" data-remaining>{hhmm(TOTAL_MIN)}</p>
          </div>
        </div>

        <div class="progress mb-5" role="progressbar" aria-label="Course progress" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" data-bar-wrap>
          <div class="progress-bar" style="width:0%" data-bar></div>
        </div>

        <label class="form-label" for="paceHours">Hours you can give it a week</label>
        <output class="tracker-out" id="paceOut" for="paceHours">3 hours</output>
        <div class="form-range mb-4">
          <input type="range" class="form-range-input" id="paceHours" min="1" max="20" step="1" value="3">
        </div>

        <p class="tracker-eta mb-4" data-eta></p>
        <button class="btn-text theme-secondary tracker-reset" type="button" data-reset>Clear my progress</button>
      </div>"""


def page_index():
    reviews = "\n".join(f"""        <div class="lg:col-4"><figure class="review surface surface-pad h-100">
          <blockquote class="mb-5"><p class="mb-0">{q}</p></blockquote>
          <figcaption><p class="fw-semibold mb-0">{name}</p><p class="fg-3 fs-sm mb-0">{role}</p></figcaption>
        </figure></div>""" for q, name, role in REVIEWS)

    faq = "\n".join(f"""            <details name="faq">
              <summary>{q}</summary>
              <div class="faq-body"><p class="fg-2 mb-0">{a}</p></div>
            </details>""" for q, a in FAQ)

    return HEAD.format(
        title="Syllabus — Free Bootstrap 6 Online Course &amp; E-Learning Template",
        desc="Syllabus is a free Bootstrap 6 e-learning template whose curriculum ticks off, remembers your progress, and turns your available hours a week into a real finish date.",
    ) + BODY + chrome() + f"""
<section class="hero">
  <div class="container">
    <div class="row g-7 align-items-center">
      <div class="lg:col-7">
        <p class="pill mb-5">A single course &middot; no cohort, no expiry</p>
        <h1 class="hero-title display-serif fs-5xl mb-5">Typography for interfaces.</h1>
        <p class="hero-lede fs-lg fg-2 mb-6">
          {TOTAL_LESSONS} lessons and {hhmm(TOTAL_MIN)} on the part of interface work
          nobody taught you: choosing type for a reason, building a scale that
          survives real content, and setting text that people can actually read.
        </p>
        <div class="d-flex flex-wrap gap-4 mb-5">
          <a class="btn-solid theme-primary btn-lg" href="#enrol">Enrol &mdash; &pound;180</a>
          <a class="btn-outline theme-secondary btn-lg" href="lesson.html">Watch a lesson free</a>
        </div>
        <p class="fs-sm fg-3 mb-0">30-day refund, no questions. Access does not expire.</p>
      </div>

      <div class="lg:col-5">
        <div class="ph ph-4x3 framed"><img src="img/hero.jpg" alt="Type specimens laid out on a desk" width="900" height="675" loading="eager"></div>
      </div>
    </div>
  </div>
</section>

<main id="main">

  <!-- Outcomes -->
  <section class="section" id="outcomes">
    <div class="container">
      <div class="row g-6 mb-7 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-4">What you'll learn</p>
          <h2 class="section-title display-serif fs-4xl mb-0">Six things you will be able to do afterwards</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            Not "understand" or "appreciate" — do, on Monday, in the file you
            already have open.
          </p>
        </div>
      </div>

      <div class="row g-5">
        <div class="md:col-6 lg:col-4"><article class="outcome surface surface-pad lift h-100"><span class="outcome-no">01</span><h3 class="fs-lg mb-3">Pick a typeface you can defend</h3><p class="fg-2 fs-sm mb-0">Work from the brief and the content rather than the mood board, and say out loud why this one and not that one.</p></article></div>
        <div class="md:col-6 lg:col-4"><article class="outcome surface surface-pad lift h-100"><span class="outcome-no">02</span><h3 class="fs-lg mb-3">Build a scale that holds up</h3><p class="fg-2 fs-sm mb-0">Set a modular scale in code, then know exactly where to break it when a real screen demands it.</p></article></div>
        <div class="md:col-6 lg:col-4"><article class="outcome surface surface-pad lift h-100"><span class="outcome-no">03</span><h3 class="fs-lg mb-3">Set long text properly</h3><p class="fg-2 fs-sm mb-0">Measure, leading, hyphenation and the punctuation you have been getting wrong since school.</p></article></div>
        <div class="md:col-6 lg:col-4"><article class="outcome surface surface-pad lift h-100"><span class="outcome-no">04</span><h3 class="fs-lg mb-3">Make dense screens readable</h3><p class="fg-2 fs-sm mb-0">Tables, labels, numerals and truncation — where typography stops being decoration and starts being load-bearing.</p></article></div>
        <div class="md:col-6 lg:col-4"><article class="outcome surface surface-pad lift h-100"><span class="outcome-no">05</span><h3 class="fs-lg mb-3">Meet accessibility properly</h3><p class="fg-2 fs-sm mb-0">Contrast against strokes not boxes, spacing requirements, and reflow at 400% without a horizontal scrollbar.</p></article></div>
        <div class="md:col-6 lg:col-4"><article class="outcome surface surface-pad lift h-100"><span class="outcome-no">06</span><h3 class="fs-lg mb-3">Ship it and keep it</h3><p class="fg-2 fs-sm mb-0">Subsetting, fallback stacks that do not shift the layout, and writing the type section of a design system.</p></article></div>
      </div>
    </div>
  </section>

  <!-- Curriculum -->
  <section class="section bg-2" id="curriculum">
    <div class="container">
      <div class="row g-6 mb-7 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-4">Curriculum</p>
          <h2 class="section-title display-serif fs-4xl mb-0">{len(MODULES)} modules, {TOTAL_LESSONS} lessons, {hhmm(TOTAL_MIN)}</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            Tick lessons off as you go — it is remembered in this browser, with
            no account to make. The planner works out when you would finish.
          </p>
        </div>
      </div>

      <div class="row g-6">
        <div class="lg:col-8">
          <div class="modules" data-curriculum>
{curriculum()}
          </div>
        </div>
        <div class="lg:col-4">
{progress_panel()}
        </div>
      </div>
    </div>
  </section>

  <!-- Teacher -->
  <section class="section" id="teacher">
    <div class="container">
      <div class="row g-7 align-items-center">
        <div class="lg:col-5">
          <div class="ph ph-3x4 framed"><img src="img/teacher.jpg" alt="Marit Halvorsen" width="700" height="933" loading="lazy"></div>
        </div>
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-4">Who teaches it</p>
          <h2 class="section-title display-serif fs-4xl mb-5">Marit Halvorsen</h2>
          <p class="fg-2 mb-5">
            Marit has spent eighteen years setting type on screens — six of them
            on a banking app used by nine million people, where a 13px label
            being wrong meant someone misread their balance.
          </p>
          <p class="fg-2 mb-5">
            She is not a type designer and says so early. This is a course about
            <em>using</em> type well, taught by someone who has had to defend
            every decision in it to an engineer, a lawyer and a brand team, often
            in the same week.
          </p>
          <dl class="facts">
            <div><dt>Teaching since</dt><dd>2018</dd></div>
            <div><dt>Students</dt><dd>4,100</dd></div>
            <div><dt>Average rating</dt><dd>4.8 / 5 from 812 reviews</dd></div>
            <div><dt>Answers questions</dt><dd>Herself, usually within two days</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </section>

  <!-- Reviews -->
  <section class="section bg-2">
    <div class="container">
      <div class="row g-5">
{reviews}
      </div>
    </div>
  </section>

  <!-- Enrol -->
  <section class="section" id="enrol">
    <div class="container">
      <div class="row g-6 align-items-center">
        <div class="lg:col-6">
          <p class="eyebrow-rule mb-4">Enrol</p>
          <h2 class="section-title display-serif fs-4xl mb-5">One price, everything in it</h2>
          <ul class="tick-list mb-0">
            <li>All {TOTAL_LESSONS} lessons, {hhmm(TOTAL_MIN)} of material</li>
            <li>Seven exercises with worked examples</li>
            <li>Written critique of your final project</li>
            <li>Lifetime access, including future revisions</li>
            <li>30-day refund, one email, no conversation</li>
          </ul>
        </div>
        <div class="lg:col-6">
          <div class="enrol">
            <p class="enrol-price mb-1">&pound;180<small> one payment</small></p>
            <p class="fg-3 fs-sm mb-5">Or three payments of &pound;62. Students and anyone between jobs pay &pound;90 — just ask, no proof needed.</p>
            <form id="enrolForm" data-demo-form novalidate>
              <label class="form-label" for="enrolEmail">Email address</label>
              <input class="form-control mb-4" type="email" id="enrolEmail" name="email" required>
              <div class="invalid-feedback mb-4">We need an address to send access to.</div>
              <button class="btn-solid theme-primary btn-lg w-100" type="submit" data-done-text="Check your inbox ✓">Enrol now</button>
            </form>
            <p class="fs-xs fg-3 mt-4 mb-0">Frontend-only demo form — nothing is sent anywhere.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section class="section bg-2" id="faq">
    <div class="container">
      <div class="row g-7">
        <div class="lg:col-5">
          <p class="eyebrow-rule mb-4">Questions</p>
          <h2 class="section-title display-serif fs-4xl mb-5">Asked often enough to answer here</h2>
          <p class="fg-2 mb-0">
            Anything else, write to
            <a href="mailto:marit@syllabus.example">marit@syllabus.example</a> —
            it goes to her, not a queue.
          </p>
        </div>
        <div class="lg:col-7">
          <div class="faq">
{faq}
          </div>
        </div>
      </div>
    </div>
  </section>

</main>
""" + FOOTER


def page_lesson():
    """A free sample lesson. Reuses the curriculum as a sidebar so the progress
    state is the same object on both pages."""
    nav = []
    n = 0
    for mi, (title, _, lessons) in enumerate(MODULES[:3]):
        rows = []
        for title_l, m, kind in lessons:
            n += 1
            lid = f"l{n}"
            current = ' class="is-current"' if n == 3 else ''
            rows.append(f"""              <li{current}>
                <input type="checkbox" class="check" id="s{lid}" data-lesson="{lid}" data-min="{m}">
                <label for="s{lid}">{title_l}</label>
                <span class="lesson-min">{m}m</span>
              </li>""")
        nav.append(f"""          <details class="rail-module" {'open' if mi == 0 else ''}>
            <summary>{mi + 1:02d} &nbsp;{title}</summary>
            <ul class="rail-list">
{chr(10).join(rows)}
            </ul>
          </details>""")

    return HEAD.format(
        title="Seeing rhythm, colour and texture — Syllabus Bootstrap 6 Course Template",
        desc="A free sample lesson from Typography for Interfaces, with notes, resources and the same progress tracking as the full curriculum.",
    ) + BODY + chrome(home=False) + f"""
<main id="main" class="lesson-page">
  <div class="container">
    <div class="row g-6">

      <div class="lg:col-8">
        <p class="eyebrow fs-xs mb-4"><a href="index.html">Typography for Interfaces</a> &middot; Module 01 &middot; Lesson 3</p>
        <h1 class="display-serif fs-4xl mb-4">Seeing rhythm, colour and texture</h1>
        <p class="fg-3 fs-sm mb-5">17 minutes &middot; Free sample &middot; Updated March 2026</p>

        <!-- Player stand-in. Deliberately not an <iframe> to a real service:
             the template ships with nothing to embed and a dead embed looks
             broken, whereas this reads as the placeholder it is. -->
        <div class="player">
          <img src="img/lesson.jpg" alt="Still from the lesson" width="1200" height="675" loading="eager">
          <button class="player-btn" type="button" aria-label="Play lesson (demo)">
            <svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5.5v13l11-6.5-11-6.5Z"/></svg>
          </button>
          <span class="player-time">17:04</span>
        </div>

        <div class="prose">
          <p class="fs-lg">
            Most people learn to read a typeface one letter at a time — the bowl
            of the <em>a</em>, the terminal on the <em>f</em>. Useful for an exam.
            Almost useless in front of a real screen, where what you are actually
            judging is a paragraph you are looking at from two feet away.
          </p>
          <p>
            This lesson swaps the microscope for a squint. Three properties do
            nearly all the work at that distance, and once you can see them you
            can diagnose a page in about four seconds.
          </p>

          <h2>Rhythm</h2>
          <p>
            The even alternation of stem and counter — black and white — as your
            eye runs along a line. Broken rhythm is what you are noticing when a
            paragraph feels "spotty" without your being able to say why. Common
            causes: a face with inconsistent sidebearings at small sizes, letter
            spacing applied to lowercase text, or a fallback font swapping in for
            two of the twenty-six characters.
          </p>

          <h2>Colour</h2>
          <p>
            Not hue — the overall grey value of a block of set text. Two
            paragraphs in the same size, weight and colour can have visibly
            different densities, and that difference is what makes one column of
            a two-column layout look heavier than its neighbour. Squint until the
            words stop resolving and compare the greys.
          </p>

          <blockquote>
            <p>If you can still read it, you are not squinting hard enough. The point is to stop reading and start seeing.</p>
          </blockquote>

          <h2>Texture</h2>
          <p>
            The combination of the two, plus the shape of the paragraph's ragged
            edge. Texture is why a justified column and a ragged-right column of
            identical text feel like different documents, and why a measure of
            110 characters feels exhausting before you have consciously noticed
            its width.
          </p>

          <h3>Try this now</h3>
          <p>
            Open any product you use daily. Blur your eyes until the text is
            unreadable. Where does the page go grey and even, and where does it
            clot? The clots are almost always where somebody set a heading and a
            paragraph in the same weight, or where a table has crept to eleven
            columns.
          </p>
        </div>

        <div class="lesson-foot">
          <a class="btn-outline theme-secondary" href="lesson.html">&larr; Anatomy without the vocabulary test</a>
          <a class="btn-solid theme-primary" href="lesson.html">Exercise: annotate three interfaces &rarr;</a>
        </div>
      </div>

      <aside class="lg:col-4">
        <div class="rail">
          <div class="rail-card mb-5">
            <p class="tracker-k mb-1">Your progress</p>
            <p class="tracker-v mb-4"><span data-done>0</span> of {TOTAL_LESSONS} lessons</p>
            <div class="progress" role="progressbar" aria-label="Course progress" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" data-bar-wrap>
              <div class="progress-bar" style="width:0%" data-bar></div>
            </div>
            <p class="fs-sm fg-3 mt-4 mb-0"><span data-remaining>{hhmm(TOTAL_MIN)}</span> left to watch</p>
          </div>

          <div class="rail-card mb-5">
            <p class="eyebrow fs-xs fg-3 mb-4">Resources for this lesson</p>
            <ul class="link-list mb-0">
              <li><a href="lesson.html">Squint-test worksheet (PDF)</a></li>
              <li><a href="lesson.html">Specimen set used in the video</a></li>
              <li><a href="lesson.html">Transcript</a></li>
            </ul>
          </div>

          <p class="eyebrow fs-xs fg-3 mb-4">Course outline</p>
          <div data-curriculum>
{chr(10).join(nav)}
          </div>
          <p class="fs-sm mt-4 mb-0"><a href="index.html#curriculum">See all {len(MODULES)} modules</a></p>
        </div>
      </aside>

    </div>
  </div>
</main>
""" + FOOTER


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "lesson.html").write_text(page_lesson(), encoding="utf-8")
print(f"wrote index.html, lesson.html — {TOTAL_LESSONS} lessons, {hhmm(TOTAL_MIN)}")
