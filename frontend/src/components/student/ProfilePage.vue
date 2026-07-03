<template>
  <div class="profile-page">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">My Profile</h1>
      <p class="text-muted">Manage your personal information and preferences</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading your profile...</p>
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
    <div v-else>
      <!-- Profile Header Card (Simplified - No Avatar Upload) -->
      <div class="card profile-header-card border-0 mb-4">
        <div class="card-body">
          <div class="d-flex align-items-center gap-4">
            <div class="avatar rounded-circle d-flex align-items-center justify-content-center"
                 :style="{ background: avatarColor }">
              {{ getInitials(form.full_name) }}
            </div>
            <div>
              <h4 class="text-dark mb-1">{{ form.full_name || 'Your Name' }}</h4>
              <p class="text-secondary mb-0">{{ form.email || 'Email not available' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Profile Tabs -->
      <ul class="nav nav-tabs border-0 mb-4">
        <li class="nav-item" v-for="tab in tabs" :key="tab.id">
          <a class="nav-link" :class="{ active: activeTab === tab.id }" 
             @click="activeTab = tab.id" href="#">
            <i :class="tab.icon" class="me-2"></i>{{ tab.label }}
          </a>
        </li>
      </ul>

      <!-- Tab Content -->
      <div class="card profile-content-card border-0">
        <div class="card-body">
          <form @submit.prevent="updateProfile">
            <!-- Personal Info Tab -->
            <div v-show="activeTab === 'personal'">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-dark">
                    <i class="bi bi-person text-primary me-2"></i>Full Name <span class="text-danger">*</span>
                  </label>
                  <input type="text" v-model="form.full_name"
                         :class="['form-control rounded-pill', { 'is-invalid': errors.full_name }]"
                         @blur="validateField('full_name')"
                         placeholder="Enter your full name">
                  <div class="invalid-feedback">{{ errors.full_name }}</div>
                </div>

                <div class="col-md-6">
                  <label class="form-label text-dark">
                    <i class="bi bi-envelope text-primary me-2"></i>Email
                  </label>
                  <input type="email" :value="form.email" disabled
                         class="form-control rounded-pill bg-light text-secondary">
                  <small class="text-secondary">Email cannot be changed</small>
                </div>

                <div class="col-12">
                  <label class="form-label text-dark">
                    <i class="bi bi-code-square text-primary me-2"></i>Skills
                  </label>
                  <div class="input-group mb-2">
                    <input type="text" v-model="newSkill" @keydown.enter.prevent="addSkill"
                           class="form-control rounded-start-pill border-end-0"
                           placeholder="Type a skill and press Enter">
                    <button class="btn btn-primary-custom rounded-end-pill" type="button" @click="addSkill">
                      <i class="bi bi-plus"></i> Add
                    </button>
                  </div>
                  <div class="d-flex gap-2 flex-wrap">
                    <span v-for="(skill, index) in skillArray" :key="index"
                          class="badge bg-primary d-inline-flex align-items-center p-2 rounded-pill">
                      {{ skill }}
                      <i class="bi bi-x ms-2" @click="removeSkill(index)" style="cursor: pointer;"></i>
                    </span>
                    <span v-if="skillArray.length === 0" class="text-secondary">No skills added yet</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Education Tab -->
            <div v-show="activeTab === 'education'">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-dark">
                    <i class="bi bi-diagram-3 text-primary me-2"></i>Branch <span class="text-danger">*</span>
                  </label>
                  <select v-model="form.branch" :class="['form-select rounded-pill', { 'is-invalid': errors.branch }]"
                          @blur="validateField('branch')">
                    <option value="">Select branch</option>
                    <option v-for="branch in branches" :key="branch" :value="branch">
                      {{ branch }}
                    </option>
                  </select>
                  <div class="invalid-feedback">{{ errors.branch }}</div>
                </div>

                <div class="col-md-6">
                  <label class="form-label text-dark">
                    <i class="bi bi-calendar text-primary me-2"></i>Year <span class="text-danger">*</span>
                  </label>
                  <select v-model="form.year" :class="['form-select rounded-pill', { 'is-invalid': errors.year }]"
                          @blur="validateField('year')">
                    <option value="">Select year</option>
                    <option v-for="year in [1,2,3,4]" :key="year" :value="year">
                      {{ year }}{{ year === 1 ? 'st' : year === 2 ? 'nd' : year === 3 ? 'rd' : 'th' }} Year
                    </option>
                  </select>
                  <div class="invalid-feedback">{{ errors.year }}</div>
                </div>

                <div class="col-md-6">
                  <label class="form-label text-dark">
                    <i class="bi bi-star text-primary me-2"></i>CGPA <span class="text-danger">*</span>
                  </label>
                  <input type="number" step="0.01" min="0" max="10" v-model.number="form.cgpa"
                         :class="['form-control rounded-pill', { 'is-invalid': errors.cgpa }]"
                         @blur="validateField('cgpa')"
                         placeholder="Enter your CGPA">
                  <div class="invalid-feedback">{{ errors.cgpa }}</div>
                </div>

                <div class="col-md-6">
                  <label class="form-label text-dark">
                    <i class="bi bi-file-text text-primary me-2"></i>Resume URL
                  </label>
                  <input type="url" v-model="form.resume_url"
                         class="form-control rounded-pill"
                         placeholder="https://example.com/resume.pdf">
                  <small class="text-secondary">Link to your resume (Google Drive, Dropbox, etc.)</small>
                </div>
              </div>
            </div>

            <!-- Form Actions -->
            <div class="d-flex gap-2 justify-content-end mt-4 pt-3 border-top">
              <button type="button" class="btn btn-outline-custom" @click="resetForm" :disabled="saving">
                <i class="bi bi-arrow-counterclockwise me-2"></i>Reset
              </button>
              <button type="submit" class="btn btn-primary-custom" :disabled="saving || !isFormValid">
                <i :class="saving ? 'bi bi-hourglass-split' : 'bi bi-check-circle'" class="me-2"></i>
                {{ saving ? 'Saving...' : 'Save Changes' }}
              </button>
            </div>

            <!-- Save Status -->
            <div v-if="saveMessage" class="alert mt-3 rounded-pill" :class="saveStatusClass">
              <i :class="saveStatusIcon" class="me-2"></i>
              {{ saveMessage }}
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
  name: 'ProfilePage',

  emits: ['update-user-name'],

  data() {
    return {
      loading: false,
      saving: false,
      error: null,
      activeTab: 'personal',
      newSkill: '',
      saveMessage: '',
      saveStatus: 'success',
      form: {
        full_name: "",
        email: "",
        branch: "",
        year: null,
        cgpa: null,
        skills: [],
        resume_url: ""
      },
      errors: {},
      branches: [
      'CSE',
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
      originalForm: null,
      tabs: [
        { id: 'personal', label: 'Personal Info', icon: 'bi bi-person' },
        { id: 'education', label: 'Education', icon: 'bi bi-book' }
      ]
    };
  },

  computed: {
    avatarColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.form.full_name) return colors[0];
      const hash = this.form.full_name.split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
      }, 0);
      return colors[Math.abs(hash) % colors.length];
    },

    skillArray: {
      get() {
        return Array.isArray(this.form.skills) ? this.form.skills : [];
      },
      set(value) {
        this.form.skills = value;
      }
    },

    isFormValid() {
      return !this.errors.full_name && !this.errors.branch && 
             !this.errors.year && !this.errors.cgpa;
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
        "http://127.0.0.1:5000/api/student/profile",
        this.getAuthHeader()
      );

      // Parse skills string into array
      const skillsArray = res.data.skills 
        ? res.data.skills.split(',').map(s => s.trim()).filter(s => s)
        : [];

      this.form = {
        full_name: res.data.full_name || "",
        email: res.data.email || "",
        branch: res.data.branch || "",
        year: res.data.year || null,
        cgpa: res.data.cgpa || null,
        skills: skillsArray, // Store as array in frontend
        resume_url: res.data.resume_url || ""
      };

      this.originalForm = JSON.parse(JSON.stringify(this.form));
      this.$emit('update-user-name', this.form.full_name);

    } catch (err) {
      this.error = err.response?.data?.msg || "Failed to load profile";
      console.error('Profile fetch error:', err);
    } finally {
      this.loading = false;
    }
  },

  async updateProfile() {
    if (!this.validateForm()) {
      this.showSaveMessage('Please fix the errors before saving', 'error');
      return;
    }

    this.saving = true;
    this.saveMessage = '';

    try {
      // Convert skills array to comma-separated string for backend
      const skillsString = this.skillArray.length > 0 
        ? this.skillArray.join(', ') 
        : '';

      const payload = {
        full_name: this.form.full_name,
        branch: this.form.branch,
        year: this.form.year ? Number(this.form.year) : null,
        cgpa: this.form.cgpa ? Number(this.form.cgpa) : null,
        skills: skillsString, // Send as string, not array
        resume_url: this.form.resume_url || null
      };

      console.log('Sending payload:', payload); // For debugging

      await axios.put(
        "http://127.0.0.1:5000/api/student/profile",
        payload,
        this.getAuthHeader()
      );

      this.originalForm = JSON.parse(JSON.stringify(this.form));
      this.$emit('update-user-name', this.form.full_name);
      this.showSaveMessage('Profile updated successfully!', 'success');

    } catch (err) {
      console.error('Profile update error:', err.response?.data || err);
      this.showSaveMessage(err.response?.data?.msg || "Update failed", 'error');
    } finally {
      this.saving = false;
    }
  },

    validateField(field) {
      delete this.errors[field];

      switch(field) {
        case 'full_name':
          if (!this.form.full_name?.trim()) {
            this.errors.full_name = 'Full name is required';
          }
          break;
        case 'branch':
          if (!this.form.branch) {
            this.errors.branch = 'Branch is required';
          }
          break;
        case 'year':
          if (!this.form.year) {
            this.errors.year = 'Year is required';
          } else if (this.form.year < 1 || this.form.year > 4) {
            this.errors.year = 'Year must be between 1 and 4';
          }
          break;
        case 'cgpa':
          if (!this.form.cgpa && this.form.cgpa !== 0) {
            this.errors.cgpa = 'CGPA is required';
          } else if (this.form.cgpa < 0 || this.form.cgpa > 10) {
            this.errors.cgpa = 'CGPA must be between 0 and 10';
          }
          break;
      }
    },

    validateForm() {
      this.validateField('full_name');
      this.validateField('branch');
      this.validateField('year');
      this.validateField('cgpa');
      return Object.keys(this.errors).length === 0;
    },

    getInitials(name) {
      if (!name) return 'U';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },

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

    resetForm() {
      if (this.originalForm) {
        this.form = JSON.parse(JSON.stringify(this.originalForm));
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
    }
  }
};
</script>

<style scoped>
.profile-page {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}


.profile-header-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.avatar {
  width: 70px;
  height: 70px;
  font-size: 28px;
  font-weight: 600;
  color: white;
}

/* Profile Content Card */
.profile-content-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Tabs */
.nav-tabs {
  border-bottom: none;
}

.nav-tabs .nav-link {
  color: #666;
  border: none;
  padding: 0.75rem 1.5rem;
  cursor: pointer;
  border-radius: 50px;
  margin-right: 0.5rem;
  transition: all 0.3s ease;
}

.nav-tabs .nav-link:hover {
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.nav-tabs .nav-link.active {
  color: white;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Form Controls */
.form-control, .form-select {
  border: 2px solid #e0e0e0;
  padding: 0.6rem 1.2rem;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 0.2rem rgba(118, 75, 162, 0.25);
}

.form-control.rounded-pill, .form-select.rounded-pill {
  padding: 0.6rem 1.2rem;
}

.form-control.is-invalid, .form-select.is-invalid {
  border-color: #ef4444;
}

.invalid-feedback {
  color: #ef4444;
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
}

.btn-outline-custom:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Badge Styles */
.badge.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

/* Alerts */
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

.alert.rounded-pill {
  padding: 1rem 1.5rem;
}

/* Responsive */
@media (max-width: 768px) {
  .nav-tabs .nav-link {
    padding: 0.5rem 0.75rem;
    font-size: 0.9rem;
  }
  
  .nav-tabs .nav-link i {
    margin-right: 0.25rem;
  }

  .profile-header-card .d-flex {
    flex-direction: column;
    text-align: center;
  }
}
</style>