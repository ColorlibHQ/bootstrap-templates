/*!
 * Commerce — Bootstrap 6 e-commerce template
 */

import { initBase, onReady } from './base.js'

/* Price filter readout */
const initPriceFilter = () => {
  const range = document.getElementById('priceRange')
  const out = document.getElementById('priceOut')
  if (!range || !out) return

  const sync = () => { out.textContent = `$${range.value}` }
  range.addEventListener('input', sync)
  sync()
}

/* Product gallery — thumbnails swap the main image label */
const initGallery = () => {
  const main = document.getElementById('galleryMain')
  const thumbs = document.querySelectorAll('.gallery-thumb')
  if (!main || !thumbs.length) return

  thumbs.forEach((thumb) => {
    thumb.addEventListener('click', () => {
      thumbs.forEach((t) => t.classList.remove('is-active'))
      thumb.classList.add('is-active')
      main.textContent = thumb.dataset.label || main.textContent
    })
  })
}

/* Quantity stepper */
const initQty = () => {
  document.querySelectorAll('.qty').forEach((qty) => {
    const out = qty.querySelector('output')
    if (!out) return

    qty.addEventListener('click', (e) => {
      const step = e.target.closest('[data-step]')
      if (!step) return
      const next = Math.max(1, Number(out.value) + Number(step.dataset.step))
      out.value = String(next)
    })
  })
}

/* Checkout — three steps driven by the Stepper component.
   Each .stepper-item gets .active up to the current step; panels toggle [hidden]. */
const initCheckout = () => {
  const steps = document.querySelectorAll('#checkoutStepper .stepper-item')
  const panels = document.querySelectorAll('.checkout-step')
  if (!steps.length || !panels.length) return

  let current = 0

  const render = () => {
    steps.forEach((s, i) => s.classList.toggle('active', i <= current))
    panels.forEach((p, i) => { p.hidden = i !== current })
    document.getElementById('main')?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }

  document.querySelectorAll('[data-checkout-next]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const panel = panels[current]
      const form = panel.querySelector('form')

      // v6 relies on native :user-invalid for styling; don't call reportValidity()
      if (form && !form.checkValidity()) {
        form.querySelector(':invalid')?.focus()
        return
      }

      if (current < panels.length - 1) { current += 1; render() }
    })
  })

  document.querySelectorAll('[data-checkout-back]').forEach((btn) => {
    btn.addEventListener('click', () => {
      if (current > 0) { current -= 1; render() }
    })
  })

  render()
}

onReady(() => {
  initBase()
  initPriceFilter()
  initGallery()
  initQty()
  initCheckout()
})
