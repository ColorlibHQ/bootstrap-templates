/*!
 * Haven Homes — Bootstrap 6 real estate template
 */

import { initBase, onReady } from './base.js'

const bindRange = (id, outId, fmt) => {
  const r = document.getElementById(id)
  const o = document.getElementById(outId)
  if (!r || !o) return
  const sync = () => { o.textContent = fmt(r.value) }
  r.addEventListener('input', sync)
  sync()
}

onReady(() => {
  initBase()
  bindRange('vlGuide', 'vlGuideOut', (v) => `£${v}k`)
  bindRange('maxPrice', 'maxPriceOut', (v) => `£${v}k`)
})
