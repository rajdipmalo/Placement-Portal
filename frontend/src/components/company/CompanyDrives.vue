<template>
  <div class="company-drives">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">My Drives</h1>
      <p class="text-muted">Manage all your placement drives</p>
    </div>

    <!-- Filters -->
    <div class="card filters-card border-0 mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <div class="input-group">
              <span class="input-group-text bg-white text-secondary border-end-0">
                <i class="bi bi-search"></i>
              </span>
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search drives..."
                class="form-control border-start-0 rounded-end-pill"
              >
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="statusFilter" class="form-select rounded-pill">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="closed">Closed</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="sortBy" class="form-select rounded-pill">
              <option value="created_at">Sort by Date</option>
              <option value="deadline">Sort by Deadline</option>
              <option value="applications">Sort by Applications</option>
            </select>
          </div>
          <div class="col-md-2">
            <button class="btn btn-primary-custom w-100" @click="$emit('change-tab', 'create')">
              <i class="bi bi-plus-circle me-2"></i>New Drive
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading drives...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchDrives">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Drives List -->
    <div v-else>
      <div class="row g-4">
        <div v-for="drive in filteredDrives" :key="drive.id" class="col-lg-6">
          <div class="card drive-card border-0">
            <div class="card-body">
              <!-- Header -->
              <div class="d-flex justify-content-between align-items-start mb-3">
                <div>
                  <h5 class="card-title text-dark mb-1">{{ drive.role }}</h5>
                  <p class="text-secondary small mb-0">Created: {{ formatDate(drive.created_at) }}</p>
                </div>
                <span class="badge" :class="getStatusBadgeClass(drive.status)">
                  {{ drive.status }}
                </span>
              </div>

              <!-- Details -->
              <div class="row g-2 mb-3">
                <div class="col-6">
                  <div class="detail-item">
                    <small class="text-secondary d-block">Deadline</small>
                    <span class="text-dark">{{ formatDate(drive.deadline) }}</span>
                  </div>
                </div>
                <div class="col-6">
                  <div class="detail-item">
                    <small class="text-secondary d-block">Applications</small>
                    <span class="text-dark fw-bold">{{ drive.applications_count || 0 }}</span>
                  </div>
                </div>
              </div>

              <!-- Eligibility Summary -->
              <div class="bg-light p-3 rounded-3 mb-3">
                <div class="d-flex flex-wrap gap-3">
                  <span v-if="drive.cgpa_required" class="small">
                    <i class="bi bi-star text-primary me-1"></i>
                    CGPA ≥ {{ drive.cgpa_required }}
                  </span>
                  <span v-if="drive.year_required" class="small">
                    <i class="bi bi-calendar-range text-primary me-1"></i>
                    Year {{ drive.year_required }}
                  </span>
                  <span v-if="drive.branch_required?.length" class="small">
                    <i class="bi bi-diagram-3 text-primary me-1"></i>
                    {{ drive.branch_required.slice(0, 3).join(', ') }}{{ drive.branch_required.length > 3 ? '...' : '' }}
                  </span>
                </div>
              </div>

              <!-- Actions -->
              <div class="d-flex gap-2">
                <button class="btn btn-outline-custom flex-grow-1" @click="viewDriveDetails(drive)">
                  <i class="bi bi-eye me-2"></i>View Details
                </button>
                
                <button v-if="drive.status === 'pending'"
                        class="btn btn-outline-warning" 
                        @click="editDrive(drive)"
                        title="Edit Drive">
                  <i class="bi bi-pencil"></i>
                </button>
                
                <button v-if="drive.status === 'approved'"
                        class="btn btn-outline-success" 
                        @click="markDriveComplete(drive)"
                        title="Mark as Complete">
                  <i class="bi bi-check-circle"></i>
                </button>
                
                <button v-if="drive.status === 'closed'"
                        class="btn btn-outline-info" 
                        @click="reopenDrive(drive)"
                        title="Reopen Drive">
                  <i class="bi bi-arrow-repeat"></i>
                </button>
                
                <button v-if="drive.status === 'pending'"
                        class="btn btn-outline-danger" 
                        @click="deleteDrive(drive)"
                        title="Delete Drive">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredDrives.length === 0" class="text-center py-5">
        <i class="bi bi-inbox fs-1 text-secondary"></i>
        <h5 class="text-dark mt-3">No drives found</h5>
        <p class="text-secondary">Try adjusting your filters or create a new drive</p>
        <button class="btn btn-primary-custom mt-2" @click="$emit('change-tab', 'create')">
          Create New Drive
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from 'vue-router';

export default {
  name: 'CompanyDrives',
  
  setup() {
    const router = useRouter();
    return { router };
  },

  emits: ['change-tab', 'token-expired'],

  data() {
    return {
      loading: false,
      error: null,
      drives: [],
      searchQuery: '',
      statusFilter: '',
      sortBy: 'created_at'
    };
  },

  computed: {
    filteredDrives() {
      let filtered = [...this.drives];

      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(drive => 
          drive.role.toLowerCase().includes(query)
        );
      }

      if (this.statusFilter) {
        filtered = filtered.filter(drive => drive.status === this.statusFilter);
      }

      filtered.sort((a, b) => {
        switch(this.sortBy) {
          case 'deadline':
            return new Date(a.deadline) - new Date(b.deadline);
          case 'applications':
            return (b.applications_count || 0) - (a.applications_count || 0);
          default:
            return new Date(b.created_at) - new Date(a.created_at);
        }
      });

      return filtered;
    }
  },

  mounted() {
    this.fetchDrives();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchDrives() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/dashboard",
          this.getAuthHeader()
        );

        // Map backend field names to frontend expected names
        this.drives = (res.data.jobs || []).map(job => ({
          id: job.id,
          role: job.role,
          status: job.status,
          applications_count: job.applications_count || 0,
          deadline: job.deadline,
          created_at: job.created_at || new Date().toISOString(),
          // Map eligibility fields
          cgpa_required: job.eligibility_cgpa,
          year_required: job.eligibility_year,
          branch_required: job.eligibility_branch,
          description: job.description,
          salary: job.salary,
          job_type: job.job_type,
          skills_required: job.skills_required
        }));

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load drives";
        if (err.response?.status === 401) {
          this.$emit('token-expired');
        }
      } finally {
        this.loading = false;
      }
    },

    viewDriveDetails(drive) {
      this.router.push(`/company/dashboard/drives/${drive.id}`);
    },

    viewApplications(drive) {
      this.$emit('change-tab', 'applications');
      localStorage.setItem('selectedDriveId', drive.id);
    },

    editDrive(drive) {
      localStorage.setItem('editingDrive', JSON.stringify(drive));
      this.$emit('change-tab', 'create');
    },

    async markDriveComplete(drive) {
      if (confirm(`Are you sure you want to mark drive "${drive.role}" as complete?`)) {
        try {
          await axios.post(
            `http://127.0.0.1:5000/api/company/jobs/${drive.id}/complete`,
            {},
            this.getAuthHeader()
          );
          
          alert('Drive marked as complete successfully!');
          this.fetchDrives();
          
        } catch (err) {
          alert(err.response?.data?.msg || "Failed to mark drive as complete");
        }
      }
    },

    async reopenDrive(drive) {
      if (confirm(`Are you sure you want to reopen drive "${drive.role}"?`)) {
        try {
          await axios.post(
            `http://127.0.0.1:5000/api/company/jobs/${drive.id}/reopen`,
            {},
            this.getAuthHeader()
          );
          
          alert('Drive reopened successfully!');
          this.fetchDrives();
          
        } catch (err) {
          alert(err.response?.data?.msg || "Failed to reopen drive");
        }
      }
    },

    async deleteDrive(drive) {
      if (confirm(`Are you sure you want to delete drive "${drive.role}"?`)) {
        try {
          await axios.delete(
            `http://127.0.0.1:5000/api/company/jobs/${drive.id}`,
            this.getAuthHeader()
          );
          
          alert('Drive deleted successfully');
          this.fetchDrives();
          
        } catch (err) {
          alert(err.response?.data?.msg || "Failed to delete drive");
        }
      }
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

    formatDate(date) {
      if (!date) return 'N/A';
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
.company-drives {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Filters Card */
.filters-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Drive Card */
.drive-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: 1px solid transparent;
}

.drive-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.detail-item {
  padding: 0.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.drive-card:hover .detail-item {
  background: white;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
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

.input-group-text {
  background: white;
  border: 2px solid #e0e0e0;
  border-right: none;
  border-radius: 50px 0 0 50px;
}

.input-group .form-control {
  border-left: none;
  border-radius: 0 50px 50px 0;
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

.btn-primary-custom:hover {
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

.btn-outline-warning {
  border: 2px solid #f59e0b;
  color: #f59e0b;
  background: white;
  transition: all 0.3s ease;
}

.btn-outline-warning:hover {
  background: #f59e0b;
  color: white;
}

.btn-outline-success {
  border: 2px solid #10b981;
  color: #10b981;
  background: white;
  transition: all 0.3s ease;
}

.btn-outline-success:hover {
  background: #10b981;
  color: white;
}

.btn-outline-danger {
  border: 2px solid #ef4444;
  color: #ef4444;
  background: white;
  transition: all 0.3s ease;
}

.btn-outline-danger:hover {
  background: #ef4444;
  color: white;
}

.btn-outline-info {
  border: 2px solid #17a2b8;
  color: #17a2b8;
  background: white;
  transition: all 0.3s ease;
}

.btn-outline-info:hover {
  background: #17a2b8;
  color: white;
}

/* Badge Styles */
.badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
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
  background: #9ca3af !important;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .d-flex.gap-2 {
    flex-wrap: wrap;
  }
  
  .btn-sm {
    width: 100%;
  }
  
  .btn-outline-warning,
  .btn-outline-success,
  .btn-outline-danger,
  .btn-outline-info {
    padding: 0.4rem 0.8rem;
  }
}
</style>