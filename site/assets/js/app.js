/* ------------------------------------------------------------------
   Shared frontend logic.

   Progressive enhancement is the core design decision: the site reads
   everything it needs from data/catalog.json, so it works fully as a
   static deploy (GitHub Pages, or even opened over http from disk).
   If the optional FastAPI backend happens to be reachable, the page
   upgrades itself - a status pill flips to "live" and the interactive
   demo panels appear. Nothing breaks when the API is absent, which is
   the normal case for a visitor.
------------------------------------------------------------------- */

const API_CANDIDATES = ["http://127.0.0.1:8200", "http://localhost:8200"];
const state = { catalog: null, apiBase: null };

/* ----------------------------------------------------------- theme */
function initTheme() {
  const saved = localStorage.getItem("theme");
  if (saved) document.documentElement.setAttribute("data-theme", saved);
  const btn = document.getElementById("themeBtn");
  if (!btn) return;
  const sync = () => {
    const light = document.documentElement.getAttribute("data-theme") === "light";
    btn.textContent = light ? "🌙 Dark" : "☀️ Light";
  };
  btn.addEventListener("click", () => {
    const light = document.documentElement.getAttribute("data-theme") === "light";
    const next = light ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
    sync();
    document.dispatchEvent(new CustomEvent("themechange"));
  });
  sync();
}

/* ------------------------------------------------------------ data */
async function loadCatalog() {
  if (state.catalog) return state.catalog;
  const res = await fetch("data/catalog.json", { cache: "no-store" });
  if (!res.ok) throw new Error(`catalog.json ${res.status}`);
  state.catalog = await res.json();
  return state.catalog;
}

/* ------------------------------------------------------- API probe */
async function probeApi() {
  for (const base of API_CANDIDATES) {
    try {
      const ctrl = new AbortController();
      const t = setTimeout(() => ctrl.abort(), 1200);
      const r = await fetch(`${base}/api/health`, { signal: ctrl.signal });
      clearTimeout(t);
      if (r.ok) {
        state.apiBase = base;
        document.body.classList.add("live-mode");
        setStatus(true);
        return base;
      }
    } catch (_) { /* API absent - static mode is the expected default */ }
  }
  setStatus(false);
  return null;
}

function setStatus(live) {
  const el = document.getElementById("apiStatus");
  if (!el) return;
  el.classList.toggle("live", live);
  el.querySelector(".label").textContent = live ? "Live API connected" : "Static mode";
  el.title = live
    ? `Backend reachable at ${state.apiBase} - interactive demos enabled`
    : "Showing pre-computed results. Start the API to enable live demos.";
}

/* ---------------------------------------------------------- charts */
function plotColors() {
  const cs = getComputedStyle(document.documentElement);
  return {
    text: cs.getPropertyValue("--text").trim(),
    dim: cs.getPropertyValue("--text-dim").trim(),
    grid: cs.getPropertyValue("--border").trim(),
    palette: [
      cs.getPropertyValue("--accent").trim(),
      cs.getPropertyValue("--accent-2").trim(),
      cs.getPropertyValue("--warn").trim(),
      cs.getPropertyValue("--danger").trim(),
    ],
  };
}

/* Plotly draws a title as one unwrapped <text>, and keeps category tick
   labels horizontal. Both silently clip at phone width - the SVG hides the
   overflow, so the page never scrolls and the loss is invisible. Wrap the
   title ourselves and rotate long ticks instead. */
function wrapSvgText(text, maxChars) {
  const words = String(text).split(/\s+/).filter(Boolean);
  const lines = [];
  let cur = "";
  for (const w of words) {
    if (cur && (cur + " " + w).length > maxChars) { lines.push(cur); cur = w; }
    else cur = cur ? cur + " " + w : w;
  }
  if (cur) lines.push(cur);
  return lines;
}

function renderChart(el, spec) {
  const c = plotColors();
  const width = el.clientWidth || 320;
  const narrow = width < 420;

  const titleSize = narrow ? 12.5 : 14;
  // 0.55em is a good average glyph advance for this UI font.
  const titleLines = wrapSvgText(spec.title || "", Math.max(18, Math.floor((width - 16) / (titleSize * 0.55))));

  // Vertical, not diagonal. At a slant, a long category label still has a wide
  // horizontal footprint, so adjacent labels (and the y-axis ticks) collide as
  // soon as the category names grow - it only ever looks fine for the data that
  // happened to be there when it was tuned. Vertical has no horizontal footprint.
  const longestTick = (spec.x || []).reduce((m, v) => Math.max(m, String(v).length), 0);
  const tickangle = narrow && longestTick > 8 ? -90 : 0;

  const traces = spec.series.map((s, i) => ({
    x: spec.x,
    y: s.y,
    name: s.name,
    type: spec.type === "line" ? "scatter" : "bar",
    mode: spec.type === "line" ? "lines+markers" : undefined,
    marker: { color: c.palette[i % c.palette.length] },
    line: { color: c.palette[i % c.palette.length], width: 2.5 },
  }));

  const layout = {
    title: { text: titleLines.join("<br>"), font: { size: titleSize, color: c.text } },
    paper_bgcolor: "rgba(0,0,0,0)",
    plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: c.dim, size: 11 },
    // automargin lets Plotly grow past these once ticks are rotated; they are
    // floors, not fixed values.
    margin: {
      l: narrow ? 46 : 58,
      r: narrow ? 10 : 18,
      t: 26 + titleLines.length * 16,
      b: 52,
    },
    xaxis: {
      gridcolor: c.grid, zerolinecolor: c.grid, title: spec.xaxis || "",
      tickangle, automargin: true,
      tickfont: { size: tickangle ? 9.5 : 11 },
    },
    yaxis: {
      gridcolor: c.grid, zerolinecolor: c.grid, title: spec.yaxis || "",
      type: spec.log_y ? "log" : "linear", automargin: true,
    },
    showlegend: spec.series.length > 1,
    // Rotated ticks eat the space the legend would otherwise sit in.
    legend: { orientation: "h", y: tickangle ? -0.42 : -0.22 },
    shapes: [], annotations: [],
  };

  if (spec.hline) {
    layout.shapes.push({
      type: "line", xref: "paper", x0: 0, x1: 1,
      y0: spec.hline.value, y1: spec.hline.value,
      line: { color: c.palette[2], width: 2, dash: "dash" },
    });
    layout.annotations.push({
      xref: "paper", x: 1, y: spec.hline.value, xanchor: "right", yanchor: "bottom",
      text: spec.hline.label, showarrow: false, font: { color: c.palette[2], size: 10 },
    });
  }

  Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
  el._spec = spec;
  el._renderedWidth = el.clientWidth;
  if (!el._observed) { chartObserver.observe(el); el._observed = true; }
}

function rerenderCharts() {
  document.querySelectorAll(".chart").forEach((el) => {
    if (el._spec) renderChart(el, el._spec);
  });
}

/* ---------------------------------------------------------- utils */
function esc(s) {
  return String(s).replace(/[&<>"']/g, (ch) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]
  ));
}

function metricsTable(metrics) {
  if (!metrics.length) {
    return '<p class="sub">No machine-readable metrics for this project yet — see its README.</p>';
  }
  const rows = metrics.map((m) => `
    <tr class="${m.highlight ? "hl" : ""}">
      <td>${esc(m.label)}<span class="src">${esc(m.source)}</span></td>
      <td class="v">${esc(m.value)}${m.note ? `<span class="note">${esc(m.note)}</span>` : ""}</td>
    </tr>`).join("");
  return `<table class="metrics">${rows}</table>`;
}

document.addEventListener("themechange", rerenderCharts);

/* Plotly's own responsive handler reflows the plot but reuses the title line
   breaks and tick angle chosen at the previous width, so a phone rotated to
   landscape would keep the narrow layout.

   Observe the chart elements rather than listening for window resize: it also
   catches a chart whose container changed without the window doing so, and it
   is the only one of the two that can actually be verified in a test harness
   (resizing an iframe fires no resize event on its window). */
let resizeTimer = null;

function refitCharts() {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    document.querySelectorAll(".chart").forEach((el) => {
      // Re-rendering resizes the element, which re-triggers the observer; only
      // acting on a real width change is what stops that from looping. It also
      // makes it harmless for both triggers below to fire for the same resize.
      if (el._spec && el._renderedWidth !== el.clientWidth) renderChart(el, el._spec);
    });
  }, 180);
}

// Two triggers on purpose. The observer is the more complete one, but neither
// could be exercised in the test harness used here (a throttled, non-visible
// page delivers no ResizeObserver callbacks at all), so this does not stake the
// behaviour on a single unverified mechanism.
const chartObserver = new ResizeObserver(refitCharts);
window.addEventListener("resize", refitCharts);
window.addEventListener("orientationchange", refitCharts);
