# Bootstrap Templates

Free, self-contained website templates built on **Bootstrap 6 (6.0.0-alpha.1)**:
28 full site templates and 6 component packs, all MIT licensed.

Every template is a plain folder of HTML, CSS and ES modules. No build step, no
bundler, no npm install to look at one. Open `index.html` and it works.

> [!IMPORTANT]
> **Bootstrap 6 is in alpha.** 6.0.0-alpha.1 shipped on 8 October 2026
> (`npm i bootstrap@6.0.0-alpha.1`), and the Bootstrap team expects more
> breaking changes before beta. Each template bundles the exact build it was
> tested against, so nothing changes under you when upstream moves.
>
> Bootstrap 6 supports **Chrome and Edge 130+, Firefox 132+ and Safari 18+**,
> with no polyfills for older browsers.

---

## Templates

| Template | For | Pages | Demo |
| --- | --- | --- | --- |
| [`atelier`](atelier/) | Portfolio | 2 | [preview](https://uicookies.com/demo/#atelier) |
| [`bedrock`](bedrock/) | Construction & Civil Engineering | 2 | [preview](https://uicookies.com/demo/#bedrock) |
| [`caseworth`](caseworth/) | Law Firm & Accountancy | 2 | [preview](https://uicookies.com/demo/#caseworth) |
| [`commerce`](commerce/) | E-commerce | 3 | [preview](https://uicookies.com/demo/#commerce) |
| [`drafthouse`](drafthouse/) | Architecture & Interior Design | 2 | [preview](https://uicookies.com/demo/#drafthouse) |
| [`fixwell`](fixwell/) | Handyman & Home Services | 1 | [preview](https://uicookies.com/demo/#fixwell) |
| [`forecourt`](forecourt/) | Car Dealership | 2 | [preview](https://uicookies.com/demo/#forecourt) |
| [`havenhomes`](havenhomes/) | Real Estate | 2 | [preview](https://uicookies.com/demo/#havenhomes) |
| [`helm`](helm/) | Admin Dashboard | 8 | [preview](https://uicookies.com/demo/#helm) |
| [`ironworks`](ironworks/) | Gym & Fitness | 1 | [preview](https://uicookies.com/demo/#ironworks) |
| [`lantern`](lantern/) | Hotel & Resort | 2 | [preview](https://uicookies.com/demo/#lantern) |
| [`ledgerline`](ledgerline/) | Fintech & SaaS | 2 | [preview](https://uicookies.com/demo/#ledgerline) |
| [`liftoff`](liftoff/) | Coming Soon | 3 | [preview](https://uicookies.com/demo/#liftoff) |
| [`locale`](locale/) | Directory | 2 | [preview](https://uicookies.com/demo/#locale) |
| [`marigold`](marigold/) | Wedding | 2 | [preview](https://uicookies.com/demo/#marigold) |
| [`meridian`](meridian/) | Medical & Clinic | 2 | [preview](https://uicookies.com/demo/#meridian) |
| [`northgate`](northgate/) | School | 2 | [preview](https://uicookies.com/demo/#northgate) |
| [`northmark`](northmark/) | Creative & Brand Agency | 2 | [preview](https://uicookies.com/demo/#northmark) |
| [`openhands`](openhands/) | Charity & NGO | 2 | [preview](https://uicookies.com/demo/#openhands) |
| [`pressroom`](pressroom/) | Blog & Magazine | 2 | [preview](https://uicookies.com/demo/#pressroom) |
| [`shortlist`](shortlist/) | Job Board | 2 | [preview](https://uicookies.com/demo/#shortlist) |
| [`silverhalide`](silverhalide/) | Photography | 1 | [preview](https://uicookies.com/demo/#silverhalide) |
| [`soundstage`](soundstage/) | Band & Musician | 2 | [preview](https://uicookies.com/demo/#soundstage) |
| [`stonebridge`](stonebridge/) | Church | 2 | [preview](https://uicookies.com/demo/#stonebridge) |
| [`stratos`](stratos/) | SaaS | 7 | [preview](https://uicookies.com/demo/#stratos) |
| [`summit-conf`](summit-conf/) | Conference & Event | 1 | [preview](https://uicookies.com/demo/#summit-conf) |
| [`syllabus`](syllabus/) | Online Course & E-Learning | 2 | [preview](https://uicookies.com/demo/#syllabus) |
| [`tavola`](tavola/) | Restaurant | 2 | [preview](https://uicookies.com/demo/#tavola) |

## Component packs

| Template | For | Examples | Demo |
| --- | --- | --- | --- |
| [`bs6-auth`](bs6-auth/) | 8 Free Login & Sign-ups | 1 | [preview](https://uicookies.com/demo/#bs6-auth) |
| [`bs6-cards`](bs6-cards/) | 10 Free Cards | 1 | [preview](https://uicookies.com/demo/#bs6-cards) |
| [`bs6-dialogs`](bs6-dialogs/) | 10 Frees | 1 | [preview](https://uicookies.com/demo/#bs6-dialogs) |
| [`bs6-forms`](bs6-forms/) | 10 Free Forms | 1 | [preview](https://uicookies.com/demo/#bs6-forms) |
| [`bs6-navigation`](bs6-navigation/) | 8 Free Navbar, Menu & Sidebar Examples | 1 | [preview](https://uicookies.com/demo/#bs6-navigation) |
| [`bs6-tables`](bs6-tables/) | 10 Free Tables | 1 | [preview](https://uicookies.com/demo/#bs6-tables) |

---

## Using one

Take the folder. That's the whole process.

```bash
git clone https://github.com/ColorlibHQ/bootstrap-templates.git
cd bootstrap-templates/tavola
open index.html          # or: python3 -m http.server
```

Each folder carries its own `assets/vendor/bootstrap6/`, so it is independent of
this repo and of every other template. Delete the rest and nothing breaks.

### Loading Bootstrap from a CDN or npm instead

Every page loads Bootstrap in two lines in `<head>`: the stylesheet and an
[import map](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/script/type/importmap)
that tells the scripts where `bootstrap` lives. The JavaScript only ever does
`import … from 'bootstrap'`, so those two lines are the only place to change.

**jsDelivr:** point both at the CDN and delete `assets/vendor/`:

```html
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@6.0.0-alpha.1/dist/css/bootstrap.min.css">
<script type="importmap">{"imports": {"bootstrap": "https://cdn.jsdelivr.net/npm/bootstrap@6.0.0-alpha.1/dist/js/bootstrap.bundle.min.js"}}</script>
```

**npm with a bundler (Vite etc.):** `npm i bootstrap@6.0.0-alpha.1`, import
`bootstrap/dist/css/bootstrap.min.css` from your entry file, and remove the
import map; the bundler resolves `import … from 'bootstrap'` itself.

Pin an exact version either way. A floating tag such as `bootstrap@6` or
`@next` will pick up the next alpha, and alphas break markup: alpha.1 changed
how `nav-overflow` is written, for example.

Some templates have a `build.py` that generates their pages from one source of
truth — a menu, a curriculum, a pricing table — so the same figure can't end up
different on two pages. Edit the data at the top, run `python3 build.py`. If you
would rather just edit HTML, delete `build.py`; the generated files stand alone.

## What's in `_kit/`

Shared tooling, not a dependency of any template.

| File | Does |
| --- | --- |
| `base.css` | Rebuilds the whole `--bs-primary-*` family from one `--brand` token, plus the alpha1 workarounds every template needs |
| `base.js` | Colour mode, sticky header, drawer auto-close, demo form handling |
| `verify.mjs` | The gate: console errors, trailing gaps, dead links, undefined classes, v5 leftovers, themeless outline buttons |
| `fetch-images.mjs` | Pulls CC0/public-domain placeholder photography from Openverse into a template's `img/` |
| `new-template.sh` | Scaffolds a folder with the vendored framework and the kit |
| `upgrade.sh` | Re-vendors every template onto a new Bootstrap 6 build, diffs the risk, then verifies them all |

```bash
npm install                       # playwright, for verify.mjs only
node _kit/verify.mjs tavola       # verify one
_kit/upgrade.sh <sha> --apply     # move the whole catalogue to a new v6 build
```

## Bootstrap 6 gotchas worth knowing

The alpha renames more than the migration guide admits, and several of the
changes fail **silently** — the class still exists, nothing errors, the result is
just wrong. The ones that cost real debugging time:

- **`gap-lg-3` → `lg:gap-3`.** The responsive prefix moved to the front. The v5
  form isn't an error, it's a class nobody defines, so it quietly does nothing.
- **`d-` is still required.** `md:d-inline`, not `md:inline`. Paired with
  `d-none` that mistake hides an element permanently, at every width.
- **`.btn-outline` needs a `.theme-*` companion.** Alone,
  `--bs-theme-border` is undefined, which makes the `border:` shorthand invalid
  at computed-value time — so the *whole* shorthand drops and the button renders
  with no border at all. Overriding `border-color` doesn't rescue it.
- **`.form-select` is gone** as a component. Use
  `.form-control.form-control-caret` on a native `<select>`.
- **Accordions are native `<details>`/`<summary>`.** No `.accordion-button`,
  no `.collapse`.
- **Modal → Dialog, Offcanvas → Drawer, Dropdown → Menu**, all native `<dialog>`.
- **A closed `.dialog` still occupies layout** — alpha1 ships
  `.dialog { display: flex }` with no `:not([open])` guard. `base.css` fixes it.
- **`.prose` is a real component**, not a spare name: a flex column driven by
  `--bs-content-gap` with `margin-block: 0` on its children. Adding your own
  margins *adds* to the gap rather than replacing it.
- **Unlayered author CSS beats utilities.** Bootstrap wraps everything in
  `@layer`, so a shorthand `margin: 0` in your stylesheet silently kills `.mb-6`.
  Use longhands.

`verify.mjs` catches the first three automatically.

## Contributing

Bug reports and fixes are welcome. Before opening a PR:

```bash
node _kit/verify.mjs <template>    # must pass
```

Please keep templates self-contained: no shared runtime, no CDN links, no
external JS dependencies beyond the bundled framework.

## Licence

[MIT](LICENSE) — use them commercially, no attribution required.

Placeholder photography is CC0 / public domain (sourced via Openverse; see each
template's `CREDITS.txt`), or a generated gradient where no suitable public
domain image exists. Replace it with your own before you ship.

---

Built by [Colorlib](https://colorlib.com). More free templates at
[uicookies.com](https://uicookies.com/).
