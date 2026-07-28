#!/usr/bin/env node
/**
 * Fetches niche-relevant placeholder photography into a template's img/ folder.
 *
 *   node _kit/fetch-images.mjs <template-dir>
 *
 * Reads an `images` array from <template-dir>/template.json:
 *
 *   "images": [
 *     { "name": "hero", "q": "newsroom desk", "w": 1600, "h": 900 },
 *     { "name": "author-1", "q": "portrait person", "w": 400, "h": 400 }
 *   ]
 *
 * Source is the Openverse API (WordPress.org's CC search), restricted to
 * **cc0 and pdm** — public domain. That matters because these templates are
 * redistributed as downloadable zips: CC0/PDM needs no attribution and carries
 * no share-alike obligation, so a buyer can ship the demo as-is. CC-BY results
 * are deliberately excluded even though they'd often look better.
 *
 * Every image still gets recorded in CREDITS.txt with its title, license and
 * source URL — not legally required, but it means the provenance travels with
 * the template instead of living only in this script.
 */

import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync, mkdirSync, existsSync, rmSync } from 'node:fs'
import { join, resolve } from 'node:path'

const DIR = resolve(process.argv[2] || '.')
const manifest = JSON.parse(readFileSync(join(DIR, 'template.json'), 'utf8'))
const specs = manifest.images ?? []

if (!specs.length) {
  console.log('no `images` in template.json — nothing to do')
  process.exit(0)
}

const IMG = join(DIR, 'img')
mkdirSync(IMG, { recursive: true })

const sh = (cmd, args) => execFileSync(cmd, args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 })

const api = (q, photosOnly = true) => {
  const url = 'https://api.openverse.org/v1/images/'
    + `?q=${encodeURIComponent(q)}&license=cc0,pdm&size=large&page_size=20&mature=false&extension=jpg,jpeg,png`
    + (photosOnly ? '&category=photograph' : '')
  return JSON.parse(sh('curl', ['-sL', '--max-time', '25', url]))
}

// The CC0 pool is dominated by museum catalogues, so a plain noun search answers
// "school children" with a commemorative medal and "coffee" with clip art —
// both correctly matched, both useless as a section image. category=photograph
// drops digitised artwork and illustrations. Retry without it when a term comes
// back empty, so the filter only ever narrows a result set that had options.
const search = (q) => {
  const hits = api(q).results ?? []
  return hits.length ? hits : (api(q, false).results ?? [])
}

// Prefer landscape/portrait matching the target, and enough pixels to crop from.
// 0.55 rather than 0.8: sips upscales anyway, and the CC0 pool is thin enough
// that being strict here is what produced 4/24 coverage on the first run.
const score = (r, w, h) => {
  if (!r.width || !r.height) return -1
  if (r.width < w * 0.55 || r.height < h * 0.55) return -1
  const want = w / h
  const got = r.width / r.height
  return -Math.abs(Math.log(got / want))
}

// A specific phrase ("copper kettle stovetop kitchen") usually returns nothing
// under a cc0,pdm filter while its head noun returns twenty large photos. So
// walk from most specific to least rather than giving up on the first miss.
const queryLadder = (q, fallback) => {
  const w = q.split(/\s+/).filter(Boolean)
  const ladder = [q]
  if (fallback) ladder.push(fallback)
  if (w.length > 2) ladder.push(w.slice(0, 2).join(' '))
  if (w.length > 1) ladder.push(w[0], w[w.length - 1])
  return [...new Set(ladder)]
}

/* A slot with no photo would ship a broken <img> to every buyer, so there is
   always a file at the end of this: a plain diagonal gradient at exactly the
   right dimensions. Written as an uncompressed BMP (a header and raw BGR rows)
   purely so sips can transcode it without pulling in an image library. */
const writePlaceholder = (out, w, h) => {
  const rowSize = Math.ceil((w * 3) / 4) * 4
  const pixels = Buffer.alloc(rowSize * h)
  for (let y = 0; y < h; y += 1) {
    for (let x = 0; x < w; x += 1) {
      const t = (x / w + (h - 1 - y) / h) / 2          // BMP rows run bottom-up
      const o = y * rowSize + x * 3
      pixels[o] = Math.round(126 + t * 38)             // B
      pixels[o + 1] = Math.round(113 + t * 36)         // G
      pixels[o + 2] = Math.round(104 + t * 34)         // R
    }
  }
  const header = Buffer.alloc(54)
  header.write('BM', 0)
  header.writeUInt32LE(54 + pixels.length, 2)
  header.writeUInt32LE(54, 10)
  header.writeUInt32LE(40, 14)
  header.writeInt32LE(w, 18)
  header.writeInt32LE(h, 22)
  header.writeUInt16LE(1, 26)
  header.writeUInt16LE(24, 28)
  header.writeUInt32LE(pixels.length, 34)

  const bmp = out.replace(/\.jpg$/, '.bmp')
  writeFileSync(bmp, Buffer.concat([header, pixels]))
  sh('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '80', bmp, '--out', out])
  rmSync(bmp, { force: true })
}

const credits = []
let ok = 0

// `cc0q` overrides `q` here only. The two corpora want different words for the
// same picture — Unsplash rewards "friends talking coffee cup", the CC0 pool
// answers that with a village nameplate — and retuning `q` to please Openverse
// would spend Unsplash quota re-resolving a slot that was already right.
// `"cc0": false` skips the search and writes the generated placeholder straight
// away. There is one category the CC0 pool genuinely cannot serve: photographs
// of contemporary people. Every portrait query returns 19th-century studio
// tintypes, and cover-cropping those to a 3:4 box decapitates the sitter. A
// neutral gradient under a caption naming a fictional person reads as the
// placeholder it is; a cropped Victorian does not.
for (const { name, q: unsplashQ, cc0q, cc0, fallback, w, h } of specs) {
  const q = cc0q ?? unsplashQ
  const out = join(IMG, `${name}.jpg`)

  if (cc0 === false && !existsSync(out)) {
    writePlaceholder(out, w, h)
    console.log(`  ◦ ${name}.jpg  ${w}×${h}  generated gradient (cc0 opted out for this slot)`)
    credits.push(`${name}.jpg\n  Generated gradient placeholder — no photograph, no rights attached.\n`)
    ok += 1
    continue
  }
  if (existsSync(out)) {
    console.log(`  · ${name}.jpg exists, skipping`)
    credits.push(`${name}.jpg\n  (already present — see previous CREDITS.txt entry)\n`)
    ok += 1
    continue
  }

  const tmp = join(IMG, `${name}.orig`)
  let picked = null
  let usedQuery = null

  for (const term of queryLadder(q, fallback)) {
    let candidates = []
    try {
      candidates = search(term)
        .map((r) => ({ r, s: score(r, w, h) }))
        .filter((x) => x.s > -1)
        .sort((a, b) => b.s - a.s)
        .map((x) => x.r)
    } catch (e) {
      console.log(`  ! ${name}: API error on "${term}" — ${e.message.slice(0, 50)}`)
      continue
    }
    if (!candidates.length) continue

    // Wikimedia happily serves TIFF/SVG behind a .jpg-looking URL, and sips
    // refuses those — so walk the candidates until one actually converts.
    for (const cand of candidates.slice(0, 6)) {
      try {
        sh('curl', ['-sL', '--max-time', '45', '-o', tmp, cand.url])
        // Cover-crop to the requested box, then encode as progressive JPEG.
        sh('sips', ['-s', 'format', 'jpeg', '-s', 'formatOptions', '82',
          '-Z', String(Math.max(w, h) * 2), tmp, '--out', out])
        sh('sips', ['-c', String(h), String(w), out])
        picked = cand
        usedQuery = term
        break
      } catch {
        rmSync(out, { force: true })
      }
    }
    if (picked) break
  }
  rmSync(tmp, { force: true })

  if (!picked) {
    writePlaceholder(out, w, h)
    console.log(`  ◦ ${name}.jpg  ${w}×${h}  generated gradient (no CC0 match for "${q}")`)
    credits.push(`${name}.jpg\n  Generated gradient placeholder — no photograph, no rights attached.\n`)
    ok += 1
    continue
  }

  const kb = Math.round(sh('bash', ['-lc', `wc -c < ${JSON.stringify(out)}`]).trim() / 1024)
  const via = usedQuery === q ? '' : `  ← "${usedQuery}"`
  console.log(`  ✓ ${name}.jpg  ${w}×${h}  ${kb}KB  [${picked.license}]${via}`)
  credits.push(
    `${name}.jpg\n  ${picked.title || 'Untitled'}\n  ${(picked.license || '').toUpperCase()} ${picked.license_version || ''}`
    + `\n  ${picked.foreign_landing_url || picked.url}\n`)
  ok += 1
}

if (credits.length) {
  writeFileSync(join(DIR, 'CREDITS.txt'),
    'Placeholder photography\n'
    + '=======================\n\n'
    + 'Every photograph here is CC0 / Public Domain Mark, sourced via the\n'
    + 'Openverse API — no attribution required, commercial use fine. Where no\n'
    + 'public-domain photograph matched a slot, the file is a generated gradient\n'
    + 'instead; those are marked below and carry no rights at all.\n\n'
    + 'Either way these are placeholders: replace them with your own photography\n'
    + 'before launch. Provenance for each file follows.\n\n'
    + credits.join('\n'))
}

console.log(`\n${ok}/${specs.length} images ready in ${IMG}`)
process.exit(ok === specs.length ? 0 : 1)
