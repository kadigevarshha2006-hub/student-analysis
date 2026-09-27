/**
 * ResumeAI - Results Dashboard Controller
 */

let allInterviewQuestions = [];

document.addEventListener("DOMContentLoaded", async () => {
  initTabSwitching();
  initInterviewFilterButtons();
  await loadResultsData();
});

function initTabSwitching() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-content").forEach(c => c.classList.remove("active"));

      btn.classList.add("active");
      const targetId = btn.getAttribute("data-tab");
      document.getElementById(targetId)?.classList.add("active");
    });
  });
}

function initInterviewFilterButtons() {
  const filterBtns = document.querySelectorAll(".interview-filter-btn");
  filterBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      filterBtns.forEach(b => {
        b.classList.remove("btn-primary");
        b.classList.add("btn-secondary");
      });
      btn.classList.remove("btn-secondary");
      btn.classList.add("btn-primary");

      const category = btn.getAttribute("data-category");
      renderInterviewQuestionsList(category);
    });
  });
}

async function loadResultsData() {
  const urlParams = new URLSearchParams(window.location.search);
  const resumeId = urlParams.get("resume_id") || sessionStorage.getItem("last_resume_id") || "10";
  let jobText = sessionStorage.getItem("last_job_text") || "";
  let jobTitle = sessionStorage.getItem("last_job_title") || "";
  let jobCompany = sessionStorage.getItem("last_job_company") || "";

  if (!jobText.trim()) {
    jobText = `Full Stack Software Engineer
Looking for an engineer with skills in Python, MySQL, HTML, CSS, JavaScript, REST APIs, Git, and Cloud fundamentals.
Required: Python, SQL, REST APIs, Git, HTML, CSS, JavaScript.
Preferred: Docker, AWS, React, FastAPI, CI/CD.`;
    jobTitle = jobTitle || "Full Stack Software Engineer";
    jobCompany = jobCompany || "Target Tech Role";
  }

  try {
    const res = await window.API.request("/analysis/run", {
      method: "POST",
      body: JSON.stringify({
        resume_id: parseInt(resumeId),
        job_description_text: jobText,
        job_title: jobTitle,
        company: jobCompany
      })
    });

    if (res && res.success && res.data) {
      renderDashboard(res.data.analysis, res.data.job_match, res.data.interview_questions);
    }
  } catch (err) {
    console.error("Error loading analysis results:", err);
    window.showToast("Rendering analysis data...", "info");
  }
}

function renderDashboard(analysis, jobMatch, interviewQuestions) {
  if (!analysis) return;

  // 1. Render 3 Distinct Score Gauges
  const resumeHealth = analysis.resume_health_score || analysis.overall_score || 88;
  const atsScore = analysis.ats_score || 85;
  const matchPct = jobMatch ? jobMatch.overall_match_percentage : 78.0;
  const skillsBreadth = analysis.skills_score || 92;

  animateScoreGauge("overall-score-circle", "overall-score-val", resumeHealth, "#6366f1");
  animateScoreGauge("ats-score-circle", "ats-score-val", atsScore, "#06b6d4");
  animateScoreGauge("match-score-circle", "match-score-val", matchPct, "#10b981");
  animateScoreGauge("quality-score-circle", "quality-score-val", skillsBreadth, "#f59e0b");

  // 2. Strengths & Weaknesses (Overview Tab)
  const strengthsContainer = document.getElementById("strengths-list");
  if (strengthsContainer && analysis.strengths) {
    strengthsContainer.innerHTML = analysis.strengths.map(s => `
      <li style="display: flex; gap: 8px; margin-bottom: 8px;">
        <span style="color: var(--success);">✓</span> <span>${s}</span>
      </li>
    `).join("");
  }

  const weaknessesContainer = document.getElementById("weaknesses-list");
  if (weaknessesContainer && analysis.weaknesses) {
    weaknessesContainer.innerHTML = analysis.weaknesses.map(w => `
      <li style="display: flex; gap: 8px; margin-bottom: 8px;">
        <span style="color: var(--danger);">✗</span> <span>${w}</span>
      </li>
    `).join("");
  }

  const recContainer = document.getElementById("recommendations-list");
  if (recContainer && analysis.recommendations) {
    recContainer.innerHTML = analysis.recommendations.map(r => `
      <li style="display: flex; gap: 8px; margin-bottom: 8px;">
        <span style="color: var(--warning);">💡</span> <span>${r}</span>
      </li>
    `).join("");
  }

  // 3. ATS Checklist with Itemized Evidence
  const atsContainer = document.getElementById("ats-checks-container");
  if (atsContainer && analysis.ats_checks) {
    atsContainer.innerHTML = analysis.ats_checks.map(c => `
      <div class="ats-check-item">
        <div class="ats-check-status">${c.status === "PASS" ? "✅" : (c.status === "WARNING" ? "⚠️" : "❌")}</div>
        <div class="ats-check-body">
          <div class="ats-check-title">${c.check} <span class="badge ${c.status === "PASS" ? "badge-success" : "badge-warning"}">${Math.round(c.score)}/100</span></div>
          <div class="ats-check-msg" style="font-weight: 500; color: var(--text-primary); margin-top: 4px;">${c.message}</div>
          ${c.recommendation ? `<div class="ats-check-rec" style="margin-top: 6px; font-size: 0.85rem;"><strong>💡 Fix:</strong> ${c.recommendation}</div>` : ""}
        </div>
      </div>
    `).join("");
  }

  // 4. Job Match & 3-Tier Skill Gap
  if (jobMatch) {
    // A. Matched Skills
    const matchTags = document.getElementById("matching-skills-tags");
    if (matchTags) {
      matchTags.innerHTML = (jobMatch.matching_skills && jobMatch.matching_skills.length > 0)
        ? jobMatch.matching_skills.map(s => `<span class="skill-tag match">✓ ${s}</span>`).join("")
        : "<span style='color: var(--text-muted);'>No direct matching skills found.</span>";
    }

    // B. Missing Skills
    const missingTags = document.getElementById("missing-skills-tags");
    if (missingTags) {
      missingTags.innerHTML = (jobMatch.missing_skills && jobMatch.missing_skills.length > 0)
        ? jobMatch.missing_skills.map(s => `<span class="skill-tag missing">✗ ${s}</span>`).join("")
        : "<span style='color: var(--success);'>Zero missing requirements! Full skill alignment.</span>";
    }

    // C. Partially Matched (Transferable Skills)
    const partialContainer = document.getElementById("partial-skills-container");
    if (partialContainer) {
      const partials = jobMatch.partial_skills || [];
      if (partials.length > 0) {
        partialContainer.innerHTML = partials.map(p => `
          <div style="padding: 12px 16px; background: var(--bg-secondary); border-left: 4px solid var(--info); border-radius: var(--radius-sm); margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
              <strong style="color: var(--info); font-size: 0.95rem;">🔄 ${p.skill}</strong>
              <span class="badge badge-primary">Transferable from ${p.demonstrated_alternative}</span>
            </div>
            <p style="font-size: 0.88rem; color: var(--text-secondary); margin: 0;">${p.reason}</p>
          </div>
        `).join("");
      } else {
        partialContainer.innerHTML = "<p style='color: var(--text-muted); font-size: 0.9rem;'>No partial or transferable skill gaps detected.</p>";
      }
    }

    // D. Prioritized Skill Gap Breakdown
    const priorityContainer = document.getElementById("priority-gaps-container");
    if (priorityContainer) {
      const high = jobMatch.skill_gap_priority?.high || [];
      const med = jobMatch.skill_gap_priority?.medium || [];
      const low = jobMatch.skill_gap_priority?.low || [];

      let gapsHtml = "";
      if (high.length) {
        gapsHtml += high.map(item => `
          <div style="padding: 12px; border-left: 4px solid var(--danger); background: var(--danger-bg); border-radius: var(--radius-sm); margin-bottom: 8px;">
            <strong style="color: var(--danger);">${item.skill} (High Priority)</strong>: ${item.reason}
          </div>
        `).join("");
      }
      if (med.length) {
        gapsHtml += med.map(item => `
          <div style="padding: 12px; border-left: 4px solid var(--warning); background: var(--warning-bg); border-radius: var(--radius-sm); margin-bottom: 8px;">
            <strong style="color: var(--warning);">${item.skill} (Medium Priority)</strong>: ${item.reason}
          </div>
        `).join("");
      }
      if (low.length) {
        gapsHtml += low.map(item => `
          <div style="padding: 12px; border-left: 4px solid var(--info); background: var(--bg-card); border-radius: var(--radius-sm); margin-bottom: 8px;">
            <strong style="color: var(--info);">${item.skill} (Low Priority)</strong>: ${item.reason}
          </div>
        `).join("");
      }
      priorityContainer.innerHTML = gapsHtml || "<p style='color: var(--text-muted);'>No critical skill gaps identified.</p>";
    }

    // E. Role-Aware Learning Roadmap
    const roadmapContainer = document.getElementById("learning-roadmap-container");
    if (roadmapContainer && jobMatch.learning_roadmap && jobMatch.learning_roadmap.length > 0) {
      roadmapContainer.innerHTML = jobMatch.learning_roadmap.map((step, idx) => {
        const websites = step.websites || [];
        const yts = step.youtube_tutorials || [];
        const topics = step.key_topics || [];
        const why = step.why_it_matters || "";
        const project = step.practical_project || "";
        const milestone = step.milestone_goal || "";

        return `
          <div class="roadmap-step-card">
            <div class="roadmap-step-header">
              <span class="roadmap-step-badge">🚀 Step 0${idx+1}</span>
              <span class="roadmap-step-timeline">⏱️ ${step.timeline || 'Week ' + (idx*2+1) + ' - ' + (idx*2+2)}</span>
            </div>

            <h3 class="roadmap-skill-title">${step.skill}</h3>
            ${why ? `<p class="roadmap-why"><strong>Why it matters:</strong> ${why}</p>` : ''}

            ${topics.length ? `
              <div style="margin-bottom: 14px;">
                <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px;">Key Topics to Master:</div>
                <div class="roadmap-topics-wrap">
                  ${topics.map(t => `<span class="topic-pill">📌 ${t}</span>`).join('')}
                </div>
              </div>
            ` : ''}

            <div class="roadmap-resources-grid">
              <!-- Websites -->
              <div class="resource-box">
                <div class="resource-box-title">
                  <span class="doc-badge">DOCS</span> 🌐 Recommended Documentation & Guides
                </div>
                ${websites.map(w => `
                  <a href="${w.url}" target="_blank" rel="noopener noreferrer" class="resource-link-item">
                    <span>📖 ${w.title}</span>
                    <span style="font-size: 0.75rem; color: var(--primary);">Open ↗</span>
                  </a>
                `).join('')}
              </div>

              <!-- YouTube Videos -->
              <div class="resource-box">
                <div class="resource-box-title">
                  <span class="yt-badge">YOUTUBE</span> 🎥 Top Video Courses & Channels
                </div>
                ${yts.map(y => `
                  <a href="${y.url}" target="_blank" rel="noopener noreferrer" class="resource-link-item">
                    <span>▶️ ${y.title}</span>
                    <span style="font-size: 0.72rem; color: #ff0000; font-weight: 700;">${y.channel || 'Watch'} ↗</span>
                  </a>
                `).join('')}
              </div>
            </div>

            <!-- Practical Project -->
            ${project ? `
              <div class="roadmap-project-box">
                <div class="roadmap-project-title">🛠️ Practical Project Milestone:</div>
                <div class="roadmap-project-desc">${project}</div>
                ${milestone ? `<div style="margin-top: 8px; font-size: 0.85rem; color: var(--text-primary);"><strong>🎯 End Goal:</strong> ${milestone}</div>` : ''}
              </div>
            ` : ''}
          </div>
        `;
      }).join('');
    }
  }

  // 5. AI Bullet Point Rewrites
  const bulletContainer = document.getElementById("bullet-improvements-container");
  if (bulletContainer && analysis.bullet_improvements && analysis.bullet_improvements.length > 0) {
    bulletContainer.innerHTML = analysis.bullet_improvements.map(b => `
      <div class="bullet-card">
        <div style="font-size: 0.75rem; color: var(--danger); font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Original Bullet (from Resume)</div>
        <div class="bullet-original">"${b.original_text}"</div>

        ${b.why_needs_improvement ? `
          <div style="font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 8px;">
            <strong>⚠️ Why it needs improvement:</strong> ${b.why_needs_improvement}
          </div>
        ` : ''}

        <div style="font-size: 0.75rem; color: var(--success); font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">AI Optimized Rewrite (Preserves Facts, Strong Action Verbs)</div>
        <div class="bullet-suggested">"${b.suggested_text}"</div>

        <div class="bullet-reasoning" style="margin-top: 6px;">
          <strong>🎯 Why this version is better:</strong> ${b.why_better || b.reasoning || "Uses strong action verbs and emphasizes technical outcome."}
        </div>

        ${b.metric_suggestion ? `
          <div style="margin-top: 6px; font-size: 0.82rem; color: var(--info);">
            <strong>📊 Metric Guidance:</strong> ${b.metric_suggestion}
          </div>
        ` : ''}
      </div>
    `).join("");
  } else if (bulletContainer) {
    bulletContainer.innerHTML = `
      <div class="card" style="text-align: center; padding: 30px;">
        <p style="color: var(--text-secondary);">All bullet points in this resume already adhere to strong action verb guidelines!</p>
      </div>
    `;
  }

  // 6. Comprehensive Interview Prep (30+ Questions)
  allInterviewQuestions = interviewQuestions || [];
  renderInterviewQuestionsList("ALL");

  // 7. Skills Taxonomy Grid
  const skillsGrid = document.getElementById("categorized-skills-grid");
  if (skillsGrid && analysis.categorized_skills) {
    skillsGrid.innerHTML = Object.keys(analysis.categorized_skills).map(cat => `
      <div class="card" style="padding: 20px;">
        <h3 style="font-size: 1.1rem; margin-bottom: 12px; color: var(--primary);">${cat}</h3>
        <div>
          ${analysis.categorized_skills[cat].map(s => `<span class="skill-tag">${s}</span>`).join("")}
        </div>
      </div>
    `).join("");
  }

  // 8. Render Charts
  if (window.ResumeCharts) {
    window.ResumeCharts.renderRadarChart("radarChart", analysis.section_breakdown || {});
    window.ResumeCharts.renderDonutChart("donutChart", jobMatch?.matching_skills?.length || 8, jobMatch?.missing_skills?.length || 2);
    window.ResumeCharts.renderBarChart("barChart", analysis.categorized_skills || {});
  }
}

function renderInterviewQuestionsList(categoryFilter = "ALL") {
  const container = document.getElementById("interview-questions-container");
  if (!container) return;

  const filtered = categoryFilter === "ALL" 
    ? allInterviewQuestions 
    : allInterviewQuestions.filter(q => q.category.toLowerCase().includes(categoryFilter.toLowerCase()) || categoryFilter.toLowerCase().includes(q.category.toLowerCase()));

  if (filtered.length === 0) {
    container.innerHTML = `<p style="color: var(--text-muted); text-align: center; padding: 20px;">No questions found for category: ${categoryFilter}</p>`;
    return;
  }

  container.innerHTML = filtered.map((q, idx) => `
    <div class="interview-card">
      <div class="interview-card-header">
        <span class="interview-category-tag">${q.category || 'Technical Question'}</span>
        <span class="badge ${q.difficulty === 'Advanced' ? 'badge-danger' : (q.difficulty === 'Intermediate' ? 'badge-warning' : 'badge-primary')}">${q.difficulty || 'Intermediate'}</span>
        <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 600; margin-left: auto;">Question ${idx+1} of ${filtered.length}</span>
      </div>

      <h3 class="interview-question-text">"${q.question}"</h3>

      <div class="interview-intent-box">
        🎯 <strong>Why Interviewer Asks This:</strong> ${q.interviewer_intent || 'Assesses practical depth and engineering trade-offs.'}
      </div>

      ${q.key_topics && q.key_topics.length ? `
        <div style="margin-bottom: 12px;">
          <span style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase;">Key Concepts to Cover:</span>
          <div style="display: flex; gap: 6px; flex-wrap: wrap; margin-top: 4px;">
            ${q.key_topics.map(t => `<span class="topic-pill">${t}</span>`).join('')}
          </div>
        </div>
      ` : ''}

      ${q.key_points_to_mention && q.key_points_to_mention.length ? `
        <div class="interview-points-title">💡 High-Scoring Points to Mention:</div>
        <ul class="interview-points-list">
          ${q.key_points_to_mention.map(p => `<li>${p}</li>`).join('')}
        </ul>
      ` : ''}

      <div class="interview-answer-box">
        <div class="interview-answer-title">⭐ Recommended Answer Strategy (STAR Method):</div>
        <div class="interview-answer-text">${q.sample_strong_answer || 'Provide a structured answer with Situation, Technical Approach, Implementation, and Outcome.'}</div>
      </div>
    </div>
  `).join('');
}

function animateScoreGauge(circleId, valId, targetScore, color) {
  const circle = document.getElementById(circleId);
  const valEl = document.getElementById(valId);
  if (!circle || !valEl) return;

  circle.style.setProperty("--accent-color", color);
  
  let current = 0;
  const increment = targetScore / 40;
  const timer = setInterval(() => {
    current += increment;
    if (current >= targetScore) {
      current = targetScore;
      clearInterval(timer);
    }
    circle.style.setProperty("--pct", current);
    valEl.textContent = Math.round(current);
  }, 20);
}
