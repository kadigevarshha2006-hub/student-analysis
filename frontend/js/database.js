/**
 * ResumeAI - Live Database Viewer Controller
 * Fetches and displays real-time records from Render cloud database
 */

let cachedDbData = null;
let currentTab = "users";

document.addEventListener("DOMContentLoaded", () => {
  loadDatabaseData();

  const refreshBtn = document.getElementById("refresh-db-btn");
  if (refreshBtn) {
    refreshBtn.addEventListener("click", () => {
      refreshBtn.innerHTML = "⏳ Syncing...";
      refreshBtn.disabled = true;
      loadDatabaseData().finally(() => {
        refreshBtn.innerHTML = "🔄 Refresh Live Data";
        refreshBtn.disabled = false;
      });
    });
  }
});

async function loadDatabaseData() {
  try {
    const res = await window.API.request("/admin/overview");
    if (!res || !res.success || !res.data) {
      throw new Error(res?.message || "Failed to retrieve database records.");
    }

    cachedDbData = res.data;
    renderAll(cachedDbData);
    if (window.showToast) {
      window.showToast("Database records synchronized!", "success", 2000);
    }
  } catch (err) {
    console.error("Database fetch error:", err);
    if (window.showToast) {
      window.showToast(`Error connecting to database: ${err.message}`, "error");
    }
    const userTable = document.getElementById("users-table-body");
    if (userTable) {
      userTable.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--danger); padding: 30px;">Failed to connect to database: ${err.message}</td></tr>`;
    }
  }
}

function renderAll(data) {
  // Update header stats
  document.getElementById("stat-total-users").textContent = data.counts.users;
  document.getElementById("stat-total-resumes").textContent = data.counts.resumes;
  document.getElementById("stat-total-analyses").textContent = data.counts.analyses;
  document.getElementById("stat-db-engine").textContent = data.database_dialect.toUpperCase();
  document.getElementById("db-engine-badge").textContent = data.database_engine;
  document.getElementById("sync-timestamp").textContent = data.server_timestamp;

  // Update tab badges
  document.getElementById("badge-users-count").textContent = data.counts.users;
  document.getElementById("badge-resumes-count").textContent = data.counts.resumes;
  document.getElementById("badge-analyses-count").textContent = data.counts.analyses;

  // Render individual tables
  renderUsers(data.users);
  renderResumes(data.resumes);
  renderAnalyses(data.analyses);
  renderJson(data);
}

function renderUsers(users) {
  const tbody = document.getElementById("users-table-body");
  if (!tbody) return;

  if (!users || users.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; color: var(--text-muted); padding: 30px;">No registered users in the database yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = users.map(u => `
    <tr>
      <td style="font-weight: 700; color: var(--primary);">#${u.id}</td>
      <td style="font-weight: 600;">${escapeHtml(u.full_name)}</td>
      <td>
        <span style="font-family: monospace; color: var(--text-secondary);">${escapeHtml(u.email)}</span>
      </td>
      <td>
        <span class="badge ${u.resumes_count > 0 ? 'badge-primary' : 'badge-warning'}">
          ${u.resumes_count} uploaded
        </span>
      </td>
      <td style="color: var(--text-muted); font-size: 0.85rem;">${u.created_at}</td>
      <td>
        <span class="badge ${u.is_active ? 'badge-success' : 'badge-danger'}">
          ${u.is_active ? '✓ Active' : 'Disabled'}
        </span>
      </td>
    </tr>
  `).join("");
}

function renderResumes(resumes) {
  const tbody = document.getElementById("resumes-table-body");
  if (!tbody) return;

  if (!resumes || resumes.length === 0) {
    tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; color: var(--text-muted); padding: 30px;">No resumes uploaded to the database yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = resumes.map(r => {
    const sizeKb = Math.round(r.file_size_bytes / 1024);
    const overallBadge = r.overall_score !== null
      ? `<span class="badge badge-success">${r.overall_score} / 100</span>`
      : `<span class="badge badge-warning">Not Evaluated</span>`;
    
    const atsBadge = r.ats_score !== null
      ? `<span class="badge badge-primary">${r.ats_score} / 100</span>`
      : `<span class="badge badge-warning">--</span>`;

    return `
      <tr>
        <td style="font-weight: 700; color: var(--primary);">#${r.id}</td>
        <td style="font-weight: 600;">
          📄 ${escapeHtml(r.filename)}
          <span style="font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; margin-left: 4px;">(${r.file_type})</span>
        </td>
        <td>
          <div style="font-size: 0.85rem; font-weight: 500;">${escapeHtml(r.uploader_name)}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${escapeHtml(r.uploader_email)}</div>
        </td>
        <td style="color: var(--text-secondary); font-size: 0.85rem;">${sizeKb} KB</td>
        <td>${overallBadge}</td>
        <td>${atsBadge}</td>
        <td style="color: var(--text-muted); font-size: 0.85rem;">${r.created_at}</td>
        <td style="text-align: right;">
          <a href="results.html?resume_id=${r.id}" class="btn btn-outline" style="padding: 4px 10px; font-size: 0.75rem;">
            📊 View Analysis
          </a>
        </td>
      </tr>
    `;
  }).join("");
}

function renderAnalyses(analyses) {
  const tbody = document.getElementById("analyses-table-body");
  if (!tbody) return;

  if (!analyses || analyses.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: var(--text-muted); padding: 30px;">No analysis records computed yet.</td></tr>`;
    return;
  }

  tbody.innerHTML = analyses.map(a => `
    <tr>
      <td style="font-weight: 700; color: var(--primary);">#${a.id}</td>
      <td style="font-weight: 600;">
        <a href="results.html?resume_id=${a.resume_id}" style="color: var(--primary); text-decoration: underline;">
          Resume #${a.resume_id} (${escapeHtml(a.resume_filename)})
        </a>
      </td>
      <td style="font-size: 0.85rem; color: var(--text-secondary);">${escapeHtml(a.user_email)}</td>
      <td><span class="badge badge-success">${a.overall_score} / 100</span></td>
      <td><span class="badge badge-primary">${a.ats_score} / 100</span></td>
      <td><span class="badge badge-info">${a.quality_score}</span></td>
      <td><span class="badge badge-secondary">${a.readability_score}</span></td>
      <td><span class="badge badge-warning">${a.skills_score}</span></td>
      <td style="color: var(--text-muted); font-size: 0.85rem;">${a.created_at}</td>
    </tr>
  `).join("");
}

function renderJson(data) {
  const box = document.getElementById("raw-json-content");
  if (!box) return;
  box.textContent = JSON.stringify(data, null, 2);
}

function switchDbTab(tabName) {
  currentTab = tabName;
  const tabs = ["users", "resumes", "analyses", "json"];

  tabs.forEach(t => {
    const btn = document.getElementById(`tab-${t}-btn`);
    const view = document.getElementById(`view-${t}`);
    if (btn) btn.classList.toggle("active", t === tabName);
    if (view) view.style.display = t === tabName ? "block" : "none";
  });
}

function handleDbFilter() {
  const query = (document.getElementById("db-search-input")?.value || "").toLowerCase().trim();
  if (!cachedDbData) return;

  if (currentTab === "users") {
    const filtered = cachedDbData.users.filter(u => 
      u.full_name.toLowerCase().includes(query) ||
      u.email.toLowerCase().includes(query) ||
      String(u.id).includes(query)
    );
    renderUsers(filtered);
  } else if (currentTab === "resumes") {
    const filtered = cachedDbData.resumes.filter(r =>
      r.filename.toLowerCase().includes(query) ||
      r.uploader_email.toLowerCase().includes(query) ||
      r.uploader_name.toLowerCase().includes(query) ||
      String(r.id).includes(query)
    );
    renderResumes(filtered);
  } else if (currentTab === "analyses") {
    const filtered = cachedDbData.analyses.filter(a =>
      a.resume_filename.toLowerCase().includes(query) ||
      a.user_email.toLowerCase().includes(query) ||
      String(a.id).includes(query) ||
      String(a.resume_id).includes(query)
    );
    renderAnalyses(filtered);
  }
}

function copyDbJson() {
  const box = document.getElementById("raw-json-content");
  if (!box) return;
  navigator.clipboard.writeText(box.textContent).then(() => {
    if (window.showToast) window.showToast("Database JSON copied to clipboard!", "success");
  });
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

// Global exposure
window.switchDbTab = switchDbTab;
window.handleDbFilter = handleDbFilter;
window.copyDbJson = copyDbJson;
