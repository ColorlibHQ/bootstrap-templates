/*!
 * Openhands — Bootstrap 6 charity template
 */

import { initBase, onReady } from './base.js'

/* Donation amount → what it buys.
 *
 * "£50" means nothing on its own; "£50 pays for a week of hot meals" is the
 * entire fundraising argument. So the outcome updates the moment the amount
 * changes, right where the decision is being made.
 *
 * The tiers carry their own copy in data-buys, so adding a tier is an HTML edit
 * and the script needs no corresponding change. */
const initDonate = () => {
  const box = document.getElementById('buysBox')
  const amtOut = document.getElementById('buysAmt')
  const whatOut = document.getElementById('buysWhat')
  const custom = document.getElementById('custom')
  if (!box || !amtOut || !whatOut) return

  const radios = [...document.querySelectorAll('#amounts input[type="radio"]')]

  const showTier = (radio) => {
    amtOut.textContent = `£${radio.value}`
    whatOut.textContent = radio.dataset.buys
    box.hidden = false
  }

  radios.forEach((r) => r.addEventListener('change', () => {
    if (custom) custom.value = ''
    showTier(r)
  }))

  // A custom amount has no pre-written outcome, so rather than inventing one we
  // say what it does fund proportionally and stop claiming a specific thing.
  custom?.addEventListener('input', () => {
    const n = Number(custom.value.replace(/[^\d]/g, ''))
    if (!n) {
      const checked = radios.find((r) => r.checked)
      if (checked) showTier(checked)
      return
    }
    radios.forEach((r) => { r.checked = false })
    amtOut.textContent = `£${n.toLocaleString('en-GB')}`
    whatOut.textContent = n >= 250
      ? 'a caseworker’s time, meals and a bed — wherever the need is greatest that week'
      : 'meals, casework and emergency beds — wherever the need is greatest that week'
  })
}

onReady(() => {
  initBase()
  initDonate()
})
