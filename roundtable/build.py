#!/usr/bin/env python3
"""
Generates Commons: a community forum.

THREADS is declared once and rendered into the board; the ranking is left to the
browser so that Hot, New and Top genuinely reorder the same list rather than
being three tabs over one hardcoded order.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent
TITLE = "Roundtable"

# title, author, initials, category, votes, replies, hours old, tag
#
# Age is stored in hours rather than a date: a hardcoded 2026 timestamp makes
# every thread read as years stale the moment the year turns, and the ranking
# maths only ever needs the interval anyway.
THREADS = [
    ("Why does `text-wrap: balance` do nothing on my headings?", "Nadia Osei", "NO", "CSS", 148, 34, 5, "solved"),
    ("Show: I rebuilt our design tokens as plain custom properties", "Wes Tremayne", "WT", "Show &amp; tell", 96, 21, 2, ""),
    ("The case against utility classes, five years on", "Marit Halvorsen", "MH", "Discussion", 312, 187, 46, "hot"),
    ("Anyone else seeing Safari 17 ignore `content-visibility`?", "Dilan Aksoy", "DA", "Bugs", 41, 12, 1, ""),
    ("Monthly thread: what are you shipping in August?", "Rae Whitcombe", "RW", "Meta", 58, 96, 18, "pinned"),
    ("How do you test focus order without losing your mind?", "Josephine Marr", "JM", "Accessibility", 204, 63, 30, ""),
    ("A 2KB alternative to the date picker you are about to install", "Ivan Kazlouski", "IK", "Show &amp; tell", 176, 44, 11, ""),
    ("Container queries finally clicked for me and here is what did it", "Priya Raman", "PR", "CSS", 267, 71, 62, ""),
    ("Is anyone actually using `@scope` in production?", "Tom Beckwith", "TB", "CSS", 33, 28, 4, ""),
    ("We removed 340KB of JavaScript and nothing broke", "Sofia Marchetti", "SM", "Performance", 421, 112, 90, "hot"),
    ("Naming things: a thread that will solve nothing", "Gregor Fyfe", "GF", "Discussion", 87, 154, 26, ""),
    ("PSA: `:user-invalid` is not `:invalid` and the difference matters", "Elena Popova", "EP", "Forms", 189, 39, 8, "solved"),
]

CATEGORIES = [
    ("CSS", 1284, "Layout, cascade, and the parts nobody reads the spec for"),
    ("Accessibility", 612, "Screen readers, focus, contrast, and testing it properly"),
    ("Performance", 498, "Budgets, bundles, and what actually moves the needle"),
    ("Show &amp; tell", 907, "Things you made. Feedback optional, encouraged"),
    ("Forms", 341, "Validation, state, and the eternal date input"),
    ("Discussion", 1_552, "Opinions, held loosely"),
    ("Bugs", 226, "Browser bugs, with a reduced test case or it did not happen"),
    ("Meta", 118, "About this forum"),
]

# depth, author, initials, hours old, votes, body
REPLIES = [
    (0, "Wes Tremayne", "WT", 4, 62,
     "The property only balances up to four lines — past that browsers bail out because the line-breaking cost is quadratic. If your heading is wrapping to five, you will get nothing and no warning."),
    (1, "Nadia Osei", "NO", 4, 18,
     "That is exactly it, mine was six lines. Shortening the heading fixed it, which is probably the real lesson."),
    (1, "Marit Halvorsen", "MH", 3, 41,
     "Worth adding: it is <code>balance</code> for headings and <code>pretty</code> for body copy. <code>pretty</code> has no line limit because it only fixes the last line, so it is the safe one to apply broadly."),
    (2, "Wes Tremayne", "WT", 3, 12,
     "Yes — and <code>pretty</code> is cheap enough that I set it on <code>p</code> globally now."),
    (0, "Dilan Aksoy", "DA", 2, 9,
     "Unrelated but related: it also does nothing inside a flex or grid item that has not been given a width, because there is no line box to balance against yet."),
    (0, "Josephine Marr", "JM", 1, 4,
     "Marking this solved. The four-line limit is not in the MDN summary and it should be."),
]

NAV = [("index.html", "Threads"), ("thread.html", "A thread"), ("categories.html", "Categories")]

ICON = {
    "up": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M8 12.5v-9M4 7.5 8 3.5l4 4"/></svg>',
    "reply": '<svg width="14" height="14" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M14 12.5a5.5 5.5 0 0 0-5.5-5.5H4M6.5 4 3.5 7l3 3"/></svg>',
    "search": '<svg width="16" height="16" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5 14 14" stroke-linecap="round"/></svg>',
}

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


def ago(h):
    if h < 1:
        return "just now"
    if h < 24:
        return f"{h}h ago"
    d = round(h / 24)
    return f"{d}d ago" if d < 7 else f"{round(d / 7)}w ago"


def chrome(current):
    links = "\n        ".join(
        f'<a class="head-link{" is-active" if h == current else ""}" href="{h}">{label}</a>'
        for h, label in NAV)
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#main">Skip to main content</a>

<header class="site-header">
  <div class="wrap head-in">
    <a class="wordmark" href="index.html">
      <span class="wordmark-mark" aria-hidden="true">◍</span>{TITLE}
    </a>
    <nav class="head-nav d-none md:d-flex" aria-label="Main">
        {links}
    </nav>
    <div class="d-flex align-items-center gap-2 ms-auto">
      <div class="form-control form-adorn search-field d-none lg:d-flex">
        <div class="form-adorn-icon">{ICON['search']}</div>
        <input type="search" class="form-ghost" placeholder="Search the forum…" aria-label="Search">
      </div>
      {TOGGLE}
      <a class="btn-solid theme-primary btn-sm" href="thread.html">New thread</a>
    </div>
  </div>
</header>
"""


FOOTER = """
<footer class="site-footer">
  <div class="wrap">
    <p class="fs-sm fg-3 mb-0">
      &copy; <span data-year>2026</span> """ + TITLE + """ &mdash; a free Bootstrap 6 template.
      Every member, thread and reply here is fictional.
    </p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def thread_rows():
    out = []
    for i, (title, author, ini, cat, votes, replies, hours, tag) in enumerate(THREADS):
        flag = f'<span class="flag flag-{tag}">{tag}</span>' if tag else ""
        out.append(f"""        <li class="thread" data-thread data-votes="{votes}" data-hours="{hours}" data-replies="{replies}">
          <div class="vote">
            <button class="vote-btn" type="button" aria-label="Upvote: {title}" aria-pressed="false">{ICON['up']}</button>
            <span class="vote-n" data-vote-n>{votes}</span>
          </div>
          <div class="thread-main">
            <h3 class="thread-title mb-1"><a href="thread.html">{title}</a>{flag}</h3>
            <p class="thread-meta mb-0">
              <span class="avatar avatar-xs"><span class="avatar-initials">{ini}</span></span>
              <span>{author}</span>
              <span class="fg-3">in</span> <a class="thread-cat" href="categories.html">{cat}</a>
              <span class="fg-3">&middot; {ago(hours)}</span>
            </p>
          </div>
          <p class="thread-replies mb-0">{ICON['reply']} <span>{replies}</span></p>
          <p class="thread-rank mb-0" data-rank-out hidden></p>
        </li>""")
    return "\n".join(out)


def reply_blocks():
    out = []
    for i, (depth, author, ini, hours, votes, body) in enumerate(REPLIES):
        out.append(f"""          <li class="reply" style="--depth:{depth}">
            <div class="vote vote-sm">
              <button class="vote-btn" type="button" aria-label="Upvote reply from {author}" aria-pressed="false">{ICON['up']}</button>
              <span class="vote-n" data-vote-n>{votes}</span>
            </div>
            <div class="reply-main">
              <p class="reply-meta mb-2">
                <span class="avatar avatar-xs"><span class="avatar-initials">{ini}</span></span>
                <strong>{author}</strong>
                <span class="fg-3">&middot; {ago(hours)}</span>
              </p>
              <p class="reply-body mb-2">{body}</p>
              <p class="reply-actions mb-0"><button class="link-btn" type="button">Reply</button><button class="link-btn" type="button">Share</button></p>
            </div>
          </li>""")
    return "\n".join(out)


def page_index():
    cats = "\n".join(f"""          <li><a href="categories.html">{name}</a><span class="fg-3">{n:,}</span></li>"""
                     for name, n, _ in CATEGORIES[:6])

    body = f"""
<main id="main" class="page">
  <div class="wrap board">

    <div class="board-main">
      <div class="sorter" role="group" aria-label="Sort threads">
        <button class="sort-btn is-on" type="button" data-sort="hot" aria-pressed="true">Hot</button>
        <button class="sort-btn" type="button" data-sort="new" aria-pressed="false">New</button>
        <button class="sort-btn" type="button" data-sort="top" aria-pressed="false">Top</button>
        <label class="sort-show">
          <input type="checkbox" class="check" id="showRank">
          <span>Show the ranking maths</span>
        </label>
      </div>

      <ul class="thread-list" data-threads>
{thread_rows()}
      </ul>

      <p class="board-note mb-0">
        Hot is <code>(votes − 1) ÷ (hours + 2)<sup>1.5</sup></code> — the same
        shape of decay Hacker News uses. Tick the box above to see each thread's
        score, and watch a 46-hour-old thread with 312 votes lose to a 5-hour-old
        one with 148.
      </p>
    </div>

    <aside class="rail">
      <section class="rail-card">
        <h2 class="rail-title">Categories</h2>
        <ul class="rail-list">
{cats}
        </ul>
        <a class="btn-outline theme-secondary btn-sm w-100 mt-3" href="categories.html">All categories</a>
      </section>

      <section class="rail-card">
        <h2 class="rail-title">House rules</h2>
        <ol class="rail-rules">
          <li>Assume the other person has a reason.</li>
          <li>A reduced test case beats a description.</li>
          <li>“Just use X” is not an answer to “why does Y do this”.</li>
          <li>Mark it solved when it is solved.</li>
        </ol>
      </section>

      <section class="rail-card">
        <h2 class="rail-title">This week</h2>
        <dl class="rail-stats">
          <div><dt>Threads</dt><dd>142</dd></div>
          <div><dt>Replies</dt><dd>1,908</dd></div>
          <div><dt>New members</dt><dd>63</dd></div>
          <div><dt>Solved</dt><dd>71%</dd></div>
        </dl>
      </section>
    </aside>

  </div>
</main>
"""
    (ROOT / "index.html").write_text(
        HEAD.format(title=f"{TITLE} — Free Bootstrap 6 Community Forum Template",
                    desc="Roundtable is a free Bootstrap 6 forum template whose Hot, New and Top tabs genuinely reorder the board from a real ranking formula.")
        + chrome("index.html") + body + FOOTER, encoding="utf-8")


def page_thread():
    t = THREADS[0]
    body = f"""
<main id="main" class="page">
  <div class="wrap board">

    <div class="board-main">
      <p class="crumbs mb-3"><a href="index.html">Threads</a> <span class="fg-3">/</span> <a href="categories.html">{t[3]}</a></p>

      <article class="op">
        <div class="op-head">
          <div class="vote">
            <button class="vote-btn" type="button" aria-label="Upvote this thread" aria-pressed="false">{ICON['up']}</button>
            <span class="vote-n" data-vote-n>{t[4]}</span>
          </div>
          <div>
            <h1 class="op-title mb-2">{t[0]}<span class="flag flag-solved">solved</span></h1>
            <p class="thread-meta mb-0">
              <span class="avatar avatar-xs"><span class="avatar-initials">{t[2]}</span></span>
              <span>{t[1]}</span> <span class="fg-3">&middot; {ago(t[6])} &middot; {t[5]} replies</span>
            </p>
          </div>
        </div>

        <div class="prose op-body">
          <p>
            I have a heading that wraps to five or six lines on mobile and
            <code>text-wrap: balance</code> appears to do absolutely nothing.
            Same heading at three lines and it balances perfectly.
          </p>
          <p>
            No overrides that I can find, no flex weirdness, and it behaves the
            same in Chrome and Safari. Reduced test case is in the reply below.
            Am I misreading what the property is for?
          </p>
        </div>
      </article>

      <h2 class="replies-title">{len(REPLIES)} replies</h2>
      <ul class="reply-list">
{reply_blocks()}
      </ul>

      <section class="composer">
        <h2 class="rail-title mb-3">Add a reply</h2>
        <form data-demo-form novalidate>
          <label class="form-label visually-hidden" for="replyBody">Your reply</label>
          <textarea class="form-control mb-3" id="replyBody" rows="4" placeholder="Be the person you needed when you were stuck." required></textarea>
          <div class="invalid-feedback mb-2">A reply needs some text in it.</div>
          <div class="d-flex flex-wrap gap-2 align-items-center">
            <button class="btn-solid theme-primary" type="submit" data-done-text="Posted ✓">Post reply</button>
            <p class="fs-xs fg-3 mb-0">Markdown works. Be kind; rule one applies.</p>
          </div>
        </form>
      </section>
    </div>

    <aside class="rail">
      <section class="rail-card">
        <h2 class="rail-title">About this thread</h2>
        <dl class="rail-stats">
          <div><dt>Category</dt><dd>{t[3]}</dd></div>
          <div><dt>Started</dt><dd>{ago(t[6])}</dd></div>
          <div><dt>Replies</dt><dd>{t[5]}</dd></div>
          <div><dt>Status</dt><dd>Solved</dd></div>
        </dl>
      </section>

      <section class="rail-card">
        <h2 class="rail-title">Related</h2>
        <ul class="rail-list">
          <li><a href="index.html">Container queries finally clicked for me</a></li>
          <li><a href="index.html">PSA: <code>:user-invalid</code> is not <code>:invalid</code></a></li>
          <li><a href="index.html">Is anyone actually using <code>@scope</code>?</a></li>
        </ul>
      </section>
    </aside>

  </div>
</main>
"""
    (ROOT / "thread.html").write_text(
        HEAD.format(title=f"{t[0]} — {TITLE} Bootstrap 6 Forum Template",
                    desc="A forum thread page with nested replies rendered from a flat list by depth, vote controls and a reply composer.")
        + chrome("thread.html") + body + FOOTER, encoding="utf-8")


def page_categories():
    rows = "\n".join(f"""          <li class="cat">
            <div>
              <h3 class="cat-name mb-1"><a href="index.html">{name}</a></h3>
              <p class="fg-2 fs-sm mb-0">{blurb}</p>
            </div>
            <p class="cat-n mb-0">{n:,}<span class="fg-3 d-block">threads</span></p>
          </li>""" for name, n, blurb in CATEGORIES)

    body = f"""
<main id="main" class="page">
  <div class="wrap">
    <h1 class="page-title mb-2">Categories</h1>
    <p class="page-sub mb-5">{len(CATEGORIES)} of them, and the honest description of each.</p>
    <ul class="cat-list">
{rows}
    </ul>
  </div>
</main>
"""
    (ROOT / "categories.html").write_text(
        HEAD.format(title=f"Categories — {TITLE} Bootstrap 6 Forum Template",
                    desc="Forum category index with thread counts and plain descriptions.")
        + chrome("categories.html") + body + FOOTER, encoding="utf-8")


page_index()
page_thread()
page_categories()
print(f"wrote 3 pages — {len(THREADS)} threads, {len(CATEGORIES)} categories")
