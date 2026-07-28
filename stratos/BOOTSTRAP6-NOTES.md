# Bootstrap 6 alpha — build notes

Findings from building the Stratos pilot against Bootstrap **6.0.0-alpha1**.
Read this before starting the next v6 template; several things contradict the
official migration guide.

**Pinned to commit** [`59cee6c`](https://github.com/twbs/bootstrap/commit/59cee6c16323d8431ed535e262b0f5759ea91f54) (2026-07-26) of the `v6-dev` branch.

---

## 1. There is no npm package

`npm i bootstrap@6.0.0-alpha1` returns **404**. The docs site publishes that
command ahead of the release, but nothing v6 has been pushed to the registry —
`latest` is still `5.3.8` (Aug 2025) and there is no v6 dist-tag.

What does exist: `dist/` **is committed** on the `v6-dev` branch, so a complete
prebuilt alpha can be pulled straight from raw.githubusercontent. That is how
`assets/vendor/bootstrap6/` was populated.

```bash
SHA=59cee6c16323d8431ed535e262b0f5759ea91f54
curl -sL -o assets/vendor/bootstrap6/css/bootstrap.min.css \
  "https://raw.githubusercontent.com/twbs/bootstrap/$SHA/dist/css/bootstrap.min.css"
curl -sL -o assets/vendor/bootstrap6/js/bootstrap.bundle.min.js \
  "https://raw.githubusercontent.com/twbs/bootstrap/$SHA/dist/js/bootstrap.bundle.min.js"
```

Pin the SHA, never the branch name — `v6-dev` took 100+ commits in the 30 days
before this build.

---

## 2. Where the official migration skill is wrong

Bootstrap ships [`skills/bootstrap-v5-v6-migration`](https://github.com/twbs/bootstrap/tree/main/skills/bootstrap-v5-v6-migration).
It is broadly excellent, but it has drifted from the branch on these points.
**Verified against the shipped dist, not assumed.**

### Checkbox — `.check` goes on the input, with no SVG

The skill shows a `<div class="check">` wrapper containing an inline SVG. The
alpha renders the tick with a CSS `mask` on the input's `::before`, so:

```html
<!-- Skill says (wrong) -->
<div class="form-field">
  <div class="check"><input type="checkbox" id="c"><svg>…</svg></div>
  <label for="c">Check me</label>
</div>

<!-- Alpha actually wants -->
<div class="form-field">
  <input type="checkbox" id="c" class="check">
  <label for="c">Check me</label>
</div>
```

Adding the SVG double-renders the mark. Override `--bs-check-icon-checked` /
`--bs-check-icon-indeterminate` to change the icon.

### Drawer is a `<dialog>`, not a `<div>`

The skill never says this. `.drawer` must be on a native `<dialog>` element —
same as `.dialog`. A `<div class="drawer">` will not open or close.

### `data-bs-validate` is CSS-only and token-valued

It is **not** implemented in the JS bundle. The CSS keys off it with `~=`
matching:

- bare `data-bs-validate` → invalid styling only (what you usually want)
- `data-bs-validate="valid"` → *also* shows success styling

Pair it with `novalidate` on the `<form>` so the browser's bubbles don't
compete with `.invalid-feedback`. Don't call `form.reportValidity()` — that
re-enables the very bubbles `novalidate` suppresses.

### `@layer` list differs

The skill lists `colors, theme, config, …`. The shipped dist declares:

```css
@layer colors, config, root, reboot, layout, content, forms, components, custom, helpers, utilities;
```

No `theme` layer. Author CSS **outside** any layer beats all of it regardless of
specificity or source order — which is why `assets/css/style.css` is unlayered.

---

## 2b. Alpha bug: a closed `.dialog` still occupies layout

`.dialog { display: flex }` ships with **no `:not([open])` guard anywhere in the
dist** (`grep -c "not(\[open\])"` → 0). Author styles beat the UA's
`dialog:not([open]) { display: none }`, so every closed dialog on the page keeps
its full height — this template lost ~500px of blank space below the footer to it.

The dialog is invisible while closed, so it reads as a mysterious gap rather than
a stray element. Fix in unlayered author CSS:

```css
dialog.dialog:not([open]) { display: none; }
```

Scope it to `.dialog` only. **Do not** apply it to `.drawer` — the drawer must
stay in flow so `navbar-expand` can inline it on desktop (see §4). Verified that
open/close and the transition still behave with the guard in place.

## 2c. `.check` and `.switch` take opposite markup

Easy to get wrong by pattern-matching from one to the other:

```html
<!-- checkbox: class on the INPUT -->
<input type="checkbox" id="c" class="check">

<!-- switch: class on a WRAPPER div, plus the `switch` attribute on the input -->
<div class="switch">
  <input type="checkbox" value="" id="s" role="switch" switch>
</div>
```

Putting `.switch` on the input renders a plain checkbox-sized box, not a toggle.
The `switch` attribute gives haptic feedback where supported. Sizes are
`.switch-sm` / `.switch-lg` on the wrapper.

## 2e. Combobox logs a console error on every instance (upstream, harmless)

Every `data-bs-toggle="combobox"` produces:

```text
Bootstrap doesn't allow more than one instance per element. Bound instance: bs.combobox.
```

Cause is upstream, not your markup: `Combobox`'s constructor calls
`_createMenuInstance()` → `new Menu(this._toggle, …)` on the element that already
holds `bs.combobox`, and `Data.set` refuses a second key on one element.

It's a `console.error`, not a throw. Verified working regardless: the menu opens,
selection updates `.combobox-value`, and the auto-created hidden input receives
the `data-bs-value`. Don't try to work around it — just expect the noise until
it's fixed upstream.

Also: `search` and `multiple` are **typed booleans**, so a bare attribute fails
config validation with `provided type "null" but expected type "boolean"`. Write
`data-bs-search="true"`, not `data-bs-search`. (Bare marker attributes are fine
for `data-bs-otp`, `data-bs-chips`, `data-bs-strength` and `data-bs-validate`.)

## 2d. Unlayered author CSS silently kills Bootstrap utilities

The flip side of §"@layer" — being unlayered means author CSS beats *everything*,
including utility classes you're still relying on in the markup.

`.price-list { margin: 0 }` (shorthand) overrode `.mb-6` on the same element, so
`mb-6` computed to `0px` and the pricing CTA sat flush against the last feature.
Nothing in devtools flags it as a conflict — the utility just loses.

Rule of thumb: in unlayered CSS, avoid shorthand `margin` / `padding` /
`background` / `border` on elements that also carry Bootstrap utilities. Set the
specific longhand (`margin-bottom`) or drop the utility and own the value.

## 3. CSS custom properties were renamed — this bites silently

`--bs-primary`, `--bs-body-bg`, and `--bs-body-color` **do not exist in v6**.
Referencing them makes the whole `color-mix()` invalid, the declaration is
dropped, and the element renders with no background — no console error, nothing
in devtools except a missing style. This cost real debugging time on this build.

| v5 | v6 |
| --- | --- |
| `--bs-primary` | `--bs-primary-base` |
| `--bs-body-bg` | `--bs-bg-body` |
| `--bs-body-color` | `--bs-fg-body` |
| `--bs-success` | `--bs-success-base` |
| `--bs-border-radius` | `--bs-radius-0` … `--bs-radius-9`, `--bs-radius-pill` |

Also new: surface/text scales `--bs-bg-1`…`--bs-bg-4` and `--bs-fg-1`…`--bs-fg-4`,
with matching `.bg-1`–`.bg-9` / `.fg-1`–`.fg-9` utilities.

Sanity-check any custom stylesheet before shipping:

```bash
grep -oE "var\(--bs-[a-z0-9-]+" assets/css/style.css | sort -u | sed 's/var(//' \
| while read v; do
    grep -q -- "$v:" assets/vendor/bootstrap6/css/bootstrap.css || echo "MISSING: $v"
  done
```

---

## 4. Navbar + drawer: declare the nav exactly once

This is the subtlest trap in v6. At `≥lg`, this rule fires:

```css
.lg\:navbar-expand [class*="drawer"] { visibility: visible !important; … }
```

Bootstrap deliberately un-hides the drawer's contents on desktop so they render
inline as the expanded navbar (and hides `.drawer-header` there). It's the v6
equivalent of v5's `.navbar-expand-lg .offcanvas`.

So put your nav **only** inside `.drawer-body`. The first build of this template
had a separate desktop `<ul>` plus a drawer, and both rendered on desktop — the
drawer contents appeared stacked at the top of the page. If you see that, this
is why.

Anything that should sit outside the collapsing area (theme toggle, primary CTA,
the toggler itself) goes as a sibling of the `<dialog>`, not inside it.

---

## 5. Things that are simply gone

Checked against the dist — these have **zero** occurrences:

- `.navbar-collapse` — replaced by the drawer pattern above
- `.lead`, `.display-1`…`.display-6` — use the `.fs-*` scale
- `Modal`, `Offcanvas`, `Dropdown` JS exports

The bundle exports exactly: `Alert, Button, Carousel, Chips, Collapse, Combobox,
Datepicker, Dialog, Drawer, Menu, NavOverflow, OtpInput, Popover, Range,
ScrollSpy, Strength, Tab, Toast, Toggler, Tooltip`.

---

## 6. Syntax reminders

- **Responsive prefixes** are written plainly in HTML (`class="md:d-none"`) but
  escape in CSS. `2xl` starts with a digit, so it compiles to `.\32 xl\:d-none` —
  matters only if you're writing selectors against it.
- **Breakpoints moved**: `lg` 992→**1024**, `xl` 1200→**1280**, `xxl`→`2xl`
  1400→**1536**. Media queries use range syntax (`@media (width >= 1024px)`).
- **ESM-only.** `<script type="module">` is required and there is no
  `window.bootstrap`. Importing the bundle for side effects is what registers the
  `data-bs-*` API.
- **Spacer scale changed.** To preserve v5 spacing: `.p-3`→`.p-4`, `.p-4`→`.p-6`,
  `.p-5`→`.p-9`. Keys now run 0–9.

---

## 7. Browser support

v6 requires `oklch()` and `color-mix()`. That's Safari 16.4+, Chrome 111+,
Firefox 113+ — roughly mid-2023 onward. There is no graceful degradation.

**Decision (2026-07-27): this is accepted.** Templates target evergreen browsers
only; don't spend effort on legacy fallbacks.

---

## Verified working in this build

Rendered in Chromium with zero console errors:

| Component | Check |
| --- | --- |
| Dialog | opens natively, `.dialog-open` lands on `<html>`, `::backdrop` blurs |
| Drawer | opens on mobile, inlines into the navbar at ≥lg |
| Menu | opens, positioned by Floating UI |
| Accordion | native `<details name>` gives exclusive open with no JS |
| Switch | drives the pricing toggle |
| Stepper | horizontal at ≥md via `md:stepper-horizontal` |
| Avatar | `.avatar-stack` overlap works |
| Form adorn | icon + `.form-ghost` input |
| ScrollSpy | `data-bs-top-margin="96px"` clears the sticky header; nav links track sections |
| Dark mode | `data-bs-theme` on `<html>`, persisted to localStorage |

ScrollSpy note: a `<button class="nav-link">` with no `href` (the "Resources"
menu toggle) sits happily inside the spied `<ul>` — it's skipped rather than
throwing.
