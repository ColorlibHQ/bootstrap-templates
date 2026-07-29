/*!
 * Keystone — Bootstrap 6 corporate site
 */

import { initBase, onReady } from './base.js'

/* Mega menu.
 *
 * Corporate sites have deep information architecture — four sections, several
 * columns each — and almost every Bootstrap template ships a flat five-item
 * navbar that falls apart the moment a real company uses it. This is the menu
 * that shape of business actually needs, built so it works without a mouse.
 *
 * Deliberately not hover-only. Hover menus are unreachable by keyboard, hostile
 * on touch, and open by accident when the pointer crosses them on the way
 * somewhere else. Here a click or Enter opens a panel, Escape closes it and
 * returns focus to its button, Tab out closes it, and hover only opens a panel
 * when one is ALREADY open — so moving along an open bar feels immediate
 * without a stray pointer triggering anything.
 *
 * The mobile menu needs none of this: it is nested <details> elements, which
 * are a real disclosure widget with no script behind them.
 */
const initMega = () => {
  const bar = document.querySelector('.mega-bar')
  if (!bar) return

  const toggles = [...bar.querySelectorAll('[data-mega]')]
  const panelFor = (i) => bar.querySelector(`[data-mega-panel="${i}"]`)

  const close = (i) => {
    const t = toggles.find((x) => x.dataset.mega === String(i))
    if (!t) return
    t.setAttribute('aria-expanded', 'false')
    const p = panelFor(i)
    if (p) p.hidden = true
  }

  const closeAll = () => toggles.forEach((t) => close(t.dataset.mega))

  const open = (i) => {
    closeAll()
    const t = toggles.find((x) => x.dataset.mega === String(i))
    const p = panelFor(i)
    if (!t || !p) return
    t.setAttribute('aria-expanded', 'true')
    p.hidden = false
  }

  const isOpen = () => toggles.some((t) => t.getAttribute('aria-expanded') === 'true')

  toggles.forEach((t) => {
    t.addEventListener('click', () => {
      const already = t.getAttribute('aria-expanded') === 'true'
      already ? close(t.dataset.mega) : open(t.dataset.mega)
    })

    // Only follow the pointer once the bar is already open. Opening on first
    // hover is what makes mega menus fire when you were reaching for the logo.
    t.addEventListener('mouseenter', () => { if (isOpen()) open(t.dataset.mega) })
  })

  bar.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return
    const openToggle = toggles.find((t) => t.getAttribute('aria-expanded') === 'true')
    if (!openToggle) return
    close(openToggle.dataset.mega)
    openToggle.focus()
  })

  // Tabbing or clicking beyond the menu closes it. focusout fires before the
  // new element is focused, so the check is deferred a tick.
  bar.addEventListener('focusout', () => {
    setTimeout(() => { if (!bar.contains(document.activeElement)) closeAll() }, 0)
  })

  document.addEventListener('click', (e) => { if (!bar.contains(e.target)) closeAll() })
}

onReady(() => {
  initBase()
  initMega()
})
