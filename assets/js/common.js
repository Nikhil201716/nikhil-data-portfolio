/* ==========================================================================
   common.js — shared across every page
   Catalog loading, theme, nav, and the motion system (reveal, tilt,
   spotlight, counters, scroll progress).
   ========================================================================== */

const GH = "https://github.com/Nikhil201716";
const EMAIL = "nikhil.sinha16022003@gmail.com";

/* Gmail compose, which is what most people actually want when they click an
   email button. mailto: only works if a desktop mail client is configured,
   and on a laptop with none it silently does nothing. */
const GMAIL = "https://mail.google.com/mail/?view=cm&fs=1"
  + "&to=" + encodeURIComponent(EMAIL)
  + "&su=" + encodeURIComponent("Hello Nikhil")
  + "&body=" + encodeURIComponent("Hi Nikhil,\n\nI came across your project write-ups and wanted to get in touch about ");

const $  = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => [...r.querySelectorAll(s)];
const esc = (s) => String(s ?? "").replace(/[&<>"']/g,
  (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

const REDUCED = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

/* ------------------------------------------------------------------ books */
const BOOKS = [
  ["01", "UPI Payments Complaint & SLA Analytics", "01-UPI-Payments-Complaint-SLA-Dashboard", "Project-01-UPI-Complaint-SLA-Analytics-Notebook.pdf", 60],
  ["02", "E-commerce Churn & RFM Segmentation", "02-Ecommerce-Customer-Churn-RFM-Segmentation", "Project-02-Ecommerce-Churn-RFM-Notebook.pdf", 61],
  ["03", "Retail Demand Forecasting & Inventory Planning", "03-Retail-Demand-Forecasting-Inventory-Dashboard", "Project-03-Retail-Demand-Forecasting-Notebook.pdf", 81],
  ["04", "Multi-Source Sales ETL with Apache Airflow", "04-Multi-Source-Sales-ETL-Pipeline-Airflow-AWS", "Project-04-Airflow-ETL-Pipeline-Notebook.pdf", 69],
  ["05", "AI-Augmented Data Quality & Validation", "05-AI-Augmented-Data-Quality-Validation-Framework", "Project-05-Data-Quality-RAG-Copilot-Notebook.pdf", 66],
  ["06", "Real-Time Transaction Streaming & Fraud Detection", "06-Realtime-Transaction-Streaming-Pipeline", "Project-06-Realtime-Streaming-Fraud-Notebook.pdf", 61],
  ["07", "Autonomous AI Ops & Recommendation Platform", "07-Autonomous-AI-Ops-Recommendation-Platform", "Project-07-Autonomous-AI-Ops-Recommender-Notebook.pdf", 62],
  ["08", "AutoClaim Intelligence Platform", "08-AutoClaim-Intelligence-Platform", "Project-08-AutoClaim-Multimodal-AI-Notebook.pdf", 64],
  ["09", "Trust-Aware Experimentation Platform", "09-Trust-Aware-Experimentation-Platform", "Project-09-Trust-Aware-Experimentation-Notebook.pdf", 84],
  ["10", "Delivery Operations Intelligence Platform", "10-Delivery-Operations-Intelligence-Platform", "Project-10-Delivery-Ops-Causal-Inference-Notebook.pdf", 69],
  ["11", "Fair Lending Intelligence Platform", "11-Fair-Lending-Intelligence-Platform", "Project-11-Fair-Lending-Fairness-Audit-Notebook.pdf", 78],
  ["12", "Retail Intelligence Platform", "12-Retail-Intelligence-Platform", "Project-12-Retail-Intelligence-OPE-Notebook.pdf", 88],
  ["13", "Meridian Operations Cloud", "13-Meridian-Operations-Cloud", "Project-13-Meridian-Operations-Cloud-Notebook.pdf", 80],
  ["14", "Cascade Realtime Intelligence Platform", "14-Cascade-Realtime-Intelligence-Platform", "Project-14-Cascade-Realtime-Streaming-Notebook.pdf", 84],
  ["15", "Aegis Health Plan Intelligence Platform", "15-Aegis-Health-Plan-Platform", "Project-15-Aegis-Health-Plan-Notebook.pdf", 60],
].map(([id, title, repo, file, pages]) => ({ id, title, repo, file, pages }));

const BOOK_BY_ID = Object.fromEntries(BOOKS.map((b) => [b.id, b]));
const TOTAL_PAGES = BOOKS.reduce((s, b) => s + b.pages, 0);

/* --------------------------------------------------------------- findings */
const FINDINGS = [
  { metric: "0.0352", title: "The evaluation split was worth 24x",
    body: "Point-in-time-correct features scored PR-AUC 0.8495 on a random split and 0.0352 on a temporal one. Identical features. A 2x2 factorial separated the split from the leaky feature table, and the split was the larger sin.",
    id: "13", verify: "reports/feature_store_skew.json" },
  { metric: "+77.8pt", title: "An LLM judge approved every wrong answer",
    body: "28 false passes, zero false fails. A 22.2% agent would have been reported at 100%. The judge's own accuracy equalled the agent's exactly, which is the arithmetic signature of a judge that never fails anything.",
    id: "14", verify: "reports/agent_eval.json" },
  { metric: "0.1818", title: "A fraud detector an adversary switched off",
    body: "95.45% recall against an unaware adversary. Upcoding 15% of claims instead of 42% - same scheme, same codes - dropped it to 18.18%. The cheapest available adaptation was the most effective.",
    id: "15", verify: "reports/upcoding_detection.json" },
  { metric: "39,103", title: "One fast clock discarded 95.7% of a stream",
    body: "A max-based watermark jumped 200s ahead and dropped 39,103 of 40,877 messages, while every window still emitted. Changing max to p99 cut the error 15-fold; a causality check fixed the cause with no threshold at all.",
    id: "14", verify: "reports/windowing.json" },
  { metric: "+34.6%", title: "A causal estimate with the wrong sign",
    body: "The intervention reduced delivery time 18%. A naive treated-vs-control comparison reported it as 34.6% worse, because it was rolled out to regions already 27 minutes behind. Difference-in-differences recovered -19.7%.",
    id: "10", verify: "reports/causal_inference_evaluation.json" },
  { metric: "33 / 50", title: "One definition change restated the board pack",
    body: "Excluding pharmacy from loss ratio moved 33 of 50 published figures, several across the 1.0 boundary separating a profitable plan from an unprofitable one. The blast radius was computed and named, not estimated.",
    id: "15", verify: "reports/metric_regression.json" },
];

/* ---------------------------------------------------------- area blurbs */
const AREA_BLURB = {
  "Data Analysis": "SQL, metric definitions, cohort analysis, dashboards and the discipline of saying what a number does not establish.",
  "Data Engineering": "Orchestration, idempotency, data contracts, streaming semantics and warehouses that fail loudly rather than quietly.",
  "Testing & QA": "Property-based, metamorphic and contract testing, mutation and injected-bug scoring, flakiness hunting, Playwright E2E.",
  "AI & LLM Systems": "RAG with calibrated refusal, agent evaluation against golden sets, prompt-injection defence, and grounding that puts correctness in code.",
  "Machine Learning": "Model registries with gates that reject, drift monitoring, calibration, off-policy evaluation and adversarial robustness.",
};

/* ------------------------------------------------------------- catalog IO */
let _catalog = null;
async function getCatalog() {
  if (_catalog) return _catalog;
  const r = await fetch(base() + "data/catalog.json");
  if (!r.ok) throw new Error("catalog " + r.status);
  _catalog = await r.json();
  return _catalog;
}

/* Works whether the page is at / or /pages/ */
function base() {
  return location.pathname.includes("/pages/") ? "../" : "";
}

function projectUrl(id) { return base() + "pages/project.html?id=" + id; }
function codespaceUrl(repo) { return "https://codespaces.new/Nikhil201716/" + repo + "?quickstart=1"; }

/* ------------------------------------------------------------------ chrome */
function initChrome() {
  // theme
  const saved = localStorage.getItem("theme");
  if (saved) document.documentElement.dataset.theme = saved;
  $("#theme")?.addEventListener("click", () => {
    const cur = document.documentElement.dataset.theme === "light" ? "dark" : "light";
    document.documentElement.dataset.theme = cur;
    localStorage.setItem("theme", cur);
    document.dispatchEvent(new CustomEvent("themechange"));
  });

  // nav shadow on scroll + progress bar
  const nav = $(".site-nav"), bar = $(".scroll-bar");
  const onScroll = () => {
    nav?.classList.toggle("scrolled", window.scrollY > 8);
    if (bar) {
      const h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + "%";
    }
  };
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // mark the active nav item
  const here = location.pathname.split("/").pop() || "index.html";
  $$(".nav-link-x").forEach((a) => {
    const target = a.getAttribute("href").split("/").pop().split("#")[0];
    if (target === here) a.classList.add("active");
  });

  // every email button goes to Gmail compose
  $$("[data-gmail]").forEach((a) => {
    a.href = GMAIL;
    a.target = "_blank";
    a.rel = "noopener";
  });

  $$("[data-year]").forEach((el) => (el.textContent = new Date().getFullYear()));
}

/* ------------------------------------------------------------------ motion */
function initMotion() {
  // reveal on scroll
  if (REDUCED) {
    $$(".reveal").forEach((el) => el.classList.add("in"));
  } else {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });
    $$(".reveal").forEach((el) => io.observe(el));
  }

  // pointer spotlight + card glow, desktop only
  if (!REDUCED && matchMedia("(pointer: fine)").matches) {
    document.body.classList.add("has-pointer");
    const spot = $(".spot");
    addEventListener("pointermove", (e) => {
      if (spot) { spot.style.left = e.clientX + "px"; spot.style.top = e.clientY + "px"; }
    }, { passive: true });

    $$(".card-x").forEach((card) => {
      card.addEventListener("pointermove", (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
      });
    });

    // subtle 3D tilt
    $$(".tilt").forEach((el) => {
      el.addEventListener("pointermove", (e) => {
        const r = el.getBoundingClientRect();
        const px = (e.clientX - r.left) / r.width - 0.5;
        const py = (e.clientY - r.top) / r.height - 0.5;
        el.style.transform =
          `perspective(900px) rotateX(${(-py * 5).toFixed(2)}deg) rotateY(${(px * 5).toFixed(2)}deg) translateY(-4px)`;
      });
      el.addEventListener("pointerleave", () => (el.style.transform = ""));
    });
  }
}

/* Counters. The final value is written FIRST and unconditionally, because
   requestAnimationFrame does not fire in a hidden or throttled tab - a
   counter that only reaches its value inside a rAF loop shows 0 to anyone
   who opens the page in a background tab. */
function animateCounters(root = document) {
  $$("[data-count]", root).forEach((el) => {
    const target = Number(el.dataset.count) || 0;
    const suffix = el.dataset.suffix || "";
    el.textContent = target.toLocaleString() + suffix;
    if (REDUCED || target === 0) return;

    let done = false;
    const finish = () => { if (!done) { done = true; el.textContent = target.toLocaleString() + suffix; } };
    const dur = 1200, t0 = performance.now();
    (function step(now) {
      if (done) return;
      const k = Math.min((now - t0) / dur, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - k, 3))).toLocaleString() + suffix;
      if (k < 1) requestAnimationFrame(step); else finish();
    })(t0);
    setTimeout(finish, dur + 500);
  });
}

/* ----------------------------------------------------------------- charts */
function palette() {
  const cs = getComputedStyle(document.documentElement);
  const v = (n) => cs.getPropertyValue(n).trim();
  return {
    ink: v("--ink"), ink2: v("--ink-2"), ink3: v("--ink-3"),
    line: v("--line"), brand: v("--brand"), brand2: v("--brand-2"),
    accent: v("--accent"), good: v("--good"), warn: v("--warn"), bad: v("--bad"),
  };
}

function drawChart(el, spec) {
  if (typeof Plotly === "undefined") return;
  const p = palette();
  const colors = [p.brand, p.accent, p.brand2, p.good, p.warn, p.bad];
  const traces = (spec.series || []).map((s, i) => ({
    type: spec.type === "line" ? "scatter" : "bar",
    mode: spec.type === "line" ? "lines+markers" : undefined,
    name: s.name, x: spec.x, y: s.y,
    marker: { color: colors[i % colors.length] },
    line: { color: colors[i % colors.length], width: 2.5 },
  }));
  const layout = {
    margin: { l: 56, r: 16, t: 44, b: 52 },
    height: 320,
    title: { text: spec.title || "", font: { size: 13, color: p.ink2 }, x: 0, xanchor: "left" },
    paper_bgcolor: "rgba(0,0,0,0)", plot_bgcolor: "rgba(0,0,0,0)",
    font: { color: p.ink3, size: 11, family: "Inter, sans-serif" },
    xaxis: { gridcolor: p.line, zerolinecolor: p.line, automargin: true },
    yaxis: { gridcolor: p.line, zerolinecolor: p.line, title: spec.yaxis || "",
             type: spec.log_y ? "log" : "linear", automargin: true },
    showlegend: (spec.series || []).length > 1,
    legend: { orientation: "h", y: -0.22, font: { size: 10 } },
  };
  Plotly.newPlot(el, traces, layout, { displayModeBar: false, responsive: true });
}

/* --------------------------------------------------------------- shared UI */
function bookCard(b) {
  if (!b) return "";
  return `<a class="book" href="${GH}/${b.repo}/blob/main/docs/${b.file}" target="_blank" rel="noopener">
    <span class="book-spine"></span>
    <div class="book-t">Project ${esc(b.id)} — ${esc(b.title)}</div>
    <div class="book-m">${b.pages} pages · PDF</div>
    <div class="book-cta">Read the notebook →</div>
  </a>`;
}

function projectCard(p, delayClass = "") {
  const m = (p.metrics || [])[0];
  return `<a class="card-x pcard tilt reveal ${delayClass}" href="${projectUrl(p.id)}">
    <div class="d-flex justify-content-between align-items-start">
      <span class="num-badge">PROJECT ${esc(p.id)}</span>
      ${m ? `<span class="metric-v hi">${esc(m.value)}</span>` : ""}
    </div>
    <div class="pcard-title">${esc(p.title)}</div>
    <p class="pcard-pitch">${esc(p.pitch || "")}</p>
    <div>${(p.roles || []).slice(0, 3).map((r) => `<span class="chip role">${esc(r)}</span>`).join("")}</div>
    <div class="mt-2">${(p.stack || []).slice(0, 4).map((s) => `<span class="chip">${esc(s)}</span>`).join("")}</div>
  </a>`;
}

document.addEventListener("DOMContentLoaded", () => { initChrome(); });
