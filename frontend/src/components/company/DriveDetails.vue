<template>
  <div class="drive-details-page">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to My Drives
    </button>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading drive details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchDriveDetails">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Drive Details Content -->
    <div v-else-if="drive" class="drive-details-container">
      <!-- Header Card -->
      <div class="header-card card border-0 mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="drive-icon-large rounded-circle d-flex align-items-center justify-content-center"
                   :style="{ background: getDriveColor(drive.role) }">
                <i class="bi bi-briefcase fs-1 text-white"></i>
              </div>
            </div>
            <div class="col">
              <h2 class="h2 text-dark mb-2">{{ drive.role }}</h2>
              <div class="d-flex gap-3 flex-wrap align-items-center">
                <span class="badge" :class="getStatusBadgeClass(drive.status)">
                  {{ drive.status }}
                </span>
                <span class="text-secondary">
                  <i class="bi bi-calendar me-1"></i>
                  Created: {{ formatDate(drive.created_at) }}
                </span>
                <span class="text-secondary">
                  <i class="bi bi-people me-1"></i>
                  {{ drive.applications_count || 0 }} Applications
                </span>
              </div>
            </div>
            <div class="col-auto" v-if="drive.status === 'approved'">
              <button class="btn btn-primary-custom" @click="viewApplications">
                <i class="bi bi-people me-2"></i>View Applications
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="row g-4">
        <!-- Left Column - Main Details -->
        <div class="col-lg-8">
          <!-- Description Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-file-text text-primary me-2"></i>Job Description
              </h5>
              <p class="text-secondary">{{ drive.description || 'No description provided' }}</p>
            </div>
          </div>

          <!-- Eligibility Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-list-check text-primary me-2"></i>Eligibility Criteria
              </h5>
              
              <div class="row g-4">
                <div class="col-md-4">
                  <div class="eligibility-box bg-light p-4 rounded-3 text-center">
                    <i class="bi bi-star fs-1 text-primary mb-2"></i>
                    <h6 class="text-dark mb-1">Minimum CGPA</h6>
                    <p class="h4 mb-0 text-primary">{{ drive.eligibility_cgpa || 'Any' }}</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="eligibility-box bg-light p-4 rounded-3 text-center">
                    <i class="bi bi-calendar-range fs-1 text-primary mb-2"></i>
                    <h6 class="text-dark mb-1">Eligible Year</h6>
                    <p class="h4 mb-0 text-primary">{{ drive.eligibility_year ? drive.eligibility_year + 'th Year' : 'Any' }}</p>
                  </div>
                </div>
                <div class="col-md-4">
                  <div class="eligibility-box bg-light p-4 rounded-3 text-center">
                    <i class="bi bi-diagram-3 fs-1 text-primary mb-2"></i>
                    <h6 class="text-dark mb-1">Eligible Branches</h6>
                    <p class="h4 mb-0 text-primary">{{ drive.eligibility_branch?.length || 'All' }}</p>
                  </div>
                </div>
              </div>

              <div v-if="drive.eligibility_branch?.length" class="mt-4">
                <h6 class="text-dark mb-3">Eligible Branches List</h6>
                <div class="d-flex gap-2 flex-wrap">
                  <span v-for="branch in drive.eligibility_branch" :key="branch" 
                        class="badge bg-light text-dark p-3">
                    {{ branch }}
                  </span>
                </div>
              </div>
            </div>
          </div>

          <!-- Skills Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-code-square text-primary me-2"></i>Required Skills
              </h5>
              
              <div class="d-flex gap-2 flex-wrap">
                <span v-for="skill in drive.skills_required || []" :key="skill" 
                      class="badge bg-primary p-3">
                  {{ skill }}
                </span>
                <span v-if="!drive.skills_required?.length" class="text-secondary">
                  No specific skills required
                </span>
              </div>
            </div>
          </div>

          <!-- Timeline Card -->
          <div class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-clock-history text-primary me-2"></i>Drive Timeline
              </h5>
              
              <div class="timeline">
                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon bg-primary bg-opacity-10 rounded-circle me-3 d-flex align-items-center justify-content-center"
                       style="width: 40px; height: 40px;">
                    <i class="bi bi-plus-circle text-primary"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Created</h6>
                    <p class="text-secondary small mb-0">{{ formatDateTime(drive.created_at) }}</p>
                  </div>
                </div>

                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon" :class="getDeadlineIconClass()"
                       style="width: 40px; height: 40px;">
                    <i :class="getDeadlineIcon()"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Application Deadline</h6>
                    <p class="text-secondary small mb-0">{{ formatDateTime(drive.application_deadline) }}</p>
                    <p v-if="isDeadlineNear" class="text-danger small mt-1">
                      <i class="bi bi-exclamation-triangle me-1"></i>Deadline approaching!
                    </p>
                  </div>
                </div>

                <div v-if="drive.drive_date" class="timeline-item d-flex">
                  <div class="timeline-icon bg-success bg-opacity-10 rounded-circle me-3 d-flex align-items-center justify-content-center"
                       style="width: 40px; height: 40px;">
                    <i class="bi bi-calendar-event text-success"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Drive Date</h6>
                    <p class="text-secondary small mb-0">{{ formatDate(drive.drive_date) }}</p>
                    <p v-if="drive.drive_location" class="text-secondary small mt-1">
                      <i class="bi bi-geo-alt me-1"></i>{{ drive.drive_location }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Stats & Actions -->
        <div class="col-lg-4">
          <!-- Stats Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-graph-up text-primary me-2"></i>Statistics
              </h5>
              
              <div class="stats-list">
                <div class="stat-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded-3">
                  <span class="text-secondary">Total Applications</span>
                  <span class="h4 mb-0 text-primary">{{ stats.total }}</span>
                </div>
                <div class="stat-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded-3">
                  <span class="text-secondary">Shortlisted</span>
                  <span class="h4 mb-0 text-warning">{{ stats.shortlisted }}</span>
                </div>
                <div class="stat-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded-3">
                  <span class="text-secondary">Selected</span>
                  <span class="h4 mb-0 text-success">{{ stats.selected }}</span>
                </div>
                <div class="stat-item d-flex justify-content-between align-items-center p-3 bg-light rounded-3">
                  <span class="text-secondary">Rejected</span>
                  <span class="h4 mb-0 text-danger">{{ stats.rejected }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Actions Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-gear text-primary me-2"></i>Actions
              </h5>
              
              <div class="d-grid gap-2">
                <button v-if="drive.status === 'approved'" 
                        class="btn btn-outline-primary" 
                        @click="viewApplications">
                  <i class="bi bi-people me-2"></i>View Applications
                </button>
                
                <button v-if="drive.status === 'pending'" 
                        class="btn btn-outline-warning" 
                        @click="editDrive">
                  <i class="bi bi-pencil me-2"></i>Edit Drive
                </button>
                
                <button v-if="drive.status === 'approved'" 
                        class="btn btn-outline-success" 
                        @click="markComplete">
                  <i class="bi bi-check-circle me-2"></i>Mark as Complete
                </button>
                
                <button v-if="drive.status === 'closed'" 
                        class="btn btn-outline-info" 
                        @click="reopenDrive">
                  <i class="bi bi-arrow-repeat me-2"></i>Reopen Drive
                </button>
                
                <button v-if="drive.status === 'pending'" 
                        class="btn btn-outline-danger" 
                        @click="deleteDrive">
                  <i class="bi bi-trash me-2"></i>Delete Drive
                </button>
              </div>
            </div>
          </div>

          <!-- Info Card -->
          <div class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-info-circle text-primary me-2"></i>Additional Info
              </h5>
              
              <div class="info-list">
                <div class="info-item d-flex align-items-center mb-3">
                  <i class="bi bi-cash text-primary me-3 fs-5"></i>
                  <div>
                    <small class="text-secondary d-block">Salary</small>
                    <span class="text-dark">{{ drive.salary || 'Not specified' }}</span>
                  </div>
                </div>
                <div class="info-item d-flex align-items-center">
                  <i class="bi bi-briefcase text-primary me-3 fs-5"></i>
                  <div>
                    <small class="text-secondary d-block">Job Type</small>
                    <span class="text-dark">{{ drive.job_type || 'Full Time' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from 'vue-router';

export default {
  name: 'DriveDetails',

  props: {
    driveId: {
      type: [String, Number],
      required: true
    }
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  emits: ['back-to-drives', 'token-expired'],

  data() {
    return {
      loading: false,
      error: null,
      drive: null,
      applications: [],
      stats: {
        total: 0,
        shortlisted: 0,
        selected: 0,
        rejected: 0
      }
    };
  },

  computed: {
    isDeadlineNear() {
      if (!this.drive?.application_deadline) return false;
      const deadline = new Date(this.drive.application_deadline);
      const now = new Date();
      const daysLeft = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));
      return daysLeft <= 3 && daysLeft > 0;
    }
  },

  mounted() {
    this.fetchDriveDetails();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchDriveDetails() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/company/jobs/${this.driveId}`,
          this.getAuthHeader()
        );

        this.drive = {
          ...res.data,
          created_at: res.data.created_at || new Date().toISOString()
        };
        
        this.stats = res.data.stats || {
          total: 0,
          shortlisted: 0,
          selected: 0,
          rejected: 0
        };

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load drive details";
      } finally {
        this.loading = false;
      }
    },

    calculateStats() {
      this.stats = {
        total: this.applications.length,
        shortlisted: this.applications.filter(app => app.application_status === 'shortlisted').length,
        selected: this.applications.filter(app => app.application_status === 'selected').length,
        rejected: this.applications.filter(app => app.application_status === 'rejected').length
      };
    },

    getDriveColor(role) {
      const colors = [
        'linear-gradient(135deg, #667eea, #764ba2)',
        'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        'linear-gradient(135deg, #10b981, #059669)',
        'linear-gradient(135deg, #f59e0b, #d97706)',
        'linear-gradient(135deg, #8b5cf6, #6d28d9)'
      ];
      
      let hash = 0;
      for (let i = 0; i < role.length; i++) {
        hash = ((hash << 5) - hash) + role.charCodeAt(i);
        hash |= 0;
      }
      return colors[Math.abs(hash) % colors.length];
    },

    getStatusBadgeClass(status) {
      const classes = {
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'closed': 'bg-secondary',
        'rejected': 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getDeadlineIconClass() {
      if (!this.drive?.application_deadline) return 'bg-light';
      const now = new Date();
      const deadline = new Date(this.drive.application_deadline);
      return deadline > now ? 'bg-warning bg-opacity-10' : 'bg-secondary bg-opacity-10';
    },

    getDeadlineIcon() {
      if (!this.drive?.application_deadline) return 'bi bi-calendar text-secondary';
      const now = new Date();
      const deadline = new Date(this.drive.application_deadline);
      return deadline > now ? 'bi bi-calendar text-warning' : 'bi bi-calendar-x text-secondary';
    },

    goBack() {
      this.router.push('/company/dashboard/drives');
    },

    viewApplications() {
      this.router.push('/company/dashboard/applications');
      localStorage.setItem('selectedDriveId', this.driveId);
    },

    editDrive() {
      localStorage.setItem('editingDrive', JSON.stringify(this.drive));
      this.router.push('/company/dashboard/create');
    },

    async markComplete() {
      if (confirm(`Are you sure you want to mark drive "${this.drive.role}" as complete?`)) {
        try {
          await axios.post(
            `http://127.0.0.1:5000/api/company/jobs/${this.drive.id}/complete`,
            {},
            this.getAuthHeader()
          );
          
          alert('Drive marked as complete successfully!');
          this.fetchDriveDetails();
          
        } catch (err) {
          alert(err.response?.data?.msg || "Failed to mark drive as complete");
        }
      }
    },

    async reopenDrive() {
      if (confirm(`Are you sure you want to reopen drive "${this.drive.role}"?`)) {
        try {
          await axios.post(
            `http://127.0.0.1:5000/api/company/jobs/${this.drive.id}/reopen`,
            {},
            this.getAuthHeader()
          );
          
          alert('Drive reopened successfully!');
          this.fetchDriveDetails();
          
        } catch (err) {
          alert(err.response?.data?.msg || "Failed to reopen drive");
        }
      }
    },

    async deleteDrive() {
      if (confirm(`Are you sure you want to delete drive "${this.drive.role}"?`)) {
        try {
          await axios.delete(
            `http://127.0.0.1:5000/api/company/jobs/${this.drive.id}`,
            this.getAuthHeader()
          );
          
          alert('Drive deleted successfully!');
          this.goBack();
          
        } catch (err) {
          alert(err.response?.data?.msg || "Failed to delete drive");
        }
      }
    },

    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatDateTime(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.drive-details-page {
  color: #333;
  min-height: 100%;
  background: #f8f9fa;
}

/* Back Button */
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

/* Header Card */
.header-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.drive-icon-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
}

/* Cards */
.card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: none;
}

/* Eligibility Box */
.eligibility-box {
  transition: all 0.3s ease;
}

.eligibility-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

/* Timeline */
.timeline-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.timeline-item {
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 19px;
  top: 45px;
  bottom: -15px;
  width: 2px;
  background: #e0e0e0;
}

/* Stats */
.stat-item {
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

/* Info Item - Updated to match Stats hover effect */
.info-item {
  transition: all 0.3s ease;
  padding: 0.75rem;
  border-radius: 8px;
}

.info-item:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
  background: transparent;
}

.info-item i {
  transition: all 0.3s ease;
}

.info-item:hover i {
  transform: scale(1.1);
  color: #764ba2 !important;
}

.info-item:hover .text-dark {
  color: #667eea !important;
  font-weight: 500;
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

.btn-outline-primary,
.btn-outline-warning,
.btn-outline-success,
.btn-outline-danger {
  border-width: 2px;
  border-radius: 50px;
  padding: 0.6rem 1rem;
  transition: all 0.3s ease;
}

.btn-outline-primary {
  border-color: #667eea;
  color: #667eea;
}

.btn-outline-primary:hover {
  background: #667eea;
  color: white;
}

.btn-outline-warning {
  border-color: #f59e0b;
  color: #f59e0b;
}

.btn-outline-warning:hover {
  background: #f59e0b;
  color: white;
}

.btn-outline-success {
  border-color: #10b981;
  color: #10b981;
}

.btn-outline-success:hover {
  background: #10b981;
  color: white;
}

.btn-outline-danger {
  border-color: #ef4444;
  color: #ef4444;
}

.btn-outline-danger:hover {
  background: #ef4444;
  color: white;
}

/* Badge Styles */
.badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.bg-success {
  background: #10b981 !important;
  color: white;
}

.badge.bg-warning {
  background: #f59e0b !important;
  color: white;
}

.badge.bg-danger {
  background: #ef4444 !important;
  color: white;
}

.badge.bg-secondary {
  background: #6c757d !important;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .drive-details-page {
    padding: 1rem;
  }
  
  .header-card .row {
    flex-direction: column;
    text-align: center;
  }
  
  .drive-icon-large {
    margin-bottom: 1rem;
  }
  
  .timeline-item:not(:last-child)::after {
    left: 15px;
  }
  
  .btn-outline-primary,
  .btn-outline-warning,
  .btn-outline-success,
  .btn-outline-danger {
    width: 100%;
  }
}
</style>