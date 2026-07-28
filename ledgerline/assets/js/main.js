/*!
 * Ledgerline — Bootstrap 6 fintech template
 */

import { initBase, onReady } from './base.js'

const gbp = (n, dp = 0) => n.toLocaleString('en-GB', {
  style: 'currency', currency: 'GBP', minimumFractionDigits: dp, maximumFractionDigits: dp,
})

/* Plan pricing calculator.
 *
 * Every SaaS pricing page puts three tiers side by side and leaves the visitor
 * to work out which one is actually cheapest for them — which is convenient,
 * because the answer is often the free one. This does the arithmetic instead,
 * and names the exact volume where the next plan up takes over.
 *
 * Plans arrive as JSON on the element rather than being hardcoded here, so the
 * table, the cards and the maths are all fed from the same list in build.py and
 * cannot drift apart.
 */
const initCalculator = () => {
  document.querySelectorAll('[data-calc]').forEach((root) => {
    let plans
    try { plans = JSON.parse(root.dataset.plans) } catch { return }
    if (!Array.isArray(plans) || !plans.length) return

    const count = root.querySelector('#calcCount')
    const avg = root.querySelector('#calcAvg')
    const countOut = root.querySelector('#calcCountOut')
    const avgOut = root.querySelector('#calcAvgOut')
    const volume = root.querySelector('[data-volume]')
    const note = root.querySelector('[data-crossover]')
    if (!count || !avg) return

    // Monthly bill: the platform fee plus a per-payment charge that is itself a
    // percentage of the basket plus a flat amount.
    const costOf = (plan, n, basket) => plan.base + n * (plan.pct * basket + plan.fixed)

    // Where two plans cost the same. Positive only when the pricier base buys a
    // cheaper per-payment rate — otherwise that plan never wins and there is no
    // crossover to quote.
    const crossover = (cheap, dear, basket) => {
      const perCheap = cheap.pct * basket + cheap.fixed
      const perDear = dear.pct * basket + dear.fixed
      const gap = perCheap - perDear
      if (gap <= 0) return null
      return Math.ceil((dear.base - cheap.base) / gap)
    }

    const render = () => {
      const n = Number(count.value)
      const basket = Number(avg.value)

      if (countOut) countOut.textContent = n.toLocaleString('en-GB')
      if (avgOut) avgOut.textContent = gbp(basket)
      if (volume) volume.textContent = gbp(n * basket)

      const totals = plans.map((p) => ({ plan: p, total: costOf(p, n, basket) }))
      const best = totals.reduce((a, b) => (b.total < a.total ? b : a))

      totals.forEach(({ plan, total }) => {
        const card = root.querySelector(`[data-plan="${plan.key}"]`)
        if (!card) return
        const isBest = plan.key === best.plan.key
        card.classList.toggle('is-best', isBest)
        const flag = card.querySelector('[data-best]')
        if (flag) flag.hidden = !isBest
        card.querySelector('[data-total]').textContent = gbp(total)
        // What the bill works out to as a share of money processed — the number
        // that actually lets you compare two plans priced differently.
        card.querySelector('[data-eff]').textContent =
          n * basket > 0 ? `${((total / (n * basket)) * 100).toFixed(2)}%` : '—'
      })

      if (!note) return
      const i = plans.findIndex((p) => p.key === best.plan.key)
      const parts = []
      const up = plans[i + 1] && crossover(plans[i], plans[i + 1], basket)
      const down = plans[i - 1] && crossover(plans[i - 1], plans[i], basket)

      if (down) parts.push(`${plans[i - 1].name} is cheaper below ${down.toLocaleString('en-GB')} payments`)
      if (up) parts.push(`${plans[i + 1].name} takes over above ${up.toLocaleString('en-GB')}`)

      note.textContent = parts.length
        ? `${best.plan.name} is cheapest for you — ${parts.join(', and ')}, at this average payment.`
        : `${best.plan.name} is cheapest for you at this average payment.`
    }

    ;[count, avg].forEach((el) => el.addEventListener('input', render))
    render()
  })
}

onReady(() => {
  initBase()
  initCalculator()
})
