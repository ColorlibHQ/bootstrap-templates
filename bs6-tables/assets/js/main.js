/*!
 * Bootstrap 6 Tables — component pack
 *
 * Every behaviour here works on the rows already in the DOM. That is a
 * deliberate ceiling: it keeps the markup the source of truth, keeps the tables
 * readable with JavaScript off, and stays fast to a few hundred rows. Past that
 * you want the server doing the work, not a bigger script.
 */

import { initBase, onReady } from './base.js'

/* ------------------------------------------------------------------ sorting */

const cellText = (row, index) => row.cells[index]?.textContent.trim() ?? ''

const sortValue = (text, type) => {
  if (type !== 'num') return text.toLowerCase()
  // Strip currency symbols and separators before comparing.
  const n = Number.parseFloat(text.replace(/[^\d.-]/g, ''))
  return Number.isNaN(n) ? -Infinity : n
}

const initSortable = () => {
  document.querySelectorAll('table[data-sortable]').forEach((table) => {
    const body = table.tBodies[0]
    if (!body) return

    table.querySelectorAll('.th-sort').forEach((btn) => {
      btn.addEventListener('click', () => {
        const col = Number(btn.dataset.sortCol)
        const type = btn.dataset.sortType || 'text'
        const asc = btn.getAttribute('aria-sort') !== 'ascending'

        // Only one column carries a sort state at a time.
        table.querySelectorAll('.th-sort').forEach((b) => b.setAttribute('aria-sort', 'none'))
        btn.setAttribute('aria-sort', asc ? 'ascending' : 'descending')

        const rows = [...body.rows]
        rows.sort((a, b) => {
          const x = sortValue(cellText(a, col), type)
          const y = sortValue(cellText(b, col), type)
          if (x < y) return asc ? -1 : 1
          if (x > y) return asc ? 1 : -1
          return 0
        })
        rows.forEach((r) => body.append(r))
      })
    })
  })
}

/* ---------------------------------------------------------------- filtering */

const initFilterable = () => {
  document.querySelectorAll('[data-filterable]').forEach((shell) => {
    const table = shell.querySelector('table')
    const search = shell.querySelector('[data-filter-text]')
    const count = shell.querySelector('[data-filter-count]')
    const empty = shell.querySelector('[data-filter-empty]')
    if (!table?.tBodies[0]) return

    const rows = [...table.tBodies[0].rows]
    let status = ''

    const apply = () => {
      const q = (search?.value || '').trim().toLowerCase()
      let shown = 0
      for (const row of rows) {
        const text = row.textContent.toLowerCase()
        const hit = (!q || text.includes(q)) && (!status || text.includes(status))
        row.hidden = !hit
        if (hit) shown += 1
      }
      if (count) count.textContent = `${shown} of ${rows.length}`
      if (empty) empty.hidden = shown !== 0
    }

    search?.addEventListener('input', apply)

    // Combobox writes its choice into its own label rather than firing a native
    // change event, so listen on the menu items instead of waiting for one.
    shell.querySelectorAll('.menu-item').forEach((item) => {
      item.addEventListener('click', () => {
        status = (item.dataset.bsValue || '').toLowerCase()
        apply()
      })
    })

    apply()
  })
}

/* --------------------------------------------------------------- pagination */

const initPaginate = () => {
  document.querySelectorAll('[data-paginate]').forEach((shell) => {
    const table = shell.querySelector('table')
    const list = shell.querySelector('[data-page-list]')
    const range = shell.querySelector('[data-page-range]')
    const size = Number(shell.dataset.paginate) || 10
    if (!table?.tBodies[0] || !list) return

    const rows = [...table.tBodies[0].rows]
    const pages = Math.max(1, Math.ceil(rows.length / size))
    let page = 1

    const render = () => {
      const first = (page - 1) * size
      const last = Math.min(first + size, rows.length)
      rows.forEach((row, i) => { row.hidden = i < first || i >= last })
      if (range) range.textContent = `Showing ${first + 1}–${last} of ${rows.length}`

      list.textContent = ''
      const add = (label, target, { disabled = false, current = false, aria } = {}) => {
        const li = document.createElement('li')
        li.className = `page-item${disabled ? ' disabled' : ''}${current ? ' active' : ''}`
        const btn = document.createElement('button')
        btn.type = 'button'
        btn.className = 'page-link'
        btn.textContent = label
        if (aria) btn.setAttribute('aria-label', aria)
        if (current) btn.setAttribute('aria-current', 'page')
        if (disabled) btn.disabled = true
        btn.addEventListener('click', () => { page = target; render() })
        li.append(btn)
        list.append(li)
      }

      add('‹', page - 1, { disabled: page === 1, aria: 'Previous page' })
      for (let p = 1; p <= pages; p += 1) add(String(p), p, { current: p === page })
      add('›', page + 1, { disabled: page === pages, aria: 'Next page' })
    }

    render()
  })
}

/* ---------------------------------------------------------------- selection */

const initSelectable = () => {
  document.querySelectorAll('[data-selectable]').forEach((shell) => {
    const all = shell.querySelector('#checkAll')
    const boxes = [...shell.querySelectorAll('[data-row-check]')]
    const bar = shell.querySelector('[data-bulk-bar]')
    const count = shell.querySelector('[data-bulk-count]')
    if (!boxes.length) return

    const sync = () => {
      const n = boxes.filter((b) => b.checked).length
      if (all) {
        all.checked = n === boxes.length && n > 0
        // Partial selection is neither checked nor unchecked.
        all.indeterminate = n > 0 && n < boxes.length
      }
      if (bar) bar.hidden = n === 0
      if (count) count.textContent = `${n} selected`
      boxes.forEach((b) => b.closest('tr')?.classList.toggle('table-active', b.checked))
    }

    all?.addEventListener('change', () => {
      boxes.forEach((b) => { b.checked = all.checked })
      sync()
    })
    boxes.forEach((b) => b.addEventListener('change', sync))
    sync()
  })
}

/* Fills the sticky-header demo with enough rows to actually need scrolling.
   Generated rather than written out so the variant's markup stays readable. */
const initStickyRows = () => {
  const body = document.getElementById('stickyBody')
  if (!body) return

  const clients = ['Northwind Trading', 'Kestrel Logistics', 'Lumen Studio', 'Fieldstone Group',
    'Ardent Works', 'Halden & Co', 'Pemberton Civils', 'Sable Interiors']
  const owners = ['Priya N.', 'Marcus L.', 'Dana R.', 'Tomas B.']
  const states = [['Paid', 'success'], ['Pending', 'warning'], ['Overdue', 'danger'], ['Draft', 'secondary']]

  const money = (n) => `£${n.toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
  const pad = (n) => String(n).padStart(2, '0')

  let html = ''
  for (let i = 0; i < 24; i += 1) {
    const net = 500 + ((i * 977) % 19000)
    const vat = net * 0.2
    const [label, theme] = states[i % states.length]
    const day = (i % 27) + 1
    html += `<tr>
      <th scope="row" class="fw-normal">INV-${2041 + i}</th>
      <td>${clients[i % clients.length]}</td>
      <td><span class="badge badge-subtle theme-${theme}">${label}</span></td>
      <td class="fg-3">2026-06-${pad(day)}</td>
      <td class="fg-3">2026-07-${pad(day)}</td>
      <td class="fg-3">30 days</td>
      <td>${owners[i % owners.length]}</td>
      <td class="num">${money(net)}</td>
      <td class="num">${money(vat)}</td>
      <td class="num">${money(net + vat)}</td>
    </tr>`
  }
  body.innerHTML = html
}

onReady(() => {
  initBase()
  initSortable()
  initFilterable()
  initPaginate()
  initSelectable()
  initStickyRows()
})
