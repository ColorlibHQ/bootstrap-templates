/*!
 * Lantern — Bootstrap 6 hotel & resort template
 */

import { initBase, onReady } from './base.js'

/* Guest counter beside the date fields. A plain input-group rather than a
   number input, because iOS renders the spinner too small to hit and the
   readonly field keeps the value inside the range without validation. */
const initGuestStepper = () => {
  const field = document.getElementById('bkGuests')
  if (!field) return

  const MIN = 1
  const MAX = 8

  document.querySelectorAll('[data-guest-step]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const delta = Number(btn.dataset.guestStep)
      const next = Math.min(MAX, Math.max(MIN, Number(field.value || 1) + delta))
      field.value = String(next)
      field.setAttribute('aria-label', `${next} ${next === 1 ? 'guest' : 'guests'}`)
      updateSummary()
    })
  })
}

/* Reads the two datepicker fields and reports the length of stay. The pickers
   write a plain date string into the input, so this parses rather than reaching
   into the component instance. */
const readStay = () => {
  const inEl = document.getElementById('bkIn')
  const outEl = document.getElementById('bkOut')
  if (!inEl || !outEl || !inEl.value || !outEl.value) return null

  const a = new Date(inEl.value)
  const b = new Date(outEl.value)
  if (Number.isNaN(a.getTime()) || Number.isNaN(b.getTime())) return null

  const nights = Math.round((b - a) / 86400000)
  return nights > 0 ? nights : null
}

const updateSummary = () => {
  const note = document.getElementById('bkNights')
  const dock = document.getElementById('dockSummary')
  const guests = document.getElementById('bkGuests')?.value ?? '2'
  const nights = readStay()

  if (!nights) {
    if (dock) dock.textContent = 'Add dates for live rates'
    return
  }

  const line = `${nights} ${nights === 1 ? 'night' : 'nights'} · ${guests} ${guests === '1' ? 'guest' : 'guests'}`
  if (dock) dock.textContent = line
  if (note) note.innerHTML = `<strong class="fg-1">${line}</strong> — best rate guaranteed when you book direct`
}

const initStayLength = () => {
  const inEl = document.getElementById('bkIn')
  const outEl = document.getElementById('bkOut')
  if (!inEl || !outEl) return

  // The datepicker writes the value programmatically, which fires no input
  // event in every browser, so watch the attribute as well as the events.
  ;[inEl, outEl].forEach((el) => {
    el.addEventListener('change', updateSummary)
    el.addEventListener('input', updateSummary)
    new MutationObserver(updateSummary).observe(el, { attributes: true, attributeFilter: ['value'] })
  })
}

/* The booking bar straddles the hero seam. Once it scrolls out of view a
   compact version docks to the top — IntersectionObserver rather than a scroll
   handler so it costs nothing while idle. */
const initBookDock = () => {
  const bar = document.getElementById('bookBar')
  const dock = document.getElementById('bookDock')
  if (!bar || !dock) return

  new IntersectionObserver(
    ([entry]) => dock.classList.toggle('is-docked', !entry.isIntersecting),
    { rootMargin: '-80px 0px 0px 0px', threshold: 0 },
  ).observe(bar)

  dock.querySelector('[data-scroll-top]')?.addEventListener('click', (e) => {
    e.preventDefault()
    bar.scrollIntoView({ behavior: 'smooth', block: 'center' })
    bar.querySelector('input')?.focus({ preventScroll: true })
  })
}

/* Gallery lightbox. One dialog, re-pointed at whichever thumbnail was clicked. */
const initLightbox = () => {
  const dialog = document.getElementById('lightbox')
  const img = document.getElementById('lightboxImg')
  const cap = document.getElementById('lightboxCap')
  if (!dialog || !img) return

  document.querySelectorAll('[data-bs-target="#lightbox"]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const source = btn.querySelector('img')
      if (source) {
        img.src = source.src
        img.alt = source.alt
      }
      if (cap) cap.textContent = btn.dataset.cap || 'Gallery'
    })
  })
}

onReady(() => {
  initBase()
  initGuestStepper()
  initStayLength()
  initBookDock()
  initLightbox()
})
