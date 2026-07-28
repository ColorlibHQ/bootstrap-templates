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

onReady(() => {
  initBase()
  initMobileThemeToggle()
})
