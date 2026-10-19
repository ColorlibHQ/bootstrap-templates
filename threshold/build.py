#!/usr/bin/env python3
"""
Generates Threshold: a single-page product landing page, plus a thank-you page.

One page, one job: get an email address. Everything here is either the argument
for doing that or the mechanism for doing it.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
TITLE = "Threshold"

FEATURES = [
    ("Reads your calendar, not your mind",
     "Threshold blocks the focus time you said you wanted before someone else books it. No meeting is cancelled without you.",
     "M2 8h12M8 2v12"),
    ("One rule, not forty settings",
     "You get four hours a day and a lunch break. That is the whole configuration, and it is why people actually keep it on.",
     "M3 8h10M3 4.5h10M3 11.5h6"),
    ("It says no on your behalf",
     "Declines land with a real alternative time, so the person asking gets an answer rather than silence and a follow-up.",
     "M4 4l8 8M12 4l-8 8"),
    ("Honest about what it broke",
     "Weekly note tells you what it moved, what it declined, and where it got it wrong. Turn any of it back with one click.",
     "M8 2v6l4 2"),
]

STEPS = [
    ("Connect a calendar", "Google or Microsoft. Read and write, nothing else, revocable from your own account settings."),
    ("Say when you think", "Two questions: which hours, and how long a block is worth having. Takes about forty seconds."),
    ("Leave it alone", "It defends those blocks from the next booking. You will notice within a week, mostly by not being interrupted."),
]

PROOF = [
    ("We got 6 hours a week back per engineer, measured properly rather than surveyed.",
     "Wes Tremayne", "VP Engineering, Ordinal Systems"),
    ("The declines going out with an alternative time is the whole product. Everything else is packaging.",
     "Nadia Osei", "Design Director, Meridian Labs"),
    ("I turned it off for a fortnight as a test and asked to have it back on day four.",
     "Priya Raman", "Head of Ops, Northwind Logistics"),
]

COMPARE = [
    ("Blocks focus time automatically", True, False, False),
    ("Declines with an alternative time", True, False, False),
    ("Works without asking your team to adopt it", True, True, False),
    ("Configuration under a minute", True, False, True),
    ("Weekly report of what it changed", True, False, False),
    ("Free for one calendar", True, True, True),
]

FAQ = [
    ("What does it actually have access to?",
     "Read and write on your calendar events, and nothing else. Not your mail, not your files, not your contacts. You can revoke it from Google or Microsoft directly without telling us."),
    ("Will it cancel meetings I care about?",
     "It never cancels. It declines new invitations that land on a protected block, and only when you have more than one such block that day — so a single unavoidable meeting still gets through."),
    ("What happens to the declines?",
     "The organiser gets a normal decline with the next two times you are genuinely free. Most people rebook into one of them, which is the point."),
    ("Does everyone on my team need it?",
     "No, and that is deliberate. It works entirely from your side of the calendar. Nobody else installs anything or changes how they book."),
    ("What does it cost?",
     "Free for one calendar, for as long as you like. £6 a month if you want more than one, or the weekly report by email."),
    ("How do I turn it off?",
     "One switch, and every protected block disappears immediately. Disconnecting the calendar deletes what we hold within 24 hours."),
]


# --- client logos: a geometric mark plus a wordmark, monochrome via
# currentColor so one set serves light and dark. Drawn rather than set as SVG
# <text>, which keeps typography under CSS instead of a font that may be absent.
MARKS = {'northwind': '<path d="M12 2 15 12 12 22 9 12Z" fill="currentColor"/><path d="M2 12 12 9l10 3-10 3Z" fill="currentColor" opacity=".45"/>', 'palisade': '<path d="M4 22V9.5L6 6l2 3.5V22M11 22V5.5L13 2l2 3.5V22M18 22V10.5L20 7l2 3.5V22" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linejoin="round"/>', 'ordinal': '<rect x="4" y="4" width="16" height="16" rx="2.5" transform="rotate(45 12 12)" stroke="currentColor" stroke-width="1.8" fill="none"/><circle cx="12" cy="12" r="2.8" fill="currentColor"/>', 'meridian': '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7" fill="none"/><ellipse cx="12" cy="12" rx="4" ry="9" stroke="currentColor" stroke-width="1.5" fill="none"/><path d="M3.2 12h17.6" stroke="currentColor" stroke-width="1.5"/>', 'kettle': '<path d="M4 11h12v4.5A4.5 4.5 0 0 1 11.5 20h-3A4.5 4.5 0 0 1 4 15.5Z" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linejoin="round"/><path d="M16 12.5h1.6a2.4 2.4 0 0 1 0 4.8H16" stroke="currentColor" stroke-width="1.7" fill="none"/><path d="M7.5 3.5v3M11.5 2.5v4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>', 'brightsea': '<path d="M2.5 16.5c2.5-2 4.5 0 7 0s4.5-2 7 0 3.5 0 4-.5" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linecap="round"/><path d="M2.5 20.5c2.5-2 4.5 0 7 0s4.5-2 7 0 3.5 0 4-.5" stroke="currentColor" stroke-width="1.7" fill="none" stroke-linecap="round" opacity=".5"/><circle cx="17" cy="7" r="4" stroke="currentColor" stroke-width="1.7" fill="none"/>'}


def logo(key, word):
    return (f'<span class="logo"><svg class="logo-mark" viewBox="0 0 24 24" width="22" height="22" '
            f'aria-hidden="true">{MARKS[key]}</svg><span class="logo-word">{word}</span></span>')


# Six, not five: six divides evenly into the 2, 3 and 6 column counts the grid
# resolves to across breakpoints, so no width leaves a short last row.
CLIENTS = [("northwind", "Northwind"), ("palisade", "Palisade"), ("ordinal", "Ordinal"),
           ("meridian", "Meridian Labs"), ("kettle", "Kettle &amp; Co"), ("brightsea", "Brightsea")]

LOGO_ROW = '<div class="logo-row">' + "".join(logo(k, w) for k, w in CLIENTS) + '</div>' 

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
<script type="importmap">{{"imports": {{"bootstrap": "./assets/vendor/bootstrap6/js/bootstrap.bundle.min.js"}}}}</script>
<link rel="stylesheet" href="assets/css/base.css">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
"""



# The hero product shot, as data. col, row, span, kind, label.
# Rows are 15-minute-ish bands; a Focus block spans three.
WEEK_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri"]
WEEK = [
    (1, 1, 1, "meet", "Standup"),   (1, 2, 3, "focus", "Focus"),
    (2, 1, 1, "meet", "Standup"),   (2, 2, 3, "focus", "Focus"),  (2, 5, 1, "meet", "1:1"),
    (3, 1, 1, "meet", "Standup"),   (3, 2, 3, "focus", "Focus"),  (3, 5, 1, "dec", "Declined"),
    (4, 1, 1, "meet", "Standup"),   (4, 2, 3, "focus", "Focus"),  (4, 6, 1, "meet", "Review"),
    (5, 1, 1, "meet", "Standup"),   (5, 2, 3, "focus", "Focus"),
]

# Two slots in one cell overlap silently — the browser just draws one over the
# other and both labels become unreadable. That shipped once; assert instead.
_seen = {}
for _c, _r, _h, _kind, _label in WEEK:
    for _row in range(_r, _r + _h):
        _key = (_c, _row)
        assert _key not in _seen, (
            f"week grid: {_label!r} overlaps {_seen[_key]!r} at column {_c}, row {_row}")
        _seen[_key] = _label


def week_grid():
    head = "".join(f"<span>{d}</span>" for d in WEEK_DAYS)
    slots = "\n          ".join(
        f'<div class="slot slot-{kind}" style="--r:{r};--c:{c}' + (f';--h:{h}' if h > 1 else '') + f'">{label}</div>'
        for c, r, h, kind, label in WEEK)
    return f"""<div class="week" aria-hidden="true">
        <div class="week-head">{head}</div>
        <div class="week-grid">
          {slots}
        </div>
      </div>"""


def signup(where, *, big=False):
    """The capture form, rendered twice — hero and sticky bar. Both carry
    data-signup, and the script keeps their value in step, so a half-typed
    address is never lost when one scrolls out of view and the other takes over."""
    size = " btn-lg" if big else ""
    return f"""<form class="signup" data-signup data-demo-form novalidate>
        <label class="visually-hidden" for="email-{where}">Work email</label>
        <input class="form-control{' form-control-lg' if big else ''}" type="email" id="email-{where}" name="email"
               placeholder="you@company.com" autocomplete="email" required data-signup-input>
        <button class="btn-solid theme-primary{size}" type="submit" data-done-text="Check your inbox ✓">Get early access</button>
        <div class="invalid-feedback">A work email, so we can tell you when your calendar is supported.</div>
      </form>"""


def chrome():
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="wrap head-in">
    <a class="wordmark" href="index.html"><span class="wordmark-mark" aria-hidden="true">◤</span>{TITLE}</a>
    <nav class="head-nav d-none md:d-flex" aria-label="Main">
      <a class="head-link" href="#how">How it works</a>
      <a class="head-link" href="#compare">Compare</a>
      <a class="head-link" href="#faq">Questions</a>
    </nav>
    <div class="d-flex align-items-center gap-2 ms-auto">
      {TOGGLE}
      <a class="btn-outline theme-secondary btn-sm" href="#get">Get early access</a>
    </div>
  </div>
</header>
"""


FOOTER = """
<footer class="site-footer">
  <div class="wrap foot-in">
    <p class="fs-sm fg-3 mb-0">
      &copy; <span data-year>2026</span> """ + TITLE + """ &mdash; a free Bootstrap 6 template.
      The product, the people quoted and every figure here are fictional.
    </p>
    <p class="fs-sm fg-3 mb-0"><a href="index.html">Privacy</a> &middot; <a href="index.html">Terms</a> &middot; <a href="thanks.html">Status</a></p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page_index():
    features = "\n".join(f"""        <article class="feat">
          <span class="feat-icon" aria-hidden="true"><svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"><path d="{path}"/></svg></span>
          <h3 class="feat-name mb-2">{name}</h3>
          <p class="fg-2 fs-sm mb-0">{blurb}</p>
        </article>""" for name, blurb, path in FEATURES)

    steps = "\n".join(f"""        <li class="step">
          <span class="step-n" aria-hidden="true">{i + 1}</span>
          <div>
            <h3 class="step-name mb-2">{name}</h3>
            <p class="fg-2 mb-0">{blurb}</p>
          </div>
        </li>""" for i, (name, blurb) in enumerate(STEPS))

    proof = "\n".join(f"""        <figure class="quote">
          <blockquote class="mb-3"><p class="mb-0">{q}</p></blockquote>
          <figcaption><strong>{who}</strong><span class="fg-3 d-block">{role}</span></figcaption>
        </figure>""" for q, who, role in PROOF)

    yes = '<span class="yes" aria-label="Yes">✓</span>'
    no = '<span class="no" aria-label="No">—</span>'
    rows = "\n".join(f"""            <tr>
              <th scope="row">{label}</th>
              <td data-cell="Threshold">{yes if a else no}</td>
              <td data-cell="Calendar blocking apps">{yes if b else no}</td>
              <td data-cell="Doing it by hand">{yes if c else no}</td>
            </tr>""" for label, a, b, c in COMPARE)

    faq = "\n".join(f"""          <details name="faq">
            <summary>{q}</summary>
            <div class="faq-body"><p class="fg-2 mb-0">{a}</p></div>
          </details>""" for q, a in FAQ)

    body = f"""
<main id="main">

  <section class="hero" id="get">
    <div class="wrap hero-in">
      <p class="pill mb-4"><span class="pill-dot" aria-hidden="true"></span> Private beta &middot; 1,400 on the list</p>
      <h1 class="hero-title mb-4">Your calendar defends<br>your afternoons.</h1>
      <p class="hero-lede mb-5">
        Threshold blocks the focus time you keep meaning to protect, and declines
        what lands on it with a real alternative. One rule, no settings screen,
        and nobody else on your team has to install anything.
      </p>

      {signup('hero', big=True)}

      <p class="hero-note mb-0">Free for one calendar. No card. Revoke access from Google or Microsoft whenever you like.</p>

      {week_grid()}
    </div>
  </section>

  <div class="logo-band">
    <div class="wrap">
      <p class="fs-xs eyebrow fg-3 mb-3">Protecting time at</p>
      {LOGO_ROW}
    </div>
  </div>

  <section class="band">
    <div class="wrap">
      <h2 class="band-title mb-5">Four things it does, and nothing else</h2>
      <div class="feat-grid">
{features}
      </div>
    </div>
  </section>

  <section class="band band-alt" id="how">
    <div class="wrap">
      <h2 class="band-title mb-5">Set up once, in under a minute</h2>
      <ol class="step-list">
{steps}
      </ol>
    </div>
  </section>

  <section class="band">
    <div class="wrap">
      <h2 class="band-title mb-5">People who kept it on</h2>
      <div class="quote-grid">
{proof}
      </div>
    </div>
  </section>

  <section class="band band-alt" id="compare">
    <div class="wrap">
      <h2 class="band-title mb-2">Against the two things you are doing now</h2>
      <p class="fg-2 mb-5">Honest columns. Doing it by hand genuinely works — it just does not survive a busy fortnight.</p>
      <div class="table-responsive">
        <table class="table md:table-stacked align-middle compare">
          <thead><tr><th scope="col">&nbsp;</th><th scope="col">{TITLE}</th><th scope="col">Blocking apps</th><th scope="col">By hand</th></tr></thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <section class="band" id="faq">
    <div class="wrap faq-wrap">
      <h2 class="band-title mb-5">The questions people actually ask</h2>
      <div class="faq">
{faq}
      </div>
    </div>
  </section>

  <section class="closer">
    <div class="wrap">
      <h2 class="closer-title mb-3">Get your afternoons back</h2>
      <p class="fg-2 mb-5">Free for one calendar. Takes under a minute. Turn it off with one switch.</p>
      {signup('closer', big=True)}
      <p class="hero-note mb-0">1,400 people on the list. We are letting in about 80 a week.</p>
    </div>
  </section>

</main>

<!-- Sticky bar. Appears only once the hero form has scrolled away, and shares
     its value, so a half-typed address is never lost. -->
<div class="sticky-bar" data-sticky hidden>
  <div class="wrap sticky-in">
    <p class="sticky-copy mb-0"><strong>Get your afternoons back.</strong> <span class="fg-3">Free for one calendar.</span></p>
    {signup('sticky')}
  </div>
</div>
"""
    (ROOT / "index.html").write_text(
        HEAD.format(title=f"{TITLE} — Free Bootstrap 6 Landing Page Template",
                    desc="Threshold is a free Bootstrap 6 landing page template with a sticky conversion bar that shares state with the hero form, so a half-typed email is never lost.")
        + chrome() + body + FOOTER, encoding="utf-8")


def page_thanks():
    body = f"""
<main id="main" class="thanks">
  <div class="wrap thanks-in">
    <span class="thanks-tick" aria-hidden="true">✓</span>
    <h1 class="hero-title mb-3">You are on the list.</h1>
    <p class="hero-lede mb-5">
      Position <strong>1,401</strong>. We let in about eighty people a week, so
      that is roughly a fortnight. You will get one email when it is your turn
      and nothing before it.
    </p>

    <div class="thanks-grid">
      <div class="thanks-card">
        <h2 class="feat-name mb-2">Move up the list</h2>
        <p class="fg-2 fs-sm mb-3">Anyone who joins through your link puts you five places forward. Ten of them and you are in this week.</p>
        <div class="copy-row">
          <input class="form-control" type="text" value="threshold.example/r/9K4D2" readonly aria-label="Your referral link" id="refLink">
          <button class="btn-solid theme-primary" type="button" data-copy="#refLink" data-done-text="Copied ✓">Copy</button>
        </div>
      </div>

      <div class="thanks-card">
        <h2 class="feat-name mb-2">While you wait</h2>
        <p class="fg-2 fs-sm mb-3">The manual version of this works. Block two hours tomorrow afternoon and decline anything that lands on it with an alternative time.</p>
        <a class="btn-outline theme-secondary" href="index.html#how">Read how it works</a>
      </div>
    </div>

    <p class="fs-sm fg-3 mt-5 mb-0">
      Wrong address, or changed your mind? <a href="index.html">Start again</a> —
      we have not stored anything a delete cannot remove.
    </p>
  </div>
</main>
"""
    (ROOT / "thanks.html").write_text(
        HEAD.format(title=f"You are on the list — {TITLE} Bootstrap 6 Landing Page Template",
                    desc="A thank-you page with queue position, a referral link with copy-to-clipboard, and something useful to do while waiting.")
        + chrome() + body + FOOTER, encoding="utf-8")


page_index()
page_thanks()
print(f"wrote 2 pages — {len(FEATURES)} features, {len(FAQ)} questions")
