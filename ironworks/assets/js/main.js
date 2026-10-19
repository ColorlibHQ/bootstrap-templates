/*!
 * Ironworks — Bootstrap 6 gym template
 */

import { initBase, onReady } from './base.js'

/* The rail nav is desktop-only, so the mobile bar carries its own toggle.
   Both drive the same data-bs-theme attribute. */
const initMobileThemeToggle = () => {
  const btn = document.getElementById('themeToggleMobile')
  if (!btn) return

  btn.addEventListener('click', () => {
    const root = document.documentElement
    const next = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'
    localStorage.setItem('bs6-theme', next)
    root.setAttribute('data-bs-theme', next)
  })
}

/* Timetable filter: dims the slots of every other class rather than removing
   them, so the week keeps its shape and you can still see when the gym is busy. */
const initTimetableFilter = () => {
  const toggle = document.getElementById('timetableFilter')
  const table = document.getElementById('timetableGrid')
  const status = document.getElementById('timetableStatus')
  if (!toggle || !table) return

  toggle.addEventListener('change.bs.combobox', (event) => {
    const value = event.value ?? 'all'
    let shown = 0
    table.querySelectorAll('.slot[data-class]').forEach((slot) => {
      const match = value === 'all' || slot.dataset.class === value
      slot.classList.toggle('slot-dim', !match)
      if (match) shown += 1
    })
    if (status) {
      const label = event.item?.textContent.trim() ?? 'All classes'
      status.textContent = value === 'all' ? 'Showing all classes' : `Showing ${label}: ${shown} sessions this week`
    }
  })
}

onReady(() => {
  initBase()
  initMobileThemeToggle()
  initTimetableFilter()
})
