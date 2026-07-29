/*!
 * Roundtable — Bootstrap 6 community forum
 */

import { initBase, onReady } from './base.js'

/* Hot / New / Top, genuinely reordering the board.
 *
 * Forum templates ship three tabs over one hardcoded order, so switching them
 * changes the underline and nothing else. Here each thread carries its votes,
 * age and reply count, and the sort is computed:
 *
 *   hot = (votes − 1) ÷ (hours + 2)^1.5
 *
 * That is the shape Hacker News uses. The +2 stops a brand-new thread with one
 * vote dividing by nearly zero and pinning itself to the top; the exponent is
 * what lets a young thread overtake an older, better-voted one. Tick "show the
 * ranking maths" and the score is printed on each row, which is the honest way
 * to demonstrate that the control does something.
 */
const initBoard = () => {
  const list = document.querySelector('[data-threads]')
  if (!list) return

  const rows = [...list.querySelectorAll('[data-thread]')]
  const buttons = [...document.querySelectorAll('[data-sort]')]
  const showRank = document.getElementById('showRank')

  const votesOf = (el) => Number(el.querySelector('[data-vote-n]').textContent)
  const hot = (el) => (votesOf(el) - 1) / (Number(el.dataset.hours) + 2) ** 1.5

  const score = {
    hot,
    new: (el) => -Number(el.dataset.hours),
    top: (el) => votesOf(el),
  }

  let mode = 'hot'

  const render = () => {
    const ranked = [...rows].sort((a, b) => score[mode](b) - score[mode](a))
    // Re-appending a node that is already a child moves it, so this reorders
    // in place without rebuilding the list or losing focus.
    ranked.forEach((el) => list.append(el))

    rows.forEach((el) => {
      const out = el.querySelector('[data-rank-out]')
      if (!out) return
      out.hidden = !showRank?.checked
      out.textContent = `hot ${hot(el).toFixed(2)} · ${votesOf(el)} votes · ${el.dataset.hours}h`
    })
  }

  buttons.forEach((b) => {
    b.addEventListener('click', () => {
      mode = b.dataset.sort
      buttons.forEach((o) => {
        const on = o === b
        o.classList.toggle('is-on', on)
        o.setAttribute('aria-pressed', String(on))
      })
      render()
    })
  })

  showRank?.addEventListener('change', render)
  render()
}

/* Vote buttons. Toggling, because a vote you cannot take back is a bad vote —
   and the board re-sorts underneath so the effect on ranking is visible. */
const initVotes = () => {
  document.querySelectorAll('.vote-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      const out = btn.parentElement.querySelector('[data-vote-n]')
      const on = btn.getAttribute('aria-pressed') === 'true'
      btn.setAttribute('aria-pressed', String(!on))
      btn.classList.toggle('is-on', !on)
      out.textContent = Number(out.textContent) + (on ? -1 : 1)
      btn.closest('[data-threads]')?.dispatchEvent(new CustomEvent('revote'))
    })
  })
}

onReady(() => {
  initBase()
  initVotes()
  initBoard()
  // A vote changes the ranking, so the board restacks.
  document.querySelector('[data-threads]')
    ?.addEventListener('revote', () => document.querySelector('.sort-btn.is-on')?.click())
})
