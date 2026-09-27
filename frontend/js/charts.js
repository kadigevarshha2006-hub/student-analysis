/**
 * ResumeAI - Chart.js Visualizations (Radar, Donut, Bar)
 */

const ResumeCharts = {
  radarChartInstance: null,
  donutChartInstance: null,
  barChartInstance: null,

  // Render Radar Chart for Section Breakdown
  renderRadarChart(canvasId, sectionBreakdown) {
    const ctx = document.getElementById(canvasId)?.getContext("2d");
    if (!ctx) return;

    if (this.radarChartInstance) {
      this.radarChartInstance.destroy();
    }

    const labels = Object.keys(sectionBreakdown).map(k => k.replace("_", " ").toUpperCase());
    const dataValues = Object.values(sectionBreakdown);

    this.radarChartInstance = new Chart(ctx, {
      type: "radar",
      data: {
        labels: labels.length ? labels : ["CONTACT", "HEADINGS", "SKILLS", "EXPERIENCE", "PROJECTS"],
        datasets: [{
          label: "Section Score",
          data: dataValues.length ? dataValues : [95, 90, 85, 80, 75],
          backgroundColor: "rgba(99, 102, 241, 0.25)",
          borderColor: "#6366f1",
          borderWidth: 2,
          pointBackgroundColor: "#818cf8",
          pointBorderColor: "#fff",
          pointHoverBackgroundColor: "#fff",
          pointHoverBorderColor: "#6366f1"
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: "rgba(255, 255, 255, 0.1)" },
            grid: { color: "rgba(255, 255, 255, 0.1)" },
            pointLabels: {
              color: "#9ca3af",
              font: { size: 11, weight: "600" }
            },
            ticks: {
              backdropColor: "transparent",
              color: "#6b7280",
              min: 0,
              max: 100,
              stepSize: 20
            }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  },

  // Render Donut Chart for Match Overlap
  renderDonutChart(canvasId, matchingCount, missingCount) {
    const ctx = document.getElementById(canvasId)?.getContext("2d");
    if (!ctx) return;

    if (this.donutChartInstance) {
      this.donutChartInstance.destroy();
    }

    this.donutChartInstance = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Matching Skills", "Missing Skills"],
        datasets: [{
          data: [matchingCount || 8, missingCount || 2],
          backgroundColor: ["#10b981", "#ef4444"],
          borderColor: "rgba(17, 24, 39, 0.8)",
          borderWidth: 2,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "bottom",
            labels: { color: "#9ca3af", font: { size: 12 } }
          }
        },
        cutout: "70%"
      }
    });
  },

  // Render Bar Chart for Skill Categories
  renderBarChart(canvasId, categorizedSkills) {
    const ctx = document.getElementById(canvasId)?.getContext("2d");
    if (!ctx) return;

    if (this.barChartInstance) {
      this.barChartInstance.destroy();
    }

    const categories = Object.keys(categorizedSkills || {});
    const counts = categories.map(cat => categorizedSkills[cat].length);

    this.barChartInstance = new Chart(ctx, {
      type: "bar",
      data: {
        labels: categories.length ? categories : ["Programming", "Web Dev", "Databases", "AI/ML", "DevOps"],
        datasets: [{
          label: "Skills Count",
          data: counts.length ? counts : [5, 4, 3, 4, 3],
          backgroundColor: [
            "rgba(99, 102, 241, 0.8)",
            "rgba(6, 182, 212, 0.8)",
            "rgba(16, 185, 129, 0.8)",
            "rgba(245, 158, 11, 0.8)",
            "rgba(139, 92, 246, 0.8)"
          ],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            grid: { display: false },
            ticks: { color: "#9ca3af", font: { size: 11 } }
          },
          y: {
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            ticks: { color: "#6b7280", stepSize: 1, precision: 0 },
            beginAtZero: true
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
};

window.ResumeCharts = ResumeCharts;
