<template>
  <div class="company-home">
    <!-- Welcome Section -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold">
        Welcome back, <span class="text-gradient">{{ companyName || 'Company' }}</span>!
      </h1>
      <p class="text-muted">Here's what's happening with your placement drives.</p>
    </div>

    <!-- Statistics Cards -->
    <div class="row g-3 mb-4">
      <div class="col-md-3 col-sm-6" v-for="stat in statsList" :key="stat.label">
        <div class="card stat-card border-0 h-100">
          <div class="card-body d-flex align-items-center gap-3">
            <div class="stat-icon rounded-3 d-flex align-items-center justify-content-center"
                 :style="{ background: stat.iconBg }">
              <i :class="stat.icon" class="text-white fs-4"></i>
            </div>
            <div>
              <h3 class="h2 mb-0 text-dark">{{ stat.value }}</h3>
              <p class="text-secondary mb-0">{{ stat.label }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Applications -->
    <div class="card applications-card border-0 mb-4">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="h4 mb-0 text-dark">Recent Applications</h5>
          <button class="btn btn-outline-custom btn-sm" @click="$emit('change-tab', 'applications')">
            View All <i class="bi bi-arrow-right ms-2"></i>
          </button>
        </div>

        <div v-if="recentApplications.length > 0" class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Student</th>
                <th>Job Role</th>
                <th>Applied On</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in recentApplications" :key="app.application_id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="student-avatar rounded-circle bg-light d-flex align-items-center justify-content-center me-2"
                         :style="{ width: '35px', height: '35px' }">
                      <span class="small fw-bold text-primary">{{ getInitials(app.full_name) }}</span>
                    </div>
                    <div>
                      <div class="fw-medium">{{ app.full_name }}</div>
                      <small class="text-secondary">{{ app.branch }}</small>
                    </div>
                  </div>
                </td>
                <td>{{ app.job_role }}</td>
                <td>{{ formatDate(app.applied_on) }}</td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(app.application_status)">
                    {{ app.application_status }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary" @click="viewApplicationDetails(app)" title="View Application Details">
                    <i class="bi bi-eye"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="text-center py-4">
          <p class="text-secondary mb-0">No recent applications</p>
        </div>
      </div>
    </div>

    <!-- Active Drives -->
    <div class="card drives-card border-0">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h5 class="h4 mb-0 text-dark">Active Drives</h5>
          <button class="btn btn-outline-custom btn-sm" @click="$emit('change-tab', 'drives')">
            View All <i class="bi bi-arrow-right ms-2"></i>
          </button>
        </div>

        <div v-if="activeDrives.length > 0" class="row g-3">
          <div v-for="drive in activeDrives" :key="drive.id" class="col-md-6">
            <div class="drive-card p-3">
              <div class="d-flex justify-content-between align-items-start mb-2">
                <h6 class="text-dark mb-0">{{ drive.role }}</h6>
                <span class="badge" :class="getStatusBadgeClass(drive.status)">
                  {{ drive.status }}
                </span>
              </div>
              <p class="text-secondary small mb-2">
                <i class="bi bi-people me-1"></i>{{ drive.applications_count || 0 }} applications
              </p>
              <p class="text-secondary small mb-2">
                <i class="bi bi-calendar me-1"></i>Deadline: {{ formatDate(drive.deadline) }}
              </p>
              
              <!-- Improved View Details Button -->
              <button 
                class="btn btn-view-details w-100" 
                @click="viewDriveDetails(drive)"
                :title="`View details for ${drive.role}`"
              >
                <span class="btn-content">
                  <i class="bi bi-eye me-2"></i>
                  <span>View Details</span>
                  <i class="bi bi-arrow-right-short ms-2"></i>
                </span>
              </button>
            </div>
          </div>
        </div>
        <div v-else class="text-center py-4">
          <p class="text-secondary mb-0">No active drives</p>
          <button class="btn btn-primary-custom mt-3" @click="$emit('change-tab', 'create')">
            Create New Drive
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { useRouter } from 'vue-router';

export default {
  name: 'CompanyHome',
  
  emits: ['change-tab', 'update-company-name', 'token-expired'],

  setup() {
    const router = useRouter();
    return { router };
  },

  data() {
    return {
      loading: false,
      companyName: localStorage.getItem('companyName') || '',
      stats: {
        total_jobs: 0,
        active_jobs: 0,
        total_applications: 0,
        placements: 0
      },
      recentApplications: [],
      activeDrives: [],
      statsList: []
    };
  },

  mounted() {
    this.fetchDashboardData();
    this.fetchRecentApplications();
    this.fetchActiveDrives();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchDashboardData() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/dashboard",
          this.getAuthHeader()
        );
        
        if (res.data.company_name) {
          this.companyName = res.data.company_name;
          this.$emit('update-company-name', res.data.company_name);
        }

        this.fetchStatistics();

      } catch (err) {
        console.error('Failed to fetch dashboard:', err);
      }
    },

    async fetchStatistics() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/statistics",
          this.getAuthHeader()
        );
        
        this.stats = res.data;
        
        this.statsList = [
          {
            label: 'Total Jobs',
            value: this.stats.total_jobs || 0,
            icon: 'bi bi-briefcase',
            iconBg: 'linear-gradient(135deg, #667eea, #764ba2)'
          },
          {
            label: 'Active Drives',
            value: this.stats.active_jobs || 0,
            icon: 'bi bi-check-circle',
            iconBg: 'linear-gradient(135deg, #10b981, #059669)'
          },
          {
            label: 'Applications',
            value: this.stats.total_applications || 0,
            icon: 'bi bi-people',
            iconBg: 'linear-gradient(135deg, #f59e0b, #d97706)'
          },
          {
            label: 'Placements',
            value: this.stats.placements || 0,
            icon: 'bi bi-trophy',
            iconBg: 'linear-gradient(135deg, #8b5cf6, #6d28d9)'
          }
        ];

      } catch (err) {
        console.error('Failed to fetch statistics:', err);
      }
    },

    async fetchRecentApplications() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/applications",
          this.getAuthHeader()
        );
        
        this.recentApplications = (res.data || []).slice(0, 5);

      } catch (err) {
        console.error('Failed to fetch applications:', err);
      }
    },

    async fetchActiveDrives() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/dashboard",
          this.getAuthHeader()
        );
        
        const allJobs = res.data.jobs || [];
        this.activeDrives = allJobs.filter(job => job.status === 'approved').slice(0, 4);

      } catch (err) {
        console.error('Failed to fetch drives:', err);
      }
    },

    viewApplicationDetails(app) {
      console.log('Navigating to application:', app.application_id);
      this.router.push(`/company/dashboard/applications/${app.application_id}`);
    },

    viewDriveDetails(drive) {
      console.log('Navigating to drive:', drive.id);
      this.router.push(`/company/dashboard/drives/${drive.id}`);
    },

    getInitials(name) {
      if (!name) return 'U';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },

    getStatusBadgeClass(status) {
      const classes = {
        'applied': 'bg-primary',
        'shortlisted': 'bg-warning',
        'selected': 'bg-success',
        'rejected': 'bg-danger',
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'closed': 'bg-secondary'
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
.company-home {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Stat Cards */
.stat-card {
  background: white;
  border-radius: 15px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
}

/* Applications Card */
.applications-card,
.drives-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Drive Card */
.drive-card {
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.drive-card:hover {
  border-color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

/* Improved View Details Button */
.btn-view-details {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 50px;
  font-weight: 500;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  margin-top: 0.5rem;
}

.btn-view-details:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-view-details:active {
  transform: translateY(0);
}

.btn-view-details .btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn-view-details:hover .btn-content {
  letter-spacing: 0.5px;
}

.btn-view-details:hover .bi-arrow-right-short {
  transform: translateX(3px);
}

.btn-view-details .bi-eye,
.btn-view-details .bi-arrow-right-short {
  transition: all 0.3s ease;
}

.btn-view-details:hover .bi-eye {
  transform: scale(1.1);
}

/* Table */
.table th {
  border-bottom: 2px solid #e0e0e0;
  color: #666;
  font-weight: 600;
  font-size: 0.9rem;
}

.table td {
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
  font-size: 0.95rem;
}

.student-avatar {
  width: 35px;
  height: 35px;
  background: #f0f0f0;
}

.student-avatar-large {
  width: 80px;
  height: 80px;
  background: rgba(102, 126, 234, 0.1);
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
  padding: 0.4rem 1.2rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-outline-custom:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-outline-primary {
  border: 2px solid #667eea;
  color: #667eea;
  background: white;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: #667eea;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
}

/* Badge Styles */
.badge {
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.8rem;
  font-weight: 500;
}

.badge.bg-primary {
  background: #667eea !important;
  color: white;
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

/* Modal Styles (keep if needed) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  border-radius: 25px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideIn 0.3s ease;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
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

/* Responsive */
@media (max-width: 768px) {
  .table {
    font-size: 0.85rem;
  }
  
  .btn-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.8rem;
  }
  
  .btn-view-details {
    padding: 0.5rem 0.75rem;
    font-size: 0.85rem;
  }
}
</style>