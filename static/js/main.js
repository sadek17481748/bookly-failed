// ===========================================================================
// GLOBAL JAVASCRIPT (static/js/main.js)
// - Loaded by base.html with `defer`
// - Adds small progressive enhancements only
// ===========================================================================

// ================= MOBILE NAV TOGGLE =================
// Toggles `.open` on #navLinks and updates `aria-expanded`.
function setupNavToggle() {
  // Grab the toggle button and the nav container.
  const toggle = document.querySelector(".nav-toggle");
  const links = document.getElementById("navLinks");
