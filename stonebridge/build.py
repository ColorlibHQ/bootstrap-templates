#!/usr/bin/env python3
"""
Generates Stonebridge: a church homepage and a "what's on" page.

Chrome is written once so the two pages cannot drift, and the weekly gatherings
are declared once in GATHERINGS and rendered into both — the homepage as cards,
the what's-on page grouped by day. Adding a midweek service is a one-line edit
here, not a hunt through two files.
"""

import pathlib

ROOT = pathlib.Path(__file__).parent

# (day, start, minutes, name, where, blurb, on_home)
#
# `day` is a weekday key the script understands; start is local wall-clock, the
# same way a notice board means it. Duration is what makes "on now" possible.
GATHERINGS = [
    ("sun", "10:30", 75, "Sunday Morning", "Main church",
     "Our main gathering. Songs, a talk, coffee afterwards that goes on longer than the service. Kids' groups leave after fifteen minutes.", True),
    ("sun", "18:30", 60, "Sunday Evening", "Side chapel",
     "Quieter and mostly sung, with communion every week. Around forty of us, and nobody minds which seat you take.", True),
    ("wed", "18:00", 90, "The Wednesday Table", "Church hall",
     "A free hot meal for anyone who wants one, then twenty minutes of something worth talking about. No sign-up, no collection.", True),
    ("thu", "08:00", 30, "Morning Prayer", "Side chapel",
     "Half an hour, said not sung, done by half eight so you can still get to work.", True),
    ("tue", "10:00", 120, "Community Pantry", "Church hall",
     "Food, toiletries and a cup of tea. No referral needed and no questions asked.", False),
    ("tue", "13:30", 90, "Bereavement Café", "Meeting room",
     "For anyone who has lost someone, however long ago. Tea, cake, and no pressure to speak.", False),
    ("wed", "10:00", 90, "Little Steps", "Church hall",
     "Toddler group — toys out, songs at eleven, toast for everyone at quarter past.", False),
    ("thu", "19:30", 90, "Choir Practice", "Main church",
     "We rehearse for Sunday and for the carol service. You do not need to read music.", False),
    ("fri", "19:00", 120, "Youth (school years 7–13)", "Church hall",
     "Games, food, and a short discussion. Ends at nine, and we walk everyone to the bus stop.", False),
    # Rules are weekly by design, so blurbs must not claim otherwise — "first
    # Saturday of the month" here would have the page contradict itself.
    ("sat", "09:30", 120, "Churchyard Working Party", "Churchyard",
     "Tools provided, bacon sandwiches at eleven. Come for an hour or the whole morning.", False),
]

# Dated one-offs. The script marks anything in the past as passed rather than
# leaving a stale "coming up" list — the usual failure of a church website.
# Real weekdays: 27 Sep 2026 and 28 Mar 2027 are Sundays, 24 Dec 2026 a Thursday,
# 26 Mar 2027 is Good Friday, 16 May 2027 a Sunday, 26 Jun 2027 a Saturday.
EVENTS = [
    ("2026-09-27T10:30", "Harvest Festival", "Main church",
     "Bring tinned goods if you can. Everything collected goes to the pantry that week."),
    ("2026-12-24T16:00", "Crib Service", "Main church",
     "Thirty minutes, aimed squarely at under-sevens. Costumes strongly encouraged."),
    ("2027-03-26T19:30", "Good Friday: The Cross in Music", "Main church",
     "Our choir and a string quartet. Free, no ticket needed, doors from seven."),
    ("2027-03-28T06:15", "Easter Sunrise on Bridge Hill", "Bridge Hill",
     "Twenty minutes at first light, then breakfast back at the hall. Wear boots."),
    ("2027-05-16T12:30", "Parish Lunch", "Church hall",
     "Roast, pudding, and the annual meeting nobody can escape. £6, under-12s free."),
    ("2027-06-26T14:00", "Summer Fair", "Churchyard",
     "Stalls, cakes, a very competitive tombola. All proceeds to the pantry."),
]

ROOMS = [
    ("Main church", "180 seated", "£45 / session", "Piano, sound system, induction loop. No catering."),
    ("Church hall", "90 seated, 120 standing", "£30 / session", "Kitchen, tables and chairs, level access from Market Street."),
    ("Meeting room", "16 around a table", "£15 / session", "Screen, kettle, quiet. Upstairs — no lift."),
    ("Churchyard", "Outdoor", "By arrangement", "For fairs and fêtes. Talk to the office first."),
]

TALKS = [
    ("Luke: The Long Way Round", "What the tax collector saw", "Rev. Anna Oyelaran", "Luke 19:1–10", "21 Mar 2027", "28 min"),
    ("Luke: The Long Way Round", "Two sons, one father", "Rev. Anna Oyelaran", "Luke 15:11–32", "14 Mar 2027", "31 min"),
    ("Luke: The Long Way Round", "Dinner with the wrong people", "Tom Beckwith", "Luke 5:27–32", "7 Mar 2027", "26 min"),
    ("Lent: Enough", "On having enough", "Rev. Anna Oyelaran", "Exodus 16:13–21", "28 Feb 2027", "24 min"),
]

DAY_NAMES = {
    "sun": "Sunday", "mon": "Monday", "tue": "Tuesday", "wed": "Wednesday",
    "thu": "Thursday", "fri": "Friday", "sat": "Saturday",
}


def human_time(t):
    """10:30 -> 10.30am, 18:30 -> 6.30pm — how a church notice board writes it."""
    h, m = (int(x) for x in t.split(":"))
    suffix = "am" if h < 12 else "pm"
    h12 = h % 12 or 12
    return f"{h12}.{m:02d}{suffix}"


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
<body>
"""

TOGGLE = """<button class="btn-icon" type="button" id="themeToggle" aria-label="Toggle color mode">
  <svg class="theme-icon-light" width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="8" cy="8" r="3.25"/><path d="M8 1v1.5M8 13.5V15M15 8h-1.5M2.5 8H1m11-4-1 1M5 11l-1 1m0-8 1 1m6 6 1 1"/></svg>
  <svg class="theme-icon-dark" width="18" height="18" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M6 .278a.77.77 0 0 1 .08.858 7.2 7.2 0 0 0-.878 3.46c0 4.021 3.278 7.277 7.318 7.277q.792-.001 1.533-.16a.79.79 0 0 1 .81.316.73.73 0 0 1-.031.893A8.35 8.35 0 0 1 8.344 16C3.734 16 0 12.286 0 7.71 0 4.266 2.114 1.312 5.124.06A.75.75 0 0 1 6 .278"/></svg>
</button>"""

MARK = """<svg class="brand-glyph" width="26" height="30" viewBox="0 0 26 30" fill="none" aria-hidden="true">
  <path d="M13 1.5 24.5 9v19.5h-23V9L13 1.5Z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/>
  <path d="M13 11v10M9 15h8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>"""


def chrome(home=True):
    p = "" if home else "index.html"
    return f"""
<a class="visually-hidden-focusable btn-solid theme-primary m-2" href="#main">Skip to main content</a>

<header class="site-header">
  <nav class="navbar lg:navbar-expand" aria-label="Main">
    <div class="container">
      <a class="wordmark" href="index.html">
        {MARK}
        <span>Stonebridge<small>Church, Market Street</small></span>
      </a>

      <dialog class="drawer drawer-end" tabindex="-1" id="navDrawer" aria-labelledby="navDrawerLabel">
        <div class="drawer-header">
          <h5 class="drawer-title" id="navDrawerLabel">Menu</h5>
          <button type="button" class="btn-close" data-bs-dismiss="drawer" aria-label="Close"></button>
        </div>
        <div class="drawer-body mb-2 lg:mb-0">
          <ul class="nav navbar-nav ms-auto lg:gap-4">
            <li class="nav-item"><a class="nav-link" href="{p}#times">Times</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#visiting">First visit</a></li>
            <li class="nav-item"><a class="nav-link" href="whats-on.html">What's on</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#talks">Talks</a></li>
            <li class="nav-item"><a class="nav-link" href="{p}#find-us">Find us</a></li>
          </ul>
        </div>
      </dialog>

      <div class="d-flex align-items-center gap-2 ms-auto">
        {TOGGLE}
        <a class="btn-solid theme-primary give-btn" href="{p}#giving">Give</a>
        <button class="btn-icon navbar-toggler" type="button" data-bs-toggle="drawer" data-bs-target="#navDrawer" aria-controls="navDrawer" aria-label="Open navigation">
          <span class="navbar-toggler-icon" aria-hidden="true"></span>
        </button>
      </div>
    </div>
  </nav>
</header>
"""


FOOTER = """
<footer class="site-footer section pb-5 bg-2">
  <div class="container">
    <div class="row g-5">
      <div class="lg:col-5">
        <p class="display-serif fs-2xl mb-2">Stonebridge Church</p>
        <p class="fg-2 mb-0">
          Market Street, Stonebridge STB1 2QA<br>
          <a href="tel:+441632960117">01632 960117</a> &middot;
          <a href="mailto:office@stonebridge.example">office@stonebridge.example</a>
        </p>
      </div>
      <div class="md:col-6 lg:col-3">
        <p class="eyebrow fs-xs fg-3 mb-3">Church office</p>
        <p class="fg-2 mb-0">Tuesday to Friday, 9.30am&ndash;2.30pm.<br>Otherwise leave a message — we do return them.</p>
      </div>
      <div class="md:col-6 lg:col-4">
        <p class="eyebrow fs-xs fg-3 mb-3">Safeguarding</p>
        <p class="fg-2 mb-0">
          Our safeguarding officer is Priya Raman, reachable directly on
          <a href="tel:+441632960118">01632 960118</a>. Concerns are taken seriously
          and you can raise one without going through the office.
        </p>
      </div>
    </div>

    <hr class="my-5">

    <p class="fs-xs fg-3 mb-0">
      &copy; <span data-year>2027</span> Stonebridge Church &mdash; a free Bootstrap 6 template.
      The church, its people and every event on this site are fictional.
    </p>
  </div>
</footer>

<script type="module" src="assets/js/main.js"></script>
</body>
</html>
"""


def gathering_attrs(day, start, mins):
    return f'data-when="{day} {start} {mins}"'


def gathering_card(g):
    day, start, mins, name, where, blurb, _ = g
    return f"""        <article class="gathering surface surface-pad lift" {gathering_attrs(day, start, mins)}>
          <p class="gathering-status" data-status hidden></p>
          <h3 class="display-serif fs-xl mb-1">{name}</h3>
          <p class="gathering-when mb-3">{DAY_NAMES[day]}s, {human_time(start)}<span class="fg-3"> &middot; {where}</span></p>
          <p class="fg-2 fs-sm mb-0">{blurb}</p>
        </article>"""


def page_index():
    cards = "\n".join(gathering_card(g) for g in GATHERINGS if g[6])
    talks = "\n".join(f"""          <li class="talk" data-series="{series}">
            <div class="talk-meta">
              <p class="eyebrow fs-xs mb-1 talk-series">{series}</p>
              <p class="fg-3 fs-xs mb-0">{date} &middot; {length}</p>
            </div>
            <div>
              <h3 class="display-serif fs-lg mb-1">{title}</h3>
              <p class="fg-2 fs-sm mb-0">{speaker} &middot; {passage}</p>
            </div>
            <a class="btn-outline theme-secondary btn-sm talk-play" href="#talks">Listen</a>
          </li>""" for series, title, speaker, passage, date, length in TALKS)

    series_names = list(dict.fromkeys(t[0] for t in TALKS))
    filters = "\n".join(
        f'          <button class="talk-filter" type="button" data-series-filter="{s}">{s}</button>'
        for s in series_names)

    return HEAD.format(
        title="Stonebridge — Free Bootstrap 6 Church Website Template",
        desc="Stonebridge is a free Bootstrap 6 church template whose service times work out their own next occurrence, so the page says “today”, “on now” or “this Sunday” instead of going stale.",
    ) + chrome() + """
<section class="welcome-hero">
  <img class="hero-bg" src="img/hero.jpg" alt="" width="1800" height="1200" loading="eager">
  <div class="container welcome-hero-inner">
    <p class="eyebrow fs-xs mb-3">Market Street &middot; Stonebridge</p>
    <h1 class="display-serif hero-title mb-4">There is a place<br>for you on Sunday.</h1>
    <p class="hero-lede fs-lg mb-5">
      A church in the middle of town. Three gatherings a week, a hot meal on
      Wednesdays, and no expectation whatsoever that you know what you are doing.
    </p>

    <div class="next-strip" data-next-strip hidden>
      <span class="next-dot" aria-hidden="true"></span>
      <p class="mb-0"><strong data-next-label></strong> <span data-next-name></span></p>
    </div>

    <div class="d-flex flex-wrap gap-3">
      <a class="btn-solid theme-primary btn-lg" href="#visiting">Coming for the first time</a>
      <a class="btn-outline theme-secondary btn-lg" href="whats-on.html">Everything that's on</a>
    </div>
  </div>
</section>

<main id="main">

  <!-- Times -->
  <section class="section" id="times">
    <div class="container">
      <div class="row g-5 mb-5 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-3">When we meet</p>
          <h2 class="display-serif section-title fs-4xl mb-0">Four gatherings, every week, whatever the weather</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            These times do not change with the seasons. If something is cancelled
            it is announced here first, and on the board by the gate second.
          </p>
        </div>
      </div>

      <div class="gathering-grid">
""" + cards + """
      </div>

      <p class="fs-sm fg-3 mt-4 mb-0">
        Times shown against your own clock. Everything happens at Market Street
        unless it says otherwise.
      </p>
    </div>
  </section>

  <!-- Welcome -->
  <section class="section bg-2">
    <div class="container">
      <div class="row g-6 align-items-center">
        <div class="lg:col-6">
          <div class="ph ph-3x4 framed"><img src="img/welcome.jpg" alt="People talking over coffee after a service" width="700" height="933" loading="lazy"></div>
        </div>
        <div class="lg:col-6">
          <p class="eyebrow-rule mb-3">Who we are</p>
          <h2 class="display-serif section-title fs-4xl mb-4">A fairly ordinary church, on purpose</h2>
          <p class="fg-2 mb-4">
            There has been a church on this corner since 1847, and a bridge over
            the beck for a good while before that. About two hundred and forty of
            us come on a normal Sunday — students, families, people who have been
            here sixty years, and a steady handful who are quietly working out
            what they think.
          </p>
          <p class="fg-2 mb-4">
            We are not a slick operation. The heating is temperamental, the coffee
            has improved, and somebody will almost certainly say hello to you
            twice by accident.
          </p>

          <dl class="facts">
            <div><dt>Founded</dt><dd>1847</dd></div>
            <div><dt>Sunday attendance</dt><dd>~240</dd></div>
            <div><dt>Meals served in 2026</dt><dd>4,100</dd></div>
            <div><dt>Staff</dt><dd>Two, plus a great many volunteers</dd></div>
          </dl>
        </div>
      </div>
    </div>
  </section>

  <!-- First visit -->
  <section class="section" id="visiting">
    <div class="container">
      <div class="row g-6">
        <div class="lg:col-5">
          <p class="eyebrow-rule mb-3">First time here</p>
          <h2 class="display-serif section-title fs-4xl mb-4">The questions people are too polite to ask</h2>
          <p class="fg-2 mb-4">
            Walking into a church you have never been to is genuinely awkward.
            Here is everything we would want to know first, answered plainly.
          </p>
          <p class="fg-2 mb-0">
            Still unsure? Email
            <a href="mailto:hello@stonebridge.example">hello@stonebridge.example</a>
            and Anna will reply herself.
          </p>
        </div>

        <div class="lg:col-7">
          <div class="faq">
            <details name="visiting" open>
              <summary>What time should I arrive?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">Five or ten minutes early is plenty. There is someone on the door from 10.15am who will find you a seat and answer anything.</p></div>
            </details>
            <details name="visiting">
              <summary>What do people wear?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">Whatever you own. You will see suits, walking gear and pyjama bottoms on the same row, and nobody is counting.</p></div>
            </details>
            <details name="visiting">
              <summary>Where do I park?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">The Market Street car park behind the church is free on Sundays. There are two accessible bays by the west door, and the 14 and 22 buses stop outside.</p></div>
            </details>
            <details name="visiting">
              <summary>What happens with my children?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">They stay with you for the first fifteen minutes, then groups go out by age to the hall. Every leader is DBS-checked and you sign your child in and out. If your child would rather stay with you, that is completely fine — nobody minds noise.</p></div>
            </details>
            <details name="visiting">
              <summary>How long does it last?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">About seventy-five minutes on a Sunday morning, then coffee for as long as you like. Evening is an hour. Morning Prayer is half an hour and finishes on time, always.</p></div>
            </details>
            <details name="visiting">
              <summary>Will I have to do or say anything?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">No. You will not be asked to stand up, introduce yourself, or put anything in a collection. Sitting quietly at the back is a perfectly normal thing to do and several of us started that way.</p></div>
            </details>
            <details name="visiting">
              <summary>Is the building accessible?</summary>
              <div class="faq-body"><p class="fg-2 mb-0">Step-free entry at the west door, an induction loop throughout, large-print orders of service at the back and an accessible toilet in the hall. The meeting room upstairs is the one space we cannot yet reach without stairs, and we are honest about that.</p></div>
            </details>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Life -->
  <section class="section bg-2" id="life">
    <div class="container">
      <div class="row g-5 mb-5 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-3">The rest of the week</p>
          <h2 class="display-serif section-title fs-4xl mb-0">Most of what we do happens Monday to Saturday</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            None of it requires membership, a form, or any prior involvement.
            Turn up, or don't — both are fine.
          </p>
        </div>
      </div>

      <div class="row g-4">
        <div class="md:col-6 lg:col-4">
          <article class="life-card surface lift">
            <div class="ph ph-1x1"><img src="img/life-kids.jpg" alt="Children at a craft table" width="600" height="600" loading="lazy"></div>
            <div class="surface-pad">
              <h3 class="display-serif fs-lg mb-2">Children &amp; youth</h3>
              <p class="fg-2 fs-sm mb-0">Groups from crawling to sixth form: Little Steps on Wednesdays, Sunday groups by age, and youth on Friday nights.</p>
            </div>
          </article>
        </div>
        <div class="md:col-6 lg:col-4">
          <article class="life-card surface lift">
            <div class="ph ph-1x1"><img src="img/life-pantry.jpg" alt="Volunteers packing food boxes" width="600" height="600" loading="lazy"></div>
            <div class="surface-pad">
              <h3 class="display-serif fs-lg mb-2">Community pantry</h3>
              <p class="fg-2 fs-sm mb-0">Tuesdays, 10am to noon. Food, toiletries and a cup of tea. No referral, no questions, no means test.</p>
            </div>
          </article>
        </div>
        <div class="md:col-6 lg:col-4">
          <article class="life-card surface lift">
            <div class="ph ph-1x1"><img src="img/life-choir.jpg" alt="A choir rehearsing" width="600" height="600" loading="lazy"></div>
            <div class="surface-pad">
              <h3 class="display-serif fs-lg mb-2">Music &amp; choir</h3>
              <p class="fg-2 fs-sm mb-0">Thursday rehearsals for Sunday and the carol service. You do not need to read music, only to turn up twice in a row.</p>
            </div>
          </article>
        </div>
        <div class="md:col-6 lg:col-4">
          <article class="life-card surface lift surface-pad">
            <h3 class="display-serif fs-lg mb-2">The Wednesday Table</h3>
            <p class="fg-2 fs-sm mb-0">A free hot meal at six for anybody at all, then twenty minutes of something worth chewing over. Around ninety people most weeks.</p>
          </article>
        </div>
        <div class="md:col-6 lg:col-4">
          <article class="life-card surface lift surface-pad">
            <h3 class="display-serif fs-lg mb-2">Home groups</h3>
            <p class="fg-2 fs-sm mb-0">Eleven groups across town meeting midweek in living rooms. The office will point you at whichever one is nearest.</p>
          </article>
        </div>
        <div class="md:col-6 lg:col-4">
          <article class="life-card surface lift surface-pad">
            <h3 class="display-serif fs-lg mb-2">Bereavement café</h3>
            <p class="fg-2 fs-sm mb-0">Tuesday afternoons, for anyone who has lost someone — this year or thirty years ago. Tea, cake, and no pressure to speak.</p>
          </article>
        </div>
      </div>
    </div>
  </section>

  <!-- Talks -->
  <section class="section" id="talks">
    <div class="container">
      <div class="row g-5 mb-5 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-3">Talks</p>
          <h2 class="display-serif section-title fs-4xl mb-0">Every Sunday talk, recorded and kept</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            Missed one, or want to hear it again before you decide what you make
            of it? They are all here, oldest to newest.
          </p>
        </div>
      </div>

      <div class="talk-filters" role="group" aria-label="Filter talks by series">
          <button class="talk-filter is-on" type="button" data-series-filter="all">All talks</button>
""" + filters + """
      </div>

      <ul class="talk-list" data-talk-list>
""" + talks + """
      </ul>
      <p class="fs-sm fg-3 mt-4 mb-0" data-talk-empty hidden>Nothing in that series yet.</p>
    </div>
  </section>

  <!-- Giving -->
  <section class="section bg-2" id="giving">
    <div class="container">
      <div class="row g-6 align-items-center">
        <div class="lg:col-6">
          <p class="eyebrow-rule mb-3">Giving</p>
          <h2 class="display-serif section-title fs-4xl mb-4">Where the money actually goes</h2>
          <p class="fg-2 mb-4">
            We are funded almost entirely by people who come here. There is no
            collection plate passed down the rows on a Sunday, because being put
            on the spot in front of strangers is a rotten way to be asked.
          </p>
          <p class="fg-2 mb-4">
            If you are visiting, please do not give. Genuinely — we would rather
            you had a coffee on us.
          </p>
          <a class="btn-solid theme-primary btn-lg" href="#find-us">Ask about giving</a>
        </div>

        <div class="lg:col-6">
          <div class="split">
            <div class="split-row">
              <div class="split-bar" style="--pct:41%"></div>
              <p class="split-label mb-0"><span>Staff &amp; ministry</span><strong>41%</strong></p>
            </div>
            <div class="split-row">
              <div class="split-bar" style="--pct:24%"></div>
              <p class="split-label mb-0"><span>Pantry &amp; Wednesday Table</span><strong>24%</strong></p>
            </div>
            <div class="split-row">
              <div class="split-bar" style="--pct:18%"></div>
              <p class="split-label mb-0"><span>Building &amp; heating</span><strong>18%</strong></p>
            </div>
            <div class="split-row">
              <div class="split-bar" style="--pct:12%"></div>
              <p class="split-label mb-0"><span>Given away</span><strong>12%</strong></p>
            </div>
            <div class="split-row">
              <div class="split-bar" style="--pct:5%"></div>
              <p class="split-label mb-0"><span>Children &amp; youth</span><strong>5%</strong></p>
            </div>
            <p class="fs-xs fg-3 mt-4 mb-0">Year to December 2026. Full accounts are on the noticeboard and available on request.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Find us -->
  <section class="section" id="find-us">
    <div class="container">
      <div class="row g-6">
        <div class="lg:col-6">
          <p class="eyebrow-rule mb-3">Find us</p>
          <h2 class="display-serif section-title fs-4xl mb-4">On the corner of Market Street and Beck Lane</h2>

          <div class="ph ph-16x9 framed mb-4"><img src="img/building.jpg" alt="The church seen from Market Street" width="900" height="506" loading="lazy"></div>

          <dl class="facts">
            <div><dt>Address</dt><dd>Market Street, Stonebridge STB1 2QA</dd></div>
            <div><dt>Parking</dt><dd>Market Street car park, free on Sundays</dd></div>
            <div><dt>Buses</dt><dd>14 and 22 stop outside; 6 stops on Beck Lane</dd></div>
            <div><dt>Office hours</dt><dd>Tuesday to Friday, 9.30am&ndash;2.30pm</dd></div>
          </dl>
        </div>

        <div class="lg:col-6">
          <div class="surface surface-pad">
            <h3 class="display-serif fs-xl mb-2">Send us a message</h3>
            <p class="fg-2 fs-sm mb-4">
              It reaches the office, and a person reads it. If it is urgent or
              about a bereavement, please ring instead — <a href="tel:+441632960117">01632 960117</a>.
            </p>

            <form id="contactForm" data-demo-form novalidate>
              <div class="row g-3">
                <div class="md:col-6">
                  <label class="form-label" for="cfName">Your name</label>
                  <input class="form-control" type="text" id="cfName" name="name" required>
                  <div class="invalid-feedback">Please tell us who you are.</div>
                </div>
                <div class="md:col-6">
                  <label class="form-label" for="cfEmail">Email</label>
                  <input class="form-control" type="email" id="cfEmail" name="email" required>
                  <div class="invalid-feedback">We need an address to reply to.</div>
                </div>
                <div class="col-12">
                  <label class="form-label" for="cfTopic">What is it about?</label>
                  <!-- v6 has no .form-select component: a native select takes
                       .form-control plus .form-control-caret for the chevron. -->
                  <select class="form-control form-control-caret" id="cfTopic" name="topic">
                    <option>Visiting for the first time</option>
                    <option>Baptism, wedding or funeral</option>
                    <option>Children &amp; youth</option>
                    <option>The pantry or Wednesday Table</option>
                    <option>Hiring a room</option>
                    <option>Something else</option>
                  </select>
                </div>
                <div class="col-12">
                  <label class="form-label" for="cfMsg">Message</label>
                  <textarea class="form-control" id="cfMsg" name="message" rows="4" required></textarea>
                  <div class="invalid-feedback">A sentence or two is plenty.</div>
                </div>
                <div class="col-12">
                  <button class="btn-solid theme-primary" type="submit" data-done-text="Thank you — we'll be in touch">Send message</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </section>

</main>
""" + FOOTER


def page_whats_on():
    # Grouped by day, in week order starting Sunday.
    order = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"]
    blocks = []
    for day in order:
        # GATHERINGS is authored in whatever order reads best for the homepage;
        # a day column has to run down the clock regardless.
        items = sorted((g for g in GATHERINGS if g[0] == day), key=lambda g: g[1])
        if not items:
            continue
        rows = "\n".join(f"""          <li class="week-item" {gathering_attrs(g[0], g[1], g[2])}>
            <p class="week-time mb-0"><time datetime="{g[1]}">{human_time(g[1])}</time></p>
            <div>
              <h3 class="fs-lg display-serif mb-1">{g[3]} <span class="week-flag" data-status hidden></span></h3>
              <p class="fg-2 fs-sm mb-0">{g[5]}</p>
            </div>
            <p class="week-where fg-3 fs-sm mb-0">{g[4]}</p>
          </li>""" for g in items)
        blocks.append(f"""      <section class="week-day">
        <h2 class="display-serif fs-2xl week-day-name">{DAY_NAMES[day]}</h2>
        <ul class="week-list">
{rows}
        </ul>
      </section>""")

    events = "\n".join(f"""        <li class="event" data-date="{when}">
          <div class="event-date">
            <span class="event-day">{when[8:10]}</span>
            <span class="event-mon">{["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][int(when[5:7]) - 1]}</span>
            <span class="event-year">{when[0:4]}</span>
          </div>
          <div>
            <h3 class="display-serif fs-xl mb-1">{title} <span class="event-flag" data-passed hidden>Passed</span></h3>
            <p class="fg-3 fs-sm mb-2">{human_time(when[11:16])} &middot; {where}</p>
            <p class="fg-2 fs-sm mb-0">{blurb}</p>
          </div>
        </li>""" for when, title, where, blurb in EVENTS)

    rooms = "\n".join(f"""            <tr>
              <th scope="row">{name}</th>
              <td data-cell="Capacity">{cap}</td>
              <td data-cell="Rate">{rate}</td>
              <td data-cell="Notes">{notes}</td>
            </tr>""" for name, cap, rate, notes in ROOMS)

    return HEAD.format(
        title="What's on — Stonebridge Bootstrap 6 Church Template",
        desc="The full week at Stonebridge: regular gatherings grouped by day, dated events that mark themselves as passed, and room hire rates.",
    ) + chrome(home=False) + f"""
<section class="page-head">
  <div class="container">
    <p class="eyebrow fs-xs mb-3"><a href="index.html">Stonebridge</a> &middot; What's on</p>
    <h1 class="display-serif hero-title mb-4">The whole week,<br>as it actually runs</h1>
    <p class="hero-lede fs-lg mb-0">
      Everything below happens every week without needing to be announced. Dated
      one-offs are further down, and anything that has already happened says so.
    </p>
  </div>
</section>

<main id="main">

  <!-- Weekly rhythm -->
  <section class="section">
    <div class="container">
{chr(10).join(blocks)}
    </div>
  </section>

  <!-- Dated events -->
  <section class="section bg-2" id="events">
    <div class="container">
      <div class="row g-5 mb-5 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-3">Coming up</p>
          <h2 class="display-serif section-title fs-4xl mb-0">One-offs, festivals and the fête</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            These carry real dates, so anything in the past greys itself out
            rather than sitting here pretending to be news.
          </p>
        </div>
      </div>

      <ul class="event-list">
{events}
      </ul>
    </div>
  </section>

  <!-- Room hire -->
  <section class="section" id="hire">
    <div class="container">
      <div class="row g-5 mb-5 align-items-end">
        <div class="lg:col-7">
          <p class="eyebrow-rule mb-3">Room hire</p>
          <h2 class="display-serif section-title fs-4xl mb-0">The building is for the town, not just for Sundays</h2>
        </div>
        <div class="lg:col-5">
          <p class="fg-2 mb-0">
            Rehearsals, AGMs, birthday parties, polling. Community groups pay
            half, and nobody has ever been charged for a wake.
          </p>
        </div>
      </div>

      <div class="table-responsive">
        <table class="table md:table-stacked align-middle">
          <caption class="fs-sm fg-3">A session is a morning, afternoon or evening. Rates held since 2025.</caption>
          <thead>
            <tr>
              <th scope="col">Space</th>
              <th scope="col">Capacity</th>
              <th scope="col">Rate</th>
              <th scope="col">Notes</th>
            </tr>
          </thead>
          <tbody>
{rooms}
          </tbody>
        </table>
      </div>

      <p class="fs-sm fg-2 mt-4 mb-0">
        To book anything, ring the office on <a href="tel:+441632960117">01632 960117</a>
        or email <a href="mailto:office@stonebridge.example">office@stonebridge.example</a>.
      </p>
    </div>
  </section>

</main>
""" + FOOTER


(ROOT / "index.html").write_text(page_index(), encoding="utf-8")
(ROOT / "whats-on.html").write_text(page_whats_on(), encoding="utf-8")
print("wrote index.html, whats-on.html")
