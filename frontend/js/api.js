/**
 * ResumeAI - API Service Layer & Global Utilities
 * Pure Vanilla JavaScript Client
 */

const API_BASE_URL = window.location.protocol === "file:"
  ? "http://127.0.0.1:8000/api"
  : "/api";

const API = {
  getToken() {
    return localStorage.getItem("resume_ai_token");
  },
  
  setToken(token) {
    localStorage.setItem("resume_ai_token", token);
  },

  removeToken() {
    localStorage.removeItem("resume_ai_token");
    localStorage.removeItem("resume_ai_user");
  },

  getUser() {
    try {
      const user = localStorage.getItem("resume_ai_user");
      return user ? JSON.parse(user) : null;
    } catch {
      return null;
    }
  },

  setUser(user) {
    localStorage.setItem("resume_ai_user", JSON.stringify(user));
  },

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const headers = options.headers || {};
    
    const token = this.getToken();
    if (token && !headers["Authorization"]) {
      headers["Authorization"] = `Bearer ${token}`;
    }

    if (!(options.body instanceof FormData) && !headers["Content-Type"]) {
      headers["Content-Type"] = "application/json";
    }

    const config = {
      ...options,
      headers
    };

    try {
      const response = await fetch(url, config);
      const data = await response.json().catch(() => null);

      if (!response.ok) {
        const errorMsg = data?.detail || data?.message || data?.error || `HTTP error ${response.status}`;
        throw new Error(errorMsg);
      }

      return data;
    } catch (err) {
      console.error(`API Error [${endpoint}]:`, err);
      throw err;
    }
  },

  // Auth Endpoints
  async register(fullName, email, password) {
    return this.request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ full_name: fullName, email, password })
    });
  },

  async login(email, password) {
    return this.request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password })
    });
  },

  async getMe() {
    return this.request("/auth/me", { method: "GET" });
  },

  // Resume Endpoints
  async uploadResume(file) {
    const formData = new FormData();
    formData.append("file", file);
    return this.request("/resume/upload", {
      method: "POST",
      body: formData
    });
  },

  async createResumeFromText(rawText, title = "Pasted_Resume") {
    return this.request("/resume/create_text", {
      method: "POST",
      body: JSON.stringify({ title, raw_text: rawText })
    });
  },

  // Demo Endpoints
  async getDemoData() {
    return this.request("/demo/data", { method: "GET" });
  },

  async getDemoAnalysis() {
    return this.request("/demo/analysis", { method: "GET" });
  },

  async getDemoMatch() {
    return this.request("/demo/match", { method: "GET" });
  }
};

/**
 * Global Toast Notification Generator
 */
function showToast(message, type = "info", duration = 4000) {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  
  let icon = "ℹ️";
  if (type === "success") icon = "✅";
  if (type === "error") icon = "❌";
  if (type === "warning") icon = "⚠️";

  toast.innerHTML = `<span>${icon}</span> <div>${message}</div>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    toast.style.transition = "all 0.3s ease";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Export to window
window.API = API;
window.showToast = showToast;
