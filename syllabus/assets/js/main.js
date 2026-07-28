/*!
 * Syllabus — Bootstrap 6 course template
 */

import { initBase, onReady } from './base.js'

const KEY = 'syllabus-progress'

const hhmm = (mins) => {
  const h = Math.floor(mins / 60)
  const m = Math.round(mins % 60)
  if (h && m) return `${h}h ${m}m`
  return h ? `${h}h` : `${m}m`
}

/* Course progress and pace planner.
 *
 * Course pages list a curriculum and leave it at that, so the two questions a
 * student actually has — how much is left, and when would I finish — go
 * unanswered. Lessons here tick off, the ticks persist, and an hours-a-week
 * slider turns what remains into a date.
 *
 * State lives in localStorage and nowhere else: no account, no request. That is
 * a real trade rather than a shortcut, so the footer says so plainly.
 *
 * Lesson identity is `data-lesson`, not the element id — the sidebar on the
 * lesson page repeats lessons from the landing page and its ids are prefixed so
 * that each <label> still points at its own control.
 */
const initProgress = () => {
  const boxes = [...document.querySelectorAll('[data-lesson]')]
  if (!boxes.length) return

  let durations = {}
  try { durations = JSON.parse(document.body.dataset.lessons ?? '{}') } catch { /* falls back to DOM */ }

  const ids = Object.keys(durations)
  const totalLessons = ids.length || boxes.length
  const totalMin = ids.length
    ? ids.reduce((s, k) => s + durations[k], 0)
    : boxes.reduce((s, b) => s + Number(b.dataset.min || 0), 0)

  const load = () => {
    try { return new Set(JSON.parse(localStorage.getItem(KEY) ?? '[]')) } catch { return new Set() }
  }
  const save = (set) => {
    try { localStorage.setItem(KEY, JSON.stringify([...set])) } catch { /* private mode — session only */ }
  }

  let done = load()

  const pace = document.getElementById('paceHours')
  const paceOut = document.getElementById('paceOut')

  const render = () => {
    // Every checkbox for a lesson reflects the same state, on either page.
    boxes.forEach((b) => { b.checked = done.has(b.dataset.lesson) })

    const doneMin = [...done].reduce((s, id) => s + (durations[id] ?? 0), 0)
    const leftMin = Math.max(0, totalMin - doneMin)
    const pct = totalLessons ? Math.round((done.size / totalLessons) * 100) : 0

    document.querySelectorAll('[data-done]').forEach((el) => { el.textContent = done.size })
    document.querySelectorAll('[data-remaining]').forEach((el) => { el.textContent = hhmm(leftMin) })
    document.querySelectorAll('[data-bar]').forEach((el) => { el.style.width = `${pct}%` })
    document.querySelectorAll('[data-bar-wrap]').forEach((el) => { el.setAttribute('aria-valuenow', String(pct)) })

    // Per-module counts, from the boxes that module actually contains.
    document.querySelectorAll('.module, .rail-module').forEach((mod) => {
      const out = mod.querySelector('[data-module-done]')
      if (!out) return
      const inMod = [...mod.querySelectorAll('[data-lesson]')]
      out.textContent = String(inMod.filter((b) => done.has(b.dataset.lesson)).length)
    })

    const eta = document.querySelector('[data-eta]')
    if (!eta) return

    if (leftMin === 0) {
      eta.textContent = 'Finished — every lesson ticked off. Go and set something.'
      return
    }

    const hours = Number(pace?.value ?? 3)
    if (paceOut) paceOut.textContent = `${hours} hour${hours === 1 ? '' : 's'}`

    const weeks = leftMin / 60 / hours
    const end = new Date()
    end.setDate(end.getDate() + Math.ceil(weeks * 7))
    const when = end.toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' })

    eta.innerHTML = weeks < 1
      ? `At ${hours} hour${hours === 1 ? '' : 's'} a week you would finish <strong>this week</strong>.`
      : `At ${hours} hour${hours === 1 ? '' : 's'} a week that is about <strong>${Math.ceil(weeks)} week${Math.ceil(weeks) === 1 ? '' : 's'}</strong> — finishing around <strong>${when}</strong>.`
  }

  boxes.forEach((b) => {
    b.addEventListener('change', () => {
      if (b.checked) done.add(b.dataset.lesson)
      else done.delete(b.dataset.lesson)
      save(done)
      render()
    })
  })

  pace?.addEventListener('input', render)

  document.querySelector('[data-reset]')?.addEventListener('click', () => {
    done = new Set()
    save(done)
    render()
  })

  // Another tab ticking a lesson should not leave this one lying.
  window.addEventListener('storage', (e) => {
    if (e.key !== KEY) return
    done = load()
    render()
  })

  render()
}

onReady(() => {
  initBase()
  initProgress()
})
