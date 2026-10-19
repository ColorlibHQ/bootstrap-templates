#!/usr/bin/env python3
"""
Generates Liftoff: three coming-soon layouts sharing one stylesheet and script.

Coming-soon is a niche where people choose by layout, not by feature list, so
one layout would be a third of a product. The countdown, notify form, social row
and variant switcher are written once here and shared, so the three pages cannot
drift apart.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
LAUNCH = "2027-03-01T09:00:00Z"

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="{theme}">
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

PAGES = [("index.html", "Full bleed"), ("split.html", "Split"), ("minimal.html", "Minimal")]


def switcher(current):
    links = "".join(
        f'<a class="{"active" if f == current else ""}" href="{f}">{label}</a>'
        for f, label in PAGES)
    return f'<nav class="variant-switch" aria-label="Layout variants">{links}</nav>'


def wordmark():
    return ('<a class="wordmark" href="index.html">'
            '<span class="wordmark-mark" aria-hidden="true">L</span> Liftoff</a>')


def countdown(compact=False):
    cls = ' style="--count-compact:1"' if compact else ""
    cells = "".join(
        f'<div class="count-cell"><span class="count-value" id="cd{k}">--</span>'
        f'<span class="count-label">{lab}</span></div>'
        for k, lab in (("D", "Days"), ("H", "Hours"), ("M", "Minutes"), ("S", "Seconds")))
    return (f'<div class="countdown"{cls} role="timer" aria-live="off" '
            f'data-countdown="{LAUNCH}">{cells}</div>')


def notify(id_prefix, start=False):
    align = " notify-start" if start else ""
    return f"""<form class="notify{align}" data-demo-form data-bs-validate novalidate>
        <div class="form-field">
          <label class="visually-hidden" for="{id_prefix}Email">Email address</label>
          <input type="email" class="form-control" id="{id_prefix}Email" placeholder="you@example.com" required>
          <div class="invalid-feedback">A valid email, please.</div>
        </div>
        <button class="btn-solid theme-primary" type="submit" data-done-text="You&#8217;re on the list &#10003;">Notify me</button>
      </form>"""


def social():
    icons = {
        "Instagram": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="2.5" y="2.5" width="11" height="11" rx="3.2"/><circle cx="8" cy="8" r="2.6"/><circle cx="11.4" cy="4.6" r=".7" fill="currentColor" stroke="none"/></svg>',
        "X": '<svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M12.6 1.5h2.2l-4.8 5.5 5.7 7.5h-4.5l-3.5-4.6-4 4.6H1.5l5.2-5.9L1.2 1.5h4.6l3.2 4.2zm-.8 11.7h1.2L4.9 2.7H3.6z"/></svg>',
        "LinkedIn": '<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M3.4 5.5h2.2V13H3.4zM4.5 2.2a1.3 1.3 0 1 1 0 2.6 1.3 1.3 0 0 1 0-2.6M7.2 5.5h2.1v1c.3-.6 1.1-1.2 2.2-1.2 2 0 2.5 1.3 2.5 3.1V13h-2.2V8.9c0-1-.2-1.7-1.2-1.7s-1.3.7-1.3 1.6V13H7.2z"/></svg>',
    }
    links = "".join(f'<a href="#" aria-label="{n}">{svg}</a>' for n, svg in icons.items())
    return f'<span class="social">{links}</span>'


def build_bar(pct=72):
    return f"""<div class="build-bar">
        <div class="d-flex justify-content-between fs-xs mb-1">
          <span class="fg-3">Build progress</span><span class="fw-semibold">{pct}%</span>
        </div>
        <div class="progress" role="progressbar" aria-label="Build progress" aria-valuenow="{pct}" aria-valuemin="0" aria-valuemax="100">
          <div class="progress-bar" style="width:{pct}%"></div>
        </div>
      </div>"""


# ------------------------------------------------------------------ variants

def page_index():
    return HEAD.format(
        theme="dark",
        title="Liftoff — Free Bootstrap 6 Coming Soon Template",
        desc="Liftoff is a free Bootstrap 6 coming-soon template in three layouts — full-bleed countdown, split screen and minimal. Live countdown, notify form and build progress.",
    ) + f"""
<div class="screen screen-photo">
  <img class="backdrop" src="img/backdrop.jpg" alt="" width="1800" height="1200" loading="eager">

  <header class="screen-head">
    {wordmark()}
    <div class="ms-auto d-flex align-items-center gap-3">
      {switcher("index.html")}
      {TOGGLE}
    </div>
  </header>

  <main class="screen-body">
    <div class="text-center" style="max-width:44rem">
      <span class="badge badge-subtle theme-primary mb-5">Launching 1 March</span>
      <h1 class="headline mb-5">Something worth the wait</h1>
      <p class="fs-lg mb-6 fg-2">
        We are rebuilding from the ground up. Same team, same prices, considerably
        fewer things that annoy you.
      </p>
      {countdown()}
      <div class="mt-6 mb-5">
        {notify("fb")}
      </div>
      <p class="fs-xs fg-3 mb-0">No launch spam. One email when we go live, and that is it.</p>
    </div>
  </main>

  <footer class="screen-foot">
    <p class="fs-xs fg-3 mb-0">&copy; <span data-year></span> Liftoff. A free Bootstrap 6 template.</p>
    <span class="ms-auto">{social()}</span>
  </footer>
</div>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page_split():
    return HEAD.format(
        theme="light",
        title="Split layout — Liftoff | Free Bootstrap 6 Coming Soon Template",
        desc="Split-screen coming-soon layout from the Liftoff Bootstrap 6 template — photo panel beside a solid form panel with a live countdown.",
    ) + f"""
<div class="split">
  <div class="split-media">
    <img src="img/backdrop.jpg" alt="" width="1200" height="1400" loading="eager">
  </div>

  <div class="split-panel">
    <header class="d-flex flex-wrap align-items-center gap-4 mb-auto">
      {wordmark()}
      <div class="ms-auto d-flex align-items-center gap-3">
        {switcher("split.html")}
        {TOGGLE}
      </div>
    </header>

    <main class="split-panel-body py-6">
      <span class="badge badge-subtle theme-primary mb-5 align-self-start">Launching 1 March</span>
      <h1 class="headline mb-5">Something worth the wait</h1>
      <p class="fs-lg fg-2 mb-6" style="max-width:32rem">
        We are rebuilding from the ground up. Same team, same prices, considerably
        fewer things that annoy you.
      </p>

      <div class="mb-6" style="max-width:34rem">
        <div class="countdown justify-content-start" role="timer" aria-live="off" data-countdown="{LAUNCH}">
          <div class="count-cell"><span class="count-value" id="cdD">--</span><span class="count-label">Days</span></div>
          <div class="count-cell"><span class="count-value" id="cdH">--</span><span class="count-label">Hours</span></div>
          <div class="count-cell"><span class="count-value" id="cdM">--</span><span class="count-label">Minutes</span></div>
          <div class="count-cell"><span class="count-value" id="cdS">--</span><span class="count-label">Seconds</span></div>
        </div>
      </div>

      <div style="max-width:28rem">
        <div class="mb-4">
          {notify("sp", start=True)}
        </div>
        {build_bar()}
      </div>
    </main>

    <footer class="d-flex flex-wrap align-items-center gap-4 mt-auto pt-5">
      <p class="fs-xs fg-3 mb-0">&copy; <span data-year></span> Liftoff.</p>
      <span class="ms-auto">{social()}</span>
    </footer>
  </div>
</div>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def page_minimal():
    return HEAD.format(
        theme="light",
        title="Minimal layout — Liftoff | Free Bootstrap 6 Coming Soon Template",
        desc="Minimal centred coming-soon layout from the Liftoff Bootstrap 6 template — no photography, live countdown and a notify form.",
    ) + f"""
<div class="screen">
  <header class="screen-head">
    {wordmark()}
    <div class="ms-auto d-flex align-items-center gap-3">
      {switcher("minimal.html")}
      {TOGGLE}
    </div>
  </header>

  <main class="screen-body">
    <div class="text-center" style="max-width:38rem">
      <p class="fs-xs fg-3 mb-5" style="letter-spacing:.22em;text-transform:uppercase">Liftoff &middot; 1 March 2027</p>
      <h1 class="headline mb-5">Something worth the wait</h1>
      <p class="fs-lg fg-2 mb-6">
        No photography, no gradient, nothing to load. Sometimes a holding page
        should just hold.
      </p>
      {countdown()}
      <div class="mt-6 mb-5">
        {notify("mn")}
      </div>
      {build_bar()}
    </div>
  </main>

  <footer class="screen-foot">
    <p class="fs-xs fg-3 mb-0">&copy; <span data-year></span> Liftoff. A free Bootstrap 6 template.</p>
    <span class="ms-auto">{social()}</span>
  </footer>
</div>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "split.html").write_text(page_split(), encoding="utf-8")
(ROOT / "minimal.html").write_text(page_minimal(), encoding="utf-8")
print("wrote 3 layouts")
