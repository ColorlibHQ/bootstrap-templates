#!/usr/bin/env node
/**
 * Verification gate for a Bootstrap 6 template.
 *
 *   node _kit/verify.mjs <template-dir> [--hero <slug>]
 *
 * Exits non-zero on the first template that fails, so it works as a CI step and
 * as a pre-publish guard. Every check here exists because something shipped
 * broken without it:
 *
 *   1. Console / page errors and failed requests, per page.
 *   2. A trailing gap below the footer — alpha1's `.dialog { display: flex }`
 *      has no `:not([open])` guard, so a closed dialog holds ~500px of layout.
 *   3. Internal .html links that resolve to nothing.
 *   4. Classes used in markup that exist in no stylesheet — which is how v5's
 *      `gap-lg-3` ordering gets caught, since v6 wants `lg:gap-3` and the wrong
 *      one simply does nothing.
 *   5. v5 leftovers that still *look* valid.
 *   6. `.btn-outline` / `.btn-subtle` with no `.theme-*` companion. See below —
 *      this one renders a button with no border at all and nothing errors.
 *
 * Needs playwright (`npm i`) and python3 for the static server.
 */

import { execFileSync, spawn } from 'node:child_process'
import { readFileSync, existsSync, readdirSync } from 'node:fs'
import { join, resolve, basename } from 'node:path'
import { chromium } from 'playwright'

const DIR = resolve(process.argv[2] || '.')
const heroFlag = process.argv.indexOf('--hero')
const HERO = heroFlag > -1 ? process.argv[heroFlag + 1] : null
const NAME = basename(DIR)

// Derived from the directory name so several templates can verify in parallel
// without fighting over a port.
const PORT = 8123 + (NAME.length % 40) + (NAME.charCodeAt(0) % 17)

const sh = (cmd, args, opts = {}) =>
  execFileSync(cmd, args, { encoding: 'utf8', maxBuffer: 32 * 1024 * 1024, ...opts })

const log = (s) => console.log(s)
const fail = (s) => { console.error('✗ ' + s); process.exit(1) }

if (!existsSync(DIR)) fail(`no such directory: ${DIR}`)

const server = spawn('python3', ['-m', 'http.server', String(PORT)], { cwd: DIR, stdio: 'ignore' })
const stop = () => { try { server.kill() } catch {} }
process.on('exit', stop)
await new Promise((r) => setTimeout(r, 900))

const pages = sh('bash', ['-lc',
  `cd ${JSON.stringify(DIR)} && ls -1 *.html && ls -1 */index.html 2>/dev/null || true`])
  .trim().split('\n').filter(Boolean)

log(`\n▸ ${NAME} — verifying ${pages.length} page(s)`)

const browser = await chromium.launch()
let problems = 0
let heroDone = false

for (const page of pages) {
  const errs = []
  const p = await browser.newPage({ viewport: { width: 1440, height: 950 } })
  p.on('pageerror', (e) => errs.push('pageerror: ' + e.message))
  p.on('console', (m) => m.type() === 'error' && errs.push('console: ' + m.text()))
  p.on('requestfailed', (r) => errs.push('requestfailed: ' + r.url()))

  await p.goto(`http://localhost:${PORT}/${page}`, { waitUntil: 'networkidle' })
  await p.waitForTimeout(500)

  // The only accepted noise: alpha1's Combobox constructs a Menu on an element
  // that already holds bs.combobox, so Data.set logs. Harmless, upstream.
  const real = errs.filter((e) => !e.includes('more than one instance'))

  const gap = await p.evaluate(() => {
    // `.site-footer` first, then the last <footer> that is genuinely page-level.
    // Both fallbacks matter: `querySelector('.site-footer, footer')` returns
    // whichever matches first in DOCUMENT ORDER, and a semantically correct
    // <footer> inside a blockquote citation or a dashboard card is not the
    // bottom of the page — measuring from one reports the entire rest of the
    // document as a trailing gap.
    const f = document.querySelector('.site-footer')
      ?? [...document.querySelectorAll('footer')]
           .filter((el) => !el.closest('article, section, aside, blockquote, table, .card')).pop()
    if (!f) return 0
    // scrollHeight floors at the viewport height, so a page shorter than the
    // window always looks like it has a trailing gap. Only a page that actually
    // scrolls can have a real one.
    const doc = document.documentElement
    if (doc.scrollHeight <= window.innerHeight + 1) return 0
    const r = f.getBoundingClientRect()
    return Math.max(0, Math.round(doc.scrollHeight - (r.bottom + window.scrollY)))
  })

  const links = await p.$$eval('a[href$=".html"]', (as) => [...new Set(as.map((a) => a.getAttribute('href')))])
  const pageDir = page.includes('/') ? join(DIR, page, '..') : DIR
  const broken = links.filter((l) => !existsSync(join(pageDir, l)))

  const status = [
    real.length ? `${real.length} errors` : null,
    gap > 2 ? `${gap}px trailing gap` : null,
    broken.length ? `broken: ${broken.join(',')}` : null,
  ].filter(Boolean)

  if (status.length) { problems += 1; log(`  ✗ ${page.padEnd(18)} ${status.join(' | ')}`); real.forEach((e) => log('      ' + e)) }
  else log(`  ✓ ${page}`)

  if (HERO && page === 'index.html' && !heroDone) {
    const hp = await browser.newPage({ viewport: { width: 1440, height: 978 }, deviceScaleFactor: 1.25 })
    await hp.goto(`http://localhost:${PORT}/index.html`, { waitUntil: 'networkidle' })
    await hp.waitForTimeout(800)
    await hp.screenshot({ path: join(DIR, `${HERO}-hd-1.png`) })
    await hp.close()
    heroDone = true
  }
  await p.close()
}
await browser.close()

/* Class names out of a stylesheet.
   The first character must be a letter, underscore or hyphen. A CSS class
   cannot start with a digit, and that single guard is what keeps the decimal in
   `padding: 0.05rem` from being read as a class called `05`. Do NOT also demand
   that the dot follow a non-word character — that would drop the second half of
   every compound selector like `.top-link.is-active`. */
const classesIn = (css) => new Set(
  [...css.matchAll(/\.((?:[A-Za-z_-]|\\:)(?:[A-Za-z0-9_-]|\\:)*)/g)]
    .map((m) => m[1].replace(/\\:/g, ':')))

/* --------------------------------------------------- undefined classes ---
   v6 changed the responsive prefix from a suffix to a prefix: `gap-lg-3` became
   `lg:gap-3`. The v5 form is not an error, it is simply a class nobody defines,
   so it does nothing and the layout is subtly wrong. Same for any typo. Compare
   every class used against every class any loaded stylesheet defines. */
const stylesheets = []
for (const rel of ['assets/vendor/bootstrap6/css/bootstrap.min.css', 'assets/css/base.css', 'assets/css/style.css']) {
  if (existsSync(join(DIR, rel))) stylesheets.push(readFileSync(join(DIR, rel), 'utf8'))
}
// Sub-page templates keep their stylesheets one level up.
for (const sub of readdirSync(DIR, { withFileTypes: true }).filter((d) => d.isDirectory())) {
  const css = join(DIR, sub.name, 'assets/css/style.css')
  if (existsSync(css)) stylesheets.push(readFileSync(css, 'utf8'))
}

if (stylesheets.length) {
  const defined = classesIn(stylesheets.join('\n'))

  const used = new Set()
  for (const page of pages) {
    for (const m of readFileSync(join(DIR, page), 'utf8').matchAll(/class="([^"]+)"/g)) {
      m[1].split(/\s+/).filter(Boolean).forEach((c) => used.add(c))
    }
  }

  // A class carrying a responsive prefix or a v5-style suffix is meant to come
  // from the framework; anything else is plausibly a JS hook or a bare wrapper.
  const undef = [...used].filter((c) => !defined.has(c))
  const suspicious = undef.filter((c) => /:|-(sm|md|lg|xl|xxl)-/.test(c))
  if (suspicious.length) {
    problems += 1
    log(`  ✗ ${suspicious.length} responsive class(es) that exist in no stylesheet — check prefix order (v6 wants lg:gap-3, not gap-lg-3):`)
    suspicious.slice(0, 6).forEach((c) => log(`      ${c}`))
  } else if (undef.length) {
    log(`  · ${undef.length} unstyled class(es), assumed to be hooks: ${undef.slice(0, 6).join(', ')}`)
  }
}

/* ------------------------------------------------ component collisions ---
   A generic-sounding class name is often already a v6 component. `.card`,
   `.prose` and `kbd` each cost real debugging time this way: the template's own
   rules land on top of a real component, the half that was not overridden keeps
   applying, and the result is wrong in a way nothing reports. `.card-body` is a
   flex column with align-items:flex-start, so block children silently shrink to
   their content width.

   Informational, not fatal — overriding a component on purpose is legitimate.
   The point is to know you are doing it. */
const own = existsSync(join(DIR, 'assets/css/style.css'))
  ? readFileSync(join(DIR, 'assets/css/style.css'), 'utf8') : ''
const vendor = existsSync(join(DIR, 'assets/vendor/bootstrap6/css/bootstrap.min.css'))
  ? readFileSync(join(DIR, 'assets/vendor/bootstrap6/css/bootstrap.min.css'), 'utf8') : ''

if (own && vendor) {
  const bs = classesIn(vendor)
  const mine = classesIn(own)
  const clash = [...mine].filter((c) => bs.has(c)).sort()
  if (clash.length) {
    log(`  · ${clash.length} class(es) also defined by Bootstrap — you are restyling components, not naming your own: ${clash.slice(0, 10).join(', ')}${clash.length > 10 ? ' …' : ''}`)
  }
}

/* ------------------------------------------------------- v5 leftovers --- */
const v5 = sh('bash', ['-lc',
  `cd ${JSON.stringify(DIR)} && grep -lE 'class="[^"]*(btn-primary|btn-outline-|text-muted|form-select|form-check|navbar-collapse|modal-dialog|offcanvas|dropdown-menu)' *.html || true`]).trim()
if (v5) { problems += 1; log(`  ✗ v5 leftovers in: ${v5.replace(/\n/g, ', ')}`) }

/* ----------------------------------------- themeless outline buttons ---
   .btn-outline / .btn-subtle resolve --bs-btn-border-color to
   var(--bs-theme-border), which only exists inside a .theme-* class. Without
   one the variable is empty, the
       border: <width> solid var(--bs-btn-border-color)
   shorthand is invalid at computed-value time, and the WHOLE shorthand drops —
   so border-style falls back to `none` and the button silently renders as bare
   text. Nothing errors and the class exists, so the sweep above misses it.
   (.btn-text is fine: it sets its own transparent border colour.) */
const themeless = sh('bash', ['-lc',
  `cd ${JSON.stringify(DIR)} && grep -oE 'class="[^"]*btn-(outline|subtle)[^"]*"' *.html | grep -v 'theme-' || true`]).trim()
if (themeless) {
  problems += 1
  const n = themeless.split('\n').length
  log(`  ✗ ${n} btn-outline/btn-subtle without a theme-* class (renders borderless):`)
  themeless.split('\n').slice(0, 3).forEach((l) => log(`      ${l}`))
}

stop()
if (problems) fail(`${problems} problem(s) in ${NAME}`)
log('  all checks passed')
