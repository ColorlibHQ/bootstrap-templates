/*!
 * Northmark — Bootstrap 6 creative & brand agency template
 *
 * Thin by design. The work index reveals its thumbnails on :hover in CSS —
 * no JS, so it degrades to a plain readable list wherever hover does not exist
 * (touch), which is the correct behaviour rather than a fallback.
 */

import { initBase, onReady } from "./base.js"

onReady(() => {
  initBase()
})
