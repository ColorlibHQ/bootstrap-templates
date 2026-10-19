#!/usr/bin/env python3
"""
Generates the Bootstrap 6 Forms pack: an index gallery plus one page per variant.

Every variant shares the same chrome (sticky bar with a back link and a colour-mode
toggle) so the pack reads as one product, while each form body is genuinely
different. Ten variants, and between them they exercise every form component that
Bootstrap 6 added over v5.
"""

import pathlib

PACK_TITLE = "Bootstrap 6 Forms"
ROOT = pathlib.Path(__file__).parent

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<!-- Bootstrap 6, bundled in assets/vendor/bootstrap6 (version in the CSS file header). To load it from jsDelivr instead, replace both paths below with https://cdn.jsdelivr.net/npm/bootstrap@VERSION/dist/... -->
<link rel="stylesheet" href="{p}assets/vendor/bootstrap6/css/bootstrap.min.css">
<script type="importmap">{{"imports": {{"bootstrap": "./{p}assets/vendor/bootstrap6/js/bootstrap.bundle.min.js"}}}}</script>
<link rel="stylesheet" href="{p}assets/css/base.css">
<link rel="stylesheet" href="{p}assets/css/style.css">
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

MAIL = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" '
        'aria-hidden="true"><rect x="1.5" y="3" width="13" height="10" rx="1.5"/><path d="m2 4 6 4.5L14 4"/></svg>')

SEARCH = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
          'aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 4 4" stroke-linecap="round"/></svg>')

ACC_ICON = ('<svg class="accordion-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16" fill="none" '
            'stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"><path d="m2 5 6 6 6-6"/></svg>')


def combobox(name, placeholder, options, search=False, multiple=False):
    attrs = 'data-bs-toggle="combobox"'
    if search:
        attrs += ' data-bs-search="true"'
    if multiple:
        attrs += ' data-bs-multiple="true"'
    items = "\n      ".join(
        f'<button class="menu-item" type="button" data-bs-value="{v}">{l}</button>' for v, l in options)
    return f"""<button class="form-control combobox-toggle" type="button" {attrs} data-bs-name="{name}" data-bs-placeholder="{placeholder}">
      <span class="combobox-value">{placeholder}</span>
      {CARET}
    </button>
    <div class="menu">
      {items}
    </div>"""


# (folder, nav title, card title, blurb, sketch html, wide?, form html)
VARIANTS = [
    ("01-stacked", "Stacked", "Stacked contact form",
     "The default. Labelled fields in a single column with help text, an adorned email input and native :user-invalid validation.",
     '<i class="w40"></i><i class="tall"></i><i class="w40"></i><i class="tall"></i><i class="w60"></i><i class="tall"></i><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Get in touch</h1>
  <p class="fg-2 mb-5">We reply to everything within one working day.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="s1name">Full name</label>
      <input type="text" class="form-control" id="s1name" required>
      <div class="invalid-feedback">Please tell us your name.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="s1email">Email</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="s1email" required>
      </div>
      <div class="form-text">We&#8217;ll only use this to reply.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="s1msg">Message</label>
      <textarea class="form-control" id="s1msg" rows="4" required></textarea>
      <div class="invalid-feedback">A sentence or two is plenty.</div>
    </div>
    <div class="form-field">
      <input type="checkbox" class="check" id="s1ok" required>
      <label for="s1ok">I&#8217;m happy to be contacted about this enquiry</label>
    </div>
    <div><button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Sent &#10003;">Send message</button></div>
  </form>
</div>"""),

    ("02-split", "Split", "Split brand panel",
     "A gradient brand panel beside the fields — the pattern most SaaS sign-up flows land on.",
     '<div class="row2"><i class="tall" style="min-height:5rem"></i><i class="tall" style="min-height:5rem"></i></div><i class="w60"></i><i class="cta"></i>',
     True, """<div class="split-form">
  <div class="split-brand">
    <div>
      <p class="fs-xs mb-4" style="letter-spacing:.16em;text-transform:uppercase;opacity:.8">Start free</p>
      <h1 class="fs-3xl fw-bold mb-3" style="letter-spacing:-.03em">Fourteen days, no card</h1>
      <p class="mb-0" style="opacity:.85">Full access to everything. If it isn&#8217;t for you, do nothing and it simply stops.</p>
    </div>
    <ul class="vstack gap-2 fs-sm list-unstyled mb-0" style="opacity:.9">
      <li>&#10003; Unlimited projects</li>
      <li>&#10003; Cancel from settings</li>
      <li>&#10003; No sales call</li>
    </ul>
  </div>
  <div class="split-body">
    <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
      <div class="form-field">
        <label class="form-label" for="s2name">Full name</label>
        <input type="text" class="form-control" id="s2name" required>
        <div class="invalid-feedback">Required.</div>
      </div>
      <div class="form-field">
        <label class="form-label" for="s2email">Work email</label>
        <div class="form-control form-adorn">
          <div class="form-adorn-icon">""" + MAIL + """</div>
          <input type="email" class="form-ghost" id="s2email" required>
        </div>
      </div>
      <div>
        <label class="form-label">Team size</label>
        """ + combobox("teamsize", "Choose one…", [("1", "Just me"), ("2", "2–10"), ("3", "11–50"), ("4", "50+")]) + """
      </div>
      <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Workspace created &#10003;">Create workspace</button></div>
    </form>
  </div>
</div>"""),

    ("03-stepper", "Stepper", "Multi-step form",
     "Long forms split across steps with Bootstrap 6&#8217;s new Stepper marking progress.",
     '<div class="row2"><i></i><i></i><i></i></div><i class="w40"></i><i class="tall"></i><i class="w60"></i><i class="tall"></i><i class="cta"></i>',
     False, """<div class="form-shell">
  <div class="contains-inline mb-5">
    <ol class="stepper sm:stepper-horizontal">
      <li class="stepper-item active">Details</li>
      <li class="stepper-item active">Project</li>
      <li class="stepper-item">Budget</li>
    </ol>
  </div>
  <h1 class="fs-xl fw-semibold mb-4">About the project</h1>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div>
      <label class="form-label">What do you need?</label>
      """ + combobox("need", "Select one or more…",
                     [("brand", "Brand identity"), ("web", "Website build"), ("app", "Product design"),
                      ("audit", "Accessibility audit")], search=True, multiple=True) + """
    </div>
    <div class="form-field">
      <label class="form-label" for="s3when">Ideal start</label>
      <input type="text" class="form-control" id="s3when" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date&#8230;">
    </div>
    <div class="form-field">
      <label class="form-label" for="s3brief">Brief</label>
      <textarea class="form-control" id="s3brief" rows="3" required></textarea>
      <div class="invalid-feedback">Required.</div>
    </div>
    <div class="d-flex gap-2">
      <button class="btn-text" type="button">Back</button>
      <button class="btn-solid theme-primary ms-auto" type="submit" data-done-text="Saved &#10003;">Continue</button>
    </div>
  </form>
</div>"""),

    ("04-toolbar", "Toolbar", "Inline filter toolbar",
     "A horizontal search and filter bar built from Combobox — the pattern every listing page needs.",
     '<div class="row2"><i class="tall"></i><i class="tall"></i><i class="tall"></i></div><div class="row2"><i class="w40"></i><i class="w40"></i></div>',
     True, """<div class="w-100">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Filter results</h1>
  <p class="fg-2 mb-4">Search, area and category in a single row, collapsing to a stack on small screens.</p>
  <form class="toolbar mb-4" role="search" onsubmit="return false">
    <div class="form-control form-adorn">
      <div class="form-adorn-icon">""" + SEARCH + """</div>
      <input type="search" class="form-ghost" placeholder="Search by keyword…" aria-label="Search">
    </div>
    """ + combobox("area", "Any area", [("n", "North"), ("s", "South"), ("e", "East"), ("w", "West")], search=True) + """
    """ + combobox("cat", "All categories", [("a", "Design"), ("b", "Engineering"), ("c", "Marketing"), ("d", "Operations")], search=True, multiple=True) + """
    <button class="btn-solid theme-primary" type="submit">Search</button>
  </form>
  <div class="d-flex flex-wrap gap-2">
    <span class="chip">North <button type="button" class="chip-dismiss" aria-label="Remove North"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="4" x2="12" y2="12"/><line x1="12" y1="4" x2="4" y2="12"/></svg></button></span>
    <span class="chip">Design <button type="button" class="chip-dismiss" aria-label="Remove Design"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><line x1="4" y1="4" x2="12" y2="12"/><line x1="12" y1="4" x2="4" y2="12"/></svg></button></span>
    <button class="btn-text btn-sm" type="button">Clear all</button>
  </div>
</div>"""),

    ("05-booking", "Booking", "Appointment booking",
     "Datepicker plus time-slot toggles — the shape almost every clinic, salon and studio needs.",
     '<i class="w40"></i><i class="tall" style="min-height:3.5rem"></i><div class="row2"><i></i><i></i><i></i><i></i></div><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Book an appointment</h1>
  <p class="fg-2 mb-5">Same-week slots, cancel free up to 24 hours before.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div>
      <label class="form-label">Service</label>
      """ + combobox("service", "Choose a service…",
                     [("con", "Consultation — 30 min"), ("rev", "Review — 45 min"), ("full", "Full assessment — 90 min")], search=True) + """
    </div>
    <div class="form-field">
      <label class="form-label" for="s5date">Date</label>
      <input type="text" class="form-control" id="s5date" data-bs-toggle="datepicker" autocomplete="off" placeholder="Choose a date…" required>
      <div class="invalid-feedback">Please pick a date.</div>
    </div>
    <div>
      <label class="form-label d-block">Available times</label>
      <div class="slots">
        <label class="btn-check btn-outline theme-primary btn-sm"><input type="radio" name="slot"> 09:20</label>
        <label class="btn-check btn-outline theme-primary btn-sm"><input type="radio" name="slot" checked> 10:40</label>
        <label class="btn-check btn-outline theme-primary btn-sm"><input type="radio" name="slot"> 13:15</label>
        <label class="btn-check btn-outline theme-primary btn-sm"><input type="radio" name="slot"> 16:30</label>
      </div>
    </div>
    <div class="form-field">
      <div class="switch"><input type="checkbox" value="" id="s5remind" role="switch" switch checked></div>
      <label for="s5remind">Text me a reminder the day before</label>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Booked &#10003;">Confirm booking</button></div>
  </form>
</div>"""),

    ("06-strength", "Strength", "Sign-up with strength meter",
     "Registration using the new password Strength component, which fills as the password improves.",
     '<i class="w40"></i><i class="tall"></i><i class="w40"></i><i class="tall"></i><div class="row2"><i></i><i></i><i></i><i></i></div><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Create your account</h1>
  <p class="fg-2 mb-5">Type into the password field to watch the meter fill.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="s6email">Email</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="s6email" required>
      </div>
    </div>
    <div class="form-field">
      <label class="form-label" for="s6pw">Password</label>
      <input type="password" class="form-control" id="s6pw" required>
      <div class="strength" data-bs-strength>
        <div class="strength-segment"></div><div class="strength-segment"></div>
        <div class="strength-segment"></div><div class="strength-segment"></div>
      </div>
      <div class="form-text">At least 12 characters, and please don&#8217;t reuse one.</div>
    </div>
    <div class="form-field">
      <input type="checkbox" class="check" id="s6terms" required>
      <label for="s6terms">I accept the terms of service</label>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Account created &#10003;">Create account</button></div>
  </form>
</div>"""),

    ("07-otp", "OTP", "Verification code",
     "One-time-code entry with the new OTP input: per-character boxes, paste handling and one-time-code autofill.",
     '<i class="w60" style="margin-inline:auto"></i><div class="row2"><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i></div><i class="cta" style="margin-inline:auto"></i>',
     False, """<div class="form-shell text-center">
  <span class="icon-tile mx-auto mb-4">""" + MAIL + """</span>
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Check your phone</h1>
  <p class="fg-2 mb-5">We sent a six-digit code to the number ending 4417.</p>
  <form class="vstack gap-4" data-demo-form novalidate>
    <div>
      <label class="form-label visually-hidden" for="s7otp">Verification code</label>
      <div class="otp d-inline-flex" data-bs-otp>
        <input type="text" class="otp-input" maxlength="6" id="s7otp" aria-label="Verification code" autocomplete="one-time-code">
      </div>
    </div>
    <div><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Verified &#10003;">Verify</button></div>
    <p class="fs-sm fg-3 mb-0">Didn&#8217;t get it? <a href="#">Send another</a> &#183; <a href="#">Use a different number</a></p>
  </form>
</div>"""),

    ("08-chips", "Chips", "Tag and interest picker",
     "Chip input for tokens the visitor types themselves, plus chips as removable applied filters.",
     '<i class="w40"></i><i class="tall"></i><div class="row2"><i></i><i></i><i></i></div><i class="w60"></i><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Tell us what you&#8217;re into</h1>
  <p class="fg-2 mb-5">Type and press Enter to add. Backspace removes the last one.</p>
  <form class="vstack gap-4" data-demo-form data-bs-validate novalidate>
    <div>
      <label class="form-label" for="s8topics">Topics</label>
      <div class="chip-input" data-bs-chips>
        <span class="chip">engineering</span>
        <span class="chip">design systems</span>
        <input type="text" class="form-ghost" id="s8topics" placeholder="Add a topic…">
      </div>
    </div>
    <div>
      <label class="form-label" for="s8skills">Skills</label>
      <div class="chip-input" data-bs-chips>
        <span class="chip">typescript</span>
        <input type="text" class="form-ghost" id="s8skills" placeholder="Add a skill…">
      </div>
    </div>
    <div class="form-field">
      <label class="form-label" for="s8email">Where should we send it?</label>
      <div class="form-control form-adorn">
        <div class="form-adorn-icon">""" + MAIL + """</div>
        <input type="email" class="form-ghost" id="s8email" required>
      </div>
    </div>
    <div><button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Saved &#10003;">Save preferences</button></div>
  </form>
</div>"""),

    ("09-range", "Range", "Quote calculator",
     "Range sliders with live value bubbles driving a running estimate — no plugin, no chart library.",
     '<i class="w40"></i><i></i><i class="w40"></i><i></i><i class="w75"></i><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Estimate your project</h1>
  <p class="fg-2 mb-5">Rough numbers. We&#8217;ll confirm everything before anything is agreed.</p>
  <form class="vstack gap-4" data-demo-form novalidate>
    <div>
      <label class="form-label" for="s9pages">Number of pages</label>
      <div class="form-range" data-bs-bubble>
        <input type="range" class="form-range-input" id="s9pages" min="1" max="40" value="8"
               data-range-out="s9pagesOut" aria-label="Number of pages">
      </div>
      <p class="fs-xs fg-3 mb-0"><strong class="fg-1" id="s9pagesOut">8</strong> pages</p>
    </div>
    <div>
      <label class="form-label" for="s9weeks">Timeline</label>
      <div class="form-range" data-bs-bubble>
        <input type="range" class="form-range-input" id="s9weeks" min="2" max="26" value="8"
               data-range-out="s9weeksOut" data-range-suffix=" weeks" aria-label="Timeline in weeks">
      </div>
      <p class="fs-xs fg-3 mb-0"><strong class="fg-1" id="s9weeksOut">8 weeks</strong> from kick-off</p>
    </div>
    <div>
      <label class="form-label" for="s9budget">Budget</label>
      <div class="form-range" data-bs-bubble>
        <input type="range" class="form-range-input" id="s9budget" min="5" max="120" step="5" value="35"
               data-range-out="s9budgetOut" data-range-prefix="£" data-range-suffix="k" aria-label="Budget">
      </div>
      <p class="fs-xs fg-3 mb-0">Around <strong class="fg-1" id="s9budgetOut">£35k</strong></p>
    </div>
    <div><button class="btn-solid theme-primary btn-lg" type="submit" data-done-text="Sent &#10003;">Send for a quote</button></div>
  </form>
</div>"""),

    ("10-floating", "Floating", "Floating labels",
     "Floating labels with adorned inputs and a native select, for dense forms where every row counts.",
     '<i class="tall"></i><i class="tall"></i><div class="row2"><i class="tall"></i><i class="tall"></i></div><i class="cta"></i>',
     False, """<div class="form-shell">
  <h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Billing details</h1>
  <p class="fg-2 mb-5">Labels float out of the way once a field has content.</p>
  <form class="vstack gap-3" data-demo-form data-bs-validate novalidate>
    <div class="form-floating">
      <input type="text" class="form-control" id="s10name" placeholder="Full name" required>
      <label for="s10name">Full name</label>
    </div>
    <div class="form-floating">
      <input type="email" class="form-control" id="s10email" placeholder="you@example.com" required>
      <label for="s10email">Email address</label>
    </div>
    <div class="form-floating">
      <input type="text" class="form-control" id="s10addr" placeholder="Address" required>
      <label for="s10addr">Address</label>
    </div>
    <div class="row g-3">
      <div class="col-7">
        <div class="form-floating">
          <input type="text" class="form-control" id="s10city" placeholder="City" required>
          <label for="s10city">City</label>
        </div>
      </div>
      <div class="col-5">
        <div class="form-floating">
          <input type="text" class="form-control" id="s10post" placeholder="Postcode" required>
          <label for="s10post">Postcode</label>
        </div>
      </div>
    </div>
    <div class="form-floating">
      <select class="form-control" id="s10country">
        <option selected>United Kingdom</option><option>Ireland</option><option>Germany</option><option>France</option>
      </select>
      <label for="s10country">Country</label>
    </div>
    <div class="mt-2"><button class="btn-solid theme-primary w-100 btn-lg" type="submit" data-done-text="Saved &#10003;">Save details</button></div>
  </form>
</div>"""),
]


def write_variant(i, folder, nav, card, blurb, sketch, wide, body):
    prev_i = (i - 1) % len(VARIANTS)
    next_i = (i + 1) % len(VARIANTS)
    html = HEAD.format(
        title=f"{card} — {PACK_TITLE}",
        desc=f"{blurb} A free Bootstrap 6 form example.",
        p="../")
    html += f"""
<div class="variant-bar">
  <a class="btn-text btn-sm" href="../index.html">&#8592; All forms</a>
  <span class="fs-sm fw-semibold ms-2">{card}</span>
  <span class="fs-xs fg-3 d-none md:d-inline">{i + 1} of {len(VARIANTS)}</span>
  <div class="d-flex align-items-center gap-2 ms-auto">
    <a class="btn-icon btn-sm" href="../{VARIANTS[prev_i][0]}/index.html" aria-label="Previous form">&#8249;</a>
    <a class="btn-icon btn-sm" href="../{VARIANTS[next_i][0]}/index.html" aria-label="Next form">&#8250;</a>
    {TOGGLE}
  </div>
</div>

<main class="variant-stage">
  <div class="variant-inner{' is-wide' if wide else ''}">
    {body}
  </div>
</main>

<script type="module" src="../assets/js/main.js"></script>
</body>
</html>
"""
    d = ROOT / folder
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(html, encoding="utf-8")


def write_index():
    cards = []
    for i, (folder, nav, card, blurb, sketch, wide, body) in enumerate(VARIANTS, 1):
        cards.append(f"""      <a class="pack-card" href="{folder}/index.html">
        <div class="pack-thumb"><div class="sketch">{sketch}</div></div>
        <div class="pack-card-body">
          <p class="fs-xs fg-3 mb-1">{i:02d}</p>
          <h2 class="pack-card-title">{card}</h2>
          <p class="fg-2 fs-sm mb-0">{blurb}</p>
        </div>
      </a>""")

    html = HEAD.format(
        title=f"{PACK_TITLE} — 10 Free Bootstrap 6 Form Templates",
        desc="Ten free Bootstrap 6 form templates — contact, sign-up, booking, multi-step, OTP verification, chips, range and floating labels. No build step.",
        p="")
    html += f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#forms">Skip to the forms</a>

<div class="pack-head">
  <div class="container">
    <div class="d-flex flex-wrap align-items-start gap-3">
      <div class="me-auto" style="max-width:44rem">
        <span class="badge badge-subtle theme-primary mb-3">Bootstrap 6.0.0-alpha1</span>
        <h1 class="fs-4xl fw-bold mb-3" style="letter-spacing:-.03em">{PACK_TITLE}</h1>
        <p class="fs-lg fg-2 mb-0">
          Ten form layouts covering the shapes real projects need &#8212; contact,
          sign-up, booking, multi-step, verification and filtering. Between them they
          use every form component Bootstrap 6 added over v5.
        </p>
      </div>
      {TOGGLE}
    </div>
  </div>
</div>

<main id="forms" class="section">
  <div class="container">
    <div class="pack-grid">
{chr(10).join(cards)}
    </div>

    <section class="mt-9" style="max-width:46rem">
      <h2 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">Using these</h2>
      <div class="prose">
        <p>Each form is a standalone page. Copy the markup out of the one you want and
        drop it into your project &#8212; the only requirements are Bootstrap 6&#8217;s CSS and, if
        you use Combobox, Datepicker, OTP, Chips or Range, its JavaScript bundle.</p>
        <p>Bootstrap 6 is ESM-only, so the script tag needs <code>type="module"</code> and
        there is no <code>window.bootstrap</code> global. Importing the bundle for its side
        effects is what registers the data-attribute API.</p>
        <h3>Validation</h3>
        <p><code>.needs-validation</code> and <code>.was-validated</code> are gone. Put
        <code>data-bs-validate</code> and <code>novalidate</code> on the form and native
        <code>:user-invalid</code> handles the styling &#8212; feedback only appears after the
        visitor has actually interacted with a field. Add
        <code>data-bs-validate="valid"</code> if you also want success styling.</p>
        <h3>A gotcha worth knowing</h3>
        <p>Combobox&#8217;s <code>search</code> and <code>multiple</code> options are typed
        booleans, so a bare attribute fails config validation. Write
        <code>data-bs-search="true"</code>, not <code>data-bs-search</code>. Bare marker
        attributes are correct for <code>data-bs-otp</code>, <code>data-bs-chips</code>,
        <code>data-bs-strength</code> and <code>data-bs-validate</code>.</p>
      </div>
    </section>
  </div>
</main>

<footer class="site-footer bg-2 py-6 mt-9">
  <div class="container d-flex flex-wrap justify-content-between align-items-center gap-3">
    <p class="fg-3 fs-xs mb-0">&copy; <span data-year>2026</span> {PACK_TITLE}. A free pack for uicookies.</p>
    <p class="fg-3 fs-xs mb-0">Built with Bootstrap 6.0.0-alpha1</p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""
    (ROOT / "index.html").write_text(html, encoding="utf-8")


for i, v in enumerate(VARIANTS):
    write_variant(i, *v)
write_index()
print(f"wrote index.html + {len(VARIANTS)} variants")
