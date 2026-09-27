/**
 * ResumeAI - Authentication Controller (Vanilla JS)
 */

document.addEventListener("DOMContentLoaded", () => {
  initPasswordToggles();
  initLoginForm();
  initRegisterForm();
  initPasswordStrengthChecker();
});

// Password Show / Hide Toggle
function initPasswordToggles() {
  const toggleButtons = document.querySelectorAll(".password-toggle");
  toggleButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const input = btn.previousElementSibling;
      if (input.type === "password") {
        input.type = "text";
        btn.textContent = "🙈";
      } else {
        input.type = "password";
        btn.textContent = "👁️";
      }
    });
  });
}

// Password Strength Meter
function initPasswordStrengthChecker() {
  const passwordInput = document.getElementById("register-password");
  const strengthBar = document.getElementById("password-strength-bar");
  
  if (!passwordInput || !strengthBar) return;

  passwordInput.addEventListener("input", () => {
    const val = passwordInput.value;
    strengthBar.className = "password-strength-bar";

    if (val.length === 0) {
      strengthBar.style.width = "0%";
    } else if (val.length < 6) {
      strengthBar.classList.add("strength-weak");
    } else if (val.length >= 6 && /[A-Z]/.test(val) && /[0-9]/.test(val)) {
      strengthBar.classList.add("strength-strong");
    } else {
      strengthBar.classList.add("strength-medium");
    }
  });
}

// Handle Login Form Submission
function initLoginForm() {
  const form = document.getElementById("login-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("login-email").value.trim();
    const password = document.getElementById("login-password").value;
    const submitBtn = form.querySelector("button[type='submit']");
    const errorMsg = document.getElementById("login-error");

    if (errorMsg) errorMsg.style.display = "none";
    
    // UI Loading State
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="spinner"></span> Signing in...';
    submitBtn.disabled = true;

    try {
      const res = await window.API.login(email, password);
      if (res.success && res.data) {
        window.API.setToken(res.data.access_token);
        window.API.setUser(res.data.user);
        window.showToast("Login successful! Redirecting...", "success");
        setTimeout(() => {
          window.location.href = "analyzer.html";
        }, 800);
      }
    } catch (err) {
      if (errorMsg) {
        errorMsg.textContent = err.message || "Failed to sign in. Please verify your credentials.";
        errorMsg.style.display = "block";
      }
      window.showToast(err.message || "Invalid credentials", "error");
    } finally {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
}

// Handle Registration Form Submission
function initRegisterForm() {
  const form = document.getElementById("register-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const fullName = document.getElementById("register-name").value.trim();
    const email = document.getElementById("register-email").value.trim();
    const password = document.getElementById("register-password").value;
    const submitBtn = form.querySelector("button[type='submit']");
    const errorMsg = document.getElementById("register-error");

    if (errorMsg) errorMsg.style.display = "none";

    if (password.length < 6) {
      if (errorMsg) {
        errorMsg.textContent = "Password must be at least 6 characters long.";
        errorMsg.style.display = "block";
      }
      return;
    }

    // UI Loading State
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML = '<span class="spinner"></span> Creating Account...';
    submitBtn.disabled = true;

    try {
      const res = await window.API.register(fullName, email, password);
      if (res.success && res.data) {
        window.API.setToken(res.data.access_token);
        window.API.setUser(res.data.user);
        window.showToast("Account created successfully! Redirecting...", "success");
        setTimeout(() => {
          window.location.href = "analyzer.html";
        }, 800);
      }
    } catch (err) {
      if (errorMsg) {
        errorMsg.textContent = err.message || "Registration failed. Please try again.";
        errorMsg.style.display = "block";
      }
      window.showToast(err.message || "Registration failed", "error");
    } finally {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }
  });
}
