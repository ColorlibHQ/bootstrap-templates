/*!
 * Marigold — Bootstrap 6 wedding template
 */

import { initBase, onReady } from './base.js'

/* Days until the wedding. Reads the date from data-countdown so changing it is
   an HTML edit. aria-live is off — a region updating every minute is noise for
   a screen reader, and the date is stated in text directly above it. */
const initCountdown = () => {
  const el = document.querySelector('[data-countdown]')
  if (!el) return
  const target = Date.parse(el.dataset.countdown)
  if (Number.isNaN(target)) return

  const cells = { D: document.getElementById('cdD'), H: document.getElementById('cdH'), M: document.getElementById('cdM') }
  if (!cells.D) return

  const tick = () => {
    const s = Math.max(0, Math.floor((target - Date.now()) / 1000))
    cells.D.textContent = Math.floor(s / 86400)
    cells.H.textContent = String(Math.floor(s / 3600) % 24).padStart(2, '0')
    cells.M.textContent = String(Math.floor(s / 60) % 60).padStart(2, '0')
  }
  tick()
  setInterval(tick, 30000)
}

/* Party RSVP.
 *
 * Wedding sites almost always ship an RSVP that handles one person, so a family
 * of four either submits it four times or gives up and emails — and the couple
 * reconciles a spreadsheet either way. This builds a block per named guest with
 * their own attendance, meal and dietary note.
 *
 * Blocks are cloned from a <template> rather than built from strings, so the
 * markup lives in the HTML where it can be restyled without touching the script.
 * Field names are indexed on add so a normal form POST arrives as a usable
 * array rather than four fields with identical names. */
const initParty = () => {
  const list = document.getElementById('guests')
  const addBtn = document.getElementById('addGuest')
  const tpl = document.getElementById('guestTpl')
  const count = document.getElementById('guestCount')
  if (!list || !addBtn || !tpl) return

  const MAX = 8

  const renumber = () => {
    ;[...list.children].forEach((block, i) => {
      block.querySelector('[data-guest-no]').textContent = `Guest ${i + 1}`
      block.querySelectorAll('[data-name]').forEach((field) => {
        field.name = `${field.dataset.name}[${i}]`
      })
      // The first guest can't be removed — there has to be at least one.
      const remove = block.querySelector('[data-remove]')
      if (remove) remove.hidden = i === 0
    })
    const n = list.children.length
    if (count) count.textContent = `${n} guest${n === 1 ? '' : 's'}`
    addBtn.disabled = n >= MAX
    addBtn.textContent = n >= MAX ? 'Maximum party size reached' : '+ Add another guest'
  }

  const add = () => {
    if (list.children.length >= MAX) return
    const block = tpl.content.firstElementChild.cloneNode(true)
    // Unique ids so every label still points at its own control.
    const uid = `g${Date.now().toString(36)}${list.children.length}`
    block.querySelectorAll('[id]').forEach((el) => {
      const old = el.id
      el.id = `${old}-${uid}`
      block.querySelectorAll(`[for="${old}"]`).forEach((lab) => { lab.setAttribute('for', el.id) })
    })
    block.querySelector('[data-remove]')?.addEventListener('click', () => {
      block.remove()
      renumber()
    })
    list.append(block)
    renumber()
    block.querySelector('input[type="text"]')?.focus()
  }

  addBtn.addEventListener('click', add)
  add()   // every party has at least one guest
}

onReady(() => {
  initBase()
  initCountdown()
  initParty()
})
