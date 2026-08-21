/* books.js — the books page */

(async function boot() {
  const stats = [
    { v: BOOKS.length, k: "Books" },
    { v: TOTAL_PAGES, k: "Pages" },
    { v: Math.round(TOTAL_PAGES / BOOKS.length), k: "Average length" },
    { v: 15, k: "Public repositories" },
  ];
  $("#book-stats").innerHTML = stats.map((s, i) => `
    <div class="col-6 col-lg-3"><div class="stat reveal d${i}">
      <div class="stat-v" data-count="${s.v}">0</div>
      <div class="stat-k">${esc(s.k)}</div>
    </div></div>`).join("");

  $("#books-grid").innerHTML = BOOKS.map((b, i) => `
    <div class="col-md-6 col-lg-4">
      <div class="reveal d${i % 4}">
        ${bookCard(b)}
        <div class="mt-2 text-center">
          <a class="text-ink-3 small" href="project.html?id=${b.id}">the project it documents →</a>
        </div>
      </div>
    </div>`).join("");

  const t = $("#pages-total");
  if (t) t.textContent = TOTAL_PAGES.toLocaleString();

  try {
    const cat = await getCatalog();
    const g = cat.generated_at;
    $("#build-stamp").textContent = g ? `catalog built ${String(g).slice(0, 10)}` : "";
  } catch { /* the books list is static, so the page still works */ }

  initMotion();
  animateCounters();
})();
