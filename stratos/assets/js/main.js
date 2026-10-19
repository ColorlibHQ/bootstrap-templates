/*!
 * Stratos — SaaS landing template
 * Bootstrap 6.0.0-alpha1
 *
 * Bootstrap 6 is ESM-only. There is no `window.bootstrap` global any more,
 * so anything we need must be imported explicitly. Importing the bundle for
 * its side effects is what registers the data-attribute API
 * (data-bs-toggle="dialog", "drawer", "menu", …).
 */

import { Tooltip, Popover, Toast } from 'bootstrap'

/* ---------------------------------------------------------------
   Opt-in plugins
   Tooltip and Popover are never auto-initialised — they have to be
   constructed for each trigger, exactly as in v5.
   --------------------------------------------------------------- */

const initTooltips = () => {
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
    .forEach((el) => Tooltip.getOrCreateInstance(el))
}

const initPopovers = () => {
  document.querySelectorAll('[data-bs-toggle="popover"]')
    .forEach((el) => Popover.getOrCreateInstance(el))
}

const initToastDemo = () => {
  const btn = document.getElementById('toastBtn')
  const el = document.getElementById('demoToast')
  if (!btn || !el) return

  const toast = Toast.getOrCreateInstance(el)
  btn.addEventListener('click', () => toast.show())
}

/* ---------------------------------------------------------------
   Color mode
   v6 has no $enable-dark-mode Sass flag — dark is always compiled
   and switched at runtime with data-bs-theme on <html>.
   --------------------------------------------------------------- */

const initColorMode = () => {
  const toggle = document.getElementById('themeToggle')
  if (!toggle) return

  const root = document.documentElement
  const stored = localStorage.getItem('stratos-theme')
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')

  const apply = (mode) => {
    root.setAttribute('data-bs-theme', mode)
    toggle.setAttribute('aria-pressed', String(mode === 'dark'))
  }

  apply(stored ?? (prefersDark.matches ? 'dark' : 'light'))

  toggle.addEventListener('click', () => {
    const next = root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'
    localStorage.setItem('stratos-theme', next)
    apply(next)
  })

  // Follow the OS only while the visitor hasn't made an explicit choice.
  prefersDark.addEventListener('change', (event) => {
    if (localStorage.getItem('stratos-theme')) return
    apply(event.matches ? 'dark' : 'light')
  })
}

/* ---------------------------------------------------------------
   Sticky header
   CSS position:sticky alone can't tell us when it has stuck, so we
   watch a zero-height sentinel at the top of the document.
   --------------------------------------------------------------- */

const initStickyHeader = () => {
  const header = document.getElementById('siteHeader')
  if (!header) return

  const sentinel = document.createElement('div')
  sentinel.setAttribute('aria-hidden', 'true')
  document.body.prepend(sentinel)

  new IntersectionObserver(
    ([entry]) => header.classList.toggle('is-stuck', !entry.isIntersecting),
    { threshold: 0 }
  ).observe(sentinel)
}

/* ---------------------------------------------------------------
   Pricing: monthly / yearly
   --------------------------------------------------------------- */

const initPricingToggle = () => {
  const toggle = document.getElementById('billingToggle')
  const grid = document.getElementById('pricingGrid')
  if (!toggle || !grid) return

  const monthly = document.getElementById('billMonthly')
  const yearly = document.getElementById('billYearly')

  const sync = () => {
    grid.classList.toggle('is-yearly', toggle.checked)
    monthly?.classList.toggle('is-active', !toggle.checked)
    yearly?.classList.toggle('is-active', toggle.checked)
  }

  toggle.addEventListener('change', sync)
  sync()
}

/* ---------------------------------------------------------------
   Signup form
   v6 replaces .needs-validation / .was-validated with the
   data-bs-validate attribute and native :user-invalid styling,
   so there is no class juggling left to do here.
   --------------------------------------------------------------- */

const initSignupForm = () => {
  const form = document.getElementById('signupForm')
  if (!form) return

  form.addEventListener('submit', (event) => {
    event.preventDefault()

    if (!form.checkValidity()) {
      // Don't call reportValidity() — `novalidate` is on the form precisely to
      // suppress the browser's bubbles so Bootstrap's :user-invalid styling and
      // .invalid-feedback can show instead. Just move focus to the first problem.
      form.querySelector(':invalid')?.focus()
      return
    }

    // Frontend-only template: swap this for a real endpoint.
    const submit = document.querySelector('[form="signupForm"]')
    if (submit) {
      submit.disabled = true
      submit.textContent = 'Workspace created ✓'
    }

    window.setTimeout(() => {
      document.getElementById('signupDialog')?.close()
      form.reset()
      if (submit) {
        submit.disabled = false
        submit.textContent = 'Create workspace'
      }
    }, 1200)
  })
}

/* ---------------------------------------------------------------
   Close the mobile drawer after tapping an in-page link
   --------------------------------------------------------------- */

const initDrawerAutoClose = () => {
  const drawer = document.getElementById('navDrawer')
  if (!drawer) return

  drawer.addEventListener('click', (event) => {
    const link = event.target.closest('a[href^="#"]')
    if (link) drawer.close()
  })
}

/* ---------------------------------------------------------------
   Footer year
   --------------------------------------------------------------- */

const initYear = () => {
  const el = document.getElementById('year')
  if (el) el.textContent = String(new Date().getFullYear())
}

/* --------------------------------------------------------------- */

const init = () => {
  initColorMode()
  initStickyHeader()
  initPricingToggle()
  initSignupForm()
  initDrawerAutoClose()
  initTooltips()
  initPopovers()
  initToastDemo()
  initYear()
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', init)
} else {
  init()
}
