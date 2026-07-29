/*!
 * Threshold — Bootstrap 6 landing page
 */

import { initBase, onReady } from './base.js'

/* One capture form, rendered three times, sharing one value.
 *
 * A landing page puts an email field in the hero, another in the closer, and a
 * third in a sticky bar — and in every template they are three unrelated
 * inputs. So somebody types half an address, scrolls, and the sticky bar hands
 * them an empty box. This keeps them in step: type anywhere, and every copy
 * has it.
 *
 * Not a framework and not state management — one input event and a loop. */
const initSignup = () => {
  const inputs = [...document.querySelectorAll('[data-signup-input]')]
  if (inputs.length < 2) return

  inputs.forEach((input) => {
    input.addEventListener('input', () => {
      inputs.forEach((other) => {
        if (other !== input) other.value = input.value
      })
    })
  })
}

/* The sticky bar appears when the hero form leaves the viewport, and hides
   again over the closer — a second call to action stacked on top of the real
   one is just clutter. IntersectionObserver rather than a scroll handler, so
   nothing runs on frames where nothing changed. */
const initSticky = () => {
  const bar = document.querySelector('[data-sticky]')
  const hero = document.querySelector('.hero .signup')
  const closer = document.querySelector('.closer')
  if (!bar || !hero) return

  let heroGone = false
  let atCloser = false

  const apply = () => { bar.hidden = !(heroGone && !atCloser) }

  new IntersectionObserver(([e]) => { heroGone = !e.isIntersecting; apply() }, { threshold: 0 }).observe(hero)

  if (closer) {
    new IntersectionObserver(([e]) => { atCloser = e.isIntersecting; apply() }, { threshold: 0.15 }).observe(closer)
  }
}

/* Copy to clipboard, with the fallback that matters: the async Clipboard API
   is unavailable on insecure origins, which includes the file:// and plain-http
   previews people open a template with. */
const initCopy = () => {
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const field = document.querySelector(btn.dataset.copy)
      if (!field) return

      try {
        await navigator.clipboard.writeText(field.value)
      } catch {
        field.select()
        field.setSelectionRange(0, 99999)
        document.execCommand?.('copy')
      }

      const original = btn.textContent
      btn.textContent = btn.dataset.doneText || 'Copied'
      setTimeout(() => { btn.textContent = original }, 1600)
    })
  })
}

onReady(() => {
  initBase()
  initSignup()
  initSticky()
  initCopy()
})
