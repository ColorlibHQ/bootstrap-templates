/*!
 * Northstar — Bootstrap 6 SaaS analytics dashboard
 */

import { initBase, onReady } from './base.js'

const gbp = (n, dp = 0) => {
  const abs = Math.abs(n)
  if (abs >= 1_000_000) return `${n < 0 ? '−' : ''}£${(abs / 1_000_000).toFixed(2)}m`
  if (abs >= 10_000) return `${n < 0 ? '−' : ''}£${Math.round(abs / 1000)}k`
  return `${n < 0 ? '−' : ''}£${abs.toLocaleString('en-GB', { maximumFractionDigits: dp })}`
}

const pct = (n, dp = 1) => `${n >= 0 ? '' : '−'}${Math.abs(n).toFixed(dp)}%`

/* The date range, doing what it says.
 *
 * Every dashboard template ships a "Last 30 days" control that is decorative —
 * the numbers beside it are typed into the markup, so changing it changes
 * nothing. Here the whole page is derived from one 90-day series that travels
 * on <body>, and the range picks the window. KPIs, deltas, the chart path, the
 * axis labels and the MRR waterfall are all recomputed together, so they cannot
 * describe different periods.
 */
const initRange = () => {
  let data
  try { data = JSON.parse(document.body.dataset.series) } catch { return }
  const days = data?.days
  if (!Array.isArray(days) || !days.length) return

  const buttons = [...document.querySelectorAll('[data-range]')]

  const sum = (rows, key) => rows.reduce((s, d) => s + d[key], 0)

  const render = (n) => {
    const window_ = days.slice(-n)
    // The comparison window is the equal-length period immediately before, so a
    // delta always compares like with like rather than against a fixed month.
    const prev = days.slice(-n * 2, -n)

    const opening = days[days.length - n - 1]?.m ?? data.opening
    const closing = window_[window_.length - 1].m
    const movements = ['n', 'e', 'r', 'c', 'k']
    const moved = Object.fromEntries(movements.map((k) => [k, sum(window_, k)]))
    const net = movements.reduce((s, k) => s + moved[k], 0)

    const signups = sum(window_, 's')
    const prevSignups = prev.length ? sum(prev, 's') : signups
    const grossChurn = opening ? (-moved.k / opening) * 100 : 0
    const growth = moved.n + moved.e + moved.r
    const losses = -(moved.c + moved.k)

    // `null` means "this figure has no meaningful delta"; `undefined` means
    // there is no earlier window to compare against at all. The 90-day range
    // hits the second case, and printing "▲ 0.0%" there would invent a
    // comparison that does not exist.
    const comparable = prev.length > 0
    const change = (a, b) => (comparable && b ? ((a - b) / b) * 100 : undefined)

    const figures = {
      mrr: [gbp(closing), change(closing, opening)],
      arr: [gbp(closing * 12), change(closing, opening)],
      net: [gbp(net), null],
      signups: [signups.toLocaleString('en-GB'), change(signups, prevSignups)],
      churn: [pct(grossChurn), null],
      quick: [losses ? (growth / losses).toFixed(1) : '—', null],
    }

    document.querySelectorAll('[data-kpi]').forEach((el) => {
      const f = figures[el.dataset.kpi]
      if (!f) return
      el.querySelector('[data-value]').textContent = f[0]
      const d = el.querySelector('[data-delta]')
      const [, delta] = f
      if (delta === undefined) { d.textContent = 'no earlier period to compare'; d.className = 'kpi-delta mb-0 is-flat'; return }
      if (delta === null) { d.textContent = `over ${n} days`; d.className = 'kpi-delta mb-0 is-flat'; return }
      d.textContent = `${delta >= 0 ? '▲' : '▼'} ${pct(delta)} vs previous ${n} days`
      d.className = `kpi-delta mb-0 ${delta >= 0 ? 'is-up' : 'is-down'}`
    })

    // Chart. Drawn from the window rather than a fixed path in the markup —
    // that is the whole point of the control.
    const vals = window_.map((d) => d.m)
    const lo = Math.min(...vals)
    const hi = Math.max(...vals)
    const span = (hi - lo) || 1
    const W = 640
    const H = 200
    const step = W / (vals.length - 1 || 1)
    const xy = vals.map((v, i) => [i * step, H - 8 - ((v - lo) / span) * (H - 30)])
    const line = xy.map(([x, y], i) => `${i ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`).join(' ')

    document.querySelectorAll('[data-chart-line]').forEach((p) => p.setAttribute('d', line))
    document.querySelectorAll('[data-chart-area]').forEach((p) =>
      p.setAttribute('d', `${line} L${W},${H} L0,${H} Z`))

    document.querySelectorAll('[data-axis-start]').forEach((e) => { e.textContent = `${n}d ago` })
    document.querySelectorAll('[data-axis-mid]').forEach((e) => { e.textContent = `${Math.round(n / 2)}d ago` })
    document.querySelectorAll('[data-range-label]').forEach((e) => { e.textContent = `Last ${n} days` })

    // Waterfall. Opening plus every movement must equal closing — if it ever
    // does not, the arithmetic is wrong and the page says so rather than
    // quietly printing a bridge that does not reconcile.
    const peak = Math.max(...movements.map((k) => Math.abs(moved[k])), 1)
    document.querySelectorAll('[data-waterfall]').forEach((wf) => {
      wf.querySelectorAll('[data-wf]').forEach((row) => {
        const key = row.dataset.wf
        const out = row.querySelector('[data-v]')
        const bar = row.querySelector('.wf-bar i')
        if (key === 'opening') { out.textContent = gbp(opening); return }
        if (key === 'closing') { out.textContent = gbp(closing); return }
        const v = moved[key]
        out.textContent = `${v >= 0 ? '+' : '−'}${gbp(Math.abs(v))}`
        if (bar) bar.style.setProperty('--w', `${(Math.abs(v) / peak) * 100}%`)
      })
    })

    const reconciles = Math.round(opening + net) === Math.round(closing)
    document.querySelectorAll('[data-wf-check]').forEach((e) => {
      e.textContent = reconciles
        ? `${gbp(opening)} + ${gbp(net)} net = ${gbp(closing)} — reconciles.`
        : 'These movements do not reconcile with the closing balance.'
      e.classList.toggle('is-bad', !reconciles)
    })
  }

  buttons.forEach((b) => {
    b.addEventListener('click', () => {
      buttons.forEach((o) => {
        const on = o === b
        o.classList.toggle('is-on', on)
        o.setAttribute('aria-pressed', String(on))
      })
      render(Number(b.dataset.range))
    })
  })

  const active = buttons.find((b) => b.classList.contains('is-on'))
  render(Number(active?.dataset.range ?? 30))
}

/* Type-to-filter over a table, matching the whole row. */
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

onReady(() => {
  initBase()
  initRange()
  initFilter()
})
