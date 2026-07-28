/*!
 * Longhand — Bootstrap 6 personal site and CV
 */

import { initBase, onReady } from './base.js'

/* "Print CV" is window.print(), and that is the whole implementation.
 *
 * No PDF library, no server round trip, no canvas screenshot. The print
 * stylesheet does the work, so the browser's own dialogue produces a properly
 * set one-page CV — and "Save as PDF" in that dialogue gives a real text PDF
 * that a recruiter's system can actually parse, rather than an image of one. */
const initPrint = () => {
  document.querySelectorAll('[data-print]').forEach((btn) => {
    btn.addEventListener('click', () => window.print())
  })
}

onReady(() => {
  initBase()
  initPrint()
})
