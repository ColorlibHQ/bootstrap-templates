/*!
 * Liftoff — Bootstrap 6 coming-soon template
 */

import { initBase, onReady } from './base.js'

/* Countdown to the launch date held in data-countdown. Reads the target off the
   markup rather than a constant here, so changing the date is an HTML edit and
   the three layouts can never disagree about when launch is.

   aria-live is off deliberately: a per-second live region is unusable with a
   screen reader. The launch date is stated in text elsewhere on every layout. */
const initCountdown = () => {
  const el = document.querySelector('[data-countdown]')
  if (!el) return

  const target = Date.parse(el.dataset.countdown)
  if (Number.isNaN(target)) return

  const cells = {
    D: document.getElementById('cdD'),
    H: document.getElementById('cdH'),
    M: document.getElementById('cdM'),
    S: document.getElementById('cdS'),
  }
  if (!cells.D) return

  const pad = (n) => String(Math.max(0, n)).padStart(2, '0')

  const tick = () => {
    const left = Math.max(0, target - Date.now())
    const s = Math.floor(left / 1000)
    cells.D.textContent = pad(Math.floor(s / 86400))
    cells.H.textContent = pad(Math.floor(s / 3600) % 24)
    cells.M.textContent = pad(Math.floor(s / 60) % 60)
    cells.S.textContent = pad(s % 60)
    return left > 0
  }

  // Only start ticking if the launch is still ahead: past dates render zeros once.
  if (!tick()) return
  const timer = setInterval(() => { if (!tick()) clearInterval(timer) }, 1000)
}

onReady(() => {
  initBase()
  initCountdown()
})
