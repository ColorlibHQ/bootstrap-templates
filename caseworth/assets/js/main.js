/*!
 * Caseworth — Bootstrap 6 law & accountancy template
 *
 * Deliberately thin. This template's whole argument is typographic, so the only
 * behaviour beyond the shared base is the fee-table filter — everything else is
 * native: <details> accordions, a native <dialog> drawer, CSS-only sticky rails.
 */

import { initBase, onReady } from './base.js'

/* Filters the published fee table by matter name. Professional-services fee
   tables get long, and a client arriving from search usually has one matter in
   mind. Hides rows rather than rebuilding the table so the markup stays static
   and the table remains readable with JavaScript off. */
const initFeeFilter = () => {
  const input = document.getElementById('feeFilter')
  const table = document.getElementById('feeTable')
  if (!input || !table) return

  const rows = [...table.tBodies[0].rows]
  const empty = document.getElementById('feeEmpty')

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase()
    let shown = 0
    for (const row of rows) {
      const hit = !q || row.textContent.toLowerCase().includes(q)
      row.hidden = !hit
      if (hit) shown += 1
    }
    if (empty) empty.hidden = shown !== 0
  })
}

onReady(() => {
  initBase()
  initFeeFilter()
})
