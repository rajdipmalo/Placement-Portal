<template>
  <div class="company-applications">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Applications</h1>
      <p class="text-muted">Manage student applications for your drives</p>
    </div>

    <!-- Filters -->
    <div class="card filters-card border-0 mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-3">
            <div class="input-group">
              <span class="input-group-text bg-white text-secondary border-end-0">
                <i class="bi bi-search"></i>
              </span>
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search students..."
                class="form-control border-start-0 rounded-end-pill"
              >
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="jobFilter" class="form-select rounded-pill">
              <option value="">All Drives</option>
              <option v-for="job in jobs" :key="job.id" :value="job.id">
                {{ job.role }}
              </option>
            </select>
          </div>
          <div class="col-md-2">
            <select v-model="statusFilter" class="form-select rounded-pill">
              <option value="">All Status</option>
              <option value="applied">Applied</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="selected">Selected</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div class="col-md-2">
            <select v-model="sortBy" class="form-select rounded-pill">
              <option value="applied_on">Sort by Date</option>
              <option value="cgpa">Sort by CGPA</option>
              <option value="name">Sort by Name</option>
            </select>
          </div>
          <div class="col-md-2">
            <button class="btn btn-primary-custom w-100" @click="exportApplications">
              <i class="bi bi-download me-2"></i>Export
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
      <p class="text-secondary mt-3">Loading applications...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchApplications">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Applications Table -->
    <div v-else class="card border-0">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover mb-0">
            <thead>
              <tr>
                <th style="width: 50px;">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="selectAll" @change="toggleSelectAll">
                  </div>
                </th>
                <th>Student</th>
                <th>Drive</th>
                <th>Applied On</th>
                <th>CGPA</th>
                <th>Status</th>
                <th style="width: 250px;">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in filteredApplications" :key="app.application_id">
                <td>
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="selectedApps" :value="app.application_id">
                  </div>
                </td>
                <td>
                  <div class="d-flex align-items-center">
                    <div class="student-avatar rounded-circle bg-light d-flex align-items-center justify-content-center me-2"
                         style="width: 35px; height: 35px;">
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
                  <span :class="app.cgpa >= 8 ? 'text-success' : 'text-dark'">
                    {{ app.cgpa }}
                  </span>
                </td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(app.application_status)">
                    {{ app.application_status }}
                  </span>
                </td>
                <td>
                  <div class="d-flex gap-1">
                    <!-- View Details Button -->
                    <button class="btn btn-sm btn-outline-primary" @click="viewApplicationDetails(app)" title="View Details">
                      <i class="bi bi-eye"></i>
                    </button>
                    
                    <!-- Shortlist Button -->
                    <button 
                      class="btn btn-sm" 
                      :class="getShortlistButtonClass(app)"
                      @click="quickUpdate(app, 'shortlisted')" 
                      title="Shortlist"
                      :disabled="!canUpdateStatus(app, 'shortlisted')"
                    >
                      <i class="bi bi-star"></i>
                    </button>
                    
                    <!-- Select Button -->
                    <button 
                      class="btn btn-sm" 
                      :class="getSelectButtonClass(app)"
                      @click="quickUpdate(app, 'selected')" 
                      title="Select"
                      :disabled="!canUpdateStatus(app, 'selected')"
                    >
                      <i class="bi bi-check-circle"></i>
                    </button>
                    
                    <!-- Reject Button -->
                    <button 
                      class="btn btn-sm" 
                      :class="getRejectButtonClass(app)"
                      @click="quickUpdate(app, 'rejected')" 
                      title="Reject"
                      :disabled="!canUpdateStatus(app, 'rejected')"
                    >
                      <i class="bi bi-x-circle"></i>
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredApplications.length === 0">
                <td colspan="7" class="text-center py-4">
                  <p class="text-secondary mb-0">No applications found</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Bulk Actions with Status Validation -->
        <div v-if="selectedApps.length > 0" class="bulk-actions p-3 border-top">
          <div class="d-flex align-items-center gap-3 flex-wrap">
            <span class="text-dark">{{ selectedApps.length }} application(s) selected</span>
            
            <!-- Shortlist Selected Button with validation -->
            <button 
              class="btn btn-sm" 
              :class="getBulkShortlistButtonClass()"
              @click="bulkUpdate('shortlisted')" 
              :disabled="!canBulkUpdate('shortlisted')"
              :title="getBulkButtonTitle('shortlisted')"
            >
              <i class="bi bi-star me-1"></i>Shortlist Selected
            </button>
            
            <!-- Select Selected Button with validation -->
            <button 
              class="btn btn-sm" 
              :class="getBulkSelectButtonClass()"
              @click="bulkUpdate('selected')" 
              :disabled="!canBulkUpdate('selected')"
              :title="getBulkButtonTitle('selected')"
            >
              <i class="bi bi-check-circle me-1"></i>Select Selected
            </button>
            
            <!-- Reject Selected Button with validation -->
            <button 
              class="btn btn-sm" 
              :class="getBulkRejectButtonClass()"
              @click="bulkUpdate('rejected')" 
              :disabled="!canBulkUpdate('rejected')"
              :title="getBulkButtonTitle('rejected')"
            >
              <i class="bi bi-x-circle me-1"></i>Reject Selected
            </button>
            
            <button class="btn btn-sm btn-outline-secondary" @click="selectedApps = []">
              Clear
            </button>
          </div>
          
          <!-- Status Summary -->
          <div v-if="selectedApps.length > 0" class="mt-2 small text-secondary">
            <span>Selected applications status distribution: </span>
            <span v-for="(count, status) in selectedStatusCounts" :key="status" class="me-2">
              <span class="badge" :class="getStatusBadgeClass(status)">{{ status }}: {{ count }}</span>
            </span>
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
  name: 'CompanyApplications',

  setup() {
    const router = useRouter();
    return { router };
  },

  data() {
    return {
      loading: false,
      error: null,
      applications: [],
      jobs: [],
      searchQuery: '',
      jobFilter: '',
      statusFilter: '',
      sortBy: 'applied_on',
      selectedApps: [],
      selectAll: false,
      statusOrder: ['applied', 'shortlisted', 'selected', 'rejected']
    };
  },

  computed: {
    filteredApplications() {
      let filtered = [...this.applications];

      // Search filter
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(app => 
          app.full_name.toLowerCase().includes(query) ||
          app.student_email?.toLowerCase().includes(query)
        );
      }

      // Job filter
      if (this.jobFilter) {
        filtered = filtered.filter(app => app.job_id === Number(this.jobFilter));
      }

      // Status filter
      if (this.statusFilter) {
        filtered = filtered.filter(app => app.application_status === this.statusFilter);
      }

      // Sorting
      filtered.sort((a, b) => {
        switch(this.sortBy) {
          case 'cgpa':
            return b.cgpa - a.cgpa;
          case 'name':
            return a.full_name.localeCompare(b.full_name);
          default:
            return new Date(b.applied_on) - new Date(a.applied_on);
        }
      });

      return filtered;
    },

    // Get selected applications objects
    selectedApplications() {
      return this.applications.filter(app => this.selectedApps.includes(app.application_id));
    },

    // Count statuses of selected applications
    selectedStatusCounts() {
      const counts = {};
      this.selectedApplications.forEach(app => {
        counts[app.application_status] = (counts[app.application_status] || 0) + 1;
      });
      return counts;
    }
  },

  mounted() {
    this.fetchApplications();
    this.fetchJobs();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchApplications() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/applications",
          this.getAuthHeader()
        );

        this.applications = res.data || [];

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load applications";
      } finally {
        this.loading = false;
      }
    },

    async fetchJobs() {
      try {
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/dashboard",
          this.getAuthHeader()
        );
        this.jobs = res.data.jobs || [];
      } catch (err) {
        console.error('Failed to fetch jobs:', err);
      }
    },

    // Check if a single application can be updated to a specific status
    canUpdateStatus(app, targetStatus) {
      const currentStatus = app.application_status;
      
      switch(targetStatus) {
        case 'shortlisted':
          return !['shortlisted', 'selected', 'rejected'].includes(currentStatus);
        case 'selected':
          return !['selected', 'rejected'].includes(currentStatus);
        case 'rejected':
          return currentStatus !== 'rejected';
        default:
          return false;
      }
    },

    // Check if bulk update to a specific status is possible
    canBulkUpdate(targetStatus) {
      if (this.selectedApplications.length === 0) return false;
      
      // Check each selected application
      return this.selectedApplications.every(app => this.canUpdateStatus(app, targetStatus));
    },

    // Get title for bulk button explaining why it's disabled
    getBulkButtonTitle(targetStatus) {
      if (this.selectedApplications.length === 0) return 'No applications selected';
      
      const invalidApps = this.selectedApplications.filter(app => !this.canUpdateStatus(app, targetStatus));
      
      if (invalidApps.length === 0) return `Update all ${this.selectedApplications.length} applications to ${targetStatus}`;
      
      const statuses = [...new Set(invalidApps.map(app => app.application_status))];
      return `${invalidApps.length} application(s) cannot be updated to ${targetStatus} due to their current status: ${statuses.join(', ')}`;
    },

    // Button class methods for individual actions
    getShortlistButtonClass(app) {
      if (!this.canUpdateStatus(app, 'shortlisted')) return 'btn-outline-secondary';
      return 'btn-outline-warning';
    },

    getSelectButtonClass(app) {
      if (!this.canUpdateStatus(app, 'selected')) return 'btn-outline-secondary';
      return 'btn-outline-success';
    },

    getRejectButtonClass(app) {
      if (!this.canUpdateStatus(app, 'rejected')) return 'btn-outline-secondary';
      return 'btn-outline-danger';
    },

    // Bulk button classes
    getBulkShortlistButtonClass() {
      if (!this.canBulkUpdate('shortlisted')) return 'btn-outline-secondary';
      return 'btn-outline-warning';
    },

    getBulkSelectButtonClass() {
      if (!this.canBulkUpdate('selected')) return 'btn-outline-secondary';
      return 'btn-outline-success';
    },

    getBulkRejectButtonClass() {
      if (!this.canBulkUpdate('rejected')) return 'btn-outline-secondary';
      return 'btn-outline-danger';
    },

    viewApplicationDetails(app) {
      this.router.push(`/company/dashboard/applications/${app.application_id}`);
    },

    async quickUpdate(app, status) {
      if (!this.canUpdateStatus(app, status)) {
        alert(`Cannot mark as ${status} due to current status: ${app.application_status}`);
        return;
      }

      if (!confirm(`Mark ${app.full_name} as ${status}?`)) return;

      try {
        await axios.put(
          `http://127.0.0.1:5000/api/company/applications/${app.application_id}/status`,
          { status },
          this.getAuthHeader()
        );

        alert(`Application marked as ${status}!`);
        this.fetchApplications();

      } catch (err) {
        alert(err.response?.data?.msg || "Failed to update status");
      }
    },

    async bulkUpdate(targetStatus) {
      if (this.selectedApps.length === 0) return;

      // Validate all selected applications can be updated
      if (!this.canBulkUpdate(targetStatus)) {
        alert(`Some selected applications cannot be updated to ${targetStatus} due to their current status.`);
        return;
      }

      const statusCounts = this.selectedStatusCounts;
      const statusSummary = Object.entries(statusCounts)
        .map(([status, count]) => `${count} ${status}`)
        .join(', ');

      if (!confirm(`Update ${this.selectedApps.length} application(s) to ${targetStatus}?\n\nCurrent status distribution: ${statusSummary}`)) {
        return;
      }

      try {
        let successCount = 0;
        let failCount = 0;

        for (const appId of this.selectedApps) {
          try {
            await axios.put(
              `http://127.0.0.1:5000/api/company/applications/${appId}/status`,
              { status: targetStatus },
              this.getAuthHeader()
            );
            successCount++;
          } catch (err) {
            console.error(`Failed to update application ${appId}:`, err);
            failCount++;
          }
        }
        
        if (failCount === 0) {
          alert(`Successfully updated all ${successCount} application(s) to ${targetStatus}!`);
        } else {
          alert(`Updated ${successCount} application(s) to ${targetStatus}. Failed to update ${failCount} application(s).`);
        }
        
        this.selectedApps = [];
        this.selectAll = false;
        this.fetchApplications();
        
      } catch (err) {
        alert('Failed to update some applications');
      }
    },

    toggleSelectAll() {
      if (this.selectAll) {
        this.selectedApps = this.filteredApplications.map(a => a.application_id);
      } else {
        this.selectedApps = [];
      }
    },

    exportApplications() {
      const headers = ['Student Name', 'Email', 'Branch', 'Year', 'CGPA', 'Job Role', 'Status', 'Applied On'];
      const data = this.filteredApplications.map(app => [
        app.full_name,
        app.student_email,
        app.branch,
        app.year,
        app.cgpa,
        app.job_role,
        app.application_status,
        new Date(app.applied_on).toLocaleDateString()
      ]);

      const csv = [headers, ...data].map(row => row.join(',')).join('\n');
      
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `applications_${new Date().toISOString().split('T')[0]}.csv`;
      a.click();
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
  },

  watch: {
    selectedApps() {
      this.selectAll = this.selectedApps.length === this.filteredApplications.length && this.filteredApplications.length > 0;
    }
  }
};
</script>

<style scoped>
.company-applications {
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

/* Table */
.table {
  margin-bottom: 0;
}

.table th {
  background: #f8f9fa;
  border-bottom: 2px solid #e0e0e0;
  color: #666;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 1rem;
}

.table td {
  padding: 1rem;
  vertical-align: middle;
  border-bottom: 1px solid #f0f0f0;
}

.student-avatar {
  width: 35px;
  height: 35px;
  background: #f0f0f0;
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

.btn-outline-primary,
.btn-outline-success,
.btn-outline-warning,
.btn-outline-danger,
.btn-outline-secondary {
  border-width: 2px;
  border-radius: 8px;
  padding: 0.25rem 0.5rem;
  font-size: 0.85rem;
  transition: all 0.3s ease;
}

.btn-outline-primary {
  border-color: #667eea;
  color: #667eea;
  background: white;
}

.btn-outline-primary:hover:not(:disabled) {
  background: #667eea;
  color: white;
}

.btn-outline-warning {
  border-color: #f59e0b;
  color: #f59e0b;
  background: white;
}

.btn-outline-warning:hover:not(:disabled) {
  background: #f59e0b;
  color: white;
}

.btn-outline-success {
  border-color: #10b981;
  color: #10b981;
  background: white;
}

.btn-outline-success:hover:not(:disabled) {
  background: #10b981;
  color: white;
}

.btn-outline-danger {
  border-color: #ef4444;
  color: #ef4444;
  background: white;
}

.btn-outline-danger:hover:not(:disabled) {
  background: #ef4444;
  color: white;
}

.btn-outline-secondary {
  border-color: #6c757d;
  color: #6c757d;
  background: white;
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-outline-secondary:hover {
  background: #6c757d;
  color: white;
}

/* Badge Styles */
.badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.bg-primary {
  background: #667eea !important;
  color: white;
}

.badge.bg-warning {
  background: #f59e0b !important;
  color: white;
}

.badge.bg-success {
  background: #10b981 !important;
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

/* Bulk Actions */
.bulk-actions {
  background: #f8f9fa;
  border-bottom-left-radius: 12px;
  border-bottom-right-radius: 12px;
}

/* Responsive */
@media (max-width: 768px) {
  .d-flex.gap-1 {
    flex-direction: column;
    gap: 0.25rem !important;
  }
  
  .btn-sm {
    width: 100%;
  }
  
  .bulk-actions .d-flex {
    flex-direction: column;
    align-items: flex-start !important;
  }
}
</style>