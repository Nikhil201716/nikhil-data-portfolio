# Nikhil Sinha — Portfolio Website

A single static site covering all fifteen projects in the portfolio. No build step, no
framework, no CDN, no hosting bill: three files plus a JSON catalog, deployed free on
GitHub Pages.

```bash
python -m http.server 8700
```

Then open <http://127.0.0.1:8700>.

## The rule this site is built on

**No number here is typed by hand.** `build/build_catalog.py` opens each project's own
`reports/*.json` and extracts its metrics with a per-project extractor, so every figure on
the page traces back to a file produced by a real executed run — 78 metrics across 15
projects at the last build. Projects 1–4 predate that convention, so their numbers are quoted
from the results table in their README and tagged `readme` in the UI: the provenance is
visible rather than implied. If an extractor cannot find its report, the project renders with
"no machine-readable metrics" instead of a plausible-looking fabrication.

That is also the site's argument. A portfolio that asserts "+35% efficiency" is asking to be
believed. This one links the claim to the repository, the report file and the line of code
that produced it.

```bash
python build/build_catalog.py     # regenerate after any project reruns
```

## Structure

| Path | What it is |
|---|---|
| `index.html` | The whole page. Static shell; every list is rendered by JS from the catalog. |
| `assets/js/site.js` | Rendering, filtering, the project modal, and chart drawing. |
| `assets/css/site.css` | Theme tokens for dark/light, layout, motion. |
| `data/catalog.json` | The extracted evidence — projects, metrics, charts, provenance tags. |
| `assets/vendor/plotly-2.35.2.min.js` | Vendored Plotly (MIT). No CDN request is ever made. |
| `build/` | The catalog generator. Not served. |
| `api/main.py` | Optional local FastAPI backend (see below). Not needed by the site. |

Sections: hero → **Evidence** (why the numbers are checkable) → **Findings** (six results worth
an interview conversation) → **Skills** (five roles, each filtering the project grid) →
**Projects** (15 cards, searchable, each opening a modal with its measured metrics and charts) →
**Books** (the 60-page technical notebook per project) → About.

## Optional live backend

`python api/main.py` serves the same site on `:8200` plus three endpoints that reuse Project 12's
real artifacts rather than reimplementing anything: the bigram ticket router, the mutation-tested
pricing guardrails, and supply-chain impact by graph traversal. Each loads lazily and returns a
clear 503 if that project's artifacts are missing. The published site does not depend on it.

## Verified in a browser

- 15 project cards, 6 findings, 5 role filters, 39 stack chips, 15 book entries, **0 JS errors**
- Role filter (QA / SDET → 4 of 15) and free-text search ("survival" → 1 of 15) both correct
- Project modal opens with its metrics and draws **all** its charts from the catalog (P14: 8 metrics, 3/3 charts)
- Light and dark themes both render; charts are redrawn on theme change
- **Mobile, 375×812:** no horizontal overflow, hamburger menu opens, hero fits the viewport
- Plotly is vendored: zero requests to `cdn.plot.ly`

### Known limitation

`file://` is **not** supported. `fetch("data/catalog.json")` is blocked by Chrome's opaque origin
for local files, so the shell would paint with no content. Serve the directory over HTTP — which is
what GitHub Pages does. Making `file://` work would mean emitting the catalog as
`catalog.js` (`window.CATALOG = {...}`) instead of fetching JSON.

The hero counters animate, but the final value is written **before** the animation starts, with a
timeout fallback. `requestAnimationFrame` does not fire in a hidden or throttled tab, so a counter
that only reached its value inside the rAF loop showed `0` to anyone opening the page in a
background tab. That was a real bug, caught in testing, and is fixed.
