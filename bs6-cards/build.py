#!/usr/bin/env python3
"""
Generates the Bootstrap 6 Cards pack: an index gallery plus one page per variant.

Every variant shares the same chrome (sticky bar with a back link and a colour-mode
toggle) so the pack reads as one product. Ten card patterns covering what real
projects reach for — content, media, horizontal, pricing, profile, metric,
product, article, whole-card link and a responsive grid.

No bundled photography anywhere: media areas are CSS gradients, so the pack has
zero image dependencies and nothing to re-license.
"""

import pathlib

PACK_TITLE = "Bootstrap 6 Cards"
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

TICK = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
        '<path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1m3.2 5.2-4 4a.75.75 0 0 1-1.06 0l-2-2 1.06-1.06L7.67 8.6z"/></svg>')

STAR = ('<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
        '<path d="m8 1.5 1.9 4 4.35.6-3.15 3.05.76 4.35L8 11.45 4.14 13.5l.76-4.35L1.75 6.1 6.1 5.5z"/></svg>')

ARROW_UP = ('<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
            '<path d="m8 3 5 6H3z"/></svg>')

ARROW_DOWN = ('<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
              '<path d="m8 13 5-6H3z"/></svg>')


def spark(values):
    peak = max(values)
    bars = "".join(f'<span style="height:{round(v / peak * 100)}%"></span>' for v in values)
    return f'<div class="spark" role="img" aria-label="Trend over the last twelve weeks">{bars}</div>'


# (folder, nav title, card title, blurb, sketch html, wide?, body html)
VARIANTS = [
    ("01-basic", "Basic", "Content card",
     "Header, body and footer. The shape everything else in this pack is a variation on.",
     '<div class="box"><i class="w60"></i><i></i><i></i><i class="w75"></i><i class="cta"></i></div>',
     False, """<div class="card">
  <div class="card-header">
    <h2 class="fs-lg fw-semibold mb-0">Weekly summary</h2>
  </div>
  <div class="card-body">
    <p class="fg-2 mb-3">
      Eleven issues closed, four opened, and the release went out on Thursday
      without anyone staying late. Deployment time is down to just under six minutes.
    </p>
    <p class="fg-3 fs-sm mb-0">Compiled automatically every Friday at 17:00.</p>
  </div>
  <div class="card-footer d-flex flex-wrap gap-2">
    <button class="btn-solid theme-primary btn-sm" type="button">Open report</button>
    <button class="btn-text btn-sm" type="button">Dismiss</button>
  </div>
</div>"""),

    ("02-media", "Media", "Media card",
     "Image above the body. The media area here is a CSS gradient, so the pack ships with no photography to license.",
     '<div class="box"><i class="media"></i><i class="w60"></i><i></i><i class="w75"></i></div>',
     False, """<div class="card">
  <div class="card-media">Media</div>
  <div class="card-body">
    <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Field notes</p>
    <h2 class="fs-xl fw-semibold mb-2">What we learned shipping on Fridays</h2>
    <p class="fg-2 mb-3">
      We moved releases to Friday morning for six months to see what would break.
      Mostly it was our assumptions about who was on call.
    </p>
    <a class="btn-outline theme-secondary btn-sm" href="#">Read the write-up</a>
  </div>
</div>
<p class="fs-sm fg-3 mt-3 mb-0">
  Swap <code>.card-media</code> for an <code>&lt;img&gt;</code> with
  <code>object-fit: cover</code> and keep the aspect ratio to avoid layout shift.
</p>"""),

    ("03-horizontal", "Horizontal", "Horizontal card",
     "Media beside the body instead of above it, collapsing to stacked below the breakpoint.",
     '<div class="box"><div class="row2"><i class="media" style="flex:0 0 35%"></i><div style="flex:1;display:grid;gap:.3rem"><i class="w75"></i><i></i><i class="w60"></i></div></div></div>',
     True, """<div class="card card-row">
  <div class="card-media">Media</div>
  <div class="card-body">
    <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Case study</p>
    <h2 class="fs-xl fw-semibold mb-2">Kestrel Logistics</h2>
    <p class="fg-2 mb-3">
      Cut their dispatch reconciliation from four hours a day to about twenty
      minutes, mostly by deleting steps rather than automating them.
    </p>
    <div class="d-flex flex-wrap gap-2">
      <span class="badge badge-subtle theme-primary">Logistics</span>
      <span class="badge badge-subtle theme-secondary">8 min read</span>
    </div>
  </div>
</div>
<p class="fs-sm fg-3 mt-3 mb-0">
  Below <code>576px</code> the grid drops to one column, so the media returns to the top.
</p>"""),

    ("04-pricing", "Pricing", "Pricing cards",
     "Three tiers with the middle one marked. The featured card is outlined rather than scaled, so nothing shifts on hover.",
     '<div class="grid3"><div class="box"><i></i><i class="w60"></i><i class="cta" style="width:100%"></i></div><div class="box"><i></i><i class="w60"></i><i class="cta" style="width:100%"></i></div><div class="box"><i></i><i class="w60"></i><i class="cta" style="width:100%"></i></div></div>',
     True, f"""<div class="row g-4">
  <div class="md:col-4">
    <div class="card h-100">
      <div class="card-body d-flex flex-column">
        <p class="fw-semibold mb-1">Starter</p>
        <p class="fg-3 fs-sm mb-4">For one person and a side project.</p>
        <p class="price-figure mb-1">&pound;12<span class="fs-sm fg-3 fw-normal">/mo</span></p>
        <p class="fg-3 fs-xs mb-4">billed annually</p>
        <ul class="price-list fs-sm fg-2 mb-4">
          <li>{TICK} Three projects</li>
          <li>{TICK} 7-day history</li>
          <li>{TICK} Community support</li>
        </ul>
        <button class="btn-outline theme-secondary w-100 mt-auto" type="button">Choose Starter</button>
      </div>
    </div>
  </div>
  <div class="md:col-4">
    <div class="card card-featured h-100">
      <div class="card-body d-flex flex-column">
        <div class="d-flex align-items-center justify-content-between mb-1">
          <p class="fw-semibold mb-0">Team</p>
          <span class="badge badge-subtle theme-primary">Most chosen</span>
        </div>
        <p class="fg-3 fs-sm mb-4">For a team that ships together.</p>
        <p class="price-figure mb-1">&pound;29<span class="fs-sm fg-3 fw-normal">/mo</span></p>
        <p class="fg-3 fs-xs mb-4">billed annually</p>
        <ul class="price-list fs-sm fg-2 mb-4">
          <li>{TICK} Unlimited projects</li>
          <li>{TICK} 90-day history</li>
          <li>{TICK} Custom domains</li>
          <li>{TICK} Priority support</li>
        </ul>
        <button class="btn-solid theme-primary w-100 mt-auto" type="button">Choose Team</button>
      </div>
    </div>
  </div>
  <div class="md:col-4">
    <div class="card h-100">
      <div class="card-body d-flex flex-column">
        <p class="fw-semibold mb-1">Scale</p>
        <p class="fg-3 fs-sm mb-4">When procurement gets involved.</p>
        <p class="price-figure mb-1">&pound;79<span class="fs-sm fg-3 fw-normal">/mo</span></p>
        <p class="fg-3 fs-xs mb-4">billed annually</p>
        <ul class="price-list fs-sm fg-2 mb-4">
          <li>{TICK} Everything in Team</li>
          <li>{TICK} SSO &amp; SCIM</li>
          <li>{TICK} Audit log</li>
          <li>{TICK} 99.9% SLA</li>
        </ul>
        <button class="btn-outline theme-secondary w-100 mt-auto" type="button">Talk to sales</button>
      </div>
    </div>
  </div>
</div>"""),

    ("05-profile", "Profile", "Profile card",
     "Avatar, role and contact actions. Uses the v6 Avatar component rather than a bare rounded image.",
     '<div class="box"><div class="row2" style="align-items:center"><i class="dot"></i><div style="flex:1;display:grid;gap:.3rem"><i class="w75"></i><i class="w40"></i></div></div><i></i><i class="w60"></i><div class="row2"><i class="cta" style="width:100%"></i><i class="cta" style="width:100%;background:transparent;border:1px solid currentColor;opacity:.3"></i></div></div>',
     False, """<div class="card">
  <div class="card-body">
    <div class="d-flex align-items-center gap-3 mb-4">
      <span class="avatar avatar-lg"><span class="avatar-initials">AN</span></span>
      <div>
        <h2 class="fs-lg fw-semibold mb-0">Adaeze Nwosu</h2>
        <p class="fg-3 fs-sm mb-0">Principal engineer &middot; Platform</p>
      </div>
      <span class="badge badge-subtle theme-success ms-auto">Available</span>
    </div>
    <p class="fg-2 fs-sm mb-4">
      Works on the deployment pipeline and the bits of the API nobody else wants
      to touch. Mentors two of the graduate intake.
    </p>
    <div class="d-flex flex-wrap gap-2 mb-4">
      <span class="chip">Go</span>
      <span class="chip">Postgres</span>
      <span class="chip">Terraform</span>
    </div>
    <div class="d-flex flex-wrap gap-2">
      <button class="btn-solid theme-primary btn-sm" type="button">Message</button>
      <button class="btn-outline theme-secondary btn-sm" type="button">View profile</button>
    </div>
  </div>
</div>"""),

    ("06-metric", "Metric", "Metric cards",
     "Dashboard tiles with a figure, a direction-of-travel delta and a CSS sparkline &#8212; no chart library.",
     '<div class="grid2"><div class="box"><i class="w40"></i><i class="tall"></i><i class="w60"></i></div><div class="box"><i class="w40"></i><i class="tall"></i><i class="w60"></i></div></div>',
     True, f"""<div class="row g-4">
  <div class="sm:col-6 lg:col-3">
    <div class="card h-100"><div class="card-body">
      <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Revenue</p>
      <p class="metric-figure mb-1">&pound;48.2k</p>
      <p class="metric-delta metric-up mb-3">{ARROW_UP} 12.4% vs last month</p>
      {spark([12, 15, 13, 18, 17, 21, 19, 24, 22, 27, 26, 31])}
    </div></div>
  </div>
  <div class="sm:col-6 lg:col-3">
    <div class="card h-100"><div class="card-body">
      <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Active users</p>
      <p class="metric-figure mb-1">3,918</p>
      <p class="metric-delta metric-up mb-3">{ARROW_UP} 4.1% vs last month</p>
      {spark([20, 21, 19, 22, 24, 23, 26, 25, 28, 27, 30, 31])}
    </div></div>
  </div>
  <div class="sm:col-6 lg:col-3">
    <div class="card h-100"><div class="card-body">
      <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Churn</p>
      <p class="metric-figure mb-1">2.1%</p>
      <p class="metric-delta metric-down mb-3">{ARROW_DOWN} 0.4pp vs last month</p>
      {spark([31, 29, 30, 27, 28, 25, 24, 22, 23, 20, 18, 17])}
    </div></div>
  </div>
  <div class="sm:col-6 lg:col-3">
    <div class="card h-100"><div class="card-body">
      <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Avg. deploy</p>
      <p class="metric-figure mb-1">5m 48s</p>
      <p class="metric-delta metric-up mb-3">{ARROW_UP} 38s faster</p>
      {spark([30, 28, 29, 26, 24, 25, 22, 20, 21, 18, 17, 15])}
    </div></div>
  </div>
</div>
<p class="fs-sm fg-3 mt-4 mb-0">
  The sparkline is a flex row of <code>&lt;span&gt;</code> elements with percentage
  heights, labelled with <code>role="img"</code> so it is not read as noise.
</p>"""),

    ("07-product", "Product", "Product card",
     "Commerce shape &#8212; media, sale badge, rating, struck-through was-price and an add-to-basket action.",
     '<div class="box"><i class="media"></i><i class="w75"></i><div class="row2"><i class="w40"></i><i class="w40"></i></div><i class="cta" style="width:100%"></i></div>',
     True, f"""<div class="row g-4">
  <div class="sm:col-6 lg:col-4">
    <div class="card h-100">
      <div class="position-relative">
        <div class="card-media card-media-sq">Product</div>
        <span class="badge theme-danger position-absolute" style="top:.75rem;left:.75rem">&minus;20%</span>
      </div>
      <div class="card-body d-flex flex-column">
        <p class="fs-xs fg-3 mb-1">Kitchen</p>
        <h2 class="fs-lg fw-semibold mb-2">Hammered copper kettle</h2>
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="stars" role="img" aria-label="Rated 4.5 out of 5">{STAR}{STAR}{STAR}{STAR}{STAR}</span>
          <span class="fs-xs fg-3">4.5 (128)</span>
        </div>
        <p class="mb-3">
          <span class="product-price fs-lg">&pound;68.00</span>
          <span class="product-was fs-sm ms-2">&pound;85.00</span>
        </p>
        <button class="btn-solid theme-primary w-100 mt-auto" type="button">Add to basket</button>
      </div>
    </div>
  </div>
  <div class="sm:col-6 lg:col-4">
    <div class="card h-100">
      <div class="card-media card-media-sq">Product</div>
      <div class="card-body d-flex flex-column">
        <p class="fs-xs fg-3 mb-1">Textiles</p>
        <h2 class="fs-lg fw-semibold mb-2">Washed linen throw</h2>
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="stars" role="img" aria-label="Rated 4.8 out of 5">{STAR}{STAR}{STAR}{STAR}{STAR}</span>
          <span class="fs-xs fg-3">4.8 (64)</span>
        </div>
        <p class="mb-3"><span class="product-price fs-lg">&pound;120.00</span></p>
        <button class="btn-solid theme-primary w-100 mt-auto" type="button">Add to basket</button>
      </div>
    </div>
  </div>
  <div class="sm:col-6 lg:col-4">
    <div class="card h-100">
      <div class="position-relative">
        <div class="card-media card-media-sq">Product</div>
        <span class="badge theme-secondary position-absolute" style="top:.75rem;left:.75rem">Sold out</span>
      </div>
      <div class="card-body d-flex flex-column">
        <p class="fs-xs fg-3 mb-1">Tableware</p>
        <h2 class="fs-lg fw-semibold mb-2">Stoneware serving bowl</h2>
        <div class="d-flex align-items-center gap-2 mb-3">
          <span class="stars" role="img" aria-label="Rated 4.2 out of 5">{STAR}{STAR}{STAR}{STAR}</span>
          <span class="fs-xs fg-3">4.2 (39)</span>
        </div>
        <p class="mb-3"><span class="product-price fs-lg fg-3">&pound;42.00</span></p>
        <button class="btn-outline theme-secondary w-100 mt-auto" type="button" disabled>Notify me</button>
      </div>
    </div>
  </div>
</div>"""),

    ("08-article", "Article", "Article card",
     "Editorial shape with a kicker, author row and reading time. Meta goes in the footer so cards in a row stay aligned.",
     '<div class="box"><i class="media"></i><i class="w40"></i><i class="w75"></i><i></i><div class="row2" style="align-items:center"><i class="dot" style="height:1rem;width:1rem"></i><i class="w60"></i></div></div>',
     True, """<div class="row g-4">
  <div class="md:col-6">
    <article class="card h-100">
      <div class="card-media">Cover</div>
      <div class="card-body">
        <p class="fs-xs fg-primary text-uppercase mb-2" style="letter-spacing:.12em">Engineering</p>
        <h2 class="fs-xl fw-semibold mb-2">The migration we did not need to do</h2>
        <p class="fg-2 fs-sm mb-0">
          Eight months of planning, three of execution, and a retrospective that
          concluded the original system would have been fine for another four years.
        </p>
      </div>
      <div class="card-footer d-flex align-items-center gap-2">
        <span class="avatar avatar-sm"><span class="avatar-initials">ML</span></span>
        <span class="fs-sm">Marcus L.</span>
        <span class="fs-xs fg-3 ms-auto">14 Jul &middot; 11 min</span>
      </div>
    </article>
  </div>
  <div class="md:col-6">
    <article class="card h-100">
      <div class="card-media">Cover</div>
      <div class="card-body">
        <p class="fs-xs fg-primary text-uppercase mb-2" style="letter-spacing:.12em">Design</p>
        <h2 class="fs-xl fw-semibold mb-2">Nobody reads the empty state, so write it anyway</h2>
        <p class="fg-2 fs-sm mb-0">
          Empty states are the only screen guaranteed to be seen by every new user,
          and they are almost always written last by whoever is left.
        </p>
      </div>
      <div class="card-footer d-flex align-items-center gap-2">
        <span class="avatar avatar-sm"><span class="avatar-initials">DR</span></span>
        <span class="fs-sm">Dana R.</span>
        <span class="fs-xs fg-3 ms-auto">2 Jul &middot; 6 min</span>
      </div>
    </article>
  </div>
</div>"""),

    ("09-linked", "Whole-card link", "Clickable card",
     "The entire surface is clickable, but only the title is in the tab order &#8212; one link, stretched with a pseudo-element.",
     '<div class="box"><i class="w60"></i><i></i><i class="w75"></i><i class="w40"></i></div>',
     True, """<div class="row g-4">
  <div class="md:col-6">
    <div class="card card-linked h-100">
      <div class="card-body">
        <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Documentation</p>
        <h2 class="fs-lg fw-semibold mb-2">
          <a class="stretched-title" href="#" style="color:inherit;text-decoration:none">Getting started with the API</a>
        </h2>
        <p class="fg-2 fs-sm mb-0">Authentication, your first request, and the three mistakes everyone makes on day one.</p>
      </div>
    </div>
  </div>
  <div class="md:col-6">
    <div class="card card-linked h-100">
      <div class="card-body">
        <p class="fs-xs fg-3 text-uppercase mb-2" style="letter-spacing:.12em">Documentation</p>
        <h2 class="fs-lg fw-semibold mb-2">
          <a class="stretched-title" href="#" style="color:inherit;text-decoration:none">Webhooks and retries</a>
        </h2>
        <p class="fg-2 fs-sm mb-0">Delivery guarantees, signature verification and what happens when your endpoint is down.</p>
      </div>
    </div>
  </div>
</div>
<p class="fs-sm fg-3 mt-4 mb-0">
  Wrapping the whole card in an anchor would swallow any button inside it and
  read the entire card as one enormous link name. Stretching a single title link
  with <code>::after</code> keeps the accessible name short and leaves room for
  other controls.
</p>"""),

    ("10-grid", "Grid", "Responsive card grid",
     "Cards in an auto-filling grid that reflows without breakpoint classes &#8212; <code>repeat(auto-fill, minmax())</code> doing the work.",
     '<div class="grid3"><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i><i class="tall"></i></div>',
     True, """<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Card grid</h1>
<p class="fg-2 mb-4">No column classes. The grid decides how many fit and reflows as the window changes.</p>
<div class="card-grid">
  <div class="card"><div class="card-body">
    <span class="badge badge-subtle theme-primary mb-3">Guide</span>
    <h2 class="fs-lg fw-semibold mb-2">Deploying to production</h2>
    <p class="fg-2 fs-sm mb-0">Environments, secrets and the rollback you hope never to use.</p>
  </div></div>
  <div class="card"><div class="card-body">
    <span class="badge badge-subtle theme-success mb-3">Tutorial</span>
    <h2 class="fs-lg fw-semibold mb-2">Your first integration</h2>
    <p class="fg-2 fs-sm mb-0">Forty minutes end to end, assuming the credentials arrive on time.</p>
  </div></div>
  <div class="card"><div class="card-body">
    <span class="badge badge-subtle theme-warning mb-3">Reference</span>
    <h2 class="fs-lg fw-semibold mb-2">Rate limits</h2>
    <p class="fg-2 fs-sm mb-0">What the headers mean and how to back off politely.</p>
  </div></div>
  <div class="card"><div class="card-body">
    <span class="badge badge-subtle theme-secondary mb-3">Concept</span>
    <h2 class="fs-lg fw-semibold mb-2">Idempotency keys</h2>
    <p class="fg-2 fs-sm mb-0">Why retrying a payment twice should only charge once.</p>
  </div></div>
  <div class="card"><div class="card-body">
    <span class="badge badge-subtle theme-danger mb-3">Troubleshooting</span>
    <h2 class="fs-lg fw-semibold mb-2">Common 4xx responses</h2>
    <p class="fg-2 fs-sm mb-0">Each one, what causes it, and the fix that usually works.</p>
  </div></div>
  <div class="card"><div class="card-body">
    <span class="badge badge-subtle theme-primary mb-3">Guide</span>
    <h2 class="fs-lg fw-semibold mb-2">Migrating from v1</h2>
    <p class="fg-2 fs-sm mb-0">Breaking changes, the compatibility shim and the deprecation dates.</p>
  </div></div>
</div>"""),
]


def write_variant(i, folder, nav, card, blurb, sketch, wide, body):
    prev_i = (i - 1) % len(VARIANTS)
    next_i = (i + 1) % len(VARIANTS)
    html = HEAD.format(
        title=f"{card} — {PACK_TITLE}",
        desc=f"{blurb} A free Bootstrap 6 card example.".replace("<code>", "").replace("</code>", ""),
        p="../")
    html += f"""
<div class="variant-bar">
  <a class="btn-text btn-sm" href="../index.html">&#8592; All cards</a>
  <span class="fs-sm fw-semibold ms-2">{card}</span>
  <span class="fs-xs fg-3 d-none md:d-inline">{i + 1} of {len(VARIANTS)}</span>
  <div class="d-flex align-items-center gap-2 ms-auto">
    <a class="btn-icon btn-sm" href="../{VARIANTS[prev_i][0]}/index.html" aria-label="Previous card">&#8249;</a>
    <a class="btn-icon btn-sm" href="../{VARIANTS[next_i][0]}/index.html" aria-label="Next card">&#8250;</a>
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
        title=f"{PACK_TITLE} — 10 Free Bootstrap 6 Card Templates",
        desc="Ten free Bootstrap 6 card templates — content, media, horizontal, pricing, profile, metric with sparkline, product, article, whole-card link and a responsive auto-fill grid. No images to license, no build step.",
        p="")
    html += f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#cards">Skip to the cards</a>

<div class="pack-head">
  <div class="container">
    <div class="d-flex flex-wrap align-items-start gap-3">
      <div class="me-auto" style="max-width:44rem">
        <span class="badge badge-subtle theme-primary mb-3">Bootstrap 6.0.0-alpha1</span>
        <h1 class="fs-4xl fw-bold mb-3" style="letter-spacing:-.03em">{PACK_TITLE}</h1>
        <p class="fs-lg fg-2 mb-0">
          Ten card patterns covering what projects actually reach for &#8212; content,
          media, horizontal, pricing, profile, dashboard metrics, product, article,
          whole-card links and a grid that reflows without breakpoint classes.
          Every media area is a CSS gradient, so there is no photography to license.
        </p>
      </div>
      {TOGGLE}
    </div>
  </div>
</div>

<main id="cards" class="section">
  <div class="container">
    <div class="pack-grid">
{chr(10).join(cards)}
    </div>

    <section class="mt-9" style="max-width:46rem">
      <h2 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">Using these</h2>
      <div class="prose">
        <p>Each card is a standalone page. Copy the markup out of the one you want
        and drop it in &#8212; every variant needs only Bootstrap 6&#8217;s CSS. The only
        JavaScript in this pack is the shared colour-mode toggle.</p>

        <h3>Making a whole card clickable</h3>
        <p>Do not wrap the card in an anchor. It swallows any button inside it and
        gives the link an accessible name made of the entire card&#8217;s text. Put one
        link on the title and stretch it with a pseudo-element instead &#8212; the whole
        surface becomes clickable, the tab order stays sane, and the link is
        announced as its title.</p>

        <h3>Equal heights</h3>
        <p><code>h-100</code> on the card plus <code>d-flex flex-column</code> on the
        body, then <code>mt-auto</code> on the action. That pins buttons to the
        bottom so a row of cards with different amounts of copy still lines up.</p>

        <h3>Media</h3>
        <p>Give the media area a fixed <code>aspect-ratio</code> and use
        <code>object-fit: cover</code> on real images. Without it the card resizes
        as each image decodes, which is most of the layout shift on a typical
        card grid.</p>

        <h3>Grids</h3>
        <p>The last variant uses
        <code>repeat(auto-fill, minmax(17rem, 1fr))</code> rather than column
        classes. It reflows at whatever width the content needs instead of at
        breakpoints you picked in advance, which matters when a card grid sits
        inside a sidebar layout.</p>
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
