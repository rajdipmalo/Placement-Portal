<template>
  <div class="admin-drive-details">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to Drives
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
                   :style="{ background: driveColor }">
                <i class="bi bi-briefcase fs-1 text-white"></i>
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-1">{{ drive.role }}</h2>
              <p class="text-primary mb-2">{{ drive.company }}</p>
              <div class="d-flex gap-3 flex-wrap">
                <span class="badge bg-light text-dark">
                  <i class="bi bi-briefcase me-1"></i>{{ drive.job_type }}
                </span>
                <span class="badge" :class="getStatusBadgeClass(drive.status)">
                  {{ drive.status }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-people me-1"></i>{{ drive.stats?.total || 0 }} Applications
                </span>
              </div>
            </div>
            <div class="col-auto">
              <div class="btn-group gap-2">
                <button class="btn btn-outline-success rounded-pill" @click="approveDrive"
                        :disabled="drive.status === 'approved'">
                  <i class="bi bi-check-lg me-2"></i>Approve
                </button>
                <button class="btn btn-outline-danger rounded-pill" @click="rejectDrive"
                        :disabled="drive.status === 'rejected'">
                  <i class="bi bi-x-lg me-2"></i>Reject
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Drive Details Grid -->
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
                        class="badge bg-light text-dark p-3 rounded-pill">
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
                      class="badge bg-primary p-3 rounded-pill">
                  {{ skill }}
                </span>
                <span v-if="!drive.skills_required?.length" class="text-secondary">
                  No specific skills required
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Info & Stats -->
        <div class="col-lg-4">
          <!-- Key Info Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-info-circle text-primary me-2"></i>Key Information
              </h5>
              
              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-cash text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Salary</small>
                  <strong class="text-dark">{{ drive.salary || 'Not specified' }}</strong>
                </div>
              </div>

              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-geo-alt text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Location</small>
                  <strong class="text-dark">{{ drive.drive_location || 'Not specified' }}</strong>
                </div>
              </div>

              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-calendar text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Deadline</small>
                  <strong class="text-dark">{{ formatDate(drive.deadline) }}</strong>
                </div>
              </div>

              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-calendar-event text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Drive Date</small>
                  <strong class="text-dark">{{ formatDate(drive.drive_date) || 'TBD' }}</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- Statistics Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-graph-up text-primary me-2"></i>Application Statistics
              </h5>
              
              <div class="stats-list">
                <div class="stat-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded-3">
                  <span class="text-secondary">Total Applications</span>
                  <span class="h4 mb-0 text-primary">{{ drive.stats?.total || 0 }}</span>
                </div>
                <div class="stat-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded-3">
                  <span class="text-secondary">Shortlisted</span>
                  <span class="h4 mb-0 text-warning">{{ drive.stats?.shortlisted || 0 }}</span>
                </div>
                <div class="stat-item d-flex justify-content-between align-items-center mb-3 p-3 bg-light rounded-3">
                  <span class="text-secondary">Selected</span>
                  <span class="h4 mb-0 text-success">{{ drive.stats?.selected || 0 }}</span>
                </div>
                <div class="stat-item d-flex justify-content-between align-items-center p-3 bg-light rounded-3">
                  <span class="text-secondary">Rejected</span>
                  <span class="h4 mb-0 text-danger">{{ drive.stats?.rejected || 0 }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Applications Table -->
      <div class="card border-0 mt-4">
        <div class="card-body">
          <h5 class="text-dark mb-3">
            <i class="bi bi-people text-primary me-2"></i>Applications ({{ drive.applications?.length || 0 }})
          </h5>
          <div class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Student</th>
                  <th>Email</th>
                  <th>Applied On</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in drive.applications" :key="app.id">
                  <td>{{ app.student_name }}</td>
                  <td>{{ app.student_email }}</td>
                  <td>{{ formatDate(app.applied_on) }}</td>
                  <td>
                    <span class="badge" :class="getApplicationStatusBadgeClass(app.status)">
                      {{ app.status }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-sm btn-outline-primary rounded-pill" @click="viewApplication(app.id)">
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
</template>

<script>
import axios from "axios";

export default {
  name: 'AdminDriveDetails',

  props: {
    driveId: {
      type: [String, Number],
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      drive: null
    };
  },

  computed: {
    driveColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.drive?.role) return colors[0];
      let hash = 0;
      for (let i = 0; i < this.drive.role.length; i++) {
        hash = ((hash << 5) - hash) + this.drive.role.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
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
          `http://127.0.0.1:5000/api/admin/drives/${this.driveId}`,
          this.getAuthHeader()
        );
        this.drive = res.data;
      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load drive details";
      } finally {
        this.loading = false;
      }
    },

    async approveDrive() {
      if (confirm('Approve this drive?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/drives/${this.driveId}/approve`, {}, this.getAuthHeader());
          await this.fetchDriveDetails();
          alert('Drive approved successfully');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to approve drive');
        }
      }
    },

    async rejectDrive() {
      if (confirm('Reject this drive?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/drives/${this.driveId}/reject`, {}, this.getAuthHeader());
          await this.fetchDriveDetails();
          alert('Drive rejected');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to reject drive');
        }
      }
    },

    viewApplication(id) {
      this.$router.push(`/admin/dashboard/applications/${id}`);
    },

    goBack() {
      this.$router.push('/admin/dashboard/drives');
    },

    getStatusBadgeClass(status) {
      const classes = {
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'rejected': 'bg-danger',
        'closed': 'bg-secondary'
      };
      return classes[status] || 'bg-secondary';
    },

    getApplicationStatusBadgeClass(status) {
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
  }
};
</script>

<style scoped>
.admin-drive-details {
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

.drive-icon-large {
  width: 80px;
  height: 80px;
}

.card {
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.eligibility-box {
  transition: all 0.3s ease;
}

.eligibility-box:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.info-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.key-info-item {
  padding: 0.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.key-info-item:hover {
  background: #f8f9fa;
}

.stat-item {
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateX(5px);
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