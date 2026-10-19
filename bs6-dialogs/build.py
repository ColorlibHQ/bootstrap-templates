#!/usr/bin/env python3
"""
Generates the Bootstrap 6 Dialogs & Drawers pack.

v6 rebuilt this whole area: Modal became Dialog and Offcanvas became Drawer, and
both are now native <dialog> elements rather than divs with a backdrop faked
underneath. That brings the top layer, real focus trapping and Escape handling
for free — and it brings a few things v5 simply could not do, which is what most
of these ten variants are about.
"""

import pathlib

PACK_TITLE = "Bootstrap 6 Dialogs & Drawers"
ROOT = pathlib.Path(__file__).parent

HEAD = """<!doctype html>
<html lang="en" data-bs-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
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

FILLER = """<div class="filler fg-2">
    <p>Bootstrap 6 renders dialogs and drawers as native <code>&lt;dialog&gt;</code>
    elements. That means the browser puts them in the top layer, so they sit above
    every stacking context on the page without a z-index arms race.</p>
    <p>It also means focus is trapped for you, Escape closes by default, and the
    rest of the page is inert while the dialog is open — three things that took a
    surprising amount of JavaScript in v5.</p>
    <p>The trade is that the markup must actually be a <code>&lt;dialog&gt;</code>.
    A div with <code>class="dialog"</code> will style correctly and then never
    open, which is the single most common mistake when porting from v5.</p>
    <p>Drawers are the same element with a different class. There is no separate
    offcanvas component any more, and no separate JavaScript for it either.</p>
</div>"""


def dlg(id_, title, body, *, cls="", footer=None, static=False, nonmodal=False):
    extra = f" {cls}" if cls else ""
    attrs = ' data-bs-static="true"' if static else ""
    # .dialog-nonmodal is a STYLE class only — it drops the backdrop and nothing
    # else. Whether the browser calls show() or showModal() comes from the
    # `modal` config option, so the behaviour needs data-bs-modal="false" as
    # well. Typed boolean, so the value has to be written out.
    if nonmodal:
        attrs += ' data-bs-modal="false"'
    foot = footer if footer is not None else (
        '<button type="button" class="btn-text" data-bs-dismiss="dialog">Close</button>'
        '<button type="button" class="btn-solid theme-primary" data-bs-dismiss="dialog">Save changes</button>')
    return f"""<dialog class="dialog{extra}" id="{id_}" aria-labelledby="{id_}Label"{attrs}>
  <div class="dialog-header">
    <h2 class="dialog-title fs-lg" id="{id_}Label">{title}</h2>
    <button type="button" class="btn-close" data-bs-dismiss="dialog" aria-label="Close"></button>
  </div>
  <div class="dialog-body">
    {body}
  </div>
  <div class="dialog-footer">
    {foot}
  </div>
</dialog>"""


def drw(id_, title, body, *, cls="drawer-end"):
    return f"""<dialog class="drawer {cls}" id="{id_}" aria-labelledby="{id_}Label">
  <div class="drawer-header">
    <h2 class="drawer-title fs-lg" id="{id_}Label">{title}</h2>
    <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
  </div>
  <div class="drawer-body">
    {body}
  </div>
</dialog>"""


def trig(target, label, kind="dialog", style="btn-outline theme-secondary"):
    return (f'<button class="{style}" type="button" data-bs-toggle="{kind}" '
            f'data-bs-target="#{target}">{label}</button>')


# (folder, nav, card title, blurb, sketch, wide?, body)
VARIANTS = [
    ("01-basic", "Basic", "Basic dialog",
     "The default. A native <code>&lt;dialog&gt;</code> with header, body and footer — focus trapping and Escape come from the browser.",
     '<div class="page"><i></i><i class="w60"></i><i></i><div class="panel p-centre"><i></i><i class="mute"></i><i class="w60 mute"></i></div></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Basic dialog</h1>
<p class="fg-2 mb-4">Everything else in this pack is a variation on this markup.</p>
<div class="trigger-grid mb-4">
  {trig("dlgBasic", "Open dialog", style="btn-solid theme-primary")}
</div>
<div class="note fs-sm">
  <p class="mb-0"><strong>The element must be a <code>&lt;dialog&gt;</code>.</strong>
  A <code>&lt;div class="dialog"&gt;</code> styles perfectly and then never opens —
  the most common mistake when porting a v5 modal.</p>
</div>
{dlg("dlgBasic", "Publish this release", "<p class='fg-2 mb-0'>This will make version 4.2 available to everyone on the stable channel. You can roll it back for up to 24 hours.</p>")}"""),

    ("02-scrollable", "Scrollable", "Scrollable dialog",
     "<code>.dialog-scrollable</code> keeps the header and footer fixed while only the body scrolls, so the actions never leave the screen.",
     '<div class="page"><i></i><i class="w60"></i><div class="panel p-tall"><i></i><i class="mute"></i><i class="mute"></i><i class="mute"></i><i class="w60"></i></div></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Scrollable dialog</h1>
<p class="fg-2 mb-4">Long content, fixed actions. Compare with the basic dialog, where the whole box grows.</p>
<div class="trigger-grid mb-4">
  {trig("dlgScroll", "Open scrollable", style="btn-solid theme-primary")}
  {trig("dlgUnscroll", "Open non-scrollable")}
</div>
<div class="note fs-sm">
  <p class="mb-0">Without <code>.dialog-scrollable</code> the dialog grows and the
  page behind it scrolls instead — which on a phone usually means the confirm
  button is somewhere below the fold.</p>
</div>
{dlg("dlgScroll", "Terms of service", FILLER + FILLER, cls="dialog-scrollable dialog-lg")}
{dlg("dlgUnscroll", "Terms of service", FILLER, cls="dialog-lg")}"""),

    ("03-sizes", "Sizes", "Sizes &amp; fullscreen",
     "<code>.dialog-sm</code> through <code>.dialog-xl</code>, plus <code>.dialog-fullscreen</code> for the takeover pattern.",
     '<div class="page"><i></i><i class="w60"></i><div class="panel p-small"><i></i><i class="mute"></i></div></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Sizes</h1>
<p class="fg-2 mb-4">Four widths and a fullscreen takeover.</p>
<div class="trigger-grid mb-4">
  {trig("dlgSm", "Small")}
  {trig("dlgMd", "Default")}
  {trig("dlgLg", "Large")}
  {trig("dlgXl", "Extra large")}
  {trig("dlgFull", "Fullscreen", style="btn-solid theme-primary")}
</div>
<div class="note fs-sm">
  <p class="mb-0">Fullscreen is the right call for anything that is really a page
  in disguise — an editor, a media picker, a multi-step flow. If a visitor could
  reasonably want to deep-link to it, it should be a route instead.</p>
</div>
{dlg("dlgSm", "Small", "<p class='fg-2 mb-0'>Good for a single confirmation.</p>", cls="dialog-sm")}
{dlg("dlgMd", "Default", "<p class='fg-2 mb-0'>The default width suits most content.</p>")}
{dlg("dlgLg", "Large", "<p class='fg-2 mb-0'>Room for a form in two columns.</p>", cls="dialog-lg")}
{dlg("dlgXl", "Extra large", "<p class='fg-2 mb-0'>For tables and side-by-side comparisons.</p>", cls="dialog-xl")}
{dlg("dlgFull", "Fullscreen", FILLER, cls="dialog-fullscreen")}"""),

    ("04-form", "Form", "Form dialog",
     "A form inside a dialog, submitted from the footer using <code>form=</code> so the button can live outside the form element.",
     '<div class="page"><i></i><div class="panel p-centre"><i class="mute"></i><i></i><i class="mute"></i><i class="w40"></i></div></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Form dialog</h1>
<p class="fg-2 mb-4">The submit button sits in the footer, outside the form, wired up with <code>form="…"</code>.</p>
<div class="trigger-grid mb-4">
  {trig("dlgForm", "Invite a teammate", style="btn-solid theme-primary")}
</div>
<div class="note fs-sm">
  <p class="mb-0">Keep <code>novalidate</code> plus <code>data-bs-validate</code>
  on the form. v6 dropped <code>.needs-validation</code> and
  <code>.was-validated</code> in favour of native <code>:user-invalid</code>, so
  errors only appear once someone has actually interacted with a field.</p>
</div>
<dialog class="dialog" id="dlgForm" aria-labelledby="dlgFormLabel">
  <div class="dialog-header">
    <h2 class="dialog-title fs-lg" id="dlgFormLabel">Invite a teammate</h2>
    <button type="button" class="btn-close" data-bs-dismiss="dialog" aria-label="Close"></button>
  </div>
  <form class="dialog-body vstack gap-3" id="inviteForm" data-demo-form data-bs-validate novalidate>
    <div class="form-field">
      <label class="form-label" for="invEmail">Email address</label>
      <input type="email" class="form-control" id="invEmail" required>
      <div class="invalid-feedback">A valid work email, please.</div>
    </div>
    <div class="form-field">
      <label class="form-label" for="invRole">Role</label>
      <select class="form-select" id="invRole">
        <option>Viewer</option>
        <option selected>Editor</option>
        <option>Admin</option>
      </select>
    </div>
    <div class="form-field">
      <div class="switch"><input type="checkbox" id="invNotify" role="switch" switch checked></div>
      <label for="invNotify">Email them an invitation now</label>
    </div>
  </form>
  <div class="dialog-footer">
    <button type="button" class="btn-text" data-bs-dismiss="dialog">Cancel</button>
    <button type="submit" form="inviteForm" class="btn-solid theme-primary" data-done-text="Invited &#10003;">Send invite</button>
  </div>
</dialog>"""),

    ("05-confirm", "Confirm", "Destructive confirm",
     "<code>data-bs-static</code> stops a backdrop click dismissing it, so a destructive action needs a deliberate answer.",
     '<div class="page"><i></i><i class="w60"></i><div class="panel p-small"><i></i><i class="mute"></i></div></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Destructive confirm</h1>
<p class="fg-2 mb-4">Try clicking the backdrop on the static one — it stays put.</p>
<div class="trigger-grid mb-4">
  {trig("dlgDanger", "Delete project", style="btn-solid theme-danger")}
  {trig("dlgSoft", "Dismissible version")}
</div>
<div class="note fs-sm">
  <p class="mb-0">Static is for irreversible actions only. Using it everywhere
  just trains people to hunt for the close button, and Escape still works
  regardless — the browser owns that.</p>
</div>
{dlg("dlgDanger", "Delete this project?", "<p class='fg-2 mb-2'>This removes <strong>Kestrel Logistics</strong> and all 1,284 of its records.</p><p class='fg-3 fs-sm mb-0'>This cannot be undone.</p>", cls="dialog-sm", static=True, footer='<button type="button" class="btn-text" data-bs-dismiss="dialog">Keep it</button><button type="button" class="btn-solid theme-danger" data-bs-dismiss="dialog">Delete permanently</button>')}
{dlg("dlgSoft", "Discard changes?", "<p class='fg-2 mb-0'>Your edits since 14:20 will be lost.</p>", cls="dialog-sm", footer='<button type="button" class="btn-text" data-bs-dismiss="dialog">Keep editing</button><button type="button" class="btn-solid theme-primary" data-bs-dismiss="dialog">Discard</button>')}"""),

    ("06-nonmodal", "Non-modal", "Non-modal dialog",
     "<code>.dialog-nonmodal</code> has no backdrop and leaves the page usable underneath — impossible with a v5 modal.",
     '<div class="page"><i></i><i class="w60"></i><i></i><div class="panel p-corner"><i></i><i class="mute"></i></div></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Non-modal dialog</h1>
<p class="fg-2 mb-4">
  Open it, then keep typing in the field below. The page stays live — no backdrop,
  no inert content, no focus trap.
</p>
<div class="trigger-grid mb-4">
  {trig("dlgNon", "Open helper panel", style="btn-solid theme-primary")}
</div>
<div class="form-field mb-4" style="max-width:26rem">
  <label class="form-label" for="nmProof">Type here while it is open</label>
  <input type="text" class="form-control" id="nmProof" placeholder="Still works&#8230;">
</div>
<div class="note fs-sm">
  <p class="mb-2">Good for inspectors, live help and anything a person needs
  alongside their work rather than instead of it. In v5 this required building a
  floating panel by hand, because a modal always blocked the page.</p>
  <p class="mb-0"><strong>Two things are needed, not one.</strong>
  <code>.dialog-nonmodal</code> is a style class — it removes the backdrop and
  nothing more. Whether the browser calls <code>show()</code> or
  <code>showModal()</code> comes from the <code>modal</code> option, so you also
  need <code>data-bs-modal="false"</code>. With only the class you get a dialog
  that looks non-modal and still blocks the page.</p>
</div>
{dlg("dlgNon", "Formatting help", "<p class='fg-2 mb-2'>Use <code>**bold**</code>, <code>_italic_</code> and <code>`code`</code>.</p><p class='fg-2 mb-0'>Two blank lines start a new paragraph.</p>", cls="dialog-nonmodal dialog-sm", nonmodal=True, footer='<button type="button" class="btn-text" data-bs-dismiss="dialog">Close</button>')}"""),

    ("07-drawer-sides", "Drawer sides", "Drawers, four sides",
     "<code>.drawer-start</code>, <code>-end</code>, <code>-top</code> and <code>-bottom</code>. Offcanvas is gone; a drawer is a <code>&lt;dialog&gt;</code> too.",
     '<div class="page"><i></i><i class="w60"></i><div class="panel p-end"><i></i><i class="mute"></i><i class="mute"></i></div></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Drawers</h1>
<p class="fg-2 mb-4">Same element, same JavaScript, four positions.</p>
<div class="trigger-grid mb-4">
  {trig("drwStart", "From the start", "drawer")}
  {trig("drwEnd", "From the end", "drawer", "btn-solid theme-primary")}
  {trig("drwTop", "From the top", "drawer")}
  {trig("drwBottom", "From the bottom", "drawer")}
</div>
<div class="note fs-sm">
  <p class="mb-0"><strong>A drawer must also be a <code>&lt;dialog&gt;</code>.</strong>
  Porting an offcanvas div across is the second most common v5 mistake — and if
  you leave it as a div inside a <code>navbar-expand</code> ancestor, its contents
  render inline on desktop instead of staying hidden.</p>
</div>
{drw("drwStart", "Filters", "<p class='fg-2 mb-0'>Faceted filters usually belong on the start edge, near the results they modify.</p>", cls="drawer-start")}
{drw("drwEnd", "Basket", "<p class='fg-2 mb-0'>Baskets, notifications and detail panels read better from the end edge.</p>", cls="drawer-end")}
{drw("drwTop", "Announcement", "<p class='fg-2 mb-0'>Top drawers suit site-wide notices. Use them sparingly.</p>", cls="drawer-top")}
{drw("drwBottom", "Quick actions", "<p class='fg-2 mb-0'>Bottom is the natural place on a phone — it is where thumbs are.</p>", cls="drawer-bottom")}"""),

    ("08-sheet", "Bottom sheet", "Bottom sheet",
     "<code>.drawer-sheet</code> with <code>.drawer-fit-content</code> — the mobile sheet pattern, sized to its content.",
     '<div class="page"><i></i><i class="w60"></i><i></i><div class="panel p-bottom"><i class="w40"></i><i class="mute"></i><i class="mute"></i></div></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Bottom sheet</h1>
<p class="fg-2 mb-4">Rounded top corners, sized to its content rather than the viewport.</p>
<div class="trigger-grid mb-4">
  {trig("drwSheet", "Open sheet", "drawer", "btn-solid theme-primary")}
  {trig("drwSheetTall", "Taller sheet", "drawer")}
</div>
<div class="note fs-sm">
  <p class="mb-0"><code>.drawer-fit-content</code> stops a short sheet stretching
  to full height. Pair it with <code>.drawer-sheet</code> for the rounded top
  edge that signals the thing is draggable-looking even though it is not.</p>
</div>
{drw("drwSheet", "Share", "<div class='d-grid gap-2'><button class='btn-outline theme-secondary' type='button'>Copy link</button><button class='btn-outline theme-secondary' type='button'>Email</button><button class='btn-outline theme-secondary' type='button'>Export as PDF</button></div>", cls="drawer-bottom drawer-sheet drawer-fit-content")}
{drw("drwSheetTall", "Choose a plan", FILLER, cls="drawer-bottom drawer-sheet")}"""),

    ("09-toasts", "Toasts", "Toasts",
     "Stacked notifications in a <code>.toast-container</code>, including the translucent variant. Markup plus a class, no component to construct.",
     '<div class="page"><i></i><i class="w60"></i><i></i><div class="panel p-corner"><i class="w60"></i><i class="mute"></i></div></div>',
     True, """<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Toasts</h1>
<p class="fg-2 mb-4">Non-blocking confirmations. They auto-dismiss after four seconds here.</p>
<div class="trigger-grid mb-4">
  <button class="btn-solid theme-primary" type="button" data-toast-show="toastSaved">Show success</button>
  <button class="btn-outline theme-secondary" type="button" data-toast-show="toastWarn">Show warning</button>
  <button class="btn-outline theme-secondary" type="button" data-toast-show="toastGlass">Show translucent</button>
</div>
<div class="note fs-sm">
  <p class="mb-0">Toasts are for things the person does not need to act on. If a
  decision is required, it is a dialog — a toast that disappears while someone is
  reading it is worse than no toast at all.</p>
</div>

<div class="toast-container" style="position:fixed;bottom:1rem;right:1rem;z-index:1090">
  <div class="toast mb-2" id="toastSaved" role="status" hidden>
    <div class="toast-header">
      <strong class="me-auto">Saved</strong>
      <button type="button" class="btn-close" data-toast-dismiss aria-label="Close"></button>
    </div>
    <div class="toast-body">Your changes were saved to the draft.</div>
  </div>
  <div class="toast mb-2" id="toastWarn" role="status" hidden>
    <div class="toast-header">
      <strong class="me-auto">Heads up</strong>
      <button type="button" class="btn-close" data-toast-dismiss aria-label="Close"></button>
    </div>
    <div class="toast-body">Two collaborators are editing this page right now.</div>
  </div>
  <div class="toast toast-translucent" id="toastGlass" role="status" hidden>
    <div class="toast-header">
      <strong class="me-auto">Translucent</strong>
      <button type="button" class="btn-close" data-toast-dismiss aria-label="Close"></button>
    </div>
    <div class="toast-body">Uses <code>.toast-translucent</code> for a blurred backdrop.</div>
  </div>
</div>"""),

    ("10-motion", "Motion", "Entry animations",
     "<code>.dialog-slide-up</code>, <code>.dialog-slide-down</code> and <code>.dialog-instant</code> — and why the last one matters.",
     '<div class="page"><i></i><i class="w60"></i><div class="panel p-centre"><i></i><i class="mute"></i></div></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Entry animations</h1>
<p class="fg-2 mb-4">Three entrances, plus the escape hatch.</p>
<div class="trigger-grid mb-4">
  {trig("dlgUp", "Slide up", style="btn-solid theme-primary")}
  {trig("dlgDown", "Slide down")}
  {trig("dlgInstant", "Instant")}
  {trig("drwInstant", "Instant drawer", "drawer")}
</div>
<div class="note fs-sm">
  <p class="mb-2"><code>.dialog-instant</code> and <code>.drawer-instant</code>
  skip the transition entirely. That is the right choice when a dialog opens in
  response to something already in motion — a drag, a swipe, a second dialog —
  where an entry animation reads as lag rather than polish.</p>
  <p class="mb-0">You do not need to disable these for reduced-motion users;
  Bootstrap 6 already honours the media query.</p>
</div>
{dlg("dlgUp", "Slide up", "<p class='fg-2 mb-0'>Rises from below. The default feel on mobile.</p>", cls="dialog-slide-up dialog-sm")}
{dlg("dlgDown", "Slide down", "<p class='fg-2 mb-0'>Drops in from above — suits notification-style dialogs.</p>", cls="dialog-slide-down dialog-sm")}
{dlg("dlgInstant", "Instant", "<p class='fg-2 mb-0'>No transition at all.</p>", cls="dialog-instant dialog-sm")}
{drw("drwInstant", "Instant drawer", "<p class='fg-2 mb-0'>Same idea, applied to a drawer.</p>", cls="drawer-end drawer-instant")}"""),
]


def write_variant(i, folder, nav, card, blurb, sketch, wide, body):
    prev_i = (i - 1) % len(VARIANTS)
    next_i = (i + 1) % len(VARIANTS)
    html = HEAD.format(
        title=f"{card} — {PACK_TITLE}",
        desc=f"{blurb} A free Bootstrap 6 dialog example.".replace("<code>", "").replace("</code>", ""),
        p="../")
    html += f"""
<div class="variant-bar">
  <a class="btn-text btn-sm" href="../index.html">&#8592; All dialogs</a>
  <span class="fs-sm fw-semibold ms-2">{card}</span>
  <span class="fs-xs fg-3 d-none md:d-inline">{i + 1} of {len(VARIANTS)}</span>
  <div class="d-flex align-items-center gap-2 ms-auto">
    <a class="btn-icon btn-sm" href="../{VARIANTS[prev_i][0]}/index.html" aria-label="Previous">&#8249;</a>
    <a class="btn-icon btn-sm" href="../{VARIANTS[next_i][0]}/index.html" aria-label="Next">&#8250;</a>
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
        title=f"{PACK_TITLE} — 10 Free Bootstrap 6 Dialog Templates",
        desc="Ten free Bootstrap 6 dialog and drawer templates — basic, scrollable, sizes, forms, destructive confirms, non-modal, four-sided drawers, bottom sheets, toasts and entry animations. Native dialog elements, no build step.",
        p="")
    html += f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#dialogs">Skip to the dialogs</a>

<div class="pack-head">
  <div class="container">
    <div class="d-flex flex-wrap align-items-start gap-3">
      <div class="me-auto" style="max-width:44rem">
        <span class="badge badge-subtle theme-primary mb-3">Bootstrap 6.0.0-alpha1</span>
        <h1 class="fs-4xl fw-bold mb-3" style="letter-spacing:-.03em">{PACK_TITLE}</h1>
        <p class="fs-lg fg-2 mb-0">
          v6 rebuilt this area completely: Modal became Dialog, Offcanvas became
          Drawer, and both are now native <code>&lt;dialog&gt;</code> elements.
          Ten variants covering sizes, scrolling, forms, destructive confirms,
          non-modal panels, four-sided drawers, bottom sheets, toasts and motion.
        </p>
      </div>
      {TOGGLE}
    </div>
  </div>
</div>

<main id="dialogs" class="section">
  <div class="container">
    <div class="pack-grid">
{chr(10).join(cards)}
    </div>

    <section class="mt-9" style="max-width:46rem">
      <h2 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">Porting from v5</h2>
      <div class="prose">
        <p>The renames are the easy part: <code>Modal</code> is
        <code>Dialog</code>, <code>Offcanvas</code> is <code>Drawer</code>, and
        the data attributes follow — <code>data-bs-toggle="dialog"</code>,
        <code>data-bs-dismiss="drawer"</code>. There is no
        <code>window.bootstrap</code> global any more either; v6 is ESM-only, so
        the script tag needs <code>type="module"</code>.</p>

        <h3>The mistake everyone makes</h3>
        <p>Both components must be actual <code>&lt;dialog&gt;</code> elements. A
        <code>&lt;div class="dialog"&gt;</code> or
        <code>&lt;div class="drawer"&gt;</code> will style correctly, look
        finished, and never open. Nothing is logged. If a drawer div also sits
        inside a <code>navbar-expand</code> ancestor, its contents render inline
        on desktop, which usually shows up as a navigation menu appearing twice.</p>

        <h3>What you get for free</h3>
        <p>The top layer, so no z-index conflicts with sticky headers. Focus
        trapping while open and focus restored to the trigger on close. Escape to
        dismiss. Content behind marked inert. All of that was hand-rolled
        JavaScript in v5.</p>

        <h3>What is genuinely new</h3>
        <p><code>.dialog-nonmodal</code> has no v5 equivalent — a dialog with no
        backdrop that leaves the page interactive underneath, for inspectors and
        help panels. <code>.drawer-sheet</code> with
        <code>.drawer-fit-content</code> gives you the mobile bottom-sheet
        pattern without writing any of it. And
        <code>.dialog-instant</code> lets you skip the entry animation where it
        would read as lag.</p>
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
