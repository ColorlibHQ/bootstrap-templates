/*!
 * Forecourt — Bootstrap 6 car dealership template
 */

import { initBase, onReady } from './base.js'

/* Live finance calculator.
 *
 * Deliberately a flat-rate illustration, and the page says so in three places.
 * A real agreement is an APR calculation on a reducing balance and depends on
 * the customer's credit profile — approximating that here would produce numbers
 * that look authoritative and are wrong, which is worse than obviously simple
 * ones labelled as estimates.
 *
 * The same formula runs in build.py, so the figures baked into the markup match
 * what this computes on load and nothing jumps on first paint. */
const monthlyFor = (cash, { apr, term, depositPct }) => {
  const financed = cash * (1 - depositPct / 100)
  const total = financed * (1 + (apr / 100) * (term / 12))
  return Math.round(total / term)
}

const money = (n) => `£${Math.round(n).toLocaleString('en-GB')}`

const initFinance = () => {
  const dep = document.getElementById('cDep')
  const term = document.getElementById('cTerm')
  const apr = document.getElementById('cApr')

  // Every element carrying data-cash is a quoted monthly figure — the hero
  // calculator and every card in the grid. They all move together.
  const quotes = [...document.querySelectorAll('[data-cash]')]
  if (!quotes.length) return

  const out = {
    dep: document.getElementById('cDepOut'),
    term: document.getElementById('cTermOut'),
    apr: document.getElementById('cAprOut'),
    depAmt: document.getElementById('cDepAmt'),
    fin: document.getElementById('cFin'),
    total: document.getElementById('cTotal'),
  }

  const read = () => ({
    depositPct: dep ? Number(dep.value) : 10,
    term: term ? Number(term.value) : 48,
    apr: apr ? Number(apr.value) : 9.9,
  })

  const apply = () => {
    const cfg = read()

    for (const el of quotes) {
      const cash = Number(el.dataset.cash)
      if (!Number.isFinite(cash)) continue
      const pm = monthlyFor(cash, cfg)
      // Keep whatever "/mo" suffix markup the element already had.
      const suffix = el.querySelector('span')?.outerHTML ?? ''
      el.innerHTML = `£${pm.toLocaleString('en-GB')}${suffix}`
    }

    if (out.dep) out.dep.textContent = `${cfg.depositPct}%`
    if (out.term) out.term.textContent = `${cfg.term} months`
    if (out.apr) out.apr.textContent = `${cfg.apr.toFixed(1)}%`

    // Breakdown always refers to the calculator's own example car.
    const example = document.getElementById('cMonthly')
    if (example) {
      const cash = Number(example.dataset.cash)
      const depAmt = cash * (cfg.depositPct / 100)
      const financed = cash - depAmt
      const total = financed * (1 + (cfg.apr / 100) * (cfg.term / 12))
      if (out.depAmt) out.depAmt.textContent = money(depAmt)
      if (out.fin) out.fin.textContent = money(financed)
      if (out.total) out.total.textContent = money(total + depAmt)
    }
  }

  ;[dep, term, apr].forEach((r) => r?.addEventListener('input', apply))
  apply()
}

onReady(() => {
  initBase()
  initFinance()
})
