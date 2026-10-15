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
  ["16", "Concord, a Double-Entry Reconciliation Engine", "Concord-Reconciliation-Engine", "Concord-Notebook.pdf", 60],
  ["17", "Sift, a Log Search Engine & Index Benchmark", "Sift-Log-Search-Engine", "Sift-Notebook.pdf", 60],
  ["18", "Ironclad, Verified Cryptography & a Secure Channel", "Ironclad-Secure-Channel", "Ironclad-Notebook.pdf", 60],
  ["19", "Attest, On-Chain Provenance & Escrow", "Attest-Onchain-Provenance", "Attest-Notebook.pdf", 60],
  ["20", "Timeslice, an Operating-Systems Laboratory", "Timeslice-OS-Lab", "Timeslice-Notebook.pdf", 60],
  ["21", "Cadence, Soft-Computing Traffic Signal Control", "Cadence-Traffic-Control", "Cadence-Notebook.pdf", 60],
  ["22", "Turnstile, Event Ticketing Under Contention", "Turnstile-Event-Ticketing", "Turnstile-Notebook.pdf", 60],
  ["23", "Quantile, Applied Statistics on Air Quality", "Quantile-Air-Quality-Statistics", "Quantile-Notebook.pdf", 61],
  ["24", "Stratus, Cloud Media-Pipeline Economics", "Stratus-Cloud-Media-Pipeline", "Stratus-Notebook.pdf", 60],
  ["25", "Fieldnote, Offline-First Inspection Sync", "Fieldnote-Offline-Inspection", "Fieldnote-Notebook.pdf", 60],
  ["26", "Relay, a URL Shortener & the Test Pyramid", "Relay-URL-Shortener", "Relay-Notebook.pdf", 60],
  ["27", "Accord, REST + GraphQL Contract Testing", "Accord-Contract-Testing", "Accord-Notebook.pdf", 60],
  ["28", "Assay, ETL Data-Quality Testing", "Assay-Data-Quality", "Assay-Notebook.pdf", 60],
  ["29", "Surge, Load & Reliability Testing", "Surge-Load-Testing", "Surge-Notebook.pdf", 60],
  ["30", "Gauntlet, a CI/CD Quality Gate", "Gauntlet-Quality-Gate", "Gauntlet-Notebook.pdf", 62],
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
  // "no-cache" revalidates with the server (via ETag) before using a cached
  // copy, so a returning visitor never sees a stale catalog in the window
  // after a deploy - without refetching the whole file when it is unchanged.
  const r = await fetch(base() + "data/catalog.json", { cache: "no-cache" });
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

/* -------------------------------------------------------------- location */
/* A public page cannot auto-detect where Nikhil is, so the city is read from a
   single editable file (data/location.json). The live clock is computed in that
   city's timezone with Intl, so it is always correct without a server. Change
   the one file to relocate; every pill and footer updates. */
let _loc = null;
async function getLocation() {
  if (_loc) return _loc;
  try {
    const r = await fetch(base() + "data/location.json", { cache: "no-cache" });
    _loc = r.ok ? await r.json() : null;
  } catch { _loc = null; }
  if (!_loc) _loc = { label: "Currently in", city: "Bengaluru",
                      region: "Karnataka, India", tz: "Asia/Kolkata" };
  return _loc;
}
function _clockText(tz) {
  try {
    const t = new Intl.DateTimeFormat("en-GB",
      { timeZone: tz, hour: "2-digit", minute: "2-digit", hour12: false }).format(new Date());
    const parts = new Intl.DateTimeFormat("en-US",
      { timeZone: tz, timeZoneName: "short" }).formatToParts(new Date());
    const abbr = (parts.find((p) => p.type === "timeZoneName") || {}).value || "";
    return abbr ? `${t} ${abbr}` : t;
  } catch { return ""; }
}
async function initLocation() {
  const hooks = $$("[data-location]");
  if (!hooks.length) return;
  const loc = await getLocation();
  const clocks = [];
  hooks.forEach((el) => {
    const mode = el.getAttribute("data-location") || "inline";
    if (mode === "pill") {
      el.classList.add("loc-pill");
      el.innerHTML = `<span class="loc-dot" aria-hidden="true"></span>`
        + `<span class="loc-city">${esc(loc.city)}</span>`
        + `<span class="loc-sep">·</span><span class="loc-clock mono"></span>`;
      el.title = `${loc.label} ${loc.city}, ${loc.region}`;
    } else {
      el.innerHTML = `${esc(loc.city)} <span class="loc-sep">·</span> `
        + `<span class="loc-clock mono"></span>`;
      el.title = `${loc.label} ${loc.city}, ${loc.region}`;
    }
    const c = el.querySelector(".loc-clock");
    if (c) clocks.push(c);
  });
  const tick = () => { const t = _clockText(loc.tz); clocks.forEach((c) => (c.textContent = t)); };
  tick();
  if (!REDUCED) setInterval(tick, 1000);
}

/* ------------------------------------------------------------- profile IO */
let _profile = null, _profileP = null;
function getProfile() {
  if (_profile) return Promise.resolve(_profile);
  if (_profileP) return _profileP;
  _profileP = fetch(base() + "data/profile.json", { cache: "no-cache" })
    .then((r) => (r.ok ? r.json() : null)).catch(() => null)
    .then((p) => { _profile = p; return p; });
  return _profileP;
}
/* If a photo path is set in profile.json and it loads, swap the monogram for it.
   When it's null (default) nothing is requested, so the console stays clean. */
function hydrateAvatars() {
  getProfile().then((pr) => {
    const src = pr && pr.photo;
    if (!src) return;
    const url = /^https?:/.test(src) ? src : base() + src;
    const probe = new Image();
    probe.onload = () => $$("[data-avatar]").forEach((a) => {
      if (a.querySelector(".avatar-img")) return;
      const im = document.createElement("img");
      im.className = "avatar-img"; im.src = url; im.alt = "Nikhil Sinha";
      a.insertBefore(im, a.firstChild);
    });
    probe.src = url;
  });
}

/* -------------------------------------------------- ⌘K command palette */
/* A keyboard-first launcher over everything on the site: projects, books,
   skill areas, pages and quick actions. Built once, lazily, from the catalog. */
let _cmdkIndex = null;
async function _buildCmdkIndex() {
  if (_cmdkIndex) return _cmdkIndex;
  const b = base();
  const items = [
    { type: "Page", label: "Home", sub: "the landing page", href: b + "index.html" },
    { type: "Page", label: "Projects", sub: "all 30, filterable", href: b + "pages/projects.html" },
    { type: "Page", label: "Books", sub: "30 notebooks", href: b + "pages/books.html" },
    { type: "Page", label: "About", sub: "my story", href: b + "pages/about.html" },
    { type: "Action", label: "Toggle light / dark", sub: "theme", action: "theme" },
    { type: "Action", label: "Email me", sub: EMAIL, action: "email" },
    { type: "Action", label: "GitHub", sub: "github.com/Nikhil201716", action: "github" },
  ];
  for (const r of ["Data Analysis", "Data Engineering", "Machine Learning",
                   "AI & LLM Systems", "Testing & QA"]) {
    items.push({ type: "Area", label: r, sub: "projects in this area",
                 href: b + "pages/projects.html?role=" + encodeURIComponent(r) });
  }
  for (const bk of BOOKS) {
    items.push({ type: "Book", label: bk.title, sub: `${bk.pages}-page notebook`,
                 href: `${GH}/${bk.repo}/blob/main/docs/${bk.file}`, ext: true, kw: bk.id });
  }
  try {
    const cat = await getCatalog();
    for (const p of cat.projects) {
      items.push({
        type: "Project", label: p.title,
        sub: `Project ${p.id} · ${(p.roles || []).join(", ")}`,
        href: b + "pages/project.html?id=" + p.id,
        kw: `${p.id} ${(p.topics || []).join(" ")} ${(p.stack || []).join(" ")} ${(p.roles || []).join(" ")}`,
      });
    }
  } catch { /* catalog optional for the palette */ }
  _cmdkIndex = items;
  return items;
}
function _cmdkScore(item, tokens) {
  if (!tokens.length) return 0.001;
  const label = item.label.toLowerCase();
  const hay = (item.label + " " + item.sub + " " + (item.kw || "")).toLowerCase();
  let s = 0;
  for (const t of tokens) {
    if (hay.indexOf(t) < 0) return -1;      // every token must appear somewhere
    const li = label.indexOf(t);
    s += li === 0 ? 3 : li > 0 ? 2 : 1;
  }
  return s;
}
function initCommandPalette() {
  // inject a trigger into both nav clusters
  const trigger = () => {
    const btn = document.createElement("button");
    btn.className = "icon-btn cmdk-trigger";
    btn.type = "button";
    btn.setAttribute("aria-label", "Search (Ctrl/Cmd K)");
    btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>';
    btn.addEventListener("click", open);
    return btn;
  };
  const deskNav = $(".site-nav .d-none.d-lg-flex");
  const mobNav = $(".site-nav .d-flex.d-lg-none");
  if (deskNav) deskNav.insertBefore(trigger(), $("#theme", deskNav) || deskNav.firstChild);
  if (mobNav) mobNav.insertBefore(trigger(), mobNav.firstChild);

  const el = document.createElement("div");
  el.className = "cmdk"; el.id = "cmdk"; el.hidden = true;
  el.innerHTML = `
    <div class="cmdk-backdrop" data-close></div>
    <div class="cmdk-panel" role="dialog" aria-modal="true" aria-label="Search">
      <div class="cmdk-input-row">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>
        <input class="cmdk-input" type="text" autocomplete="off" spellcheck="false"
               placeholder="Search projects, books, skills, pages…">
        <kbd class="cmdk-esc">esc</kbd>
      </div>
      <div class="cmdk-list" role="listbox"></div>
      <div class="cmdk-foot"><span><kbd>↑</kbd><kbd>↓</kbd> navigate</span><span><kbd>↵</kbd> open</span><span class="ms-auto">Nikhil Sinha</span></div>
    </div>`;
  document.body.appendChild(el);
  const input = $(".cmdk-input", el);
  const list = $(".cmdk-list", el);
  let active = 0, results = [];

  function render() {
    const tokens = input.value.toLowerCase().split(/\s+/).filter(Boolean);
    results = (_cmdkIndex || [])
      .map((it) => ({ it, s: _cmdkScore(it, tokens) }))
      .filter((x) => x.s >= 0)
      .sort((a, b) => b.s - a.s)
      .slice(0, 14)
      .map((x) => x.it);
    active = 0;
    list.innerHTML = results.length ? results.map((it, i) => `
      <div class="cmdk-item${i === 0 ? " active" : ""}" role="option" data-i="${i}">
        <span class="cmdk-type t-${it.type.toLowerCase()}">${esc(it.type)}</span>
        <span class="cmdk-text"><span class="cmdk-label">${esc(it.label)}</span>
          <span class="cmdk-sub">${esc(it.sub)}</span></span>
        ${it.ext ? '<span class="cmdk-ext">↗</span>' : ""}
      </div>`).join("")
      : `<div class="cmdk-empty">No matches for “${esc(input.value)}”.</div>`;
    $$(".cmdk-item", list).forEach((n) => {
      n.addEventListener("mousemove", () => setActive(+n.dataset.i));
      n.addEventListener("click", () => go(results[+n.dataset.i]));
    });
  }
  function setActive(i) {
    active = i;
    $$(".cmdk-item", list).forEach((n, j) => n.classList.toggle("active", j === i));
    $$(".cmdk-item", list)[i]?.scrollIntoView({ block: "nearest" });
  }
  function go(it) {
    if (!it) return;
    close();
    if (it.action === "theme") return $("#theme")?.click();
    if (it.action === "email") return window.open(GMAIL, "_blank");
    if (it.action === "github") return window.open(GH, "_blank");
    if (it.ext) return window.open(it.href, "_blank");
    if (it.href) location.href = it.href;
  }
  async function open() {
    await _buildCmdkIndex();
    el.hidden = false;
    document.body.classList.add("cmdk-open");
    input.value = ""; render();
    requestAnimationFrame(() => input.focus());
  }
  function close() {
    el.hidden = true;
    document.body.classList.remove("cmdk-open");
  }
  input.addEventListener("input", render);
  $$("[data-close]", el).forEach((n) => n.addEventListener("click", close));
  el.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { close(); }
    else if (e.key === "ArrowDown") { e.preventDefault(); setActive(Math.min(active + 1, results.length - 1)); }
    else if (e.key === "ArrowUp") { e.preventDefault(); setActive(Math.max(active - 1, 0)); }
    else if (e.key === "Enter") { e.preventDefault(); go(results[active]); }
  });
  addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); el.hidden ? open() : close(); }
    else if (e.key === "/" && el.hidden && !/^(INPUT|TEXTAREA)$/.test(document.activeElement?.tagName || "")
             && !document.activeElement?.isContentEditable) { e.preventDefault(); open(); }
  });
}

/* ------------------------------------------------- dynamic WebGL backdrop */
/* A flowing, domain-warped gradient rendered on the GPU: resolution-independent
   (crisp at any size), a few KB, ~60fps, and it drifts toward the pointer. It
   fades to the page background in the centre so text stays readable, pauses in a
   hidden tab, renders a single still frame under prefers-reduced-motion, and
   removes itself (leaving the CSS mesh) if WebGL is unavailable. */
function _hexRGB(v) {
  v = (v || "").trim().replace("#", "");
  if (v.length === 3) v = v.split("").map((c) => c + c).join("");
  const n = parseInt(v || "000000", 16);
  return [((n >> 16) & 255) / 255, ((n >> 8) & 255) / 255, (n & 255) / 255];
}
function _cssRGB(name) {
  return _hexRGB(getComputedStyle(document.documentElement).getPropertyValue(name));
}
function initBackground() {
  const canvas = document.createElement("canvas");
  canvas.className = "bg-flow";
  canvas.setAttribute("aria-hidden", "true");
  document.body.insertBefore(canvas, document.body.firstChild);

  let gl;
  try { gl = canvas.getContext("webgl") || canvas.getContext("experimental-webgl"); }
  catch { gl = null; }
  if (!gl) { canvas.remove(); return; }

  const VS = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const FS = `precision highp float;
uniform vec2 u_res; uniform float u_time; uniform vec2 u_mouse;
uniform vec3 u_c1,u_c2,u_c3,u_bg;
float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
float noise(vec2 p){vec2 i=floor(p),f=fract(p);vec2 u=f*f*(3.-2.*f);
  return mix(mix(hash(i),hash(i+vec2(1,0)),u.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),u.x),u.y);}
float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*noise(p);p=p*2.03+vec2(1.7,9.2);a*=.5;}return v;}
void main(){
  vec2 uv=gl_FragCoord.xy/u_res.xy; vec2 p=uv*2.-1.; p.x*=u_res.x/u_res.y;
  float t=u_time*0.045;
  vec2 q=vec2(fbm(p+t), fbm(p+vec2(5.2,1.3)-t));
  vec2 r=vec2(fbm(p+3.5*q+vec2(1.7,9.2)+t*0.6+u_mouse*0.35),
              fbm(p+3.5*q+vec2(8.3,2.8)-t*0.6));
  float f=fbm(p+3.5*r);
  vec3 base=mix(u_c1,u_c2,clamp(f*f*1.6,0.,1.));
  base=mix(base,u_c3,clamp(length(q)*0.9,0.,1.));
  float vig=smoothstep(0.05,1.3,length(p));
  float amt=clamp(vig*(0.32+0.5*f),0.,0.86);
  gl_FragColor=vec4(mix(u_bg,base,amt),1.0);
}`;
  const compile = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.warn("bg-flow shader:", gl.getShaderInfoLog(s)); return null;
    }
    return s;
  };
  const vs = compile(gl.VERTEX_SHADER, VS), fs = compile(gl.FRAGMENT_SHADER, FS);
  if (!vs || !fs) { canvas.remove(); return; }
  const prog = gl.createProgram();
  gl.attachShader(prog, vs); gl.attachShader(prog, fs); gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { canvas.remove(); return; }
  gl.useProgram(prog);

  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const U = (n) => gl.getUniformLocation(prog, n);
  const uRes = U("u_res"), uTime = U("u_time"), uMouse = U("u_mouse");
  const uC1 = U("u_c1"), uC2 = U("u_c2"), uC3 = U("u_c3"), uBg = U("u_bg");

  let col = {};
  const refresh = () => {
    col = { c1: _cssRGB("--brand"), c2: _cssRGB("--accent"),
            c3: _cssRGB("--brand-2"), bg: _cssRGB("--bg") };
  };
  refresh();
  document.addEventListener("themechange", refresh);

  const scale = Math.min(window.devicePixelRatio || 1, 1) * (innerWidth < 768 ? 0.5 : 0.65);
  const size = () => {
    canvas.width = Math.max(2, Math.floor(innerWidth * scale));
    canvas.height = Math.max(2, Math.floor(innerHeight * scale));
    gl.viewport(0, 0, canvas.width, canvas.height);
  };
  size();
  addEventListener("resize", size, { passive: true });

  let mx = 0, my = 0, tmx = 0, tmy = 0;
  if (matchMedia("(pointer: fine)").matches) {
    addEventListener("pointermove", (e) => {
      tmx = (e.clientX / innerWidth) * 2 - 1;
      tmy = -((e.clientY / innerHeight) * 2 - 1);
    }, { passive: true });
  }

  const t0 = performance.now();
  const draw = (tms, mXY) => {
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uTime, tms);
    gl.uniform2f(uMouse, mXY[0], mXY[1]);
    gl.uniform3fv(uC1, col.c1); gl.uniform3fv(uC2, col.c2);
    gl.uniform3fv(uC3, col.c3); gl.uniform3fv(uBg, col.bg);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  };

  // one frame immediately, so it is never blank even in a throttled tab
  draw(8.0, [0, 0]);
  if (REDUCED) return;

  (function loop(now) {
    requestAnimationFrame(loop);
    if (document.hidden) return;
    mx += (tmx - mx) * 0.04; my += (tmy - my) * 0.04;
    draw((now - t0) / 1000, [mx, my]);
  })(performance.now());
}

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

  // subtle scroll parallax (only on elements that are NOT reveal-animated, so
  // the two transforms never fight)
  if (!REDUCED) {
    const px = $$("[data-parallax]").filter((el) => !el.classList.contains("reveal"));
    if (px.length) {
      let ticking = false;
      const apply = () => {
        const y = window.scrollY;
        px.forEach((el) => {
          const s = parseFloat(el.dataset.parallax) || 0.08;
          el.style.transform = `translate3d(0, ${(y * s).toFixed(1)}px, 0)`;
        });
        ticking = false;
      };
      addEventListener("scroll", () => {
        if (!ticking) { ticking = true; requestAnimationFrame(apply); }
      }, { passive: true });
      apply();
    }
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

/* A round avatar that shows the real photo at assets/img/nikhil.jpg when it
   exists, and falls back to the "NS" monogram if the file is not there yet. */
function avatarHTML(extra = "") {
  // Monogram by default; hydrateAvatars() swaps in the real photo if profile.photo is set.
  return `<span class="avatar ${extra}" data-avatar><span class="avatar-ini">NS</span></span>`;
}

/* Availability card, rendered from data/profile.json into any [data-availability]. */
function renderAvailability(root = document) {
  const hooks = $$("[data-availability]", root);
  if (!hooks.length) return;
  getProfile().then((pr) => {
    const a = pr && pr.availability;
    if (!a) return;
    const html = `
      <div class="avail-head"><span class="avail-dot"></span>${esc(a.status || "Open to work")}</div>
      ${a.headline ? `<div class="avail-headline">${esc(a.headline)}</div>` : ""}
      ${a.looking_for ? `<div class="avail-line">${esc(a.looking_for)}</div>` : ""}
      ${a.mode ? `<div class="avail-line text-ink-3">${esc(a.mode)}</div>` : ""}
      ${(a.points || []).length ? `<ul class="avail-points">${a.points.map((p) => `<li>${esc(p)}</li>`).join("")}</ul>` : ""}
      <a class="btn-x primary w-100 mt-2" data-gmail href="#">Get in touch</a>`;
    hooks.forEach((el) => { el.innerHTML = html; });
    $$("[data-availability] [data-gmail]", root).forEach((el) => {
      el.href = GMAIL; el.target = "_blank"; el.rel = "noopener";
    });
  });
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

document.addEventListener("DOMContentLoaded", () => {
  initBackground(); initChrome(); initLocation(); initCommandPalette();
});
