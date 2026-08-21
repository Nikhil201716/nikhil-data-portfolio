/* home.js — the landing page */

const ROLE_WORDS = [
  "Data Engineer", "Data Analyst", "ML Engineer",
  "AI Engineer", "QA / SDET",
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

function roles(cat) {
  const order = ["Data Analyst", "Data Engineer", "ML Engineer", "AI Engineer", "QA / SDET"];
  $("#role-grid").innerHTML = order.map((r, i) => {
    const n = cat.projects.filter((p) => (p.roles || []).includes(r)).length;
    return `<div class="col-md-6 col-lg-4">
      <a class="card-x tilt reveal d${i % 4}" href="pages/projects.html?role=${encodeURIComponent(r)}">
        <div class="d-flex justify-content-between align-items-baseline">
          <h3 class="h6 mb-0">${esc(r)}</h3>
          <span class="stat-v" style="font-size:1.5rem">${n}</span>
        </div>
        <p class="text-ink-2 small mt-2 mb-2">${esc(ROLE_BLURB[r] || "")}</p>
        <span class="book-cta">See the ${n} projects →</span>
      </a>
    </div>`;
  }).join("");
}

function stackMarquee(cat) {
  const items = (cat.all_stack || []).map((s) => `<span class="chip">${esc(s)}</span>`).join("");
  $("#stack-track").innerHTML = items + items; // duplicated for a seamless loop
}

function featured(cat) {
  const ids = ["13", "14", "15", "09", "12", "11"];
  const picks = ids.map((id) => cat.projects.find((p) => p.id === id)).filter(Boolean);
  $("#featured-grid").innerHTML = picks
    .map((p, i) => `<div class="col-md-6 col-lg-4">${projectCard(p, "d" + (i % 4))}</div>`)
    .join("");
}

function booksPreview() {
  $("#books-preview").innerHTML = BOOKS.slice(0, 6)
    .map((b, i) => `<div class="col-sm-6"><div class="reveal d${i % 4}">${bookCard(b)}</div></div>`)
    .join("");
  const t = $("#pages-total");
  if (t) t.textContent = TOTAL_PAGES.toLocaleString();
}

(async function boot() {
  typewriter($("#role-type"), ROLE_WORDS);
  try {
    const cat = await getCatalog();
    heroStats(cat);
    findings();
    roles(cat);
    stackMarquee(cat);
    featured(cat);
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
