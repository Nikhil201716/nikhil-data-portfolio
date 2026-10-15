/* home.js — the landing page */

let TAGLINES = [
  "I build data & AI systems",
  "and the tests that prove they work",
  "MCA · CHRIST University, Bengaluru",
  "thirty projects, every number measured",
];

function typewriter(el, words) {
  if (!el) return;
  if (REDUCED) { el.textContent = words[0]; return; }
  let w = 0, i = 0, deleting = false;
  (function tick() {
    const word = words[w];
    i += deleting ? -1 : 1;
    el.textContent = word.slice(0, i);
    let delay = deleting ? 45 : 85;
    if (!deleting && i === word.length) { delay = 1900; deleting = true; }
    else if (deleting && i === 0) { deleting = false; w = (w + 1) % words.length; delay = 320; }
    setTimeout(tick, delay);
  })();
}

function heroStats(cat) {
  const stats = [
    { v: cat.n_projects, k: "Projects" },
    { v: cat.n_metrics_extracted, k: "Metrics from source" },
    { v: cat.n_technologies, k: "Technologies" },
    { v: TOTAL_PAGES, k: "Pages written" },
    { v: BOOKS.length, k: "Technical books" },
  ];
  $("#hero-stats").innerHTML = stats.map((s, i) => `
    <div class="col-6 col-md-4 col-lg">
      <div class="stat reveal d${Math.min(i, 4)}">
        <div class="stat-v" data-count="${s.v}">0</div>
        <div class="stat-k">${esc(s.k)}</div>
      </div>
    </div>`).join("");
}

function findings() {
  $("#findings-grid").innerHTML = FINDINGS.map((f, i) => {
    const b = BOOK_BY_ID[f.id];
    return `<div class="col-md-6 col-lg-4">
      <div class="card-x tilt reveal d${i % 4}">
        <div class="stat-v" style="font-size:1.9rem">${esc(f.metric)}</div>
        <h3 class="h6 mt-2 mb-2">${esc(f.title)}</h3>
        <p class="text-ink-2 small">${esc(f.body)}</p>
        <div class="mono text-ink-3 mb-3" style="font-size:.75rem">
          verify: ${esc(f.verify)}
        </div>
        <a class="btn-x py-2 px-3" href="${projectUrl(f.id)}" style="font-size:.85rem">
          Project ${esc(f.id)} →
        </a>
      </div>
    </div>`;
  }).join("");
}

function areas(cat) {
  const order = ["Data Analysis", "Data Engineering", "Machine Learning",
                 "AI & LLM Systems", "Testing & QA"];
  $("#role-grid").innerHTML = order.map((r, i) => {
    const n = cat.projects.filter((p) => (p.roles || []).includes(r)).length;
    return `<div class="col-md-6 col-lg-4">
      <a class="card-x tilt reveal d${i % 4}" href="pages/projects.html?role=${encodeURIComponent(r)}">
        <div class="d-flex justify-content-between align-items-baseline">
          <h3 class="h6 mb-0">${esc(r)}</h3>
          <span class="stat-v" style="font-size:1.5rem">${n}</span>
        </div>
        <p class="text-ink-2 small mt-2 mb-2">${esc(AREA_BLURB[r] || "")}</p>
        <span class="book-cta">${n} projects →</span>
      </a>
    </div>`;
  }).join("");
}

function stackMarquee(cat) {
  const items = (cat.all_stack || []).map((s) => `<span class="chip">${esc(s)}</span>`).join("");
  $("#stack-track").innerHTML = items + items; // duplicated for a seamless loop
}

/* ---------------------------------------------- explore map + guided tour */
let CAT = null, curRole = null;
const ROLE_ORDER = ["Data Analysis", "Data Engineering", "Machine Learning",
                    "AI & LLM Systems", "Testing & QA"];
const ROLE_SHORT = {
  "Data Analysis": "Analysis", "Data Engineering": "Data Eng",
  "Machine Learning": "ML", "AI & LLM Systems": "AI · LLM", "Testing & QA": "Testing",
};
const ROLE_INTRO_ALL = "Thirty projects across five areas. Pick one to see the strongest work for that kind of role — or explore the whole map.";
const ROLE_INTRO = {
  "Data Analysis": "Hiring for analytics? Here's where I turned messy data into decisions you can defend — every figure traceable to its source file.",
  "Data Engineering": "Need pipelines that fail loudly, not silently? Streaming, ETL, idempotency, data contracts and event-time correctness.",
  "Machine Learning": "For ML roles: models benchmarked against a trivial baseline, calibrated, and attacked by an adversary before I trusted them.",
  "AI & LLM Systems": "Building with LLMs? I test the grounding and grade the judge instead of trusting the demo — with measured guardrails.",
  "Testing & QA": "For QA / SDET: fault-injection across unit, API, contract, data-quality, load, mutation and security — measured, never claimed.",
};

function buildConstellation(cat) {
  const W = 1000, H = 560, cx = 500, cy = 285, Rh = 135;
  const hubs = ROLE_ORDER.map((r, i) => {
    const a = -Math.PI / 2 + i * 2 * Math.PI / 5;
    return { role: r, i, a, x: cx + Rh * Math.cos(a), y: cy + Rh * Math.sin(a) };
  });
  const hubByRole = Object.fromEntries(hubs.map((h) => [h.role, h]));
  const byRole = {}; ROLE_ORDER.forEach((r) => (byRole[r] = []));
  cat.projects.forEach((p) => {
    const pr = (p.roles || []).find((r) => byRole[r]) || ROLE_ORDER[2];
    byRole[pr].push(p);
  });
  const nodes = [];
  hubs.forEach((hub) => {
    const list = byRole[hub.role] || [], n = list.length;
    list.forEach((p, k) => {
      const half = (Math.PI / 5) * 0.92;
      const frac = n > 1 ? (k / (n - 1) - 0.5) : 0;
      const ang = hub.a + frac * half * 2;
      const ring = k % 2 === 0 ? 245 : 322;
      nodes.push({ p, ri: hub.i, roles: p.roles || [hub.role],
                   x: cx + ring * Math.cos(ang), y: cy + ring * Math.sin(ang) });
    });
  });
  const edges = [];
  nodes.forEach((nd) => (nd.roles.length ? nd.roles : [ROLE_ORDER[nd.ri]]).forEach((r) => {
    const h = hubByRole[r];
    if (h) edges.push({ x1: nd.x, y1: nd.y, x2: h.x, y2: h.y, ri: h.i, id: nd.p.id });
  }));

  $("#constellation").innerHTML = `
    <svg viewBox="0 0 ${W} ${H}" class="cst-svg" preserveAspectRatio="xMidYMid meet" role="img">
      <g class="cst-edges">${edges.map((e) =>
        `<line class="cst-edge r${e.ri}" x1="${e.x1.toFixed(1)}" y1="${e.y1.toFixed(1)}" x2="${e.x2.toFixed(1)}" y2="${e.y2.toFixed(1)}"/>`).join("")}</g>
      <g class="cst-hubs">${hubs.map((h) =>
        `<g class="cst-hub r${h.i}" data-role="${esc(h.role)}" tabindex="0" role="button" aria-label="${esc(h.role)}">
           <circle cx="${h.x.toFixed(1)}" cy="${h.y.toFixed(1)}" r="32"/>
           <text x="${h.x.toFixed(1)}" y="${h.y.toFixed(1)}" dy="4" text-anchor="middle">${esc(ROLE_SHORT[h.role])}</text>
         </g>`).join("")}</g>
      <g class="cst-nodes">${nodes.map((nd, i) =>
        `<circle class="cst-node r${nd.ri}" data-i="${i}" data-roles="${esc(nd.roles.join("|"))}" cx="${nd.x.toFixed(1)}" cy="${nd.y.toFixed(1)}" r="7"><title>${esc(nd.p.title)}</title></circle>`).join("")}</g>
    </svg>`;

  const svgEl = $("#constellation .cst-svg"), tip = $("#cst-tip");
  $$(".cst-node", svgEl).forEach((n) => {
    const nd = nodes[+n.dataset.i];
    n.addEventListener("mouseenter", () => { tip.hidden = false; tip.textContent = `${nd.p.title} · Project ${nd.p.id}`; });
    n.addEventListener("mousemove", (e) => {
      const r = $("#explore").getBoundingClientRect();
      tip.style.left = (e.clientX - r.left) + "px"; tip.style.top = (e.clientY - r.top) + "px";
    });
    n.addEventListener("mouseleave", () => { tip.hidden = true; });
    n.addEventListener("click", () => (location.href = projectUrl(nd.p.id)));
  });
  $$(".cst-hub", svgEl).forEach((h) => {
    h.addEventListener("click", () => selectRole(h.dataset.role));
    h.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); selectRole(h.dataset.role); } });
  });
}

function setGraphRole(role) {
  const svgEl = $("#constellation .cst-svg"); if (!svgEl) return;
  $$(".cst-node,.cst-edge,.cst-hub", svgEl).forEach((el) => el.classList.remove("on"));
  if (!role) { svgEl.classList.remove("sel"); return; }
  svgEl.classList.add("sel");
  const i = ROLE_ORDER.indexOf(role);
  $$(".cst-node", svgEl).forEach((n) => { if ((n.dataset.roles || "").split("|").includes(role)) n.classList.add("on"); });
  $$(`.cst-edge.r${i}`, svgEl).forEach((e) => e.classList.add("on"));
  $$(".cst-hub", svgEl).forEach((h) => { if (h.dataset.role === role) h.classList.add("on"); });
}

function renderFeatured(role) {
  if (!CAT) return;
  let picks;
  if (!role) picks = ["30", "14", "15", "29", "12", "11"].map((id) => CAT.projects.find((p) => p.id === id)).filter(Boolean);
  else picks = CAT.projects.filter((p) => (p.roles || []).includes(role))
    .sort((a, b) => (((b.roles || [])[0] === role) - ((a.roles || [])[0] === role))
                 || (Number(b.id) - Number(a.id)))
    .slice(0, 6);
  $("#featured-grid").innerHTML = picks
    .map((p, i) => `<div class="col-md-6 col-lg-4">${projectCard(p, "d" + (i % 4))}</div>`).join("");
  $$("#featured-grid .reveal").forEach((e) => e.classList.add("in"));
  const h = $("#featured-head");
  if (h) h.textContent = role ? `Strongest in ${ROLE_SHORT[role] || role}` : "Featured projects";
}

function selectRole(role) {
  curRole = (!role || role === "All") ? null : role;
  $$("#tour-pills .tour-pill").forEach((p) => p.classList.toggle("active", p.dataset.role === (role || "All")));
  $("#tour-intro").textContent = curRole ? (ROLE_INTRO[curRole] || "") : ROLE_INTRO_ALL;
  setGraphRole(curRole);
  renderFeatured(curRole);
}

function buildExplore(cat) {
  $("#tour-pills").innerHTML = ["All", ...ROLE_ORDER].map((r) =>
    `<button class="tour-pill${r === "All" ? " all" : " r" + ROLE_ORDER.indexOf(r)}" data-role="${esc(r)}">${esc(r === "All" ? "Show everything" : r)}</button>`).join("");
  $$("#tour-pills .tour-pill").forEach((p) => p.addEventListener("click", () => selectRole(p.dataset.role)));
  buildConstellation(cat);
  selectRole("All");
}

function booksPreview() {
  $("#books-preview").innerHTML = BOOKS.slice(0, 6)
    .map((b, i) => `<div class="col-sm-6"><div class="reveal d${i % 4}">${bookCard(b)}</div></div>`)
    .join("");
  const t = $("#pages-total");
  if (t) t.textContent = TOTAL_PAGES.toLocaleString();
}

(async function boot() {
  // personal content first, so the hero speaks in Nikhil's own words
  const pr = await getProfile().catch(() => null);
  if (pr && Array.isArray(pr.roles) && pr.roles.length) TAGLINES = pr.roles;
  typewriter($("#role-type"), TAGLINES);
  const av = $("[data-hero-avatar]");
  if (av) av.innerHTML = avatarHTML("avatar-xl");
  hydrateAvatars();
  if (pr && pr.hero_pitch) { const hp = $("[data-hero-pitch]"); if (hp) hp.textContent = pr.hero_pitch; }
  $(".cmdk-trigger-inline")?.addEventListener("click",
    () => dispatchEvent(new KeyboardEvent("keydown", { key: "k", ctrlKey: true })));
  renderAvailability();

  try {
    const cat = await getCatalog();
    CAT = cat;
    heroStats(cat);
    findings();
    areas(cat);
    stackMarquee(cat);
    buildExplore(cat);
    booksPreview();
    const g = cat.generated_at;
    $("#build-stamp").textContent = g
      ? `catalog built ${String(g).slice(0, 10)} · ${cat.n_metrics_extracted} metrics extracted from source`
      : "";
  } catch (e) {
    console.error(e);
    $("#featured-grid").innerHTML =
      `<div class="col-12"><div class="card-x">Catalog failed to load. Run <code>python build/build_catalog.py</code>.</div></div>`;
  }
  initMotion();
  animateCounters();
})();
