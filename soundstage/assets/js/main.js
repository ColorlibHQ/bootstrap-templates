/*!
 * Soundstage — Bootstrap 6 band & musician template
 */

import { initBase, onReady } from './base.js'

/* Tracklist play state. No audio ships with the template — this exists so the
   playing/paused styling is real and wired up, and so whoever adapts it has an
   obvious place to attach an <audio> element. Only one track can be active. */
const initTracklist = () => {
  const list = document.getElementById('tracklist')
  if (!list) return

  const PLAY = '<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4 3v10l8-5z"/></svg>'
  const PAUSE = '<svg width="12" height="12" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M4.5 3h2.2v10H4.5zm4.8 0h2.2v10H9.3z"/></svg>'

  list.querySelectorAll('.track-play').forEach((btn) => {
    btn.addEventListener('click', () => {
      const row = btn.closest('.track')
      const name = row?.querySelector('.track-name')?.textContent.trim() ?? 'track'
      const playing = row?.classList.contains('is-playing')

      // Stop everything first, then start this one if it was not already running.
      list.querySelectorAll('.track.is-playing').forEach((r) => {
        r.classList.remove('is-playing')
        const b = r.querySelector('.track-play')
        if (b) {
          b.innerHTML = PLAY
          b.setAttribute('aria-label', `Play ${r.querySelector('.track-name')?.textContent.trim() ?? 'track'}`)
        }
      })

      if (!playing) {
        row?.classList.add('is-playing')
        btn.innerHTML = PAUSE
        btn.setAttribute('aria-label', `Pause ${name}`)
      }
    })
  })
}

/* Video lightbox — one dialog, re-pointed at whichever tile was clicked. */
const initVideoDialog = () => {
  const still = document.getElementById('videoStill')
  const cap = document.getElementById('videoCap')
  if (!still) return

  document.querySelectorAll('[data-bs-target="#videoDialog"]').forEach((tile) => {
    tile.addEventListener('click', () => {
      const source = tile.querySelector('img')
      if (source) { still.src = source.src; still.alt = source.alt }
      if (cap) cap.textContent = tile.dataset.cap || 'Video'
    })
  })
}

onReady(() => {
  initBase()
  initTracklist()
  initVideoDialog()
})
