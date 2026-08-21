/* projects.js — the explorer page */

const ROLES = ["All", "Data Analyst", "Data Engineer", "ML Engineer", "AI Engineer", "QA / SDET"];
const state = { role: "All", q: "", projects: [] };

function matches(p) {
  if (state.role !== "All" && !(p.roles || []).includes(state.role)) return false;
  if (!state.q) return true;
  const hay = [p.title, p.pitch, p.headline_finding,
    ...(p.topics || []), ...(p.stack || []), ...(p.roles || [])]
    .join(" ").toLowerCase();
  return hay.includes(state.q);
}

function render() {
  const shown = state.projects.filter(matches);
  $("#projects-grid").innerHTML = shown.length
    ? shown.map((p, i) => `<div class="col-md-6 col-lg-4">${projectCard(p, "d" + (i % 4))}</div>`).join("")
    : `<div class="col-12"><div class="card-x text-center py-5">
         <div class="h5">No projects match that</div>
         <p class="text-ink-2 mb-0">Try a different role or clear the search.</p>
       </div></div>`;
  $("#filter-count").textContent =
    `${shown.length} of ${state.projects.length} projects`
    + (state.role !== "All" ? ` · ${state.role}` : "");
  initMotion();
}

function renderFilters() {
  $("#filter-roles").innerHTML = ROLES.map((r) =>
    `<button class="fbtn${r === state.role ? " on" : ""}" data-role="${esc(r)}">${esc(r)}</button>`).join("");
  $$("#filter-roles .fbtn").forEach((b) =>
    b.addEventListener("click", () => {
      state.role = b.dataset.role;
      const u = new URL(location.href);
      if (state.role === "All") u.searchParams.delete("role");
      else u.searchParams.set("role", state.role);
      history.replaceState(null, "", u);
      renderFilters(); render();
    }));
}

(async function boot() {
  try {
    const cat = await getCatalog();
    state.projects = cat.projects;

    const wanted = new URL(location.href).searchParams.get("role");
    if (wanted && ROLES.includes(wanted)) state.role = wanted;

    renderFilters();
    render();

    let t;
    $("#search").addEventListener("input", (e) => {
      clearTimeout(t);
      t = setTimeout(() => { state.q = e.target.value.trim().toLowerCase(); render(); }, 120);
    });

    const g = cat.generated_at;
    $("#build-stamp").textContent = g
      ? `catalog built ${String(g).slice(0, 10)} · ${cat.n_metrics_extracted} metrics from source` : "";
  } catch (e) {
    console.error(e);
    $("#projects-grid").innerHTML =
      `<div class="col-12"><div class="card-x">Catalog failed to load.</div></div>`;
  }
})();
