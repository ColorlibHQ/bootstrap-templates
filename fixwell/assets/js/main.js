/*!
 * Fixwell — Bootstrap 6 home services template
 */

import { initBase, onReady } from './base.js'

const initHoursRange = () => {
  const r = document.getElementById('qHours')
  const o = document.getElementById('qHoursOut')
  if (!r || !o) return
  const sync = () => { o.textContent = `${r.value} hour${r.value === '1' ? '' : 's'}` }
  r.addEventListener('input', sync)
  sync()
}

/* Postcode coverage check — swap COVERED for a real lookup in production. */
const initCoverage = () => {
  const input = document.getElementById('coverPost')
  const btn = document.getElementById('coverCheck')
  const out = document.getElementById('coverResult')
  if (!input || !btn || !out) return

  const COVERED = ['M20', 'M21', 'M32', 'M33', 'M41', 'M19', 'SK4', 'SK8', 'WA14', 'WA15', 'M22']

  btn.addEventListener('click', () => {
    const value = input.value.trim().toUpperCase().replace(/\s+/g, '')
    if (!value) {
      out.className = 'fs-sm fg-3 mb-0'
      out.textContent = 'Enter a postcode to check.'
      return
    }
    const hit = COVERED.some((area) => value.startsWith(area))
    out.className = hit ? 'fs-sm fg-success fw-semibold mb-0' : 'fs-sm fg-danger fw-semibold mb-0'
    out.textContent = hit
      ? `Yes — we cover ${value}. Same-day slots are usually available.`
      : `${value} is outside our patch, but ring us and we'll suggest someone.`
  })
}

onReady(() => {
  initBase()
  initHoursRange()
  initCoverage()
})
