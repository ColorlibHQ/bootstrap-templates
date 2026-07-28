/*!
 * Cadence — Bootstrap 6 CRM dashboard
 */

import { initBase, onReady } from './base.js'

const gbp = (n) => n.toLocaleString('en-GB', {
  style: 'currency', currency: 'GBP', maximumFractionDigits: 0,
})

const short = (n) => (n >= 1_000_000 ? `£${(n / 1_000_000).toFixed(2)}m` : `£${Math.round(n / 1000)}k`)

/* Sidebar rail. Remembered, because a collapsed sidebar that springs back open
   on every navigation is worse than one that never collapsed. */
const initRail = () => {
  const btn = document.getElementById('railToggle')
  const side = document.getElementById('side')
  if (!btn || !side) return

  const apply = (on) => {
    document.body.classList.toggle('is-rail', on)
    btn.setAttribute('aria-pressed', String(on))
    btn.setAttribute('aria-label', on ? 'Expand sidebar' : 'Collapse sidebar')
  }
  apply(localStorage.getItem('cadence-rail') === '1')

  btn.addEventListener('click', () => {
    const on = !document.body.classList.contains('is-rail')
    localStorage.setItem('cadence-rail', on ? '1' : '0')
    apply(on)
  })
}

/* Weighted pipeline board.
 *
 * Every CRM template ships a kanban board with a pipeline total printed above
 * it that never changes, because the number is typed into the HTML. This one
 * derives it: each stage carries a win probability, each deal a value, and the
 * forecast is the sum of value × probability across every open deal. Move a
 * deal and all four figures follow.
 *
 * The data lives on the elements, so there is no parallel copy in the script to
 * fall out of sync with the DOM after a drag.
 *
 * Deals move by drag OR by keyboard — the arrow buttons on each card, and the
 * left/right arrow keys when a card has focus. Kanban demos almost universally
 * ship drag-only, which makes the central feature unusable without a mouse.
 */
const initBoard = () => {
  const board = document.querySelector('[data-board]')
  if (!board) return

  const columns = [...board.querySelectorAll('.col-stage')]
  const out = {
    total: document.querySelector('[data-board-total]'),
    weighted: document.querySelector('[data-board-weighted]'),
    count: document.querySelector('[data-board-count]'),
    stalled: document.querySelector('[data-board-stalled]'),
  }

  const recalc = () => {
    let total = 0
    let weighted = 0
    let count = 0
    let stalled = 0

    columns.forEach((col) => {
      const closed = col.hasAttribute('data-closed')
      const prob = Number(col.dataset.prob) / 100
      const expected = Number(col.dataset.expected)
      const deals = [...col.querySelectorAll('.deal')]
      const sum = deals.reduce((s, d) => s + Number(d.dataset.value), 0)

      col.querySelector('[data-stage-count]').textContent = deals.length
      col.querySelector('[data-stage-sum]').textContent = deals.length ? short(sum) : '—'

      deals.forEach((d) => {
        // Expected age is a property of the stage, so a deal that moves is
        // re-judged against its new column rather than the one it came from.
        const isStalled = expected > 0 && Number(d.dataset.days) > expected
        d.querySelector('.deal-age')?.classList.toggle('is-stalled', isStalled)
        if (!closed && isStalled) stalled += 1
      })

      if (closed) return
      total += sum
      weighted += sum * prob
      count += deals.length
    })

    if (out.total) out.total.textContent = short(total)
    if (out.weighted) out.weighted.textContent = short(weighted)
    if (out.count) out.count.textContent = String(count)
    if (out.stalled) out.stalled.textContent = String(stalled)
  }

  const move = (card, dir) => {
    const from = card.closest('.col-stage')
    const to = columns[columns.indexOf(from) + dir]
    if (!to) return
    to.querySelector('[data-drop]').append(card)
    recalc()
    card.focus()
  }

  board.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-move]')
    if (!btn) return
    move(btn.closest('.deal'), Number(btn.dataset.move))
  })

  board.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return
    const card = e.target.closest('.deal')
    // Only when the card itself has focus — never steal the arrow keys from a
    // button or a field inside it.
    if (!card || e.target !== card) return
    e.preventDefault()
    move(card, e.key === 'ArrowRight' ? 1 : -1)
  })

  let dragging = null

  board.addEventListener('dragstart', (e) => {
    const card = e.target.closest('.deal')
    if (!card) return
    dragging = card
    card.classList.add('is-dragging')
    e.dataTransfer.effectAllowed = 'move'
    // Firefox will not start a drag unless something is set.
    e.dataTransfer.setData('text/plain', card.dataset.deal)
  })

  board.addEventListener('dragend', () => {
    dragging?.classList.remove('is-dragging')
    board.querySelectorAll('.is-over').forEach((el) => el.classList.remove('is-over'))
    dragging = null
  })

  board.querySelectorAll('[data-drop]').forEach((zone) => {
    zone.addEventListener('dragover', (e) => {
      if (!dragging) return
      e.preventDefault()
      e.dataTransfer.dropEffect = 'move'
      zone.classList.add('is-over')
    })
    zone.addEventListener('dragleave', (e) => {
      // Moving between children fires dragleave on the zone; ignore unless the
      // pointer has genuinely left it.
      if (!zone.contains(e.relatedTarget)) zone.classList.remove('is-over')
    })
    zone.addEventListener('drop', (e) => {
      if (!dragging) return
      e.preventDefault()
      zone.classList.remove('is-over')
      zone.append(dragging)
      recalc()
    })
  })

  recalc()
}

/* Type-to-filter over a table. Matches the row's text, not one column, because
   people search for whatever they remember. */
const initFilter = () => {
  const input = document.querySelector('[data-filter]')
  if (!input) return
  const table = document.querySelector(input.dataset.filter)
  const count = document.querySelector('[data-filter-count]')
  if (!table) return

  const rows = [...table.querySelectorAll('tbody tr')]
  input.addEventListener('input', () => {
    const q = input.value.trim().toLowerCase()
    let shown = 0
    rows.forEach((r) => {
      const hit = !q || r.textContent.toLowerCase().includes(q)
      r.hidden = !hit
      if (hit) shown += 1
    })
    if (count) count.textContent = shown
  })
}

/* Open-task count on the overview card. */
const initTasks = () => {
  const list = document.querySelector('[data-tasks]')
  const out = document.querySelector('[data-task-open]')
  if (!list || !out) return

  const boxes = [...list.querySelectorAll('input[type="checkbox"]')]
  const render = () => { out.textContent = boxes.filter((b) => !b.checked).length }
  boxes.forEach((b) => b.addEventListener('change', render))
  render()
}

onReady(() => {
  initBase()
  initRail()
  initBoard()
  initFilter()
  initTasks()
})
