/*!
 * Shortlist — Bootstrap 6 job board template
 */

import { initBase, onReady } from "./base.js"

/* Salary-floor slider readout. The value is money, so it is formatted as money
   rather than shown as a raw number — 45000 in a filter reads as a typo. */
const initRanges = () => {
  document.querySelectorAll("[data-range-out]").forEach((r) => {
    const out = document.getElementById(r.dataset.rangeOut)
    if (!out) return
    const sync = () => {
      out.textContent = "\u00a3" + Number(r.value).toLocaleString("en-GB")
    }
    r.addEventListener("input", sync)
    sync()
  })
}

onReady(() => {
  initBase()
  initRanges()
})
