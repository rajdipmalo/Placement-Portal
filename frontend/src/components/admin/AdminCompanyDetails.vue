<template>
  <div class="admin-company-details">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to Companies
    </button>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading company details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchCompanyDetails">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Company Details Content -->
    <div v-else-if="company" class="company-details-container">
      <!-- Header Card -->
      <div class="header-card card border-0 mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="company-logo-large rounded-circle d-flex align-items-center justify-content-center"
                   :style="{ background: companyColor }">
                {{ company.name.charAt(0) }}
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-1">{{ company.name }}</h2>
              <p class="text-primary mb-2">{{ company.email }}</p>
              <div class="d-flex gap-3 flex-wrap">
                <span class="badge bg-light text-dark">
                  <i class="bi bi-building me-1"></i>{{ company.industry || 'N/A' }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-geo-alt me-1"></i>{{ company.location || 'N/A' }}
                </span>
                <span class="badge" :class="getStatusBadgeClass(company.status, company.is_blacklisted)">
                  {{ company.is_blacklisted ? 'Blacklisted' : company.status }}
                </span>
              </div>
            </div>
            <div class="col-auto">
              <div class="btn-group gap-2">
                <button class="btn btn-outline-success rounded-pill" @click="approveCompany"
                        :disabled="company.status === 'approved' || company.is_blacklisted">
                  <i class="bi bi-check-lg me-2"></i>Approve
                </button>
                <button class="btn btn-outline-danger rounded-pill" @click="rejectCompany"
                        :disabled="company.status === 'rejected' || company.is_blacklisted">
                  <i class="bi bi-x-lg me-2"></i>Reject
                </button>
                <button class="btn rounded-pill" :class="company.is_blacklisted ? 'btn-outline-warning' : 'btn-outline-secondary'"
                        @click="toggleBlacklist">
                  <i :class="company.is_blacklisted ? 'bi bi-person-up' : 'bi bi-person-down'" class="me-2"></i>
                  {{ company.is_blacklisted ? 'Remove Blacklist' : 'Blacklist' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Company Details Grid -->
      <div class="row g-4">
        <!-- Left Column - Company Info -->
        <div class="col-lg-4">
          <!-- Company Information -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-info-circle text-primary me-2"></i>Company Information
              </h5>
              <div class="info-list">
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Company Name</div>
                  <div class="info-value text-dark fw-medium">{{ company.name }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Email</div>
                  <div class="info-value text-dark">{{ company.email }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Industry</div>
                  <div class="info-value text-dark">{{ company.industry || 'N/A' }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Location</div>
                  <div class="info-value text-dark">{{ company.location || 'N/A' }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Website</div>
                  <div class="info-value text-dark">
                    <a v-if="company.website" :href="company.website" target="_blank" class="text-primary">
                      {{ company.website }}
                    </a>
                    <span v-else>N/A</span>
                  </div>
                </div>
                <div class="info-item d-flex">
                  <div class="info-label w-50 text-secondary">Member Since</div>
                  <div class="info-value text-dark">{{ formatDate(company.created_at) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Information -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-telephone text-primary me-2"></i>Contact Information
              </h5>
              <div class="info-list">
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">HR Email</div>
                  <div class="info-value text-dark">{{ company.hr_email || 'N/A' }}</div>
                </div>
                <div class="info-item d-flex">
                  <div class="info-label w-50 text-secondary">HR Contact</div>
                  <div class="info-value text-dark">{{ company.hr_contact || 'N/A' }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Statistics -->
          <div class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-graph-up text-primary me-2"></i>Statistics
              </h5>
              <div class="row g-3">
                <div class="col-6">
                  <div class="stat-box bg-light p-3 rounded-3 text-center">
                    <h3 class="h4 mb-1 text-dark">{{ company.jobs_count || 0 }}</h3>
                    <small class="text-secondary">Total Drives</small>
                  </div>
                </div>
                <div class="col-6">
                  <div class="stat-box bg-light p-3 rounded-3 text-center">
                    <h3 class="h4 mb-1 text-dark">{{ company.applications_count || 0 }}</h3>
                    <small class="text-secondary">Applications</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Jobs -->
        <div class="col-lg-8">
          <div class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-briefcase text-primary me-2"></i>Placement Drives ({{ company.jobs?.length || 0 }})
              </h5>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Role</th>
                      <th>Deadline</th>
                      <th>Applications</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="job in company.jobs" :key="job.id">
                      <td>
                        <strong>{{ job.role }}</strong>
                      </td>
                      <td>{{ formatDate(job.deadline) }}</td>
                      <td>
                        <span class="badge bg-primary rounded-pill">{{ job.applications_count }}</span>
                      </td>
                      <td>
                        <span class="badge" :class="getJobStatusBadgeClass(job.status)">
                          {{ job.status }}
                        </span>
                      </td>
                      <td>
                        <button class="btn btn-sm btn-outline-primary rounded-pill" @click="viewDrive(job.id)">
                          <i class="bi bi-eye"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
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

export default {
  name: 'AdminCompanyDetails',

  props: {
    companyId: {
      type: [String, Number],
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      company: null
    };
  },

  computed: {
    companyColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.company?.name) return colors[0];
      let hash = 0;
      for (let i = 0; i < this.company.name.length; i++) {
        hash = ((hash << 5) - hash) + this.company.name.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
    }
  },

  mounted() {
    this.fetchCompanyDetails();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchCompanyDetails() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/admin/companies/${this.companyId}`,
          this.getAuthHeader()
        );
        this.company = res.data;
      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load company details";
      } finally {
        this.loading = false;
      }
    },

    async approveCompany() {
      if (confirm('Approve this company?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/companies/${this.companyId}/approve`, {}, this.getAuthHeader());
          await this.fetchCompanyDetails();
          alert('Company approved successfully');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to approve company');
        }
      }
    },

    async rejectCompany() {
      if (confirm('Reject this company?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/companies/${this.companyId}/reject`, {}, this.getAuthHeader());
          await this.fetchCompanyDetails();
          alert('Company rejected');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to reject company');
        }
      }
    },

    async toggleBlacklist() {
      const action = this.company.is_blacklisted ? 'remove from' : 'add to';
      if (confirm(`Are you sure you want to ${action} blacklist?`)) {
        try {
          if (this.company.is_blacklisted) {
            await axios.put(`http://127.0.0.1:5000/api/admin/companies/${this.companyId}/unblacklist`, {}, this.getAuthHeader());
          } else {
            await axios.put(`http://127.0.0.1:5000/api/admin/companies/${this.companyId}/blacklist`, {}, this.getAuthHeader());
          }
          await this.fetchCompanyDetails();
          alert(`Company ${this.company.is_blacklisted ? 'removed from' : 'added to'} blacklist`);
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to update blacklist');
        }
      }
    },

    viewDrive(id) {
      this.$router.push(`/admin/dashboard/drives/${id}`);
    },

    goBack() {
      this.$router.push('/admin/dashboard/companies');
    },

    getStatusBadgeClass(status, isBlacklisted) {
      if (isBlacklisted) return 'bg-dark';
      const classes = {
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'rejected': 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    },

    getJobStatusBadgeClass(status) {
      const classes = {
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'rejected': 'bg-danger',
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
.admin-company-details {
  color: #333;
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

.header-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.company-logo-large {
  width: 80px;
  height: 80px;
  font-size: 36px;
  font-weight: 600;
  color: white;
}

.card {
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.info-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.stat-box {
  transition: all 0.3s ease;
}

.stat-box:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.table th {
  font-weight: 600;
  color: #4b5563;
  border-bottom-width: 2px;
}

.table td {
  vertical-align: middle;
}

.btn-group {
  gap: 0.5rem;
}
</style>