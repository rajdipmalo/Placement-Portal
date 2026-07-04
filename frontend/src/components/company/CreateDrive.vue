<template>
  <div class="create-drive">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">{{ isEditing ? 'Edit Drive' : 'Create New Drive' }}</h1>
      <p class="text-muted">{{ isEditing ? 'Update your placement drive details' : 'Fill in the details to create a new placement drive' }}</p>
    </div>

    <!-- Form Card -->
    <div class="card border-0">
      <div class="card-body p-4">
        <form @submit.prevent="submitForm">
          <!-- Basic Details -->
          <h5 class="text-dark mb-3">Basic Details</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label text-dark">
                Job Title <span class="text-danger">*</span>
              </label>
              <input 
                type="text" 
                v-model="form.role" 
                class="form-control rounded-pill" 
                placeholder="e.g., Software Developer"
                required
              >
            </div>
            <div class="col-12">
              <label class="form-label text-dark">Job Description</label>
              <textarea 
                v-model="form.description" 
                rows="4" 
                class="form-control rounded-3" 
                placeholder="Describe the job role, responsibilities, etc."
              ></textarea>
            </div>
          </div>

          <!-- Compensation & Type -->
          <h5 class="text-dark mb-3">Compensation & Type</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label text-dark">Salary</label>
              <input 
                type="text" 
                v-model="form.salary" 
                class="form-control rounded-pill" 
                placeholder="e.g., ₹6,00,000 per annum"
              >
            </div>
            <div class="col-md-6">
              <label class="form-label text-dark">Job Type</label>
              <select v-model="form.job_type" class="form-select rounded-pill">
                <option value="">Select type</option>
                <option value="Full Time">Full Time</option>
                <option value="PPO">PPO</option>
                <option value="Intern + PPO">Intern + PPO</option>
                <option value="Internship">Internship</option>
              </select>
            </div>
          </div>

          <!-- Eligibility Criteria -->
          <h5 class="text-dark mb-3">Eligibility Criteria</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-4">
              <label class="form-label text-dark">Minimum CGPA</label>
              <input 
                type="number" 
                step="0.1" 
                min="0" 
                max="10" 
                v-model="form.eligibility_cgpa" 
                class="form-control rounded-pill" 
                placeholder="e.g., 7.5"
              >
            </div>
            <div class="col-md-4">
              <label class="form-label text-dark">Eligible Year</label>
              <select v-model="form.eligibility_year" class="form-select rounded-pill">
                <option value="">Any Year</option>
                <option value="1">1st Year</option>
                <option value="2">2nd Year</option>
                <option value="3">3rd Year</option>
                <option value="4">4th Year</option>
              </select>
            </div>
          </div>

          <!-- Improved Branch Selection - Full Width -->
          <div class="mb-4">
            <label class="form-label text-dark">Eligible Branches</label>
            <div class="branch-selection-container bg-light p-3 rounded-3">
              <div class="row g-3">
                <div class="col-12 col-lg-5">
                  <select 
                    v-model="selectedBranch" 
                    class="form-select rounded-pill" 
                    @change="addBranch"
                  >
                    <option value="">Select a branch to add</option>
                    <option v-for="branch in availableBranches" :key="branch.value" :value="branch.value">
                      {{ branch.label }}
                    </option>
                  </select>
                </div>
              </div>
              
              <!-- Selected Branches with Horizontal Scroll -->
              <div class="selected-branches-wrapper mt-3">
                <div v-if="form.eligibility_branch.length > 0" class="selected-branches-scroll">
                  <span v-for="branch in form.eligibility_branch" :key="branch"
                        class="badge bg-primary d-inline-flex align-items-center p-2 rounded-pill">
                    {{ getBranchLabel(branch) }}
                    <i class="bi bi-x ms-2" @click="removeBranch(branch)" style="cursor: pointer;"></i>
                  </span>
                </div>
                <p v-else class="text-secondary mb-0">No branches selected</p>
              </div>
              <small class="text-secondary d-block mt-2">Leave empty to allow all branches</small>
            </div>
          </div>

          <!-- Skills Required -->
          <div class="mb-4">
            <label class="form-label text-dark">Required Skills</label>
            <div class="skills-input-container bg-light p-3 rounded-3">
              <div class="input-group mb-2">
                <input 
                  type="text" 
                  v-model="newSkill" 
                  @keydown.enter.prevent="addSkill"
                  class="form-control rounded-start-pill" 
                  placeholder="Type a skill and press Enter"
                >
                <button class="btn btn-primary-custom rounded-end-pill" type="button" @click="addSkill">
                  Add
                </button>
              </div>
              <div class="skills-scroll">
                <span v-for="(skill, index) in form.skills_required" :key="index" 
                      class="badge bg-primary d-inline-flex align-items-center p-2 rounded-pill">
                  {{ skill }}
                  <i class="bi bi-x ms-2" @click="removeSkill(index)" style="cursor: pointer;"></i>
                </span>
                <span v-if="form.skills_required.length === 0" class="text-secondary">
                  No skills added yet
                </span>
              </div>
            </div>
          </div>

          <!-- Dates & Location -->
          <h5 class="text-dark mb-3">Dates & Location</h5>
          <div class="row g-3 mb-4">
            <div class="col-md-6">
              <label class="form-label text-dark">
                Application Deadline <span class="text-danger">*</span>
              </label>
              <input 
                type="datetime-local" 
                v-model="form.application_deadline" 
                class="form-control rounded-pill" 
                :min="minDateTime"
                required
              >
            </div>
            <div class="col-md-6">
              <label class="form-label text-dark">Drive Date</label>
              <input 
                type="date" 
                v-model="form.drive_date" 
                class="form-control rounded-pill" 
                :min="minDate"
              >
            </div>
            <div class="col-md-6">
              <label class="form-label text-dark">Drive Location</label>
              <input 
                type="text" 
                v-model="form.drive_location" 
                class="form-control rounded-pill" 
                placeholder="e.g., Bangalore, Remote"
              >
            </div>
          </div>

          <!-- Simplified Preview -->
          <div class="preview-section bg-light p-3 rounded-3 mb-4">
            <h6 class="text-dark mb-2">Preview</h6>
            <p class="fw-bold mb-1">{{ form.role || 'Job Title' }}</p>
            <p class="text-secondary small mb-2">{{ form.description || 'No description provided' }}</p>
            <div class="d-flex flex-wrap gap-2 mb-2">
              <span v-if="form.salary" class="badge bg-light text-dark">{{ form.salary }}</span>
              <span v-if="form.job_type" class="badge bg-light text-dark">{{ form.job_type }}</span>
              <span v-if="form.drive_location" class="badge bg-light text-dark">{{ form.drive_location }}</span>
            </div>
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <span v-if="form.eligibility_cgpa" class="badge bg-light text-dark me-2">CGPA ≥ {{ form.eligibility_cgpa }}</span>
                <span v-if="form.eligibility_year" class="badge bg-light text-dark">Year {{ form.eligibility_year }}</span>
              </div>
              <small class="text-secondary">Deadline: {{ formatDate(form.application_deadline) || 'Not set' }}</small>
            </div>
          </div>

          <!-- Form Actions -->
          <div class="d-flex gap-3 justify-content-end">
            <button type="button" class="btn btn-outline-custom" @click="resetForm">
              <i class="bi bi-arrow-counterclockwise me-2"></i>Reset
            </button>
            <button type="submit" class="btn btn-primary-custom" :disabled="submitting">
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else :class="isEditing ? 'bi bi-pencil' : 'bi bi-plus-circle'" class="me-2"></i>
              {{ isEditing ? 'Update Drive' : 'Create Drive' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL } from "@/config";

export default {
  name: 'CreateDrive',
  
  emits: ['change-tab', 'token-expired'],

  data() {
    return {
      isEditing: false,
      editingId: null,
      submitting: false,
      newSkill: '',
      selectedBranch: '',
      form: {
        role: '',
        description: '',
        salary: '',
        job_type: '',
        eligibility_cgpa: '',
        eligibility_year: '',
        eligibility_branch: [],
        skills_required: [],
        application_deadline: '',
        drive_date: '',
        drive_location: ''
      },
      originalForm: null, // Store original form for reset
      branches: [
        { value: 'CSE', label: 'Computer Science (CSE)' },
        { value: 'IT', label: 'Information Technology (IT)' },
        { value: 'ECE', label: 'Electronics & Communication (ECE)' },
        { value: 'EEE', label: 'Electrical & Electronics (EEE)' },
        { value: 'EE', label: 'Electrical Engineering (EE)' },
        { value: 'MECH', label: 'Mechanical Engineering (MECH)' },
        { value: 'CIVIL', label: 'Civil Engineering (CIVIL)' },
        { value: 'CHEMICAL', label: 'Chemical Engineering' },
        { value: 'BIOTECH', label: 'Biotechnology' },
        { value: 'AIML', label: 'AI & ML (AIML)' },
        { value: 'DATA SCIENCE', label: 'Data Science' },
        { value: 'METALLURGY', label: 'Metallurgical Engineering' },
        { value: 'ENGINEERING PHYSICS', label: 'Engineering Physics' },
        { value: 'ENGINEERING MATHEMATICS', label: 'Engineering Mathematics' },
        { value: 'PRODUCTION ENGINEERING', label: 'Production Engineering' },
        { value: 'INDUSTRIAL ENGINEERING', label: 'Industrial Engineering' },
        { value: 'AEROSPACE ENGINEERING', label: 'Aerospace Engineering' },
        { value: 'AGRICULTURAL ENGINEERING', label: 'Agricultural Engineering' },
        { value: 'ENVIRONMENTAL ENGINEERING', label: 'Environmental Engineering' },
        { value: 'MATERIALS SCIENCE', label: 'Materials Science' },
        { value: 'MINING ENGINEERING', label: 'Mining Engineering' },
        { value: 'OCEAN ENGINEERING', label: 'Ocean Engineering' },
        { value: 'NAVAL ARCHITECTURE', label: 'Naval Architecture' },
        { value: 'TEXTILE ENGINEERING', label: 'Textile Engineering' },
        { value: 'INSTRUMENTATION ENGINEERING', label: 'Instrumentation Engineering' }
      ]
    };
  },

  computed: {
    minDateTime() {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      return now.toISOString().slice(0, 16);
    },
    minDate() {
      const now = new Date();
      now.setDate(now.getDate() + 1);
      return now.toISOString().split('T')[0];
    },
    availableBranches() {
      return this.branches.filter(b => !this.form.eligibility_branch.includes(b.value));
    }
  },

  mounted() {
    // Check if editing
    const editingData = localStorage.getItem('editingDrive');
    if (editingData) {
      this.isEditing = true;
      const drive = JSON.parse(editingData);
      this.editingId = drive.id;
      this.form = {
        role: drive.role || '',
        description: drive.description || '',
        salary: drive.salary || '',
        job_type: drive.job_type || '',
        eligibility_cgpa: drive.cgpa_required || '',
        eligibility_year: drive.year_required || '',
        eligibility_branch: drive.branch_required || [],
        skills_required: drive.skills_required || [],
        application_deadline: drive.deadline ? drive.deadline.slice(0, 16) : '',
        drive_date: drive.drive_date || '',
        drive_location: drive.drive_location || ''
      };
      // Store original form for reset
      this.originalForm = JSON.parse(JSON.stringify(this.form));
    } else {
      // For new drive, store empty form as original
      this.originalForm = JSON.parse(JSON.stringify(this.form));
    }
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    resetForm() {
      if (this.isEditing && this.originalForm) {
        // Reset to original drive data when editing
        this.form = JSON.parse(JSON.stringify(this.originalForm));
      } else {
        // Reset to empty form when creating new
        this.form = {
          role: '',
          description: '',
          salary: '',
          job_type: '',
          eligibility_cgpa: '',
          eligibility_year: '',
          eligibility_branch: [],
          skills_required: [],
          application_deadline: '',
          drive_date: '',
          drive_location: ''
        };
      }
      // Reset input fields
      this.newSkill = '';
      this.selectedBranch = '';
      
      // Optional: Show a brief message that form was reset
      // You could add a toast notification here
    },

    addBranch() {
      if (this.selectedBranch && !this.form.eligibility_branch.includes(this.selectedBranch)) {
        this.form.eligibility_branch.push(this.selectedBranch);
        this.selectedBranch = '';
      }
    },

    removeBranch(branch) {
      const index = this.form.eligibility_branch.indexOf(branch);
      if (index !== -1) {
        this.form.eligibility_branch.splice(index, 1);
      }
    },

    getBranchLabel(branchValue) {
      const branch = this.branches.find(b => b.value === branchValue);
      return branch ? branch.label : branchValue;
    },

    addSkill() {
      if (this.newSkill.trim()) {
        if (!this.form.skills_required.includes(this.newSkill.trim())) {
          this.form.skills_required.push(this.newSkill.trim());
        }
        this.newSkill = '';
      }
    },

    removeSkill(index) {
      this.form.skills_required.splice(index, 1);
    },

    async submitForm() {
      this.submitting = true;

      try {
        const payload = {
          role: this.form.role,
          description: this.form.description,
          salary: this.form.salary,
          job_type: this.form.job_type,
          skills_required: this.form.skills_required,
          eligibility_cgpa: this.form.eligibility_cgpa ? parseFloat(this.form.eligibility_cgpa) : null,
          eligibility_branch: this.form.eligibility_branch,
          eligibility_year: this.form.eligibility_year ? parseInt(this.form.eligibility_year) : null,
          application_deadline: this.form.application_deadline,
          drive_date: this.form.drive_date,
          drive_location: this.form.drive_location
        };

        if (this.isEditing) {
          await axios.put(
            `${API_URL}/api/company/jobs/${this.editingId}`,
            payload,
            this.getAuthHeader()
          );
          alert("Drive updated successfully!");
        } else {
          await axios.post(
            `${API_URL}/api/company/jobs`,
            payload,
            this.getAuthHeader()
          );
          alert("Drive created successfully! Awaiting admin approval.");
        }

        this.$emit('change-tab', 'drives');

      } catch (err) {
        alert(err.response?.data?.msg || "Failed to save drive");
      } finally {
        this.submitting = false;
      }
    },

    formatDate(date) {
      if (!date) return 'Not set';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    }
  }
};
</script>

<style scoped>
.create-drive {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Card */
.card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
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

.form-control.rounded-3 {
  border-radius: 15px;
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

/* FIX: Branch Selection Container - Full Width */
.branch-selection-container {
  background: #f8f9fa;
  border-radius: 15px;
  width: 100%;
}

.selected-branches-wrapper {
  width: 100%;
}

/* FIX: Horizontal Scroll for Branches */
.selected-branches-scroll {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  padding-right: 8px;
}

/* Skills with Horizontal Scroll */
.skills-input-container {
  background: #f8f9fa;
  border-radius: 15px;
}

.skills-scroll {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
  max-height: 150px;
  overflow-y: auto;
  padding-right: 8px;
}

/* Badge Styles */
.badge.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
  white-space: nowrap;
  flex-shrink: 0;
}

.badge.bg-light {
  background: #e9ecef !important;
  color: #495057;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.9rem;
}

.badge i {
  font-size: 0.8rem;
  transition: all 0.2s ease;
  cursor: pointer;
}

.badge i:hover {
  color: #ff4444;
}

/* Preview Section */
.preview-section {
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.preview-section:hover {
  border-color: #667eea;
}

/* Scrollbar Styling */
.selected-branches-scroll::-webkit-scrollbar,
.skills-scroll::-webkit-scrollbar {
  height: 6px;
}

.selected-branches-scroll::-webkit-scrollbar-track,
.skills-scroll::-webkit-scrollbar-track {
  background: #e0e0e0;
  border-radius: 3px;
}

.selected-branches-scroll::-webkit-scrollbar-thumb,
.skills-scroll::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 3px;
}

.selected-branches-scroll::-webkit-scrollbar-thumb:hover,
.skills-scroll::-webkit-scrollbar-thumb:hover {
  background: #764ba2;
}

/* Responsive */
@media (max-width: 768px) {
  .preview-section .d-flex {
    flex-direction: column;
    align-items: start !important;
    gap: 0.5rem;
  }
  
  .selected-branches-scroll,
  .skills-scroll {
    max-height: 120px;
  }
}
</style>