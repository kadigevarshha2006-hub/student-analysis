/**
 * ResumeAI - Dynamic User Dashboard Controller
 */

document.addEventListener("DOMContentLoaded", () => {
  loadUserDashboard();
});

async function loadUserDashboard() {
  const user = window.API ? window.API.getUser() : null;
  const token = window.API ? window.API.getToken() : null;

  const nameEl = document.getElementById("dash-user-name");
  const emailEl = document.getElementById("dash-user-email");
  const totalEl = document.getElementById("user-stat-total-resumes");
  const bestOverallEl = document.getElementById("user-stat-best-overall");
  const bestAtsEl = document.getElementById("user-stat-best-ats");
  const tableBody = document.getElementById("history-table-body");

  if (!token || !user) {
    if (nameEl) nameEl.textContent = "Guest / Not Logged In";
    if (emailEl) emailEl.innerHTML = `<a href="login.html" style="color: var(--primary); text-decoration: underline;">Sign In</a> to view your personal uploaded resumes.`;
    if (totalEl) totalEl.textContent = "0";
    if (bestOverallEl) bestOverallEl.textContent = "-- / 100";
    if (bestAtsEl) bestAtsEl.textContent = "-- / 100";

    if (tableBody) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" style="text-align: center; padding: 40px; color: var(--text-secondary);">
            <div style="font-size: 2rem; margin-bottom: 8px;">🔐</div>
            <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">You are currently browsing as Guest</div>
            <p style="font-size: 0.9rem; margin-bottom: 16px;">Sign in to your account to view your uploaded resumes and evaluation reports.</p>
            <div style="display: flex; gap: 10px; justify-content: center;">
              <a href="login.html" class="btn btn-primary" style="padding: 6px 16px;">Sign In</a>
              <a href="register.html" class="btn btn-secondary" style="padding: 6px 16px;">Create Account</a>
            </div>
          </td>
        </tr>
      `;
    }
    return;
  }

  // Display user profile info
  if (nameEl) nameEl.textContent = user.full_name;
  if (emailEl) emailEl.textContent = user.email;

  try {
    const res = await window.API.request("/resume/my-history");
    if (!res || !res.success || !res.data) {
      throw new Error(res?.message || "Failed to load history.");
    }

    const { stats, resumes } = res.data;

    // Update stats
    if (totalEl) totalEl.textContent = stats.total_resumes;
    if (bestOverallEl) {
      bestOverallEl.textContent = stats.best_overall > 0 ? `${stats.best_overall} / 100` : "-- / 100";
    }
    if (bestAtsEl) {
      bestAtsEl.textContent = stats.best_ats > 0 ? `${stats.best_ats} / 100` : "-- / 100";
    }

    // Render table rows
    if (tableBody) {
      if (!resumes || resumes.length === 0) {
        tableBody.innerHTML = `
          <tr>
            <td colspan="6" style="text-align: center; padding: 40px; color: var(--text-secondary);">
              <div style="font-size: 2rem; margin-bottom: 8px;">📄</div>
              <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-primary); margin-bottom: 6px;">No Resumes Uploaded Yet</div>
              <p style="font-size: 0.9rem; margin-bottom: 16px;">You haven't uploaded any resumes under <strong>${escapeHtml(user.email)}</strong> yet.</p>
              <a href="analyzer.html" class="btn btn-primary" style="padding: 8px 18px;">🚀 Upload Your First Resume</a>
            </td>
          </tr>
        `;
        return;
      }

      tableBody.innerHTML = resumes.map(r => {
        const ovBadge = r.overall_score !== null
          ? `<span class="badge badge-success">${r.overall_score} / 100</span>`
          : `<span class="badge badge-warning">Not Analyzed</span>`;

        const atsBadge = r.ats_score !== null
          ? `<span class="badge badge-primary">${r.ats_score} / 100</span>`
          : `<span class="badge badge-warning">--</span>`;

        return `
          <tr style="border-bottom: 1px solid var(--border-color);">
            <td style="padding: 16px 24px; font-weight: 600;">
              📄 ${escapeHtml(r.filename)}
              <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase;">(${r.file_type})</span>
            </td>
            <td style="padding: 16px 24px; color: var(--text-secondary); font-size: 0.85rem;">${r.created_at}</td>
            <td style="padding: 16px 24px;">${ovBadge}</td>
            <td style="padding: 16px 24px;">${atsBadge}</td>
            <td style="padding: 16px 24px;">
              <span class="badge ${r.has_analysis ? 'badge-success' : 'badge-warning'}">
                ${r.has_analysis ? '✓ Evaluated' : 'Pending'}
              </span>
            </td>
            <td style="padding: 16px 24px; text-align: right;">
              <a href="results.html?resume_id=${r.id}" class="btn btn-outline" style="padding: 4px 12px; font-size: 0.8rem;">
                View Full Report
              </a>
            </td>
          </tr>
        `;
      }).join("");
    }
  } catch (err) {
    console.error("Dashboard history load error:", err);
    // Fall back gracefully
    if (tableBody) {
      tableBody.innerHTML = `
        <tr>
          <td colspan="6" style="text-align: center; padding: 30px; color: var(--danger);">
            Could not load resume history (${escapeHtml(err.message)}).
            <div style="margin-top: 10px;">
              <a href="analyzer.html" class="btn btn-secondary" style="padding: 4px 12px; font-size: 0.8rem;">Upload & Analyze Resume</a>
            </div>
          </td>
        </tr>
      `;
    }
  }
}

function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
