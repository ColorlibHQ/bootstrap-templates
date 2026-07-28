/*!
 * Summit — Bootstrap 6 conference template
 */

import { initBase, onReady } from './base.js'

/* Countdown to the conference. Swap TARGET for your own date. */
const initCountdown = () => {
  const cells = {
    d: document.getElementById('cdD'),
    h: document.getElementById('cdH'),
    m: document.getElementById('cdM'),
    s: document.getElementById('cdS'),
  }
  if (!cells.d) return

  const TARGET = new Date('2026-10-14T09:00:00Z').getTime()
  const pad = (n) => String(Math.max(0, n)).padStart(2, '0')

  const tick = () => {
    const left = Math.max(0, TARGET - Date.now())
    const s = Math.floor(left / 1000)
    cells.d.textContent = String(Math.floor(s / 86400))
    cells.h.textContent = pad(Math.floor(s / 3600) % 24)
    cells.m.textContent = pad(Math.floor(s / 60) % 60)
    cells.s.textContent = pad(s % 60)
  }

  tick()
  window.setInterval(tick, 1000)
}

onReady(() => {
  initBase()
  initCountdown()
})
