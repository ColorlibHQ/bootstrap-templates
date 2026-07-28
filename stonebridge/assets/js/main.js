/*!
 * Stonebridge — Bootstrap 6 church template
 */

import { initBase, onReady } from './base.js'

const DAYS = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
const DAY_LABEL = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

/* 18:30 -> "6.30pm" — how a church notice board writes a time, and how the
   static markup already writes it, so the computed line reads as one voice. */
const clock = (d) => {
  const h = d.getHours()
  const m = d.getMinutes()
  return `${h % 12 || 12}.${String(m).padStart(2, '0')}${h < 12 ? 'am' : 'pm'}`
}

/* data-when="sun 10:30 75" — weekday, local start, minutes it runs for. */
const parseWhen = (raw) => {
  const [day, time, mins] = String(raw).trim().split(/\s+/)
  const idx = DAYS.indexOf(day)
  const [h, m] = String(time).split(':').map(Number)
  if (idx < 0 || !Number.isInteger(h) || !Number.isInteger(m)) return null
  return { idx, h, m, mins: Number(mins) > 0 ? Number(mins) : 60 }
}

/* This week's occurrence: today or later, never behind us by more than the
   current day. setDate() after setHours() keeps wall-clock time across a DST
   boundary, which is what "Sundays at half ten" means to a human. */
const thisWeek = (w, now) => {
  const d = new Date(now)
  d.setHours(w.h, w.m, 0, 0)
  d.setDate(d.getDate() + ((w.idx - now.getDay() + 7) % 7))
  return d
}

/* Working out what to say about one gathering.
 *
 * Church sites state their times statically — "Sundays, 10.30am" — and that is
 * correct but useless to somebody checking their phone on a Wednesday evening
 * wondering whether there is anything on tonight. This turns the same declared
 * rule into the sentence they actually want. */
const describe = (w, now) => {
  const start = thisWeek(w, now)
  const end = new Date(start.getTime() + w.mins * 60000)

  if (start <= now && now < end) {
    return { rank: -1, state: 'now', short: 'On now', long: 'until ' + clock(end) }
  }

  // Started and finished today, so the next one is a week away.
  const next = end <= now ? new Date(start.getTime() + 7 * 86400000) : start
  const mins = Math.round((next - now) / 60000)
  const rank = next - now

  if (mins <= 60) {
    return { rank, state: 'soon', short: `Starts in ${mins} min`, long: `starts in ${mins} minute${mins === 1 ? '' : 's'}` }
  }

  const midnight = new Date(now)
  midnight.setHours(0, 0, 0, 0)
  const days = Math.round((new Date(next).setHours(0, 0, 0, 0) - midnight) / 86400000)

  if (days === 0) return { rank, state: 'today', short: `Today, ${clock(next)}`, long: `today at ${clock(next)}` }
  if (days === 1) return { rank, state: 'ahead', short: `Tomorrow, ${clock(next)}`, long: `tomorrow at ${clock(next)}` }

  const name = DAY_LABEL[next.getDay()]
  return { rank, state: 'ahead', short: `${name}, ${clock(next)}`, long: `${name} at ${clock(next)}` }
}

/* Every [data-when] on the page — the homepage cards and the what's-on rows
   share one engine, so the two can never disagree.
 *
 * The static human line stays in the markup and is never replaced. Everything
 * here is additive, so with JavaScript off the page still reads correctly; it
 * simply stops volunteering what is on tonight. */
const initGatherings = () => {
  const els = [...document.querySelectorAll('[data-when]')]
  if (!els.length) return

  const strip = document.querySelector('[data-next-strip]')
  const stripLabel = document.querySelector('[data-next-label]')
  const stripName = document.querySelector('[data-next-name]')

  const tick = () => {
    const now = new Date()
    let best = null

    els.forEach((el) => {
      const w = parseWhen(el.dataset.when)
      const badge = el.querySelector('[data-status]')
      if (!w) return

      const d = describe(w, now)
      el.classList.toggle('is-now', d.state === 'now')
      el.classList.toggle('is-soon', d.state === 'soon')
      el.classList.remove('is-next')

      if (badge) {
        badge.textContent = d.short
        badge.hidden = false
        badge.dataset.state = d.state
      }

      if (!best || d.rank < best.d.rank) best = { el, d, w }
    })

    if (!best) return

    // Only one thing can be "next", and it is whatever happens soonest — which
    // on a Sunday morning is the thing already running.
    best.el.classList.add('is-next')

    if (strip && stripLabel && stripName) {
      const title = best.el.querySelector('h3')?.firstChild?.textContent?.trim() ?? ''
      stripLabel.textContent = best.d.state === 'now' ? 'On now:' : 'Next up:'
      stripName.textContent = best.d.state === 'now'
        ? `${title}, ${best.d.long}`
        : `${title}, ${best.d.long}`
      strip.hidden = false
    }
  }

  tick()
  // A page left open overnight would otherwise still be advertising yesterday.
  setInterval(tick, 60000)
}

/* Dated one-offs mark themselves as past. A "coming up" list quietly listing
   last Easter is the single most common way a church website looks abandoned. */
const initEvents = () => {
  const events = document.querySelectorAll('.event[data-date]')
  if (!events.length) return

  const now = Date.now()
  events.forEach((el) => {
    const when = Date.parse(el.dataset.date)
    if (Number.isNaN(when)) return
    const passed = when < now
    el.classList.toggle('is-passed', passed)
    const flag = el.querySelector('[data-passed]')
    if (flag) flag.hidden = !passed
  })
}

/* Series filter for the talk archive. */
const initTalkFilter = () => {
  const list = document.querySelector('[data-talk-list]')
  const buttons = [...document.querySelectorAll('[data-series-filter]')]
  const empty = document.querySelector('[data-talk-empty]')
  if (!list || !buttons.length) return

  buttons.forEach((btn) => {
    btn.addEventListener('click', () => {
      const want = btn.dataset.seriesFilter
      buttons.forEach((b) => b.classList.toggle('is-on', b === btn))

      let shown = 0
      list.querySelectorAll('.talk').forEach((talk) => {
        const match = want === 'all' || talk.dataset.series === want
        talk.hidden = !match
        if (match) shown += 1
      })
      if (empty) empty.hidden = shown > 0
    })
  })
}

onReady(() => {
  initBase()
  initGatherings()
  initEvents()
  initTalkFilter()
})
