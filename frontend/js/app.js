/**
 * ResumeAI - Core App Initializer & Global State
 */

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  syncNavAuth();
});

// Theme Management (Light / Dark Mode)
function initTheme() {
  const savedTheme = localStorage.getItem("resume_ai_theme") || "dark";
  document.documentElement.setAttribute("data-theme", savedTheme);

  const themeToggles = document.querySelectorAll(".theme-toggle-btn");
  themeToggles.forEach(btn => {
    btn.innerHTML = savedTheme === "dark" ? "☀️" : "🌙";
    btn.addEventListener("click", toggleTheme);
  });
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme") || "dark";
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("resume_ai_theme", next);

  const themeToggles = document.querySelectorAll(".theme-toggle-btn");
  themeToggles.forEach(btn => {
    btn.innerHTML = next === "dark" ? "☀️" : "🌙";
  });
}

// Sync Navigation Auth State
function syncNavAuth() {
  const user = window.API ? window.API.getUser() : null;
  const authNav = document.getElementById("auth-nav-container");

  if (authNav) {
    if (user) {
      authNav.innerHTML = `
        <span style="font-size: 0.9rem; color: var(--text-secondary); margin-right: 8px;">Hi, ${user.full_name.split(" ")[0]}</span>
        <a href="dashboard.html" class="btn btn-secondary" style="padding: 6px 14px; font-size: 0.85rem;">Dashboard</a>
        <button id="logout-btn" class="btn btn-outline" style="padding: 6px 14px; font-size: 0.85rem;">Logout</button>
      `;
      document.getElementById("logout-btn")?.addEventListener("click", () => {
        window.API.removeToken();
        window.location.href = "index.html";
      });
    } else {
      authNav.innerHTML = `
        <a href="login.html" class="btn btn-secondary" style="padding: 6px 16px; font-size: 0.9rem;">Sign In</a>
        <a href="register.html" class="btn btn-primary" style="padding: 6px 16px; font-size: 0.9rem;">Get Started</a>
      `;
    }
  }
}
