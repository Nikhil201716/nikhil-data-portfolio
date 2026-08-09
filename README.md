# Data & AI Portfolio Website

A single site covering every project in this portfolio, with **two ways to run it**:

| Mode | Command | What you get |
|---|---|---|
| **Static** | `python -m http.server 8300 --directory site` | The full site, all charts and metrics. Deploys to GitHub Pages as-is — no server, no cost, works forever. |
| **Live** | `python api/main.py` | The same site on `http://127.0.0.1:8200`, plus interactive demos that run the real models the projects trained. |

The site is built **static-first**: everything a visitor needs lives in `site/data/catalog.json`.
If the optional backend happens to be reachable, the page detects it and upgrades itself — a status
pill flips to "Live API connected" and interactive panels appear. Nothing breaks when the API is
absent, which is the normal case for someone clicking a link on a CV.

## The rule this site is built on

**No number here is typed by hand.** `build/build_catalog.py` opens each project's own
`reports/*.json` and extracts the metrics with a per-project extractor, so any figure on the site
traces back to a file produced by a real executed run. Projects 1–4 predate that convention, so
their numbers are quoted from the results table in their README and tagged `readme` in the UI —
the provenance is visible, not implied. If an extractor cannot find its report, the project renders
with "no machine-readable metrics" rather than a plausible-looking fabrication.

```bash
python build/build_catalog.py     # regenerate after any project reruns
```

## Live endpoints

These reuse Project 12's real artifacts rather than reimplementing anything:

- `POST /api/live/classify` — the bigram ticket router (the model P12 measured as worth shipping
  over a transformer that scored identically while being 36.7x slower)
- `POST /api/live/price` — the pricing guardrails, mutation-tested to 81.5%
- `GET  /api/live/impact/{id}` — supply-chain impact by graph traversal, the query where text
  retrieval scored 0.000 F1

Each loads lazily and returns a clear 503 if that project's artifacts are missing, so a partial
checkout degrades gracefully instead of taking the whole site down.

## Deploying free to GitHub Pages

```bash
python build/build_catalog.py
# commit the site/ directory; point Pages at it. Nothing else required.
```

## Verified

- Live mode: all three interactive demos driven in a real browser and returning correct results
- Static mode: API stopped, site reloaded — falls back to "Static mode", all 12 cards, charts and
  findings still render
- Charts render from a **vendored** Plotly (`assets/vendor/plotly-2.35.2.min.js`, 4.35 MB, MIT),
  confirmed by the network log: zero requests to `cdn.plot.ly`, `Plotly.version === "2.35.2"`
- **Mobile, 375x812:** all 12 project pages plus the index checked programmatically — no page
  overflow, and across all 47 rendered SVG layers no chart text is clipped by its plot area and no
  two text nodes overlap. Desktop (1280px) re-checked afterwards for regressions: titles stay on one
  line and category ticks stay horizontal, as before.

That check found two real defects that the earlier 762px pass could not see, both now fixed in
`renderChart`:

- Plotly draws a chart title as one unwrapped `<text>`. Long titles ran past the plot area and were
  **silently clipped** — the SVG hides the overflow, so the page never scrolls and nothing looks
  wrong. Titles are now wrapped to the measured chart width.
- Long category tick labels ("Difference-in-differences") overflowed the same way. They are now
  rotated vertical below 420px, not merely slanted: at a slant a long label still has a wide
  horizontal footprint, so adjacent labels collide again as soon as the category names grow — an
  intermediate `-35°` fix measured clean on some charts while still colliding on P9 and P12.

**Not verified:** the reflow when a device rotates. Charts re-fit via a `ResizeObserver` plus
`resize`/`orientationchange` listeners, but none of them could be exercised here — the test pane
runs the page throttled and non-visible (`visibilityState: "hidden"`), where the browser fires no
animation frames and therefore delivers no `ResizeObserver` callbacks at all, not even the mandatory
one on `observe()`. The redundant triggers are deliberate for that reason. The width-guard that
prevents a re-render loop is exercised by ordinary rendering; the rotation path is not.

**Claim withdrawn — "also loads correctly from `file://`".** This was listed as verified in an
earlier pass and is no longer. It could not be re-tested (the browser pane refuses to execute
`file://` pages), and there is concrete reason to doubt it: `loadCatalog()` uses
`fetch("data/catalog.json")`, and Chrome gives a `file://` page an opaque origin, which blocks
`fetch` of a sibling local file. The shell would paint but no cards or charts would populate. Vendoring
Plotly removed the *network* dependency, not this one. Treat `file://` as unsupported until someone
opens it and confirms; serving the directory over `http.server` is the supported zero-cost path.
Making it genuinely true would mean emitting the catalog as `catalog.js` (`window.CATALOG = {...}`)
instead of fetching JSON.
