#!/usr/bin/env python3
"""
Generates the Bootstrap 6 Navigation pack: an index gallery plus one page per variant.

Every variant shares the same chrome (sticky bar with a back link and a colour-mode
toggle) so the pack reads as one product, while each form body is genuinely
different. Eight navigation patterns. Bootstrap 6 changed navigation more than any other
area — .navbar-collapse is gone, Dropdown became Menu, and Nav overflow is new —
so these double as a migration reference.
"""

import pathlib

PACK_TITLE = "Bootstrap 6 Navigation"
ROOT = pathlib.Path(__file__).parent

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="{p}assets/vendor/bootstrap6/css/bootstrap.min.css">
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


# (folder, nav title, card title, blurb, sketch, wide?, body html)
VARIANTS = [
    ("01-navbar", "Navbar", "Standard navbar",
     "The v6 baseline. There is no .navbar-collapse any more — the mobile menu is a native &lt;dialog class=&quot;drawer&quot;&gt; that navbar-expand inlines on desktop.",
     '<i class="tall"></i><div class="row2"><i></i><i></i><i></i></div><i class="w60"></i>',
     False, """<div class="demo-frame">
  <nav class="navbar lg:navbar-expand" aria-label="Example">
    <div class="container-fluid">
      <a class="navbar-brand d-flex align-items-center gap-2 fw-semibold" href="#"><span class="brand-mark" aria-hidden="true">N</span> Northwind</a>
      <dialog class="drawer drawer-end" tabindex="-1" id="d1" aria-labelledby="d1l">
        <div class="drawer-header"><h5 class="drawer-title" id="d1l">Menu</h5><button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button></div>
        <div class="drawer-body mb-2 lg:mb-0">
          <ul class="nav navbar-nav me-auto">
            <li class="nav-item"><a class="nav-link active" aria-current="page" href="#">Product</a></li>
            <li class="nav-item"><a class="nav-link" href="#">Pricing</a></li>
            <li class="nav-item"><a class="nav-link" href="#">Docs</a></li>
            <li class="nav-item"><a class="nav-link disabled" aria-disabled="true">Status</a></li>
          </ul>
        </div>
      </dialog>
      <div class="d-flex align-items-center gap-2 ms-auto">
        <a class="btn-text d-none md:d-inline-flex" href="#">Sign in</a>
        <button class="btn-solid theme-primary" type="button">Start free</button>
        <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#d1" aria-controls="d1" aria-label="Open navigation"><span class="navbar-toggler-icon" aria-hidden="true"></span></button>
      </div>
    </div>
  </nav>
  <div class="fake-page"><div class="fake-line" style="width:60%"></div><div class="fake-line" style="width:80%"></div><div class="fake-line" style="width:45%"></div></div>
</div>
<p class="demo-note">Resize the window below the <code>lg</code> breakpoint (1024px in v6, up from 992px) to see the drawer take over. Declare the nav <strong>once</strong>, inside <code>.drawer-body</code> &#8212; navbar-expand un-hides it on desktop, so a duplicated desktop list renders twice.</p>"""),

    ("02-menu", "Menu", "Dropdown menus",
     "Dropdown is now Menu. No .dropdown wrapper, no .dropdown-toggle — the toggle and the .menu are siblings, positioned by Floating UI.",
     '<div class="row2"><i></i><i></i><i></i></div><i class="tall"></i><i class="w60"></i><i class="w40"></i>',
     False, """<div class="demo-frame">
  <nav class="navbar lg:navbar-expand" aria-label="Example">
    <div class="container-fluid">
      <a class="navbar-brand fw-semibold" href="#">Kestrel</a>
      <ul class="nav navbar-nav ms-4 me-auto d-none lg:d-flex">
        <li class="nav-item">
          <button class="nav-link" type="button" data-bs-toggle="menu" aria-expanded="false">Product
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 6 5 5 5-5"/></svg>
          </button>
          <div class="menu">
            <a class="menu-item" href="#">Overview</a><a class="menu-item" href="#">Integrations</a>
            <a class="menu-item" href="#">Changelog</a><hr class="menu-divider"><a class="menu-item" href="#">Roadmap</a>
          </div>
        </li>
        <li class="nav-item">
          <button class="nav-link" type="button" data-bs-toggle="menu" data-bs-placement="bottom-end" aria-expanded="false">Resources
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 6 5 5 5-5"/></svg>
          </button>
          <div class="menu">
            <a class="menu-item" href="#">Documentation</a><a class="menu-item" href="#">API reference</a><a class="menu-item" href="#">Community</a>
          </div>
        </li>
      </ul>
      <div class="d-flex gap-2 ms-auto">
        <button class="btn-icon" type="button" data-bs-toggle="menu" aria-expanded="false" aria-label="Account"><span class="avatar avatar-sm"><span class="avatar-initials">PN</span></span></button>
        <div class="menu"><a class="menu-item" href="#">Profile</a><a class="menu-item" href="#">Preferences</a><hr class="menu-divider"><a class="menu-item" href="#">Sign out</a></div>
      </div>
    </div>
  </nav>
  <div class="fake-page"><div class="fake-line" style="width:70%"></div><div class="fake-line" style="width:50%"></div></div>
</div>
<p class="demo-note">Direction is controlled by <code>data-bs-placement</code> rather than <code>.dropup</code> / <code>.dropend</code> wrappers. Events renamed to <code>*.bs.menu</code>, and the JS export is <code>Menu</code>, not <code>Dropdown</code>.</p>"""),

    ("03-overflow", "Overflow", "Nav overflow",
     "New in v6, no equivalent in Bootstrap 5. Items that do not fit fold into a menu automatically as the viewport narrows.",
     '<div class="row2"><i></i><i></i><i></i><i></i><i class="w40"></i></div><i class="tall"></i>',
     False, """<div class="demo-frame">
  <div class="p-3">
    <ul class="nav nav-pills" data-bs-toggle="nav-overflow">
      <li class="nav-item"><a class="nav-link active" aria-current="page" href="#">Overview</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Roadmap</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Releases</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Documents</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Analytics</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Integrations</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Members</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Billing</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Settings</a></li>
    </ul>
  </div>
  <div class="fake-page"><div class="fake-line" style="width:65%"></div><div class="fake-line" style="width:40%"></div></div>
</div>
<p class="demo-note">Narrow the window and watch items collapse into a &#8220;More&#8221; menu. Previously this needed a custom ResizeObserver and a lot of measuring; here it is one attribute.</p>"""),

    ("04-tabs", "Tabs", "Tabs and pills",
     "Tab panels with fade transitions, plus the pill variant. Markup and the JS API are unchanged from v5.",
     '<div class="row2"><i></i><i></i><i></i></div><i class="tall" style="min-height:3rem"></i><i class="w75"></i>',
     False, """<div class="demo-frame p-3">
  <ul class="nav nav-tabs" id="t1" role="tablist">
    <li class="nav-item" role="presentation"><button class="nav-link active" id="t1a" data-bs-toggle="tab" data-bs-target="#t1ap" type="button" role="tab" aria-controls="t1ap" aria-selected="true">Engineering</button></li>
    <li class="nav-item" role="presentation"><button class="nav-link" id="t1b" data-bs-toggle="tab" data-bs-target="#t1bp" type="button" role="tab" aria-controls="t1bp" aria-selected="false">Product</button></li>
    <li class="nav-item" role="presentation"><button class="nav-link" id="t1c" data-bs-toggle="tab" data-bs-target="#t1cp" type="button" role="tab" aria-controls="t1cp" aria-selected="false">Design</button></li>
  </ul>
  <div class="tab-content pt-4">
    <div class="tab-pane fade show active" id="t1ap" role="tabpanel" aria-labelledby="t1a" tabindex="0"><p class="fg-2 mb-0">Cycle time, review latency and carryover, measured from repository events rather than board columns.</p></div>
    <div class="tab-pane fade" id="t1bp" role="tabpanel" aria-labelledby="t1b" tabindex="0"><p class="fg-2 mb-0">Specs link to the work that implements them, so a closed ticket updates the doc describing it.</p></div>
    <div class="tab-pane fade" id="t1cp" role="tabpanel" aria-labelledby="t1c" tabindex="0"><p class="fg-2 mb-0">Frames attach to initiatives and version alongside the release they ship in.</p></div>
  </div>
  <hr class="my-4">
  <ul class="nav nav-pills">
    <li class="nav-item"><a class="nav-link active" aria-current="page" href="#">All</a></li>
    <li class="nav-item"><a class="nav-link" href="#">Open</a></li>
    <li class="nav-item"><a class="nav-link" href="#">Closed</a></li>
    <li class="nav-item"><a class="nav-link disabled" aria-disabled="true">Archived</a></li>
  </ul>
</div>
<p class="demo-note">Tabs are one of the few components v6 left alone &#8212; same markup, same <code>show.bs.tab</code> events.</p>"""),

    ("05-rail", "Rail", "Sidebar rail",
     "A vertical navigation rail for applications. Note .navbar-nav is column by default — navbar-expand is what makes it a row.",
     '<div class="row2"><i class="tall" style="min-height:4rem;max-width:30%"></i><i class="tall" style="min-height:4rem"></i></div>',
     False, """<div class="demo-frame">
  <div class="rail-demo">
    <aside class="rail-side">
      <p class="fw-semibold fs-sm mb-3">Workspace</p>
      <ul class="nav">
        <li class="nav-item"><a class="nav-link active" aria-current="page" href="#">Overview</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Roadmap</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Releases</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Documents</a></li>
      </ul>
      <hr class="my-3">
      <p class="fw-semibold fs-sm mb-3">Account</p>
      <ul class="nav">
        <li class="nav-item"><a class="nav-link" href="#">Members</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Billing</a></li>
        <li class="nav-item"><a class="nav-link" href="#">Settings</a></li>
      </ul>
    </aside>
    <div class="fake-page"><div class="fake-line" style="width:40%"></div><div class="fake-line" style="width:75%"></div><div class="fake-line" style="width:60%"></div><div class="fake-line" style="width:70%"></div></div>
  </div>
</div>
<p class="demo-note">A gotcha worth knowing: <code>.navbar-nav</code> is <code>flex-direction: column</code> by default &#8212; <code>navbar-expand</code> is what turns it into a row. Outside a navbar you either use plain <code>.nav</code> or set the direction yourself.</p>"""),

    ("06-centered", "Centered", "Centered wordmark",
     "Editorial masthead: brand centred with the navigation split either side. Common on magazines and portfolios.",
     '<div class="row2"><i class="w40"></i><i class="w60"></i><i class="w40"></i></div><i class="tall"></i>',
     False, """<div class="demo-frame">
  <div class="p-3" style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:1rem">
    <ul class="nav gap-3" style="flex-direction:row">
      <li class="nav-item"><a class="nav-link" href="#">Work</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Series</a></li>
    </ul>
    <a class="fw-semibold text-decoration-none" href="#" style="letter-spacing:.26em;text-transform:uppercase;color:inherit;padding-inline-start:.26em">Aperture</a>
    <ul class="nav gap-3 justify-content-end" style="flex-direction:row">
      <li class="nav-item"><a class="nav-link" href="#">About</a></li>
      <li class="nav-item"><a class="nav-link" href="#">Contact</a></li>
    </ul>
  </div>
  <div class="fake-page"><div class="fake-line" style="width:55%"></div><div class="fake-line" style="width:80%"></div></div>
</div>
<p class="demo-note">The layout is a three-column grid rather than flex, so the wordmark stays optically centred regardless of how uneven the two link groups are.</p>"""),

    ("07-crumbs", "Breadcrumbs", "Breadcrumbs and pagination",
     "Both changed in v6: links take .breadcrumb-link, and separators are real .breadcrumb-divider elements rather than ::before pseudo-elements.",
     '<div class="row2"><i class="w40"></i><i class="w40"></i><i class="w40"></i></div><i class="tall"></i><div class="row2"><i></i><i></i><i></i></div>',
     False, """<div class="demo-frame p-4">
  <nav aria-label="breadcrumb" class="mb-4">
    <ol class="breadcrumb">
      <li class="breadcrumb-item"><a class="breadcrumb-link" href="#">Home</a></li>
      <li class="breadcrumb-divider">/</li>
      <li class="breadcrumb-item"><a class="breadcrumb-link" href="#">Workspace</a></li>
      <li class="breadcrumb-divider">/</li>
      <li class="breadcrumb-item"><a class="breadcrumb-link" href="#">Releases</a></li>
      <li class="breadcrumb-divider">/</li>
      <li class="breadcrumb-item" aria-current="page"><a class="breadcrumb-link active" href="#">v2.4.0</a></li>
    </ol>
  </nav>
  <div class="fake-page rounded-4 mb-4"><div class="fake-line" style="width:60%"></div><div class="fake-line" style="width:45%"></div></div>
  <nav aria-label="Pages">
    <ul class="pagination mb-0">
      <li class="page-item"><a class="page-link" href="#">Previous</a></li>
      <li class="page-item"><a class="page-link active" aria-current="page" href="#">1</a></li>
      <li class="page-item"><a class="page-link" href="#">2</a></li>
      <li class="page-item"><a class="page-link" href="#">3</a></li>
      <li class="page-item"><a class="page-link" href="#">Next</a></li>
    </ul>
  </nav>
</div>
<p class="demo-note">Because the divider is a real element you can put anything in it &#8212; a slash, a chevron SVG, or nothing at all for a spaced look.</p>"""),

    ("08-scrollspy", "ScrollSpy", "ScrollSpy contents",
     "ScrollSpy was rebuilt on IntersectionObserver. The offset option is gone; use top-margin to clear a sticky header.",
     '<div class="row2"><i class="tall" style="min-height:4rem;max-width:35%"></i><i class="tall" style="min-height:4rem"></i></div>',
     False, """<div class="demo-frame">
  <div class="rail-demo">
    <aside class="rail-side">
      <p class="fw-semibold fs-sm mb-3">On this page</p>
      <nav class="nav" id="spyNav">
        <a class="nav-link" href="#sp1">Introduction</a>
        <a class="nav-link" href="#sp2">Getting started</a>
        <a class="nav-link" href="#sp3">Configuration</a>
        <a class="nav-link" href="#sp4">Troubleshooting</a>
      </nav>
    </aside>
    <div data-bs-spy="scroll" data-bs-target="#spyNav" data-bs-top-margin="10%" data-bs-smooth-scroll="true"
         style="height:22rem;overflow-y:auto;padding:1.5rem">
      <h3 id="sp1" class="fs-lg fw-semibold mb-2">Introduction</h3>
      <p class="fg-2">Scroll this panel and watch the rail on the left follow. Detection is driven by an activation line rather than scroll-position polling, so the highlighted item is the one you are actually reading.</p>
      <p class="fg-2 mb-5">Because it uses IntersectionObserver there is no scroll listener at all.</p>
      <h3 id="sp2" class="fs-lg fw-semibold mb-2">Getting started</h3>
      <p class="fg-2 mb-5">Put <code>data-bs-spy=&quot;scroll&quot;</code> on the scroll container and point <code>data-bs-target</code> at a nav. Only <code>.nav-link</code> elements are activated &#8212; a custom table of contents needs that class or nothing highlights.</p>
      <h3 id="sp3" class="fs-lg fw-semibold mb-2">Configuration</h3>
      <p class="fg-2 mb-5">The deprecated <code>offset</code> and <code>method</code> options were removed. Use <code>top-margin</code> (default 12%) to position the activation line &#8212; for example <code>96px</code> to sit below a sticky header.</p>
      <h3 id="sp4" class="fs-lg fw-semibold mb-2">Troubleshooting</h3>
      <p class="fg-2 mb-0">With <code>smooth-scroll</code> on, clicking a link restores the URL hash and moves focus to the target once the scroll settles, which keyboard and screen-reader users need.</p>
    </div>
  </div>
</div>
<p class="demo-note">Target ids are resolved with <code>getElementById</code>, so ids containing dots, colons or percent-encoding work without manual escaping.</p>"""),
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
