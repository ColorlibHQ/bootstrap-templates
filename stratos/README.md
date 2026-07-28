# Stratos — a Bootstrap 6 showcase template

A seven-page SaaS template built on **Bootstrap 6.0.0-alpha1**, exercising every
component in the alpha. No build step, no npm install, no dependencies beyond the
vendored Bootstrap dist.

> **Alpha notice.** Bootstrap 6 has not been released. There is no
> `bootstrap@6` package on npm — the CSS and JS here were built from the
> `v6-dev` branch at commit [`59cee6c`](https://github.com/twbs/bootstrap/commit/59cee6c16323d8431ed535e262b0f5759ea91f54)
> (2026-07-26) and vendored into `assets/vendor/`. Expect breaking changes
> until the real alpha ships. See [BOOTSTRAP6-NOTES.md](BOOTSTRAP6-NOTES.md).

## Preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Any static server works. Bootstrap 6 is ESM-only, so `main.js` loads as a module
— opening `index.html` over `file://` will **not** work. Serve it.

## Pages

| Page | What it demonstrates |
|---|---|
| `index.html` | Landing page — hero, stats band, features, use-case tabs, integrations with Combobox filter, stepper, pricing, comparison table, testimonials, FAQ accordion, newsletter with chip input |
| `components.html` | Every component, 26 sections with a sticky ScrollSpy table of contents |
| `forms.html` | All form controls, including the six that are new in v6 |
| `dashboard.html` | Application shell — sidebar, nav overflow, stat cards, chart, data table with row menus, filter drawer, toast |
| `pricing.html` | Plan cards, full feature comparison with tooltips, billing FAQ |
| `blog-post.html` | Long-form article using `.prose`, breadcrumb, TOC, pagination |
| `404.html` | Error page with search and popular-page chips |

## Structure

```text
bootstrap6-pilot/
├── index.html  components.html  forms.html  dashboard.html
├── pricing.html  blog-post.html  404.html
├── assets/
│   ├── css/style.css                 # custom styles (intentionally unlayered)
│   ├── js/main.js                    # ESM, one init function per feature
│   └── vendor/bootstrap6/            # pinned alpha dist — do not edit
├── BOOTSTRAP6-NOTES.md               # v6 gotchas found while building this
└── README.md
```

## Bootstrap 6 coverage

**Renamed from v5** — Dialog (was Modal), Drawer (was Offcanvas), Menu (was Dropdown).

**New in v6, no v5 equivalent** — Combobox, Datepicker, Chip / Chip input,
OTP input, password Strength, enhanced Range, Nav overflow, Toggler, Stepper,
Avatar, Form adorn, Prose.

**Rebuilt** — Accordion on native `<details>`, Carousel on CSS scroll-snap,
ScrollSpy on IntersectionObserver.

**Also covered** — buttons and theme tokens, badges, alerts, cards, collapse,
tabs, toasts, tooltips, popovers, progress, spinners, list groups, breadcrumbs,
pagination, placeholders, tables, the `fs-*` type scale and the `bg-*`/`fg-*`
surface scales.

Every page renders with **zero console errors**, apart from one known upstream
Combobox warning documented in the notes.

## Customizing

**Colors.** Bootstrap 6 is CSS-first — override the tokens, no Sass build needed:

```css
:root {
  --bs-primary-base: oklch(62% 0.19 265);
}
```

Note the names changed: it's `--bs-primary-base`, not `--bs-primary`. See the
notes for the full mapping and a script that catches undefined variables.

**Custom CSS.** Keep it out of `@layer`. Bootstrap wraps all of its own styles in
cascade layers, so unlayered author CSS wins automatically — `assets/css/style.css`
relies on this. The trade-off is that shorthand properties there will also beat
utility classes on the same element; use longhands.

**Content.** Plain HTML throughout. Placeholder avatars are initials-based
`<span class="avatar-initials">`; swap for `<img class="avatar-img" src="…" alt="…">`
when you have real photos. Logo lockups in the trust strip are inline SVG marks.

## Browser support

Modern evergreen browsers: **Safari 16.4+, Chrome 111+, Firefox 113+** (mid-2023
onward). Bootstrap 6 builds on `oklch()` and `color-mix()`, so this template
targets current browsers by design and ships no legacy fallbacks.

## Forms

Frontend-only. Forms validate with native constraints plus v6's
`data-bs-validate` styling, then fake success. Point them at a real endpoint
before using them for anything.

## License

MIT. Bootstrap is licensed separately under MIT by the Bootstrap Authors.
