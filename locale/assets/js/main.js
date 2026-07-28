/*!
 * Locale — Bootstrap 6 directory template
 */

import { initBase, onReady } from './base.js'

const bindRange = (rangeId, outId, format) => {
  const range = document.getElementById(rangeId)
  const out = document.getElementById(outId)
  if (!range || !out) return

  const sync = () => { out.textContent = format(range.value) }
  range.addEventListener('input', sync)
  sync()
}

/* Hovering a listing highlights its map pin */
const initMapSync = () => {
  const pins = document.querySelectorAll('.map-pin')
  const listings = document.querySelectorAll('.listing')
  if (!pins.length || !listings.length) return

  listings.forEach((listing, i) => {
    const pin = pins[i]
    if (!pin) return
    const on = () => { pins.forEach((p) => p.classList.remove('is-active')); pin.classList.add('is-active') }
    listing.addEventListener('mouseenter', on)
    listing.addEventListener('focusin', on)
  })
}

onReady(() => {
  initBase()
  bindRange('ratingRange', 'ratingOut', (v) => Number(v).toFixed(1))
  initMapSync()
})
