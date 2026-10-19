/*!
 * Northgate — Bootstrap 6 school template
 */

import { initBase, onReady } from './base.js'

/* Stage filter: with one card per stage, hiding cards would leave a single
   card floating in the grid, so the chosen stage is highlighted instead. */
const initStageFilter = () => {
  const toggle = document.getElementById('stageFilter')
  const grid = document.getElementById('programmeGrid')
  const status = document.getElementById('stageStatus')
  if (!toggle || !grid) return

  toggle.addEventListener('change.bs.combobox', (event) => {
    const value = event.value ?? 'all'
    grid.querySelectorAll('[data-stage]').forEach((card) => {
      const match = value === 'all' || card.dataset.stage === value
      card.classList.toggle('is-dimmed', !match)
      card.classList.toggle('is-picked', match && value !== 'all')
    })
    if (status) status.textContent = value === 'all' ? 'Showing all stages' : `Highlighted: ${event.item?.textContent.trim()}`
  })
}

onReady(() => {
  initBase()
  initStageFilter()
})
