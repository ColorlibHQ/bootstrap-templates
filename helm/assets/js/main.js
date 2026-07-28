/*!
 * Helm — Bootstrap 6 admin dashboard
 */

import { initBase, onReady } from './base.js'

/* Collapse the sidebar to an icon rail. The choice is remembered, because an
   admin tool is somewhere people live all day and re-collapsing it on every
   page load gets old fast. */
const initRail = () => {
  const app = document.getElementById('app')
  const btn = document.getElementById('railToggle')
  if (!app || !btn) return

  const KEY = 'helm-rail'
  const apply = (railed) => {
    app.classList.toggle('is-railed', railed)
    btn.setAttribute('aria-pressed', String(railed))
    btn.setAttribute('aria-label', railed ? 'Expand sidebar' : 'Collapse sidebar')
  }

  apply(localStorage.getItem(KEY) === '1')

  btn.addEventListener('click', () => {
    const railed = !app.classList.contains('is-railed')
    apply(railed)
    try { localStorage.setItem(KEY, railed ? '1' : '0') } catch { /* private mode */ }
  })
}

/* Search box over the orders table. Same approach as the tables pack: filter the
   rows already in the DOM, so the table still reads correctly without JS. */
const initFilter = () => {
  const input = document.querySelector('[data-filter-text]')
  const table = input?.closest('.panel')?.querySelector('table')
  if (!input || !table?.tBodies[0]) return

  const rows = [...table.tBodies[0].rows]
  const count = document.querySelector('[data-filter-count]')
  const empty = document.querySelector('[data-filter-empty]')

  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase()
    let shown = 0
    for (const row of rows) {
      const hit = !q || row.textContent.toLowerCase().includes(q)
      row.hidden = !hit
      if (hit) shown += 1
    }
    if (count) count.textContent = `${shown} of ${rows.length}`
    if (empty) empty.hidden = shown !== 0
  })
}

/* Row selection with a bulk-action bar. */
const initSelect = () => {
  const scope = document.querySelector('[data-selectable]')
  if (!scope) return

  const all = scope.querySelector('#checkAll')
  const boxes = [...scope.querySelectorAll('[data-row-check]')]
  const bar = scope.querySelector('[data-bulk-bar]')
  const count = scope.querySelector('[data-bulk-count]')
  if (!boxes.length) return

  const sync = () => {
    const n = boxes.filter((b) => b.checked).length
    if (all) {
      all.checked = n === boxes.length && n > 0
      all.indeterminate = n > 0 && n < boxes.length
    }
    if (bar) bar.hidden = n === 0
    if (count) count.textContent = `${n} selected`
    boxes.forEach((b) => b.closest('tr')?.classList.toggle('table-active', b.checked))
  }

  all?.addEventListener('change', () => {
    boxes.forEach((b) => { b.checked = all.checked })
    sync()
  })
  boxes.forEach((b) => b.addEventListener('change', sync))
  sync()
}

onReady(() => {
  initBase()
  initRail()
  initFilter()
  initSelect()
})
