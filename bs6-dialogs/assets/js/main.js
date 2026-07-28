/*!
 * Bootstrap 6 Dialogs & Drawers — component pack
 */

import { initBase, onReady } from "./base.js"

/* Toast demo: the pack needs a way to actually show one, since v6 toasts are
   markup plus a class rather than a component you construct. */
const initToastDemo = () => {
  document.querySelectorAll("[data-toast-show]").forEach((btn) => {
    const toast = document.getElementById(btn.dataset.toastShow)
    if (!toast) return
    btn.addEventListener("click", () => {
      toast.hidden = false
      clearTimeout(toast._t)
      toast._t = setTimeout(() => { toast.hidden = true }, 4000)
    })
  })
  document.querySelectorAll("[data-toast-dismiss]").forEach((btn) => {
    btn.addEventListener("click", () => { btn.closest(".toast").hidden = true })
  })
}

onReady(() => {
  initBase()
  initToastDemo()
})
