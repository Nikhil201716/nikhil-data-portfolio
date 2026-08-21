# Nikhil Sinha — Project Site

A static site covering the fifteen data and AI projects I built while learning the subject. No build step, no
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

That is also the site's argument. A write-up that asserts "+35% efficiency" is asking to be
believed. This one links the claim to the repository, the report file and the line of code
that produced it.

```bash
python build/build_catalog.py     # regenerate after any project reruns
```

## Structure

Multi-page, static, no build step. Bootstrap 5 handles the grid and components;
everything distinctive is hand-written CSS.

| Path | What it is |
|---|---|
| `index.html` | Landing page — hero, method, findings, subject areas, featured projects |
| `pages/projects.html` | The explorer: subject-area filters, search, deep-linkable via `?role=` |
| `pages/project.html` | Per-project page via `?id=NN` — metrics, charts, run button, notebook |
| `pages/books.html` | All fifteen notebooks |
| `pages/about.html` | Background, method, contact |
| `assets/css/site.css` | Design tokens, ambient layers, motion system, card effects |
| `assets/js/common.js` | Catalog loading, theme, nav, reveal/tilt/spotlight/counters, shared cards |
| `assets/js/{home,projects,project,books,about}.js` | One module per page |
| `data/catalog.json` | The extracted evidence — projects, metrics, charts, provenance |
| `assets/vendor/plotly-2.35.2.min.js` | Vendored Plotly (MIT). No CDN request for charts. |
| `build/` | The catalog generator. Not served. |

## Running a project from the site

Every project page has a **Run this project** button. It opens the repository in a
free GitHub Codespace, and a `.devcontainer/` in each repo installs the dependencies
and runs the full pipeline automatically — real output, real terminal, in the browser.

Static hosting cannot execute Python, so this is genuinely running on GitHub's
infrastructure rather than here. A free GitHub account is required and the compute
bills to that account's monthly allowance, not to the site owner. The exact commands
are also printed on the page for anyone who would rather run it locally.

Two projects benefit especially: Project 4 needs Airflow and Project 6 needs Redis,
neither of which runs natively on Windows — but both run fine in a Codespace.

## Contact

The email buttons open a **Gmail compose window** rather than a `mailto:` link.
`mailto:` only works when the visitor has a desktop mail client configured; on a
laptop with none it silently does nothing, which is the common case for a recruiter
clicking from a browser.

## Optional live backend

`python api/main.py` serves the same site on `:8200` plus three endpoints that reuse Project 12's
real artifacts rather than reimplementing anything: the bigram ticket router, the mutation-tested
pricing guardrails, and supply-chain impact by graph traversal. Each loads lazily and returns a
clear 503 if that project's artifacts are missing. The published site does not depend on it.

## Verified in a browser

- All five routes return 200; 15 project pages render from the catalog
- Subject-area filter deep-links (`?role=Testing & QA` → 4 of 15) and free-text search work
- Project pages draw all their charts from the catalog (P13: 7 metrics, 3/3 charts)
- Run button points at the right Codespace and the URL resolves (301 → github.com/codespaces/new)
- Light and dark themes both render; charts redraw on theme change
- **Mobile, 375x812:** no horizontal overflow, hamburger opens, terminal panel fits,
  charts render, cursor spotlight correctly disabled
- Zero JS errors on every page
- Plotly is vendored: no CDN request for charts

### Known limitation

`file://` is **not** supported. `fetch("data/catalog.json")` is blocked by Chrome's opaque origin
for local files, so the shell would paint with no content. Serve the directory over HTTP — which is
what GitHub Pages does. Making `file://` work would mean emitting the catalog as
`catalog.js` (`window.CATALOG = {...}`) instead of fetching JSON.

The hero counters animate, but the final value is written **before** the animation starts, with a
timeout fallback. `requestAnimationFrame` does not fire in a hidden or throttled tab, so a counter
that only reached its value inside the rAF loop showed `0` to anyone opening the page in a
background tab. That was a real bug, caught in testing, and is fixed.
