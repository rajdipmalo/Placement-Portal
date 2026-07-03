<template>
  <div class="company-profile">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Company Profile</h1>
      <p class="text-muted">Manage your company information</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading profile...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchProfile">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Profile Content -->
    <div v-else class="profile-content">
      <!-- Profile Header Card -->
      <div class="card profile-header-card border-0 mb-4">
        <div class="card-body">
          <div class="d-flex align-items-center gap-4 flex-wrap">
            <div class="company-logo rounded-circle d-flex align-items-center justify-content-center flex-shrink-0"
                 :style="{ background: companyColor }">
              {{ getInitials(profile.name) }}
            </div>
            <div class="flex-grow-1" style="min-width: 200px;">
              <h4 class="text-dark mb-1">{{ profile.name || 'Company Name' }}</h4>
              <p class="text-secondary mb-2">
                <span class="badge" :class="getApprovalBadgeClass(profile.approval_status)">
                  {{ profile.approval_status }}
                </span>
              </p>
              <p class="text-secondary small mb-0">
                <i class="bi bi-calendar me-2"></i>Member since {{ formatDate(profile.created_at) }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Form -->
      <div class="card profile-form-card border-0">
        <div class="card-body">
          <form @submit.prevent="updateProfile">
            <!-- Basic Information -->
            <h5 class="text-dark mb-3">Basic Information</h5>
            
            <div class="form-grid">
              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-building text-primary me-2"></i>Company Name <span class="text-danger">*</span>
                </label>
                <input 
                  type="text" 
                  v-model="form.name" 
                  class="form-control rounded-pill" 
                  :class="{ 'is-invalid': errors.name }"
                  required
                >
                <div class="invalid-feedback">{{ errors.name }}</div>
              </div>

              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-envelope text-primary me-2"></i>Email
                </label>
                <input 
                  type="email" 
                  :value="profile.email" 
                  disabled 
                  class="form-control rounded-pill bg-light text-secondary"
                >
                <small class="text-secondary d-block mt-1">Email cannot be changed</small>
              </div>

              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-diagram-3 text-primary me-2"></i>Industry
                </label>
                <input 
                  type="text" 
                  v-model="form.industry" 
                  class="form-control rounded-pill" 
                  placeholder="e.g., Information Technology"
                >
              </div>

              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-geo-alt text-primary me-2"></i>Location
                </label>
                <input 
                  type="text" 
                  v-model="form.location" 
                  class="form-control rounded-pill" 
                  placeholder="e.g., Bangalore, India"
                >
              </div>

              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-link-45deg text-primary me-2"></i>Website
                </label>
                <input 
                  type="url" 
                  v-model="form.website" 
                  class="form-control rounded-pill" 
                  placeholder="https://www.company.com"
                >
              </div>

              <!-- Contact Information -->
              <div class="col-12 mt-4">
                <h5 class="text-dark mb-3">Contact Information</h5>
              </div>

              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-envelope text-primary me-2"></i>HR Email
                </label>
                <input 
                  type="email" 
                  v-model="form.hr_email" 
                  class="form-control rounded-pill" 
                  placeholder="hr@company.com"
                >
              </div>

              <div class="form-group">
                <label class="form-label text-dark">
                  <i class="bi bi-phone text-primary me-2"></i>HR Contact
                </label>
                <input 
                  type="tel" 
                  v-model="form.hr_contact" 
                  class="form-control rounded-pill" 
                  placeholder="+91 98765 43210"
                >
              </div>
            </div>

            <!-- Form Actions -->
            <hr class="my-4">
            <div class="action-buttons">
              <button type="button" class="btn btn-outline-custom" @click="resetForm" :disabled="saving">
                <i class="bi bi-arrow-counterclockwise me-2"></i>Reset
              </button>
              <button type="submit" class="btn btn-primary-custom" :disabled="saving">
                <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="bi bi-check-circle me-2"></i>
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>

            <!-- Save Status -->
            <div v-if="saveMessage" class="mt-3">
              <div class="alert rounded-pill" :class="saveStatusClass">
                <i :class="saveStatusIcon" class="me-2"></i>
                {{ saveMessage }}
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'CompanyProfile',

  emits: ['update-company-name', 'token-expired'],

  data() {
    return {
      loading: false,
      saving: false,
      error: null,
      profile: {
        name: '',
        email: '',
        industry: '',
        location: '',
        website: '',
        hr_email: '',
        hr_contact: '',
        approval_status: 'pending',
        created_at: null
      },
      form: {
        name: '',
        industry: '',
        location: '',
        website: '',
        hr_email: '',
        hr_contact: ''
      },
      errors: {},
      originalForm: null,
      saveMessage: '',
      saveStatus: 'success'
    };
  },

  computed: {
    companyColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.profile.name) return colors[0];
      const hash = this.profile.name.split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
      }, 0);
      return colors[Math.abs(hash) % colors.length];
    },

    saveStatusClass() {
      return this.saveStatus === 'success' ? 'alert-success' : 'alert-danger';
    },

    saveStatusIcon() {
      return this.saveStatus === 'success' ? 'bi bi-check-circle' : 'bi bi-exclamation-circle';
    }
  },

  mounted() {
    this.fetchProfile();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchProfile() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/profile",
          this.getAuthHeader()
        );

        this.profile = res.data;
        this.form = {
          name: res.data.name || '',
          industry: res.data.industry || '',
          location: res.data.location || '',
          website: res.data.website || '',
          hr_email: res.data.hr_email || '',
          hr_contact: res.data.hr_contact || ''
        };
        
        this.originalForm = { ...this.form };
        this.$emit('update-company-name', res.data.name);

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load profile";
      } finally {
        this.loading = false;
      }
    },

    async updateProfile() {
      if (!this.validateForm()) {
        this.showSaveMessage('Please fill in required fields', 'error');
        return;
      }

      this.saving = true;
      this.saveMessage = '';

      try {
        await axios.put(
          "http://127.0.0.1:5000/api/company/profile",
          this.form,
          this.getAuthHeader()
        );

        this.originalForm = { ...this.form };
        this.$emit('update-company-name', this.form.name);
        this.showSaveMessage('Profile updated successfully!', 'success');

      } catch (err) {
        this.showSaveMessage(err.response?.data?.msg || "Update failed", 'error');
      } finally {
        this.saving = false;
      }
    },

    validateForm() {
      this.errors = {};
      
      if (!this.form.name?.trim()) {
        this.errors.name = 'Company name is required';
      }
      
      return Object.keys(this.errors).length === 0;
    },

    resetForm() {
      if (this.originalForm) {
        this.form = { ...this.originalForm };
        this.errors = {};
        this.showSaveMessage('Form reset to last saved state', 'success');
      }
    },

    showSaveMessage(message, status) {
      this.saveMessage = message;
      this.saveStatus = status;
      setTimeout(() => {
        this.saveMessage = '';
      }, 3000);
    },

    getInitials(name) {
      if (!name) return 'C';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },

    getApprovalBadgeClass(status) {
      const classes = {
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'rejected': 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.company-profile {
  color: #333;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  box-sizing: border-box;
  padding: 0 0.5rem;
}

.profile-content {
  width: 100%;
  max-width: 100%;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Profile Header Card */
.profile-header-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  width: 100%;
}

.profile-header-card .d-flex {
  flex-wrap: wrap;
  gap: 1rem;
}

.company-logo {
  width: 80px;
  height: 80px;
  font-size: 32px;
  font-weight: 600;
  color: white;
}

/* Profile Form Card */
.profile-form-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  width: 100%;
}

/* CSS Grid Layout for form - replaces Bootstrap grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group {
  width: 100%;
  min-width: 0; /* Prevents grid items from overflowing */
}

.form-group.col-12 {
  grid-column: span 2;
}

/* Form Controls */
.form-control, .form-select {
  border: 2px solid #e0e0e0;
  padding: 0.6rem 1.2rem;
  transition: all 0.3s ease;
  width: 100%;
  box-sizing: border-box;
}

.form-control:focus, .form-select:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 0.2rem rgba(118, 75, 162, 0.25);
}

.form-control.rounded-pill, .form-select.rounded-pill {
  padding: 0.6rem 1.2rem;
}

.form-control.is-invalid {
  border-color: #ef4444;
}

.invalid-feedback {
  color: #ef4444;
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

/* Button Styles */
.btn-primary-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-primary-custom:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-outline-custom {
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-outline-custom:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Action Buttons Container */
.action-buttons {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

/* Badge Styles */
.badge.bg-success {
  background: #10b981 !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

.badge.bg-warning {
  background: #f59e0b !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

.badge.bg-danger {
  background: #ef4444 !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

/* Alerts */
.alert {
  padding: 1rem 1.5rem;
  border-radius: 50px;
  margin-top: 1rem;
}

.alert-success {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.alert-danger {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

/* Divider */
hr {
  border: none;
  border-top: 2px solid #e0e0e0;
  opacity: 0.5;
  margin: 1.5rem 0;
}

/* Responsive */
@media (max-width: 768px) {
  .company-profile {
    padding: 0.25rem;
  }

  .form-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .form-group.col-12 {
    grid-column: span 1;
  }

  .profile-header-card .d-flex {
    flex-direction: column;
    text-align: center;
    align-items: center;
  }
  
  .company-logo {
    margin-bottom: 0.5rem;
  }

  .action-buttons {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .btn-primary-custom, 
  .btn-outline-custom {
    width: 100%;
  }
}
</style>