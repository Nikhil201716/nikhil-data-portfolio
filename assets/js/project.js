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
  "16": "./build.sh all",
  "17": "./build.sh all",
  "18": "python run.py --quick",
  "19": "npx hardhat test",
  "20": "python run.py",
  "21": "python run.py",
  "22": "./build.sh all",
  "23": "Rscript R/run_all.R",
  "24": "python run.py",
  "25": "./gradlew runTests experiments",
  "26": "python scoring/score.py",
  "27": "python scoring/score.py",
  "28": "python scoring/score.py",
  "29": "python scoring/score.py",
  "30": "python -m harness.score",
};

/* What has to be installed before the command above will run. The Java
   projects have no dependencies at all, so showing a pip line for them would
   be showing a step that does not exist. */
const INSTALL_CMD = {
  "16": null,
  "17": null,
  "18": null,
  "19": "npm install",
  "20": null,
  "22": null,
  "23": null,
  "24": null,
  "25": null,
  "26": "pip install -r backend/requirements.txt",
  "27": "pip install -r provider/requirements.txt",
  "28": "pip install -r requirements.txt",
  "29": "pip install -r requirements.txt",
  "30": "pip install -r requirements.txt",
};

/* Roughly how long a full run takes in a 2-core Codespace, so nobody is
   surprised. P12 fine-tunes a transformer on CPU. */
const RUN_MINUTES = {
  "01": "1-2", "02": "1-2", "03": "3-5", "04": "3-5", "05": "2-4",
  "06": "3-4", "07": "2-4", "08": "4-7", "09": "2-4", "10": "3-6",
  "11": "5-9", "12": "25-35", "13": "4-8", "14": "3-6", "15": "3-6",
  "16": "1-2", "17": "3-5", "18": "2-3", "19": "2-3", "20": "1-2",
  "21": "1-2", "22": "1-2", "23": "1-2", "24": "1-2", "25": "1-2", "26": "4-6",
  "27": "3-5", "28": "1-2", "29": "2-4", "30": "3-5",
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

/* ---------------------------------------------------- terminal replay engine */
/* Types the real commands, then streams the output of a real run. CASTS[id] is
   genuine captured stdout; otherwise the output is reconstructed from the
   project's own reports/*.json (also real-run data). It does NOT execute code on
   the visitor's machine — browsers don't allow that — which the panel says
   plainly. "Run live in Codespaces" is the button that executes it for real. */
function replayData(p) {
  const cmd = RUN_CMD[p.id] || "python scripts/run_pipeline.py";
  const install = p.id in INSTALL_CMD ? INSTALL_CMD[p.id] : "pip install -r requirements.txt";
  const cmds = [`git clone ${GH}/${p.dir}.git`, `cd ${p.dir}`];
  if (install) cmds.push(install);
  cmds.push(cmd);

  const cast = (typeof CASTS !== "undefined") ? CASTS[p.id] : null;
  if (cast) return { cmds, out: cast.lines, real: true,
                     source: `captured from a real run · ${cast.date}` };

  const out = ["▸ running the pipeline…", ""];
  (p.metrics || []).slice(0, 6).forEach((m) => out.push(`✓ ${m.label}: ${m.value}`));
  if (p.n_report_files) out.push("", `✓ wrote ${p.n_report_files} report file(s) → reports/`);
  return { cmds, out, real: false,
           source: "reconstructed from this project's reports/*.json (a real run)" };
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function runTerminal(host, p, token) {
  const body = host.querySelector(".term-lines");
  const runBtn = host.querySelector(".term-run");
  const skipBtn = host.querySelector(".term-skip");
  const data = replayData(p);
  host.dataset.state = "running";
  host.dataset.skip = "";
  runBtn.disabled = true;
  skipBtn.hidden = false;
  skipBtn.onclick = () => (host.dataset.skip = "1");

  const bottom = () => (body.scrollTop = body.scrollHeight);
  const cur = document.createElement("span");
  cur.className = "term-cursor";
  const addLine = (cls) => {
    const d = document.createElement("div");
    d.className = "tl " + (cls || "");
    body.appendChild(d); bottom(); return d;
  };

  const finish = () => {
    cur.remove();
    host.dataset.state = "done";
    runBtn.disabled = false;
    runBtn.textContent = "↻ Replay";
    skipBtn.hidden = true;
  };
  const dump = () => {
    body.innerHTML = "";
    data.cmds.forEach((c) => {
      const d = addLine("cmd");
      d.innerHTML = '<span class="c-dim">$</span> <span class="c-cmd"></span>';
      d.querySelector(".c-cmd").textContent = c;
    });
    data.out.forEach((o) => (addLine("out").textContent = o));
    addLine("done").textContent = "✓ done — " + data.source;
    bottom();
  };

  body.innerHTML = "";
  if (REDUCED) { dump(); return finish(); }

  for (const c of data.cmds) {
    if (token.cancelled) return;
    if (host.dataset.skip === "1") { dump(); return finish(); }
    const d = addLine("cmd");
    d.innerHTML = '<span class="c-dim">$</span> <span class="c-cmd"></span>';
    const span = d.querySelector(".c-cmd");
    d.appendChild(cur);
    for (const ch of c) {
      if (token.cancelled) return;
      if (host.dataset.skip === "1") { dump(); return finish(); }
      span.textContent += ch; bottom(); await sleep(11);
    }
    await sleep(130);
  }
  for (const o of data.out) {
    if (token.cancelled) return;
    if (host.dataset.skip === "1") { dump(); return finish(); }
    const d = addLine("out");
    d.appendChild(cur);
    d.insertBefore(document.createTextNode(o), cur);
    bottom(); await sleep(o ? 75 : 25);
  }
  finish();
}

/* ---- local runner: real execution on a machine that has the projects ----
   Detects the bundled run_local.py (served same-origin when it hosts the site,
   or at http://localhost:8800 otherwise) and, if this project is present there,
   streams its real stdout into the terminal via Server-Sent Events. */
let _runner;
async function detectRunner() {
  if (_runner !== undefined) return _runner;
  // Only probe when the page is actually served by the local runner (localhost),
  // so the public https site never fires a failed request to http://localhost.
  const h = location.hostname;
  if (h !== "localhost" && h !== "127.0.0.1") { _runner = null; return _runner; }
  const origin = location.origin;
  try {
    const ctrl = new AbortController();
    const to = setTimeout(() => ctrl.abort(), 1200);
    const r = await fetch(origin + "/api/health", { signal: ctrl.signal, cache: "no-store" });
    clearTimeout(to);
    _runner = r.ok ? { origin, health: await r.json() } : null;
  } catch { _runner = null; }
  return _runner;
}

function liveRun(origin, p) {
  const host = $("[data-term]");
  const body = host.querySelector(".term-lines");
  const runBtn = host.querySelector(".term-run");
  const skip = host.querySelector(".term-skip");
  const qs = $(".run-install")?.checked ? "?install=1" : "";
  const shown = replayData(p).cmds.filter((c) => !c.startsWith("git clone") && !c.startsWith("cd "));
  if (!confirm(`Run project ${p.id} on THIS machine?\n\nIt will execute, in ${p.dir}/:\n  `
    + shown.join("\n  ") + `\n\nThe real output streams below.`)) return;

  body.innerHTML = "";
  host.querySelector(".term-title").textContent = `${p.dir} — live on this machine`;
  const add = (cls, txt) => {
    const d = document.createElement("div");
    d.className = "tl " + cls; d.textContent = txt;
    body.appendChild(d); body.scrollTop = body.scrollHeight; return d;
  };
  add("hint", "▸ starting local run…");
  runBtn.disabled = true;

  let es;
  try { es = new EventSource(origin + "/api/run/" + p.id + qs); }
  catch { add("done", "⚠ could not reach the local runner"); runBtn.disabled = false; return; }

  let finished = false;
  skip.hidden = false; skip.textContent = "Stop";
  skip.onclick = () => { finished = true; es.close(); add("done", "■ stopped"); skip.hidden = true; runBtn.disabled = false; };
  es.onmessage = (e) => add("out", e.data);
  es.addEventListener("done", (e) => {
    finished = true; es.close();
    add("done", `✓ finished (exit ${e.data}) — executed on this machine`);
    skip.hidden = true; runBtn.disabled = false;
  });
  es.onerror = () => {
    if (finished) return;
    finished = true; es.close();
    add("done", "⚠ runner connection ended");
    skip.hidden = true; runBtn.disabled = false;
  };
}

function wireRunner(p) {
  detectRunner().then((info) => {
    if (!info || !info.health || !info.health.available) return;
    const a = info.health.available[p.id];
    const row = $("[data-runner]");
    if (!row || !a || !a.exists) return;
    row.hidden = false;
    const note = $(".runner-note");
    if (note) note.textContent = a.venv ? "local runner connected · .venv found" : "local runner connected";
    $(".term-live")?.addEventListener("click", () => liveRun(info.origin, p));
  });
}

function runPanel(p) {
  const mins = RUN_MINUTES[p.id] || "2-5";
  const ollama = NEEDS_OLLAMA.has(p.id);
  const install = p.id in INSTALL_CMD ? INSTALL_CMD[p.id] : "pip install -r requirements.txt";
  const rd = replayData(p);

  return `
  <div class="card-x reveal" id="run">
    <div class="run-head">
      <div>
        <div class="kicker">Run it</div>
        <h3 class="h5 mt-1 mb-1">See it actually run — two honest ways</h3>
        <p class="text-ink-2 small mb-0" style="max-width:64ch">
          <strong>Run live in Codespaces</strong> opens the repo in a free GitHub cloud
          sandbox that ${install ? "installs dependencies and runs" : "runs"} the whole
          pipeline for real — you watch real output in a real terminal (~${mins} min).
          Or press <strong>▶ Run</strong> below to replay a real run right here, no sign-in.
        </p>
      </div>
      <a class="btn-x run" href="${codespaceUrl(p.dir)}" target="_blank" rel="noopener">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
        Run live in Codespaces
      </a>
    </div>

    <div class="runner-row" data-runner hidden>
      <button class="btn-x run term-live">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>
        Run on this machine (live)
      </button>
      <label class="runner-chk"><input type="checkbox" class="run-install"> install deps first</label>
      <span class="runner-note mono"></span>
    </div>

    <div class="term mt-3" data-term>
      <div class="term-bar">
        <span class="term-dot" style="background:#ff5f57"></span>
        <span class="term-dot" style="background:#febc2e"></span>
        <span class="term-dot" style="background:#28c840"></span>
        <span class="term-title">${esc(p.dir)} — ${rd.real ? "replay of a real run" : "real-run results"}</span>
        <span class="term-badge">${rd.real ? "captured stdout" : "from reports/*.json"}</span>
        <span class="term-ctl">
          <button class="term-skip" hidden>Skip</button>
          <button class="term-run">▶ Run</button>
        </span>
      </div>
      <div class="term-body"><div class="term-lines"><div class="tl hint">Press ▶ Run to replay a real run of this project — ${esc(rd.source)}.</div></div></div>
    </div>

    <div class="run-actions">
      <button class="btn-x py-2 px-3" style="font-size:.85rem" id="copy-cmd">Copy the commands</button>
      <a class="btn-x py-2 px-3" style="font-size:.85rem"
         href="https://github.com/Nikhil201716/${esc(p.dir)}/blob/main/RUN.md"
         target="_blank" rel="noopener">Full run instructions →</a>
      <a class="btn-x py-2 px-3" style="font-size:.85rem"
         href="https://github.com/Nikhil201716/${esc(p.dir)}" target="_blank" rel="noopener">View the code →</a>
    </div>

    <p class="text-ink-3 small mt-3 mb-0">
      The in-page <strong>▶ Run</strong> above <strong>replays a real run's output</strong> — a
      website cannot execute code on a stranger's computer, and none should. Two ways to run it
      for real: <strong>Codespaces</strong> (free GitHub account, runs in the cloud), or — on a
      machine that has the projects — start the bundled local runner
      (<code>python run_local.py</code>) and reload; a <strong>Run on this machine</strong> button
      appears that executes this project locally and streams the real output here.
      ${ollama ? `This project has optional local-LLM stages; without Ollama they are skipped
      and the deterministic control arm still runs.` : ""}
    </p>
  </div>`;
}

function render(p, cat) {
  const book = BOOK_BY_ID[p.id];
  const metrics = p.metrics || [];
  const charts = p.charts || [];

  document.title = `${p.title} — Nikhil Sinha`;

  const hasCharts = charts.length > 0;

  $("#project-root").innerHTML = `
  <section class="section" style="padding-top:2.5rem;padding-bottom:1.5rem">
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
              <a class="btn-x run" href="${codespaceUrl(p.dir)}" target="_blank" rel="noopener">Run live in Codespaces →</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>

  ${p.headline_finding ? `
  <section style="padding:0 0 1.5rem">
    <div class="wrap">
      <div class="card-x reveal" style="border-left:3px solid var(--brand)">
        <div class="kicker">Headline finding</div>
        <p class="mb-0 mt-2" style="font-size:1.05rem">${esc(p.headline_finding)}</p>
      </div>
    </div>
  </section>` : ""}

  <section style="padding:0 0 3rem">
    <div class="wrap">
      <div class="tabbar reveal" role="tablist" aria-label="Project sections">
        <button class="tabx active" role="tab" data-tab="overview">Overview</button>
        ${hasCharts ? `<button class="tabx" role="tab" data-tab="charts">Charts</button>` : ""}
        <button class="tabx" role="tab" data-tab="run">Run &amp; replay</button>
      </div>

      <div class="tab-panel active" data-panel="overview">
        <div class="row g-4">
          <div class="col-lg-5">
            <div class="card-x h-100">
              <div class="kicker">Measured results</div>
              <p class="text-ink-3 small mt-1 mb-3">
                ${p.metrics_source === "reports"
                  ? `Extracted from this project's own <code>reports/*.json</code>, produced by a real run.`
                  : `Quoted from the project README — this project predates the reports convention, so the provenance is weaker and labelled as such.`}
              </p>
              ${metrics.length
                ? metrics.map((m) => `<div class="metric-row">
                     <span class="metric-k">${esc(m.label)}${m.note ? `<br><span class="text-ink-3" style="font-size:.78rem">${esc(m.note)}</span>` : ""}</span>
                     <span class="metric-v${m.highlight ? " hi" : ""}">${esc(m.value)}</span>
                   </div>`).join("")
                : `<p class="text-ink-2 mb-0">No machine-readable metrics for this project.</p>`}
              ${p.n_report_files ? `<div class="text-ink-3 small mono mt-3">${p.n_report_files} report file${p.n_report_files === 1 ? "" : "s"} in the repository</div>` : ""}
            </div>
          </div>
          <div class="col-lg-7">
            <div class="card-x h-100">
              <div class="kicker mb-2">What it covers</div>
              <div>${(p.topics || []).map((t) => `<span class="chip">${esc(t)}</span>`).join("")}</div>
              ${hasCharts ? `<p class="text-ink-3 small mt-3 mb-0">Open the <strong>Charts</strong> tab for the figures built from the report files.</p>` : ""}
            </div>
          </div>
        </div>
      </div>

      ${hasCharts ? `
      <div class="tab-panel" data-panel="charts">
        <div class="card-x">
          <div class="kicker mb-2">Charts from the report files</div>
          <div class="row g-3" id="charts"></div>
        </div>
      </div>` : ""}

      <div class="tab-panel" data-panel="run">${runPanel(p)}</div>
    </div>
  </section>

  <section style="padding:0 0 4rem"><div class="wrap">
    <div class="d-flex flex-wrap justify-content-between align-items-center gap-3 reveal">
      <div>
        <div class="kicker">Keep going</div>
        <h3 class="h5 mt-1 mb-0">Other projects</h3>
      </div>
      <a class="btn-x" href="projects.html">All 30 →</a>
    </div>
    <div class="row g-3 g-lg-4 mt-1" id="more"></div>
  </div></section>`;

  // ----- tabs
  let chartsDrawn = false;
  const drawAllCharts = () => {
    if (!hasCharts) return;
    $("#charts").innerHTML = charts
      .map((_, i) => `<div class="col-12"><div class="chart-box" id="chart-${i}"></div></div>`).join("");
    charts.forEach((c, i) => drawChart($(`#chart-${i}`), c));
  };
  const tabs = $$(".tabx");
  const activate = (name) => {
    tabs.forEach((t) => t.classList.toggle("active", t.dataset.tab === name));
    $$(".tab-panel").forEach((pn) => pn.classList.toggle("active", pn.dataset.panel === name));
    if (name === "charts" && !chartsDrawn) { drawAllCharts(); chartsDrawn = true; }
  };
  tabs.forEach((t, i) => {
    t.addEventListener("click", () => activate(t.dataset.tab));
    t.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight" || e.key === "ArrowLeft") {
        e.preventDefault();
        const next = (i + (e.key === "ArrowRight" ? 1 : tabs.length - 1)) % tabs.length;
        tabs[next].focus(); activate(tabs[next].dataset.tab);
      }
    });
  });
  if (hasCharts) {
    document.addEventListener("themechange", () => {
      if (chartsDrawn) charts.forEach((c, i) => drawChart($(`#chart-${i}`), c));
    });
  }

  // ----- terminal replay
  let termToken = { cancelled: false };
  const termHost = $("[data-term]");
  termHost?.querySelector(".term-run")?.addEventListener("click", () => {
    termToken.cancelled = true;
    termToken = { cancelled: false };
    runTerminal(termHost, p, termToken);
  });

  // reveal "Run on this machine" if the local runner is up
  wireRunner(p);

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
    const inst = p.id in INSTALL_CMD
      ? INSTALL_CMD[p.id]
      : "pip install -r requirements.txt";
    const text = `git clone https://github.com/Nikhil201716/${p.dir}.git\n`
      + `cd ${p.dir}\n` + (inst ? `${inst}\n` : "") + cmd;
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
