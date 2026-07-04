<template>
  <div class="login-page d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 login-card p-4">

      <div class="text-center mb-4">
        <h3 class="fw-bold brand-text">NextGig</h3>
        <p class="text-muted">Login to continue</p>
      </div>

      <!-- ✅ NEW: Email Verification Required Alert -->
      <div v-if="requiresVerification" class="alert alert-warning rounded-4 p-3 mb-4" role="alert">
        <div class="d-flex align-items-start">
          <i class="bi bi-exclamation-triangle-fill me-3 mt-1" style="font-size: 1.3rem;"></i>
          <div style="flex: 1;">
            <strong>Email Not Verified</strong>
            <p class="mb-2 small" style="margin-top: 0.3rem;">
              Your email hasn't been verified yet. Check your inbox for the verification link.
            </p>
            <small class="text-muted d-block mb-2">
              <i class="bi bi-envelope me-1"></i>
              Sent to: <strong>{{ unverifiedEmail }}</strong>
            </small>
            <button 
              type="button"
              class="btn btn-sm btn-warning rounded-pill"
              @click="resendVerification"
              :disabled="resendLoading"
            >
              <i v-if="!resendLoading" class="bi bi-arrow-repeat me-1"></i>
              <span v-if="resendLoading" class="spinner-border spinner-border-sm me-1"></span>
              {{ resendLoading ? 'Sending...' : 'Resend Verification Email' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Login Form (Hidden when email verification required) -->
      <form @submit.prevent="handleLogin" v-if="!requiresVerification">

        <!-- Email -->
        <div class="mb-3">
          <label class="form-label">Email</label>
          <input
            type="email"
            v-model="email"
            class="form-control rounded-pill"
            placeholder="Enter your email"
            required
          />
        </div>

        <!-- Password -->
        <div class="mb-3">
          <label class="form-label">Password</label>
          <div class="input-group">
            <input
              :type="showPassword ? 'text' : 'password'"
              v-model="password"
              class="form-control rounded-start-pill border-end-0"
              placeholder="Enter your password"
              required
            />
            <button
              type="button"
              class="btn btn-outline-secondary rounded-end-pill border-start-0"
              @click="togglePassword"
            >
              <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
            </button>
          </div>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger py-2 rounded-pill" role="alert">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          {{ error }}
        </div>

        <!-- Login Button -->
        <button
          type="submit"
          class="btn btn-success w-100 mt-3 rounded-pill"
          :disabled="loading"
        >
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          <span v-if="loading">Logging in...</span>
          <span v-else><i class="bi bi-box-arrow-in-right me-2"></i>Login</span>
        </button>

      </form>

      <!-- Register Options -->
      <div class="register-options mt-4">
        <div class="text-center mb-2">
          <small class="text-muted">Don't have an account?</small>
        </div>
        <div class="d-flex gap-2">
          <router-link to="/register/student" class="flex-fill">
            <button class="btn btn-outline-register student-btn w-100 rounded-pill">
              <i class="bi bi-mortarboard me-2"></i>
              Student
            </button>
          </router-link>
          <router-link to="/register/company" class="flex-fill">
            <button class="btn btn-outline-register company-btn w-100 rounded-pill">
              <i class="bi bi-building me-2"></i>
              Company
            </button>
          </router-link>
        </div>
      </div>

      <!-- Footer -->
      <div class="text-center mt-4">
        <small class="text-muted">
          <i class="bi bi-shield-check me-1"></i>
          Your gateway to dream opportunities
        </small>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios"
import { API_URL } from "@/config";

export default {
  data() {
    return {
      showPassword: false,
      email: "",
      password: "",
      loading: false,
      error: null,
      // ✅ NEW: Email verification fields
      requiresVerification: false,
      unverifiedEmail: '',
      resendLoading: false
    };
  },
  methods: {
    togglePassword() {
      this.showPassword = !this.showPassword;
    },

    async handleLogin() {
      this.loading = true;
      this.error = null;
      this.requiresVerification = false;

      try {
        const res = await axios.post(
          `${API_URL}/api/auth/login`,
          {
            email: this.email,
            password: this.password
          }
        );

        // ✅ Login successful
        localStorage.setItem("token", res.data.access_token);
        localStorage.setItem("role", res.data.role);

        if (res.data.role === "student") {
          this.$router.push("/student/dashboard");
        } else if (res.data.role === "company") {
          this.$router.push("/company/dashboard");
        } else if (res.data.role === "admin") {
          this.$router.push("/admin/dashboard");
        }

      } catch (err) {
        // ✅ NEW: Check if email verification is required
        if (err.response?.status === 403 && err.response?.data?.requires_verification) {
          this.requiresVerification = true;
          this.unverifiedEmail = this.email;
          this.error = null;
        } else {
          this.error = err.response?.data?.msg || "Login failed. Try again.";
        }
      } finally {
        this.loading = false;
      }
    },

    // ✅ NEW: Resend verification email
    async resendVerification() {
      this.resendLoading = true;

      try {
        await axios.post(
          `${API_URL}/api/auth/resend-verification`,
          { email: this.unverifiedEmail }
        );

        alert("✅ Verification email sent! Check your inbox.");

      } catch (err) {
        alert("❌ Failed to resend email. Please try again.");
      } finally {
        this.resendLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  width: 100%;
  max-width: 420px;
  border-radius: 25px;
  animation: slideIn 0.5s ease;
}

.brand-text {
  font-size: 2.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 0.5rem;
}

.form-control:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 0.2rem rgba(118, 75, 162, 0.25);
}

.form-control.rounded-pill {
  padding: 0.6rem 1.2rem;
}

.input-group .form-control.rounded-start-pill {
  padding: 0.6rem 1.2rem;
}

.input-group .btn.rounded-end-pill {
  padding: 0.6rem 1.2rem;
}

.btn-success {
  background: linear-gradient(135deg, #667eec 0%, #7a4da6 100%);
  border: none;
  transition: all 0.3s ease;
  padding: 0.7rem 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.btn-success:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b3fa0 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-success:active {
  transform: translateY(0);
}

.btn-success:disabled {
  background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
  border: none;
}

.input-group .btn-outline-secondary {
  transition: all 0.3s ease;
  background-color: white;
}

.input-group .btn-outline-secondary:hover {
  background-color: #f8f9fa;
  color: #7a4da6;
  border-color: #7a4da6;
}

/* ✅ NEW: Email Verification Alert Styles */
.alert-warning {
  background-color: #fffbeb !important;
  border: 1px solid #fcd34d !important;
  color: #78350f !important;
  border-radius: 1rem !important;
}

.alert-warning strong {
  color: #92400e;
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border: none;
  color: white;
  font-weight: 500;
}

.btn-warning:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.btn-warning:disabled {
  background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
  opacity: 0.7;
}

/* Register Options Styling */
.register-options {
  border-top: 1px solid #e0e0e0;
  padding-top: 1.2rem;
}

.btn-outline-register {
  background: white;
  border: 2px solid;
  transition: all 0.3s ease;
  padding: 0.6rem 0.8rem;
  font-weight: 500;
  font-size: 0.95rem;
}

.student-btn {
  border-color: #667eea;
  color: #667eea;
}

.student-btn:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

.company-btn {
  border-color: #7a4da6;
  color: #7a4da6;
}

.company-btn:hover {
  background: linear-gradient(135deg, #7a4da6 0%, #667eea 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(122, 77, 166, 0.3);
}

.btn-outline-register:active {
  transform: translateY(0);
}

.d-flex {
  display: flex;
}

.gap-2 {
  gap: 0.5rem;
}

.flex-fill {
  flex: 1;
}

/* Text colors */
.text-success {
  color: #7a4da6 !important;
}

.text-success:hover {
  color: #667eec !important;
  text-decoration: underline !important;
}

.alert.rounded-pill {
  border-radius: 50px !important;
  padding-left: 1.2rem !important;
  padding-right: 1.2rem !important;
}

.alert-danger {
  border-radius: 50px !important;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Responsive adjustments */
@media (max-width: 480px) {
  .login-card {
    border-radius: 20px;
    margin: 1rem;
  }
  
  .brand-text {
    font-size: 2rem;
  }

  .btn-outline-register {
    font-size: 0.85rem;
    padding: 0.5rem 0.5rem;
  }

  .btn-outline-register i {
    margin-right: 0.3rem;
  }
}
</style>