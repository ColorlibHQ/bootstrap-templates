/*!
 * Bootstrap 6 Navigation — component pack
 */

import { initBase, onReady } from './base.js'

const initRanges = () => {
  document.querySelectorAll("[data-range-out]").forEach((r) => {
    const out = document.getElementById(r.dataset.rangeOut)
    if (!out) return
    const sync = () => { out.textContent = (r.dataset.rangePrefix || "") + r.value + (r.dataset.rangeSuffix || "") }
    r.addEventListener("input", sync)
    sync()
  })
}

onReady(() => {
  initBase()
  initRanges()
})
