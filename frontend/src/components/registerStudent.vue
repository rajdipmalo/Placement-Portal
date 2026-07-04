<template>
  <div class="register-page d-flex align-items-center justify-content-center">
    <div class="card shadow-lg border-0 register-card p-4">

      <!-- REGISTRATION FORM (shown when not verificationSent) -->
      <div v-if="!verificationSent">

        <div class="text-center mb-4">
          <h3 class="fw-bold brand-text">NextGig</h3>
          <h2 class="h4 fw-semibold mt-2">Student Registration</h2>
          <p class="text-muted">Create your placement portal account</p>
        </div>

        <form @submit.prevent="registerStudent">
          <div class="row">

            <!-- LEFT COLUMN -->
            <div class="col-md-6">

              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input
                  type="text"
                  class="form-control rounded-pill"
                  placeholder="Enter your full name"
                  v-model="form.full_name"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input
                  type="email"
                  class="form-control rounded-pill"
                  placeholder="Enter your email"
                  v-model="form.email"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Branch</label>
                <select 
                  class="form-select rounded-pill" 
                  v-model="form.branch" 
                  required
                >
                  <option value="" disabled selected>Select your branch</option>
                  <option v-for="branch in branches" :key="branch" :value="branch">
                    {{ branch }}
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">Skills</label>
                <div class="input-group mb-2">
                  <input 
                    type="text" 
                    v-model="newSkill" 
                    @keydown.enter.prevent="addSkill"
                    class="form-control rounded-start-pill border-end-0"
                    placeholder="Type a skill and press Enter"
                  >
                  <button 
                    class="btn btn-primary-custom rounded-end-pill" 
                    type="button" 
                    @click="addSkill"
                  >
                    <i class="bi bi-plus"></i> Add
                  </button>
                </div>
                <div class="d-flex gap-2 flex-wrap">
                  <span 
                    v-for="(skill, index) in skillArray" 
                    :key="index"
                    class="badge bg-primary d-inline-flex align-items-center p-2 rounded-pill"
                  >
                    {{ skill }}
                    <i class="bi bi-x ms-2" @click="removeSkill(index)" style="cursor: pointer;"></i>
                  </span>
                  <span v-if="skillArray.length === 0" class="text-secondary">No skills added yet</span>
                </div>
              </div>

            </div>

            <!-- RIGHT COLUMN -->
            <div class="col-md-6">

              <div class="mb-3">
                <label class="form-label">Year</label>
                <select 
                  class="form-select rounded-pill" 
                  v-model="form.year" 
                  required
                >
                  <option value="" disabled selected>Select your year</option>
                  <option v-for="year in [1,2,3,4]" :key="year" :value="year">
                    {{ year }}{{ year === 1 ? 'st' : year === 2 ? 'nd' : year === 3 ? 'rd' : 'th' }} Year
                  </option>
                </select>
              </div>

              <div class="mb-3">
                <label class="form-label">CGPA</label>
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  max="10"
                  class="form-control rounded-pill"
                  placeholder="Enter your CGPA"
                  v-model.number="form.cgpa"
                  required
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Resume URL</label>
                <input
                  type="url"
                  class="form-control rounded-pill"
                  placeholder="Google Drive / Dropbox link"
                  v-model="form.resume_url"
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <div class="input-group">
                  <input
                    :type="showPassword ? 'text' : 'password'"
                    class="form-control rounded-start-pill border-end-0"
                    placeholder="Enter your password (min 6 characters)"
                    v-model="form.password"
                    minlength="6"
                    required
                  />
                  <button
                    type="button"
                    class="btn btn-outline-secondary rounded-end-pill border-start-0"
                    @click="showPassword = !showPassword"
                  >
                    <i :class="showPassword ? 'bi bi-eye-slash' : 'bi bi-eye'"></i>
                  </button>
                </div>
              </div>

            </div>
          </div>

          <!-- Error Alert -->
          <div v-if="error" class="alert alert-danger py-2 rounded-pill mt-3" role="alert">
            <i class="bi bi-exclamation-triangle-fill me-2"></i>
            {{ error }}
          </div>

          <!-- Register Button -->
          <button
            type="submit"
            class="btn btn-success w-100 mt-3 rounded-pill"
            :disabled="loading"
          >
            <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
            <span v-if="loading">Registering...</span>
            <span v-else><i class="bi bi-person-plus me-2"></i>Register</span>
          </button>

        </form>

        <div class="text-center mt-4">
          <small class="text-muted">
            Already registered?
            <router-link to="/login" class="text-success text-decoration-none">
              Login <i class="bi bi-arrow-right"></i>
            </router-link>
          </small>
        </div>

      </div>


      <div v-else class="text-center">
        <div class="mb-4">
          <div class="verification-icon mb-3">
            <i class="bi bi-envelope-check"></i>
          </div>
          <h3 class="fw-bold mb-2">Verification Email Sent!</h3>
          <p class="text-muted mb-3">
            We've sent a verification link to <strong>{{ registeredEmail }}</strong>
          </p>
        </div>

        <div class="alert alert-info rounded-4 p-3 mb-4" role="alert">
          <i class="bi bi-info-circle me-2"></i>
          <small>
            Click the link in the email to verify your account. The link expires in 24 hours.
          </small>
        </div>


        <div class="d-grid gap-2">
          <button 
            type="button"
            class="btn btn-success rounded-pill"
            @click="resendVerification"
            :disabled="resendLoading"
          >
            <span v-if="resendLoading" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-arrow-repeat me-2"></i>
            {{ resendLoading ? 'Sending...' : 'Resend Verification Email' }}
          </button>

          <router-link to="/login" class="btn btn-outline-secondary rounded-pill">
            <i class="bi bi-arrow-left me-2"></i>Back to Login
          </router-link>
        </div>

        <hr class="my-4">

        <p class="text-muted small">
          <i class="bi bi-lock me-1"></i>
          Your account is secure and will be activated once you verify your email.
        </p>
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
      showPassword: false,
      loading: false,
      resendLoading: false,
      error: null,
      newSkill: '',
      verificationSent: false,
      registeredEmail: '',
      branches: ['CSE',
        'IT',
        'ECE',
        'EEE',
        'EE',
        'MECH',
        'CIVIL',
        'CHEMICAL',
        'BIOTECH',
        'AIML',
        'DATA SCIENCE',
        'METALLURGY',
        'ENGINEERING PHYSICS',
        'ENGINEERING MATHEMATICS',
        'PRODUCTION ENGINEERING',
        'INDUSTRIAL ENGINEERING',
        'AEROSPACE ENGINEERING',
        'AGRICULTURAL ENGINEERING',
        'ENVIRONMENTAL ENGINEERING',
        'MATERIALS SCIENCE',
        'MINING ENGINEERING',
        'OCEAN ENGINEERING',
        'NAVAL ARCHITECTURE',
        'TEXTILE ENGINEERING',
        'INSTRUMENTATION ENGINEERING'
      ],
      form: {
        email: "",
        password: "",
        full_name: "",
        branch: "",
        year: "",
        cgpa: "",
        skills: [],
        resume_url: ""
      }
    };
  },

  computed: {
    skillArray: {
      get() {
        return Array.isArray(this.form.skills) ? this.form.skills : [];
      },
      set(value) {
        this.form.skills = value;
      }
    }
  },

  methods: {
    addSkill() {
      if (this.newSkill.trim()) {
        const skills = [...this.skillArray];
        if (!skills.includes(this.newSkill.trim())) {
          skills.push(this.newSkill.trim());
          this.skillArray = skills;
        }
        this.newSkill = '';
      }
    },

    removeSkill(index) {
      const skills = [...this.skillArray];
      skills.splice(index, 1);
      this.skillArray = skills;
    },

    async registerStudent() {
      this.loading = true;
      this.error = null;

      try {
        const payload = {
          email: this.form.email,
          password: this.form.password,
          full_name: this.form.full_name,
          branch: this.form.branch,
          year: Number(this.form.year),
          cgpa: Number(this.form.cgpa),
          resume_url: this.form.resume_url || null,
          skills: this.skillArray
        };

        const response = await axios.post(
          `${API_URL}/api/auth/register/student`,
          payload
        );

        // ✅ Show verification sent message
        this.verificationSent = true;
        this.registeredEmail = this.form.email;

      } catch (err) {
        this.error = err.response?.data?.msg || "Registration failed. Please try again.";
      } finally {
        this.loading = false;
      }
    },

    async resendVerification() {
      this.resendLoading = true;
      this.error = null;

      try {
        await axios.post(
          `${API_URL}/api/auth/resend-verification`,
          { email: this.registeredEmail }
        );

        alert("✅ Verification email sent! Check your inbox.");

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to resend email. Please try again.";
      } finally {
        this.resendLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 1rem;
}

.register-card {
  width: 100%;
  max-width: 800px;
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

.verification-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  animation: scaleIn 0.5s ease;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
}

.form-control:focus,
.form-select:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 0.2rem rgba(118, 75, 162, 0.25);
}

.form-control.rounded-pill,
.form-select.rounded-pill {
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

.btn-outline-secondary {
  border-color: #7a4da6;
  color: #7a4da6;
}

.btn-outline-secondary:hover {
  background-color: #7a4da6;
  border-color: #7a4da6;
}

.btn-primary-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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

.alert.rounded-4 {
  border-radius: 1rem !important;
  background-color: #e7f3ff;
  border: 1px solid #b3d9ff;
  color: #004085;
}

.form-label {
  font-weight: 500;
  color: #555;
  margin-bottom: 0.3rem;
}

.h4 {
  color: #333;
  margin-bottom: 0.5rem;
}

.badge.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
}

.badge i {
  font-size: 0.8rem;
  transition: all 0.2s ease;
}

.badge i:hover {
  color: #ff4444;
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

@media (max-width: 768px) {
  .register-card {
    border-radius: 20px;
    padding: 1.5rem !important;
  }
  
  .brand-text {
    font-size: 2rem;
  }
  
  .h4 {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .register-card {
    margin: 0.5rem;
    padding: 1rem !important;
  }
  
  .row {
    margin: 0;
  }
  
  .col-md-6 {
    padding: 0;
  }
}
</style>