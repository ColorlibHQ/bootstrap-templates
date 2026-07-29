/*!
 * Bootstrap 6 template kit — shared base JS
 * Bootstrap 6.0.0-alpha1 (pinned 59cee6c)
 *
 * Bootstrap 6 is ESM-only: there is no `window.bootstrap`, and importing the
 * bundle for its side effects is what registers the data-attribute API
 * (data-bs-toggle="dialog" | "drawer" | "menu" | "combobox" | "datepicker" …).
 * Tooltip, Popover and Toast stay opt-in and must be constructed.
 */

import { Tooltip, Popover, Toast } from '../vendor/bootstrap6/js/bootstrap.bundle.min.js'

/* Color mode — v6 has no $enable-dark-mode Sass flag; dark is always compiled
   and switched at runtime with data-bs-theme on <html>. */
export const initColorMode = (storageKey = 'bs6-theme') => {
  const toggle = document.getElementById('themeToggle')
  if (!toggle) return

  const root = document.documentElement
  const stored = localStorage.getItem(storageKey)
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')

  const apply = (mode) => {
    root.setAttribute('data-bs-theme', mode)
    toggle.setAttribute('aria-pressed', String(mode === 'dark'))
  }

  apply(stored ?? (prefersDark.matches ? 'dark' : 'light'))

  toggle.addEventListener('click', () => {
    const next = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'
    localStorage.setItem(storageKey, next)
    apply(next)
  })

  prefersDark.addEventListener('change', (e) => {
    if (!localStorage.getItem(storageKey)) apply(e.matches ? 'dark' : 'light')
  })
}

/* Sticky header — CSS position:sticky can't report when it stuck, so watch a
   zero-height sentinel at the top of the document. */
export const initStickyHeader = () => {
  const header = document.querySelector('.site-header')
  if (!header) return

  const sentinel = document.createElement('div')
  sentinel.setAttribute('aria-hidden', 'true')
  document.body.prepend(sentinel)

  new IntersectionObserver(
    ([entry]) => header.classList.toggle('is-stuck', !entry.isIntersecting),
    { threshold: 0 }
  ).observe(sentinel)
}

/* Close the mobile drawer after tapping an in-page link */
export const initDrawerAutoClose = () => {
  document.querySelectorAll('dialog.drawer').forEach((drawer) => {
    drawer.addEventListener('click', (e) => {
      if (e.target.closest('a[href^="#"]')) drawer.close()
    })
  })
}

export const initTooltips = () => {
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach((el) => Tooltip.getOrCreateInstance(el))
}

export const initPopovers = () => {
  document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach((el) => Popover.getOrCreateInstance(el))
}

export const initYear = () => {
  document.querySelectorAll('[data-year]')
    .forEach((el) => { el.textContent = String(new Date().getFullYear()) })
}

/* Frontend-only form handling.
   v6 replaces .needs-validation / .was-validated with the data-bs-validate
   attribute plus native :user-invalid. Never call reportValidity() — novalidate
   is on the form precisely to suppress the browser bubbles so .invalid-feedback
   can show instead. */
export const initDemoForms = () => {
  document.querySelectorAll('form[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault()

      if (!form.checkValidity()) {
        form.querySelector(':invalid')?.focus()
        return
      }

      const btn = form.querySelector('[type="submit"]')
        || document.querySelector(`[form="${form.id}"]`)
      if (!btn) return

      const original = btn.textContent
      btn.disabled = true
      btn.textContent = btn.dataset.doneText || 'Sent ✓'

      window.setTimeout(() => {
        btn.disabled = false
        btn.textContent = original
        form.reset()
        form.closest('dialog.dialog')?.close()
      }, 1400)
    })
  })
}

/* Run the whole standard set. Templates call this, then add their own. */
export const initBase = () => {
  initColorMode()
  initStickyHeader()
  initDrawerAutoClose()
  initTooltips()
  initPopovers()
  initDemoForms()
  initYear()
}

export const onReady = (fn) => {
  document.readyState === 'loading'
    ? document.addEventListener('DOMContentLoaded', fn)
    : fn()
}

export { Toast }
