/*!
 * Atelier — Bootstrap 6 portfolio template
 */

import { initBase, onReady } from './base.js'

const initBudget = () => {
  const range = document.getElementById('cBudget')
  const out = document.getElementById('budgetOut')
  if (!range || !out) return

  const sync = () => { out.textContent = `€${range.value}k` }
  range.addEventListener('input', sync)
  sync()
}

onReady(() => {
  initBase()
  initBudget()
})
