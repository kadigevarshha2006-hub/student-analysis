/**
 * ResumeAI - Resume Upload & Document Controller
 */

let selectedResumeFile = null;
let currentMode = "upload"; // "upload" or "paste"

document.addEventListener("DOMContentLoaded", () => {
  initModeTabs();
  initUploadDropzone();
  initSampleJobButtons();
  initAnalyzeButton();
});

function initModeTabs() {
  const uploadTab = document.getElementById("tab-upload-btn");
  const pasteTab = document.getElementById("tab-paste-btn");
  const uploadContainer = document.getElementById("upload-mode-container");
  const pasteContainer = document.getElementById("paste-mode-container");

  if (!uploadTab || !pasteTab) return;

  uploadTab.addEventListener("click", () => {
    currentMode = "upload";
    uploadTab.className = "btn btn-primary";
    pasteTab.className = "btn btn-secondary";
    uploadContainer.style.display = "block";
    pasteContainer.style.display = "none";
  });

  pasteTab.addEventListener("click", () => {
    currentMode = "paste";
    pasteTab.className = "btn btn-primary";
    uploadTab.className = "btn btn-secondary";
    pasteContainer.style.display = "block";
    uploadContainer.style.display = "none";
  });
}

function initUploadDropzone() {
  const dropzone = document.getElementById("resume-dropzone");
  const fileInput = document.getElementById("resume-file-input");
  const browseBtn = document.getElementById("browse-btn");
  const preview = document.getElementById("file-preview");
  const fileNameEl = document.getElementById("file-name");
  const fileSizeEl = document.getElementById("file-size");
  const removeBtn = document.getElementById("remove-file-btn");

  if (!dropzone || !fileInput) return;

  // Open file dialog on dropzone click OR browse button click
  dropzone.addEventListener("click", () => {
    fileInput.value = "";
    fileInput.click();
  });

  browseBtn?.addEventListener("click", (e) => {
    e.stopPropagation();
    fileInput.value = "";
    fileInput.click();
  });

  // Drag and Drop Events
  ["dragenter", "dragover"].forEach(event => {
    dropzone.addEventListener(event, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.add("dragover");
    });
  });

  ["dragleave", "drop"].forEach(event => {
    dropzone.addEventListener(event, (e) => {
      e.preventDefault();
      e.stopPropagation();
      dropzone.classList.remove("dragover");
    });
  });

  dropzone.addEventListener("drop", (e) => {
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFileSelection(e.target.files[0]);
    }
  });

  // Remove File
  removeBtn?.addEventListener("click", (e) => {
    e.stopPropagation();
    selectedResumeFile = null;
    fileInput.value = "";
    preview.style.display = "none";
    dropzone.style.display = "block";
    window.showToast("File removed.", "info");
  });

  function handleFileSelection(file) {
    if (!file) return;
    
    const ext = file.name.split(".").pop().toLowerCase();
    if (!["pdf", "docx", "doc", "txt"].includes(ext)) {
      window.showToast("Please select a PDF or Word document.", "error");
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      window.showToast("File exceeds 10MB maximum limit.", "error");
      return;
    }

    selectedResumeFile = file;
    fileNameEl.textContent = file.name;
    fileSizeEl.textContent = formatBytes(file.size);

    dropzone.style.display = "none";
    preview.style.display = "flex";
    window.showToast(`Selected: ${file.name}`, "success");
  }
}

function formatBytes(bytes) {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + " " + sizes[i];
}

// Quick Sample Job Description Buttons
function initSampleJobButtons() {
  const sampleBtn = document.getElementById("load-sample-jd-btn");
  const jobTextarea = document.getElementById("job-description-text");
  const jobTitleInput = document.getElementById("job-title-input");
  const jobCompanyInput = document.getElementById("job-company-input");

  if (!sampleBtn || !jobTextarea) return;

  sampleBtn.addEventListener("click", async () => {
    try {
      const demo = await window.API.getDemoData();
      if (demo && demo.data) {
        jobTextarea.value = demo.data.job_text;
        if (jobTitleInput) jobTitleInput.value = demo.data.job_title;
        if (jobCompanyInput) jobCompanyInput.value = demo.data.company;
        window.showToast("Sample Job Description loaded!", "success");
      }
    } catch (e) {
      window.showToast("Could not load sample data.", "error");
    }
  });
}

// Action: Trigger Upload and Analysis
function initAnalyzeButton() {
  const analyzeBtn = document.getElementById("start-analysis-btn");
  if (!analyzeBtn) return;

  analyzeBtn.addEventListener("click", async () => {
    const pasteText = document.getElementById("resume-paste-text")?.value.trim() || "";
    
    if (currentMode === "upload" && !selectedResumeFile) {
      window.showToast("Please select a resume file or switch to Paste Text mode.", "warning");
      return;
    }

    if (currentMode === "paste" && !pasteText) {
      window.showToast("Please paste your resume text.", "warning");
      return;
    }

    const jobText = document.getElementById("job-description-text")?.value.trim() || "";
    const jobTitle = document.getElementById("job-title-input")?.value.trim() || "";
    const jobCompany = document.getElementById("job-company-input")?.value.trim() || "";

    const progressContainer = document.getElementById("upload-progress");
    const progressBar = document.getElementById("progress-bar-fill");
    const progressText = document.getElementById("progress-percentage");

    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<span class="spinner"></span> Processing Resume & Job Match...';

    if (progressContainer) progressContainer.style.display = "block";
    if (progressBar) progressBar.style.width = "40%";
    if (progressText) progressText.textContent = "40% (Parsing Document & Extracting Skills)";

    try {
      let resumeId = null;

      if (currentMode === "upload") {
        // Upload File
        const uploadRes = await window.API.uploadResume(selectedResumeFile);
        if (!uploadRes.success || !uploadRes.data) {
          throw new Error(uploadRes.message || "Failed to upload resume file.");
        }
        resumeId = uploadRes.data.id;
      } else {
        // Create from pasted text
        const textRes = await window.API.createResumeFromText(pasteText);
        if (!textRes.success || !textRes.data) {
          throw new Error(textRes.message || "Failed to process resume text.");
        }
        resumeId = textRes.data.id;
      }

      if (progressBar) progressBar.style.width = "80%";
      if (progressText) progressText.textContent = "80% (Computing ATS & Semantic Match)";

      sessionStorage.setItem("last_resume_id", resumeId);
      sessionStorage.setItem("last_job_text", jobText);
      sessionStorage.setItem("last_job_title", jobTitle);
      sessionStorage.setItem("last_job_company", jobCompany);

      window.showToast("Resume processed! Loading dashboard...", "success");

      setTimeout(() => {
        window.location.href = `results.html?resume_id=${resumeId}${jobText ? "&has_job=true" : ""}`;
      }, 900);

    } catch (err) {
      console.error(err);
      window.showToast(err.message || "Failed to analyze resume.", "error");
      analyzeBtn.disabled = false;
      analyzeBtn.innerHTML = '🚀 Analyze Resume & Match Job';
      if (progressContainer) progressContainer.style.display = "none";
    }
  });
}
