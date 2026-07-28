/*!
 * Bedrock — Bootstrap 6 construction & civil engineering template
 */

import { initBase, onReady } from './base.js'

/* Counts the hero statistics up when the strip first scrolls into view.
   Values are read from the rendered text so the markup stays the source of
   truth and the page still reads correctly with JavaScript off. */
const initStatCount = () => {
  const strip = document.querySelector('.stat-strip')
  if (!strip) return

  // Honour a reduced-motion preference by simply leaving the numbers alone.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

  const cells = [...strip.querySelectorAll('.stat-figure')].map((el) => {
    const raw = el.textContent.trim()
    const num = Number.parseFloat(raw.replace(/[^\d.]/g, ''))
    return Number.isNaN(num) ? null : { el, raw, num, decimals: (raw.split('.')[1] || '').length }
  }).filter(Boolean)

  if (!cells.length) return

  const run = () => {
    const DURATION = 900
    const start = performance.now()

    const frame = (now) => {
      const t = Math.min(1, (now - start) / DURATION)
      const eased = 1 - (1 - t) ** 3
      for (const c of cells) {
        const value = (c.num * eased).toFixed(c.decimals)
        // Keep whatever prefix/suffix the markup had (£, m, %) around the number.
        c.el.textContent = c.raw.replace(/[\d.]+/, value)
      }
      if (t < 1) requestAnimationFrame(frame)
    }
    requestAnimationFrame(frame)
  }

  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return
    io.disconnect()
    run()
  }, { threshold: 0.4 })

  io.observe(strip)
}

onReady(() => {
  initBase()
  initStatCount()
})
