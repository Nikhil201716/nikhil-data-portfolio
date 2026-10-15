/* about.js — renders the human story from data/profile.json */
(async function boot() {
  const av = $("[data-hero-avatar]");
  if (av) av.innerHTML = avatarHTML("avatar-lg");
  hydrateAvatars();
  renderAvailability();

  const pr = await getProfile().catch(() => null);
  if (pr) {
    const bio = $("[data-bio]");
    if (bio && Array.isArray(pr.bio)) {
      bio.innerHTML = pr.bio.map((p) => `<p class="sec-sub">${esc(p)}</p>`).join("");
    }
    const j = $("[data-journey]");
    if (j && Array.isArray(pr.journey)) {
      j.innerHTML = pr.journey.map((m) => `
        <div class="tl-item">
          <div class="tl-year">${esc(m.year)}</div>
          <div class="tl-title">${esc(m.title)}</div>
          ${m.place ? `<div class="tl-place">${esc(m.place)}</div>` : ""}
          <p class="tl-body">${esc(m.body)}</p>
        </div>`).join("");
    }
    const princ = $("[data-principle]");
    if (princ && pr.principle) princ.innerHTML = `&ldquo;${esc(pr.principle)}&rdquo;`;
  }

  initMotion();
  animateCounters();
})();
