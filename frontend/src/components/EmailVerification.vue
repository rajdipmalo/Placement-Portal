<template>
  <div class="verify-page d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 verify-card p-4">

      <!-- LOADING STATE -->
      <div v-if="loading" class="text-center">
        <div class="spinner-border mb-3" role="status">
          <span class="visually-hidden">Verifying...</span>
        </div>
        <h4>Verifying your email...</h4>
        <p class="text-muted">Please wait while we confirm your email address.</p>
      </div>

      <!-- SUCCESS STATE -->
      <div v-else-if="success" class="text-center">
        <div class="success-icon mb-3">
          <i class="bi bi-check-circle"></i>
        </div>
        <h3 class="fw-bold mb-2">Email Verified! ✅</h3>
        <p class="text-muted mb-4">
          Your email has been verified successfully.
        </p>

        <!-- Auto-redirect countdown -->
        <div class="alert alert-success rounded-4 p-3 mb-4" role="alert">
          <i class="bi bi-check-circle me-2"></i>
          <small>
            <strong v-if="redirectCountdown > 0">Redirecting to login in {{ redirectCountdown }} seconds...</strong>
            <strong v-else>Redirecting now...</strong>
          </small>
        </div>

        <div class="d-grid gap-2">
          <button @click="goToLogin" class="btn btn-success rounded-pill">
            <i class="bi bi-door-open me-2"></i>Go to Login Now
          </button>
          <router-link to="/" class="btn btn-outline-secondary rounded-pill">
            <i class="bi bi-house me-2"></i>Back to Home
          </router-link>
        </div>

        <p class="text-muted small mt-4">
          <i class="bi bi-info-circle me-1"></i>
          <span v-if="userRole === 'student'">Your account is ready to use. You can login now.</span>
          <span v-else-if="userRole === 'company'">Your account is pending admin approval. You can login after approval.</span>
          <span v-else>Your account has been verified.</span>
        </p>
      </div>

      <!-- ERROR STATE -->
      <div v-else class="text-center">
        <div class="error-icon mb-3">
          <i class="bi bi-exclamation-circle"></i>
        </div>
        <h3 class="fw-bold mb-2">Verification Failed</h3>
        <p class="text-muted mb-4">
          {{ error }}
        </p>

        <div class="alert alert-warning rounded-4 p-3 mb-4" role="alert">
          <i class="bi bi-info-circle me-2"></i>
          <small>
            The link may have expired or is invalid. Please request a new verification email.
          </small>
        </div>

        <div class="d-grid gap-2">
          <router-link to="/register/student" class="btn btn-warning rounded-pill">
            <i class="bi bi-arrow-repeat me-2"></i>Resend Verification
          </router-link>
          <router-link to="/login" class="btn btn-primary rounded-pill">
            <i class="bi bi-door-open me-2"></i>Go to Login
          </router-link>
          <router-link to="/" class="btn btn-outline-secondary rounded-pill">
            <i class="bi bi-house me-2"></i>Back to Home
          </router-link>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL } from "@/config";

export default {
  data() {
    return {
      loading: true,
      success: false,
      error: null,
      userRole: null,
      redirectCountdown: 5,
      redirectTimer: null
    };
  },

  mounted() {
    this.verifyEmail();
  },

  beforeUnmount() {
    // Clear timer if component is destroyed
    if (this.redirectTimer) {
      clearTimeout(this.redirectTimer);
    }
  },

  methods: {
    async verifyEmail() {
      const token = this.$route.params.token;

      if (!token) {
        this.loading = false;
        this.error = "No verification token provided. The link may be invalid.";
        return;
      }

      try {
        const response = await axios.get(
          `${API_URL}/api/auth/verify-email/${token}`
        );

        // ✅ Email verified successfully
        this.loading = false;
        this.success = true;

        // Get user role from response if available
        if (response.data.role) {
          this.userRole = response.data.role;
        }

        // ✅ Start countdown and redirect
        this.startCountdownAndRedirect();

      } catch (err) {
        this.loading = false;
        this.success = false;
        
        // Display error message from backend
        if (err.response?.data?.msg) {
          this.error = err.response.data.msg;
        } else if (err.response?.status === 400) {
          this.error = "Invalid or expired verification link. Please request a new one.";
        } else if (err.code === 'ECONNABORTED') {
          this.error = "Connection timeout. The server may be offline.";
        } else {
          this.error = "Something went wrong. Please try again.";
        }
      }
    },

    // ✅ FIXED: Improved countdown and redirect
    startCountdownAndRedirect() {
      // Start countdown
      const countdownInterval = setInterval(() => {
        this.redirectCountdown -= 1;

        if (this.redirectCountdown <= 0) {
          clearInterval(countdownInterval);
          // Redirect to login
          this.redirectToLogin();
        }
      }, 1000);

      // Store reference
      this.redirectTimer = countdownInterval;

      // Fallback: Force redirect after 6 seconds (in case interval fails)
      const fallbackTimeout = setTimeout(() => {
        clearInterval(countdownInterval);
        this.redirectToLogin();
      }, 6000);
    },

    // ✅ Direct redirect method
    redirectToLogin() {
      console.log("🔄 Redirecting to /login");
      this.$router.push("/login").catch(err => {
        console.error("Router error:", err);
        // Fallback: use window.location
        window.location.href = "/login";
      });
    },

    // ✅ Manual button click redirect
    goToLogin() {
      console.log("👆 User clicked 'Go to Login Now'");
      this.redirectToLogin();
    }
  }
};
</script>

<style scoped>
.verify-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.verify-card {
  width: 100%;
  max-width: 500px;
  border-radius: 25px;
  animation: slideIn 0.5s ease;
}

/* Success Icon */
.success-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto;
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  animation: successPulse 0.6s ease;
}

@keyframes successPulse {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Error Icon */
.error-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto;
  background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-10px);
  }
  75% {
    transform: translateX(10px);
  }
}

/* Spinner color */
.spinner-border {
  border-color: rgba(102, 126, 234, 0.25);
  border-right-color: #667eea;
}

.btn-success {
  background: linear-gradient(135deg, #667eec 0%, #7a4da6 100%);
  border: none;
  transition: all 0.3s ease;
  padding: 0.7rem 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
  color: white;
  cursor: pointer;
}

.btn-success:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b3fa0 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  color: white;
}

.btn-success:active {
  transform: translateY(0);
}

.btn-primary {
  background: linear-gradient(135deg, #667eec 0%, #7a4da6 100%);
  border: none;
  color: white;
}

.btn-primary:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b3fa0 100%);
  color: white;
}

.btn-outline-secondary {
  border-color: #667eea;
  color: #667eea;
}

.btn-outline-secondary:hover {
  background-color: #667eea;
  border-color: #667eea;
  color: white;
}

.btn-warning {
  background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  border: none;
  color: white;
}

.btn-warning:hover {
  background: linear-gradient(135deg, #d97706 0%, #b45309 100%);
  color: white;
}

.alert {
  border-radius: 1rem !important;
}

.alert-success {
  background-color: #d1fae5;
  border: 1px solid #6ee7b7;
  color: #065f46;
}

.alert-warning {
  background-color: #fef3c7;
  border: 1px solid #fcd34d;
  color: #78350f;
}

h3, h4 {
  color: #333;
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

@media (max-width: 600px) {
  .verify-card {
    border-radius: 20px;
    padding: 1.5rem !important;
  }
  
  .success-icon,
  .error-icon {
    width: 80px;
    height: 80px;
    font-size: 2.5rem;
  }
}
</style>