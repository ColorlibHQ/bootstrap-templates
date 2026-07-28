/*!
 * Silver Halide — Bootstrap 6 photography template
 */

import { initBase, onReady } from './base.js'

/* Lightbox: the dialog is opened by the data API, we only swap its contents.
   Listening on show.bs.dialog means the caption is right before it paints. */
const initLightbox = () => {
  const box = document.getElementById('lightbox')
  const img = document.getElementById('lightboxImage')
  const cap = document.getElementById('lightboxCap')
  if (!box || !img || !cap) return

  document.querySelectorAll('.frame').forEach((frame) => {
    frame.addEventListener('click', () => {
      const label = frame.querySelector('.ph')?.textContent?.trim() ?? ''
      img.textContent = label
      cap.textContent = frame.dataset.cap ?? label
    })
  })
}

onReady(() => {
  initBase()
  initLightbox()
})
