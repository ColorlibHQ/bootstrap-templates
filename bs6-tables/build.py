#!/usr/bin/env python3
"""
Generates the Bootstrap 6 Tables pack: an index gallery plus one page per variant.

Every variant shares the same chrome (sticky bar with a back link and a colour-mode
toggle) so the pack reads as one product, and every variant renders the SAME
dataset — so the differences you see are genuinely the table treatment, not the
content. Ten variants, from a plain striped table up to sorting, filtering,
pagination, row selection and a pinned-column matrix.
"""

import pathlib

PACK_TITLE = "Bootstrap 6 Tables"
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

SEARCH = ('<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" '
          'aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="m10.5 10.5 4 4" stroke-linecap="round"/></svg>')

SORT_CARET = ('<svg class="caret" width="10" height="10" viewBox="0 0 16 16" fill="currentColor" '
              'aria-hidden="true"><path d="m8 4 5 7H3z"/></svg>')

TICK = ('<svg class="cmp-tick" width="17" height="17" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">'
        '<path d="M8 1a7 7 0 1 0 0 14A7 7 0 0 0 8 1m3.2 5.2-4 4a.75.75 0 0 1-1.06 0l-2-2 1.06-1.06L7.67 8.6z"/></svg>'
        '<span class="visually-hidden">Included</span>')

CROSS = ('<svg class="cmp-cross" width="17" height="17" viewBox="0 0 16 16" fill="none" stroke="currentColor" '
         'stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="m5 5 6 6M11 5l-6 6"/></svg>'
         '<span class="visually-hidden">Not included</span>')


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


# One dataset, rendered by every variant — invoice ledger.
# (ref, client, status, status-theme, issued, due, amount)
ROWS = [
    ("INV-2041", "Northwind Trading", "Paid", "success", "2026-06-02", "2026-07-02", 4820.00),
    ("INV-2042", "Kestrel Logistics", "Overdue", "danger", "2026-06-04", "2026-07-04", 12400.50),
    ("INV-2043", "Lumen Studio", "Paid", "success", "2026-06-09", "2026-07-09", 1750.00),
    ("INV-2044", "Fieldstone Group", "Pending", "warning", "2026-06-14", "2026-07-14", 8960.25),
    ("INV-2045", "Ardent Works", "Paid", "success", "2026-06-18", "2026-07-18", 2310.75),
    ("INV-2046", "Halden & Co", "Draft", "secondary", "2026-06-21", "2026-07-21", 640.00),
    ("INV-2047", "Pemberton Civils", "Overdue", "danger", "2026-06-25", "2026-07-25", 19875.00),
    ("INV-2048", "Sable Interiors", "Pending", "warning", "2026-07-01", "2026-08-01", 3405.60),
]


def money(v):
    return f"&pound;{v:,.2f}"


def rows_html(*, checkbox=False, indent=10):
    pad = " " * indent
    out = []
    for i, (ref, client, status, theme, issued, due, amount) in enumerate(ROWS):
        cb = (f'<td><input type="checkbox" class="check" data-row-check '
              f'aria-label="Select {ref}"></td>') if checkbox else ""
        out.append(
            f'{pad}<tr>{cb}\n'
            f'{pad}  <th scope="row" class="fw-normal">{ref}</th>\n'
            # data-cell supplies the label when the row stacks — the hidden
            # thead does not, which is easy to assume and wrong.
            f'{pad}  <td data-cell="Client">{client}</td>\n'
            f'{pad}  <td data-cell="Status"><span class="badge badge-subtle theme-{theme}">{status}</span></td>\n'
            f'{pad}  <td data-cell="Issued" class="fg-3">{issued}</td>\n'
            f'{pad}  <td data-cell="Amount" class="num">{money(amount)}</td>\n'
            f'{pad}</tr>')
    return "\n".join(out)


def head_html(*, checkbox=False, sortable=False, indent=10):
    pad = " " * indent
    cols = [("Reference", "text"), ("Client", "text"), ("Status", "text"),
            ("Issued", "text"), ("Amount", "num")]
    cells = []
    if checkbox:
        cells.append(f'{pad}<th scope="col" style="width:2.5rem">'
                     f'<input type="checkbox" class="check" id="checkAll" aria-label="Select all rows"></th>')
    for idx, (label, kind) in enumerate(cols):
        cls = ' class="num"' if kind == "num" else ""
        if sortable:
            cells.append(
                f'{pad}<th scope="col"{cls}>'
                f'<button class="th-sort" type="button" data-sort-col="{idx + (1 if checkbox else 0)}" '
                f'data-sort-type="{kind}" aria-sort="none">{label} {SORT_CARET}</button></th>')
        else:
            cells.append(f'{pad}<th scope="col"{cls}>{label}</th>')
    return "\n".join(cells)


# (folder, nav title, card title, blurb, sketch html, wide?, body html)
VARIANTS = [
    ("01-basic", "Basic", "Striped ledger",
     "The default. Semantic markup with a caption, a proper row header per row and tabular figures so the money column lines up.",
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div><div class="grid4"><i></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Invoices</h1>
<p class="fg-2 mb-4">A plain striped table. Everything else in this pack builds on this markup.</p>
<div class="table-shell">
  <div class="table-responsive">
    <table class="table table-striped">
      <caption class="fs-sm fg-3 px-3">Outstanding and settled invoices, June&#8211;July 2026</caption>
      <thead>
        <tr>
{head_html()}
        </tr>
      </thead>
      <tbody class="table-group-divider">
{rows_html()}
      </tbody>
    </table>
  </div>
</div>"""),

    ("02-bordered", "Bordered", "Bordered &amp; compact",
     "<code>.table-bordered</code> with <code>.table-sm</code> and <code>.table-hover</code> &#8212; the density finance and admin screens actually want.",
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div><div class="grid4"><i></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div><div class="grid4"><i></i><i></i><i></i><i></i></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Compact ledger</h1>
<p class="fg-2 mb-4">Ruled and dense. Hover highlighting makes long rows readable across.</p>
<div class="table-responsive">
  <table class="table table-bordered table-sm table-hover">
    <thead>
      <tr>
{head_html()}
      </tr>
    </thead>
    <tbody>
{rows_html()}
    </tbody>
  </table>
</div>"""),

    ("03-stacked", "Stacked", "Mobile reflow",
     "<code>.md:table-stacked</code> is new in v6 &#8212; below the breakpoint each row becomes a labelled block instead of forcing a horizontal scroll. Narrow the window to see it.",
     '<i class="tall"></i><i class="tall"></i><i class="tall"></i>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Reflowing table</h1>
<p class="fg-2 mb-4">
  On a phone this stops being a grid and becomes a stack of labelled rows, with
  no horizontal scrolling and no truncation. Resize the window to watch it change.
</p>
<div class="table-shell">
  <table class="table md:table-stacked">
    <thead>
      <tr>
{head_html()}
      </tr>
    </thead>
    <tbody class="table-group-divider">
{rows_html()}
      </tbody>
  </table>
</div>
<p class="fs-sm fg-3 mt-3 mb-0">
  Two things catch people out. The class is <code>md:table-stacked</code> &#8212; the bare
  <code>.table-stacked</code> stacks at <em>every</em> width. And the labels come from a
  <code>data-cell</code> attribute on each cell, not from the hidden <code>&lt;thead&gt;</code>.
</p>"""),

    ("04-sortable", "Sortable", "Click-to-sort",
     "Header buttons that sort in place and set <code>aria-sort</code>, so screen readers announce the direction. No library.",
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div><div class="grid4"><i></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Sortable columns</h1>
<p class="fg-2 mb-4">Click any header. Sorting is done on the DOM rows &#8212; fine to a few hundred rows.</p>
<div class="table-shell">
  <div class="table-responsive">
    <table class="table table-hover" data-sortable>
      <thead>
        <tr>
{head_html(sortable=True)}
        </tr>
      </thead>
      <tbody class="table-group-divider">
{rows_html()}
      </tbody>
    </table>
  </div>
</div>
<p class="fs-sm fg-3 mt-3 mb-0">
  Amount sorts numerically because the header carries <code>data-sort-type="num"</code>;
  everything else sorts as text.
</p>"""),

    ("05-filter", "Filter", "Search &amp; filter toolbar",
     "A search field and a Combobox status filter above the table, with a live result count and an empty state.",
     '<div class="row2"><i class="tall"></i><i class="tall"></i></div>'
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div><div class="grid4"><i></i><i></i><i></i><i></i></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Filterable ledger</h1>
<p class="fg-2 mb-4">Text search across every cell, plus a status filter. Both narrow the same row set.</p>
<div class="table-shell" data-filterable>
  <div class="table-head">
    <div class="form-control form-adorn" style="flex:1 1 14rem">
      <div class="form-adorn-icon">{SEARCH}</div>
      <input type="search" class="form-ghost" data-filter-text placeholder="Search invoices&#8230;" aria-label="Search invoices">
    </div>
    <div style="flex:0 1 12rem">
      {combobox("status", "Any status", [("", "Any status"), ("paid", "Paid"), ("pending", "Pending"), ("overdue", "Overdue"), ("draft", "Draft")])}
    </div>
    <span class="fs-sm fg-3 ms-auto" data-filter-count>8 of 8</span>
  </div>
  <div class="table-responsive">
    <table class="table table-hover">
      <thead>
        <tr>
{head_html()}
        </tr>
      </thead>
      <tbody class="table-group-divider">
{rows_html()}
      </tbody>
    </table>
  </div>
  <p class="p-4 mb-0 fg-3 text-center" data-filter-empty hidden>Nothing matches that search.</p>
</div>"""),

    ("06-paginated", "Paginated", "Client-side pagination",
     "Three rows a page with real <code>&lt;nav&gt;</code> pagination, a live range readout and disabled end states.",
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div><div class="grid4"><i></i><i></i><i></i><i></i></div>'
     '<div class="row2"><i class="cta" style="width:2rem"></i><i class="cta" style="width:2rem"></i></div>',
     False, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Paginated ledger</h1>
<p class="fg-2 mb-4">Deliberately three per page so the paging is visible with only eight rows.</p>
<div class="table-shell" data-paginate="3">
  <div class="table-responsive">
    <table class="table">
      <thead>
        <tr>
{head_html()}
        </tr>
      </thead>
      <tbody class="table-group-divider">
{rows_html()}
      </tbody>
    </table>
  </div>
  <div class="table-foot">
    <span class="fs-sm fg-3" data-page-range>Showing 1&#8211;3 of 8</span>
    <nav aria-label="Invoice pages">
      <ul class="pagination pagination-sm mb-0" data-page-list></ul>
    </nav>
  </div>
</div>"""),

    ("07-select", "Selectable", "Row selection &amp; bulk actions",
     "Checkbox column with a header that goes indeterminate on a partial selection, and a bulk-action bar that appears only when something is chosen.",
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i class="cta" style="width:100%;height:.5rem"></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i></i><i></i><i></i><i></i></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Selectable rows</h1>
<p class="fg-2 mb-4">Tick some rows. The header checkbox reflects a partial selection as indeterminate.</p>
<div class="table-shell" data-selectable>
  <div class="bulk-bar" data-bulk-bar hidden>
    <strong class="fs-sm" data-bulk-count>0 selected</strong>
    <div class="d-flex flex-wrap gap-2 ms-auto">
      <button class="btn-outline theme-secondary btn-sm" type="button">Export</button>
      <button class="btn-outline theme-secondary btn-sm" type="button">Send reminder</button>
      <button class="btn-solid theme-danger btn-sm" type="button">Void</button>
    </div>
  </div>
  <div class="table-responsive">
    <table class="table table-hover">
      <thead>
        <tr>
{head_html(checkbox=True)}
        </tr>
      </thead>
      <tbody class="table-group-divider">
{rows_html(checkbox=True)}
      </tbody>
    </table>
  </div>
</div>"""),

    ("08-rich", "Rich cells", "Avatars, badges &amp; progress",
     "What a dashboard table actually holds &#8212; avatar and secondary line in one cell, status badges, and an inline progress bar.",
     '<div class="grid3"><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid3"><i class="tall"></i><i class="tall"></i><i class="tall"></i></div>'
     '<div class="grid3"><i class="tall"></i><i class="tall"></i><i class="tall"></i></div>',
     True, """<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Rich cells</h1>
<p class="fg-2 mb-4">A cell can hold a small layout. It should still be one idea per column.</p>
<div class="table-shell">
  <div class="table-responsive">
    <table class="table table-hover align-middle">
      <thead>
        <tr>
          <th scope="col">Client</th>
          <th scope="col">Owner</th>
          <th scope="col">Stage</th>
          <th scope="col" style="min-width:9rem">Completion</th>
          <th scope="col" class="num">Value</th>
        </tr>
      </thead>
      <tbody class="table-group-divider">
        <tr>
          <th scope="row" class="fw-normal">
            <span class="d-block fw-semibold">Northwind Trading</span>
            <span class="fs-xs fg-3">Renewal &middot; 14 seats</span>
          </th>
          <td><span class="d-inline-flex align-items-center gap-2"><span class="avatar avatar-sm"><span class="avatar-initials">PN</span></span> Priya N.</span></td>
          <td><span class="badge badge-subtle theme-success">Won</span></td>
          <td>
            <div class="progress" role="progressbar" aria-label="Completion" aria-valuenow="100" aria-valuemin="0" aria-valuemax="100">
              <div class="progress-bar theme-success" style="width:100%"></div>
            </div>
            <span class="fs-xs fg-3">100%</span>
          </td>
          <td class="num">&pound;4,820.00</td>
        </tr>
        <tr>
          <th scope="row" class="fw-normal">
            <span class="d-block fw-semibold">Pemberton Civils</span>
            <span class="fs-xs fg-3">New business &middot; 60 seats</span>
          </th>
          <td><span class="d-inline-flex align-items-center gap-2"><span class="avatar avatar-sm"><span class="avatar-initials">ML</span></span> Marcus L.</span></td>
          <td><span class="badge badge-subtle theme-warning">Negotiation</span></td>
          <td>
            <div class="progress" role="progressbar" aria-label="Completion" aria-valuenow="70" aria-valuemin="0" aria-valuemax="100">
              <div class="progress-bar" style="width:70%"></div>
            </div>
            <span class="fs-xs fg-3">70%</span>
          </td>
          <td class="num">&pound;19,875.00</td>
        </tr>
        <tr>
          <th scope="row" class="fw-normal">
            <span class="d-block fw-semibold">Sable Interiors</span>
            <span class="fs-xs fg-3">Expansion &middot; 8 seats</span>
          </th>
          <td><span class="d-inline-flex align-items-center gap-2"><span class="avatar avatar-sm"><span class="avatar-initials">DR</span></span> Dana R.</span></td>
          <td><span class="badge badge-subtle theme-primary">Proposal</span></td>
          <td>
            <div class="progress" role="progressbar" aria-label="Completion" aria-valuenow="40" aria-valuemin="0" aria-valuemax="100">
              <div class="progress-bar" style="width:40%"></div>
            </div>
            <span class="fs-xs fg-3">40%</span>
          </td>
          <td class="num">&pound;3,405.60</td>
        </tr>
        <tr>
          <th scope="row" class="fw-normal">
            <span class="d-block fw-semibold">Halden &amp; Co</span>
            <span class="fs-xs fg-3">New business &middot; 3 seats</span>
          </th>
          <td><span class="d-inline-flex align-items-center gap-2"><span class="avatar avatar-sm"><span class="avatar-initials">TB</span></span> Tomas B.</span></td>
          <td><span class="badge badge-subtle theme-secondary">Qualifying</span></td>
          <td>
            <div class="progress" role="progressbar" aria-label="Completion" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100">
              <div class="progress-bar theme-secondary" style="width:15%"></div>
            </div>
            <span class="fs-xs fg-3">15%</span>
          </td>
          <td class="num">&pound;640.00</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>"""),

    ("09-sticky", "Sticky", "Sticky header &amp; pinned column",
     "A tall, wide table that scrolls inside its own box &#8212; header stuck to the top, reference column pinned to the left.",
     '<div class="grid4"><i class="head"></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i class="head"></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i class="head"></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i class="head"></i><i></i><i></i><i></i></div>',
     True, """<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Sticky header, pinned column</h1>
<p class="fg-2 mb-4">Scroll the box in both directions &#8212; the header row and the reference column stay put.</p>
<div class="table-shell">
  <div class="table-scroll table-pin">
    <table class="table table-sm table-hover mb-0" style="min-width:60rem">
      <thead>
        <tr>
          <th scope="col">Reference</th>
          <th scope="col">Client</th>
          <th scope="col">Status</th>
          <th scope="col">Issued</th>
          <th scope="col">Due</th>
          <th scope="col">Terms</th>
          <th scope="col">Owner</th>
          <th scope="col" class="num">Net</th>
          <th scope="col" class="num">VAT</th>
          <th scope="col" class="num">Gross</th>
        </tr>
      </thead>
      <tbody class="table-group-divider" id="stickyBody"></tbody>
    </table>
  </div>
</div>
<p class="fs-sm fg-3 mt-3 mb-0">
  Rows are generated by the page script purely to make the box tall enough to
  scroll &#8212; the sticky behaviour itself is pure CSS.
</p>"""),

    ("10-compare", "Comparison", "Feature comparison",
     "A pricing matrix with a highlighted column, ticks and crosses that are announced properly, and row headers down the side.",
     '<div class="grid4"><i></i><i class="head"></i><i class="head"></i><i class="head"></i></div>'
     '<div class="grid4"><i class="w75"></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i class="w75"></i><i></i><i></i><i></i></div>'
     '<div class="grid4"><i class="w75"></i><i></i><i></i><i></i></div>',
     True, f"""<h1 class="fs-2xl fw-bold mb-1" style="letter-spacing:-.02em">Feature comparison</h1>
<p class="fg-2 mb-4">Ticks and crosses carry visually-hidden text, so the meaning survives without the icon.</p>
<div class="table-shell">
  <div class="table-responsive">
    <table class="table table-hover align-middle mb-0">
      <caption class="fs-sm fg-3 px-3">All plans billed annually. Prices exclude VAT.</caption>
      <thead>
        <tr>
          <th scope="col" style="min-width:12rem">Feature</th>
          <th scope="col" class="text-center">Starter<br><span class="fs-xs fg-3 fw-normal">&pound;12/mo</span></th>
          <th scope="col" class="text-center cmp-featured">Team<br><span class="fs-xs fg-3 fw-normal">&pound;29/mo</span></th>
          <th scope="col" class="text-center">Scale<br><span class="fs-xs fg-3 fw-normal">&pound;79/mo</span></th>
        </tr>
      </thead>
      <tbody class="table-group-divider">
        <tr><th scope="row" class="fw-normal">Projects</th><td class="text-center">3</td><td class="text-center cmp-featured">Unlimited</td><td class="text-center">Unlimited</td></tr>
        <tr><th scope="row" class="fw-normal">Team members</th><td class="text-center">1</td><td class="text-center cmp-featured">10</td><td class="text-center">Unlimited</td></tr>
        <tr><th scope="row" class="fw-normal">Version history</th><td class="text-center">7 days</td><td class="text-center cmp-featured">90 days</td><td class="text-center">Unlimited</td></tr>
        <tr><th scope="row" class="fw-normal">Custom domains</th><td class="text-center">{CROSS}</td><td class="text-center cmp-featured">{TICK}</td><td class="text-center">{TICK}</td></tr>
        <tr><th scope="row" class="fw-normal">SSO &amp; SCIM</th><td class="text-center">{CROSS}</td><td class="text-center cmp-featured">{CROSS}</td><td class="text-center">{TICK}</td></tr>
        <tr><th scope="row" class="fw-normal">Audit log</th><td class="text-center">{CROSS}</td><td class="text-center cmp-featured">{CROSS}</td><td class="text-center">{TICK}</td></tr>
        <tr><th scope="row" class="fw-normal">Priority support</th><td class="text-center">{CROSS}</td><td class="text-center cmp-featured">{TICK}</td><td class="text-center">{TICK}</td></tr>
      </tbody>
    </table>
  </div>
  <div class="table-foot">
    <span class="fs-sm fg-3">Change plan at any time; we bill the difference pro rata.</span>
    <a class="btn-solid theme-primary btn-sm" href="#">Choose Team</a>
  </div>
</div>"""),
]


def write_variant(i, folder, nav, card, blurb, sketch, wide, body):
    prev_i = (i - 1) % len(VARIANTS)
    next_i = (i + 1) % len(VARIANTS)
    html = HEAD.format(
        title=f"{card} — {PACK_TITLE}",
        desc=f"{blurb} A free Bootstrap 6 table example.".replace("<code>", "").replace("</code>", ""),
        p="../")
    html += f"""
<div class="variant-bar">
  <a class="btn-text btn-sm" href="../index.html">&#8592; All tables</a>
  <span class="fs-sm fw-semibold ms-2">{card}</span>
  <span class="fs-xs fg-3 d-none md:d-inline">{i + 1} of {len(VARIANTS)}</span>
  <div class="d-flex align-items-center gap-2 ms-auto">
    <a class="btn-icon btn-sm" href="../{VARIANTS[prev_i][0]}/index.html" aria-label="Previous table">&#8249;</a>
    <a class="btn-icon btn-sm" href="../{VARIANTS[next_i][0]}/index.html" aria-label="Next table">&#8250;</a>
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
        title=f"{PACK_TITLE} — 10 Free Bootstrap 6 Table Templates",
        desc="Ten free Bootstrap 6 table templates — striped, bordered, mobile-reflowing, sortable, filterable, paginated, selectable, rich cells, sticky header and a comparison matrix. No build step, no datatable library.",
        p="")
    html += f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#tables">Skip to the tables</a>

<div class="pack-head">
  <div class="container">
    <div class="d-flex flex-wrap align-items-start gap-3">
      <div class="me-auto" style="max-width:44rem">
        <span class="badge badge-subtle theme-primary mb-3">Bootstrap 6.0.0-alpha1</span>
        <h1 class="fs-4xl fw-bold mb-3" style="letter-spacing:-.03em">{PACK_TITLE}</h1>
        <p class="fs-lg fg-2 mb-0">
          Ten table layouts covering what real admin and reporting screens need &#8212;
          sorting, filtering, pagination, row selection and a pinned-column matrix.
          Every one renders the same dataset, so what differs is the treatment, not
          the content. No datatable library.
        </p>
      </div>
      {TOGGLE}
    </div>
  </div>
</div>

<main id="tables" class="section">
  <div class="container">
    <div class="pack-grid">
{chr(10).join(cards)}
    </div>

    <section class="mt-9" style="max-width:46rem">
      <h2 class="fs-2xl fw-bold mb-4" style="letter-spacing:-.02em">Using these</h2>
      <div class="prose">
        <p>Each table is a standalone page. Copy the markup out of the one you want
        and drop it into your project. The static variants need only Bootstrap 6&#8217;s
        CSS; sorting, filtering, pagination and row selection are a few dozen lines
        of vanilla JavaScript in <code>assets/js/main.js</code>, which you can lift
        wholesale or ignore.</p>

        <h3>What is new in v6</h3>
        <p><code>md:table-stacked</code> is the one worth knowing about. Below the
        breakpoint it turns each row into a labelled block, so there is no horizontal
        scrolling on a phone.</p>
        <p>Three things about it are easy to get wrong, and all three fail silently.
        The bare <code>.table-stacked</code> class stacks at <em>every</em> width &#8212; the
        breakpoint prefix is what makes it responsive. The prefixed variants are
        <code>@container</code> queries, so the table needs a
        <code>.table-responsive</code> ancestor to give them something to measure.
        And the labels come from <code>data-cell="…"</code> on each cell; the hidden
        <code>&lt;thead&gt;</code> does not supply them, so without it you get an
        unlabelled stack.</p>

        <h3>Markup that pays off</h3>
        <p>Use <code>&lt;th scope="row"&gt;</code> for the identifying cell in each
        row, not <code>&lt;td&gt;</code>. It is what makes a screen reader announce
        which record a cell belongs to, and it is what
        <code>.md:table-stacked</code> keys off when it reflows. Keep a
        <code>&lt;caption&gt;</code> too &#8212; it is the accessible name of the table.</p>

        <h3>Numbers</h3>
        <p>Money and quantity columns need <code>font-variant-numeric: tabular-nums</code>
        and right alignment or the digits will not line up. That is the
        <code>.num</code> class in this pack&#8217;s stylesheet.</p>

        <h3>A gotcha worth knowing</h3>
        <p>Combobox&#8217;s <code>search</code> and <code>multiple</code> options are typed
        booleans, so a bare attribute fails config validation. Write
        <code>data-bs-search="true"</code>, not <code>data-bs-search</code>.</p>
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
