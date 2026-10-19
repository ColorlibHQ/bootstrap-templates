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
      const photo = frame.querySelector('.ph img')
      const label = frame.dataset.cap ?? photo?.alt ?? ''
      // Clone the thumbnail's <img> so the dialog shows the same file, whatever
      // its src is; fall back to the label for frames without a photo.
      img.replaceChildren(photo ? photo.cloneNode() : document.createTextNode(label))
      cap.textContent = label
    })
  })
}

onReady(() => {
  initBase()
  initLightbox()
})
