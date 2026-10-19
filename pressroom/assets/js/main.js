/*!
 * Pressroom — Bootstrap 6 magazine template
 */

import { initBase, onReady } from './base.js'

/* Cities sort: reorders the story columns in place. Each column carries its
   rank for every sort as data-*, so the order lives in the markup with the
   stories rather than in a list here that could drift from them. */
const initCitiesSort = () => {
  const toggle = document.getElementById('citiesSort')
  const row = document.getElementById('citiesStories')
  if (!toggle || !row) return

  const keys = {
    new: (el) => Number(el.dataset.new),
    read: (el) => Number(el.dataset.read),
    long: (el) => -Number(el.dataset.minutes),
  }

  toggle.addEventListener('change.bs.combobox', (event) => {
    const key = keys[event.value] ?? keys.new
    const cols = [...row.querySelectorAll(':scope > [data-new]')]
    cols.sort((a, b) => key(a) - key(b)).forEach((col) => row.append(col))
  })
}

onReady(() => {
  initBase()
  initCitiesSort()
})
