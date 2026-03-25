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
  if (!toggle || !links) return;

  toggle.addEventListener("click", () => {
    // Toggle open/closed state and sync aria-expanded for accessibility.
    const isOpen = links.classList.toggle("open");
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

// ================= CONFIRM BEFORE DESTRUCTIVE ACTIONS =================
// Any element with `data-confirm="..."` triggers a browser confirm() prompt.
function setupConfirmButtons() {
  document.addEventListener("click", (e) => {
    // Identify the clicked element.
    const target = e.target;
    if (!(target instanceof HTMLElement)) return;

    // If there is no confirm text, do nothing.
    const confirmText = target.getAttribute("data-confirm");
    if (!confirmText) return;

    // Cancel default action when the user clicks "Cancel".
    const ok = window.confirm(confirmText);
    if (!ok) {
      e.preventDefault();
      e.stopPropagation();
    }
  });
}

// ================= INITIALISE FEATURES =================
setupNavToggle();
setupConfirmButtons();
