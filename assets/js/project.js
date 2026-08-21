/* project.js — the per-project detail page (?id=NN) */

/* The exact command each project's Codespace runs on attach. Kept in sync with
   .devcontainer/run-project.sh in each repo, and shown so a visitor who would
   rather run it locally can copy it. */
const RUN_CMD = {
  "01": "python scripts/run_pipeline.py",
  "02": "python scripts/run_pipeline.py",
  "03": "python scripts/run_pipeline.py",
  "04": "airflow dags test sales_etl_pipeline 2026-07-20",
  "05": "python scripts/run_pipeline.py",
  "06": "python pipeline/consumer.py --duration 110",
  "07": "python scripts/run_pipeline.py",
  "08": "python scripts/run_pipeline.py",
  "09": "python scripts/run_pipeline.py",
  "10": "python scripts/run_pipeline.py",
  "11": "python scripts/run_pipeline.py",
  "12": "python scripts/run_pipeline.py",
  "13": "python run_all.py",
  "14": "python run_all.py",
  "15": "python run_all.py",
};

/* Roughly how long a full run takes in a 2-core Codespace, so nobody is
   surprised. P12 fine-tunes a transformer on CPU. */
const RUN_MINUTES = {
  "01": "1-2", "02": "1-2", "03": "3-5", "04": "3-5", "05": "2-4",
  "06": "3-4", "07": "2-4", "08": "4-7", "09": "2-4", "10": "3-6",
  "11": "5-9", "12": "25-35", "13": "4-8", "14": "3-6", "15": "3-6",
};

const NEEDS_OLLAMA = new Set(["05", "06", "07", "08", "09", "10", "11", "13", "14", "15"]);

function notFound() {
  $("#project-root").innerHTML = `
    <section class="section"><div class="wrap text-center py-5">
      <h2>Project not found</h2>
      <p class="sec-sub mx-auto">That project id doesn't exist in the catalog.</p>
      <a class="btn-x primary mt-3" href="projects.html">← All projects</a>
    </div></section>`;
}

function runPanel(p) {
  const cmd = RUN_CMD[p.id] || "python scripts/run_pipeline.py";
  const mins = RUN_MINUTES[p.id] || "2-5";
  const ollama = NEEDS_OLLAMA.has(p.id);

  return `
  <div class="card-x reveal" id="run">
    <div class="d-flex flex-wrap justify-content-between align-items-start gap-3">
      <div>
        <div class="kicker">Run it</div>
        <h3 class="h5 mt-1 mb-1">Run this project in your browser</h3>
        <p class="text-ink-2 small mb-0" style="max-width:60ch">
          Opens the repository in a free GitHub Codespace. It installs the
          dependencies and runs the full pipeline automatically — you watch the real
          output stream into a real terminal. Takes about <strong>${mins} minutes</strong>.
        </p>
      </div>
      <a class="btn-x run" href="${codespaceUrl(p.dir)}" target="_blank" rel="noopener">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
        Run this project
      </a>
    </div>

    <div class="term mt-3">
      <div class="term-bar">
        <span class="term-dot" style="background:#ff5f57"></span>
        <span class="term-dot" style="background:#febc2e"></span>
        <span class="term-dot" style="background:#28c840"></span>
        <span class="term-title">${esc(p.dir)} — codespace</span>
      </div>
      <div class="term-body"><pre><span class="c-dim">$</span> <span class="c-key">git clone</span> https://github.com/Nikhil201716/${esc(p.dir)}.git
<span class="c-dim">$</span> <span class="c-key">cd</span> ${esc(p.dir)}
<span class="c-dim">$</span> pip install -r requirements.txt
<span class="c-dim">$</span> ${esc(cmd)}

<span class="c-dim"># the pipeline writes everything it measures into reports/,
# which is where every number on this page comes from.</span></pre></div>
    </div>

    <div class="d-flex flex-wrap gap-2 mt-3">
      <button class="btn-x py-2 px-3" style="font-size:.85rem" id="copy-cmd">Copy the commands</button>
      <a class="btn-x py-2 px-3" style="font-size:.85rem"
         href="https://github.com/Nikhil201716/${esc(p.dir)}" target="_blank" rel="noopener">View the code →</a>
    </div>

    <p class="text-ink-3 small mt-3 mb-0">
      A free GitHub account is needed to open a Codespace, and the compute is billed
      to that account's free monthly allowance — not to me.
      ${ollama ? `This project has optional local-LLM stages; without Ollama installed
      they are skipped and the deterministic control arm still runs.` : ""}
    </p>
  </div>`;
}

function render(p, cat) {
  const book = BOOK_BY_ID[p.id];
  const metrics = p.metrics || [];
  const charts = p.charts || [];

  document.title = `${p.title} — Nikhil Sinha`;

  $("#project-root").innerHTML = `
  <section class="section" style="padding-top:2.5rem;padding-bottom:2rem">
    <div class="wrap">
      <a class="text-ink-3 small" href="projects.html">← All projects</a>

      <div class="row g-4 mt-1 align-items-start">
        <div class="col-lg-8">
          <div class="reveal">
            <span class="num-badge">PROJECT ${esc(p.id)}</span>
            <h1 class="mt-2" style="font-size:clamp(1.9rem,5vw,3rem)">${esc(p.title)}</h1>
            <p class="sec-sub">${esc(p.pitch || "")}</p>
            <div class="mt-3">
              ${(p.roles || []).map((r) => `<span class="chip role">${esc(r)}</span>`).join("")}
            </div>
            <div class="mt-2">
              ${(p.stack || []).map((s) => `<span class="chip">${esc(s)}</span>`).join("")}
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card-x reveal d1">
            <div class="kicker mb-2">Links</div>
            <div class="d-flex flex-column gap-2">
              <a class="btn-x" href="https://github.com/Nikhil201716/${esc(p.dir)}" target="_blank" rel="noopener">Repository →</a>
              ${book ? `<a class="btn-x" href="${GH}/${book.repo}/blob/main/docs/${book.file}" target="_blank" rel="noopener">
                 Notebook · ${book.pages} pages →</a>` : ""}
              <a class="btn-x run" href="${codespaceUrl(p.dir)}" target="_blank" rel="noopener">Run this project →</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  ${p.headline_finding ? `
  <section style="padding:0 0 2rem">
    <div class="wrap">
      <div class="card-x reveal" style="border-left:3px solid var(--brand)">
        <div class="kicker">Headline finding</div>
        <p class="mb-0 mt-2" style="font-size:1.05rem">${esc(p.headline_finding)}</p>
      </div>
    </div>
  </section>` : ""}

  <section style="padding:0 0 2rem">
    <div class="wrap">
      <div class="row g-4">
        <div class="col-lg-5">
          <div class="card-x reveal h-100">
            <div class="kicker">Measured results</div>
            <p class="text-ink-3 small mt-1 mb-3">
              ${p.metrics_source === "reports"
                ? `Extracted from this project's own <code>reports/*.json</code>, produced by a real run.`
                : `Quoted from the results table in the project README — this project predates the reports convention, so the provenance is weaker and is labelled as such.`}
            </p>
            ${metrics.length
              ? metrics.map((m) => `<div class="metric-row">
                   <span class="metric-k">${esc(m.label)}${m.note ? `<br><span class="text-ink-3" style="font-size:.78rem">${esc(m.note)}</span>` : ""}</span>
                   <span class="metric-v${m.highlight ? " hi" : ""}">${esc(m.value)}</span>
                 </div>`).join("")
              : `<p class="text-ink-2 mb-0">No machine-readable metrics for this project.</p>`}
            ${p.n_report_files ? `<div class="text-ink-3 small mono mt-3">${p.n_report_files} report files in the repository</div>` : ""}
          </div>
        </div>
        <div class="col-lg-7">
          <div class="card-x reveal d1 h-100">
            <div class="kicker mb-2">What it covers</div>
            <div>${(p.topics || []).map((t) => `<span class="chip">${esc(t)}</span>`).join("")}</div>
            ${charts.length ? `<div class="row g-3 mt-2" id="charts"></div>` : ""}
          </div>
        </div>
      </div>
    </div>
  </section>

  <section style="padding:0 0 3rem"><div class="wrap">${runPanel(p)}</div></section>

  <section style="padding:0 0 4rem"><div class="wrap">
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 reveal">
      <div>
        <div class="kicker">Keep going</div>
        <h3 class="h5 mt-1 mb-0">Other projects</h3>
      </div>
      <a class="btn-x" href="projects.html">All 15 →</a>
    </div>
    <div class="row g-3 g-lg-4 mt-1" id="more"></div>
  </div></section>`;

  // charts
  if (charts.length) {
    $("#charts").innerHTML = charts
      .map((_, i) => `<div class="col-12"><div class="chart-box" id="chart-${i}"></div></div>`).join("");
    charts.forEach((c, i) => drawChart($(`#chart-${i}`), c));
    document.addEventListener("themechange", () =>
      charts.forEach((c, i) => drawChart($(`#chart-${i}`), c)));
  }

  // related projects — same primary role where possible
  const role = (p.roles || [])[0];
  const more = cat.projects
    .filter((x) => x.id !== p.id)
    .sort((a, b) => ((b.roles || []).includes(role) ? 1 : 0) - ((a.roles || []).includes(role) ? 1 : 0))
    .slice(0, 3);
  $("#more").innerHTML = more
    .map((x, i) => `<div class="col-md-6 col-lg-4">${projectCard(x, "d" + i)}</div>`).join("");

  // copy button
  $("#copy-cmd")?.addEventListener("click", async (e) => {
    const cmd = RUN_CMD[p.id] || "python scripts/run_pipeline.py";
    const text = `git clone https://github.com/Nikhil201716/${p.dir}.git\n`
      + `cd ${p.dir}\npip install -r requirements.txt\n${cmd}`;
    try {
      await navigator.clipboard.writeText(text);
      const b = e.currentTarget, old = b.textContent;
      b.textContent = "Copied";
      setTimeout(() => (b.textContent = old), 1600);
    } catch { /* clipboard blocked — the commands are visible above anyway */ }
  });

  initMotion();
}

(async function boot() {
  const id = new URL(location.href).searchParams.get("id");
  if (!id) return notFound();
  try {
    const cat = await getCatalog();
    const p = cat.projects.find((x) => x.id === id);
    if (!p) return notFound();
    render(p, cat);
  } catch (e) {
    console.error(e);
    notFound();
  }
})();
