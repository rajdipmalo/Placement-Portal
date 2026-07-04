<template>
  <div class="admin-home">
    <!-- Welcome Section -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Admin Dashboard</h1>
      <p class="text-muted">Welcome back, {{ adminName }}! Here's what's happening today.</p>
    </div>

    <!-- Stats Cards -->
    <div class="row g-4 mb-4">
      <div class="col-md-3 col-sm-6" v-for="stat in stats" :key="stat.label">
        <div class="stat-card card border-0">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="stat-icon rounded-circle me-3 d-flex align-items-center justify-content-center"
                   :style="{ background: stat.color }">
                <i :class="stat.icon" class="text-white"></i>
              </div>
              <div>
                <h3 class="h2 mb-0 text-dark">{{ stat.value }}</h3>
                <small class="text-secondary">{{ stat.label }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Approvals Row -->
    <div class="row g-4 mb-4">
      <!-- Pending Companies -->
      <div class="col-lg-6">
        <div class="card border-0">
          <div class="card-body">
            <h5 class="text-dark mb-3">
              <i class="bi bi-building text-primary me-2"></i>Pending Company Approvals
              <span v-if="pendingCompanies.length" class="badge bg-warning ms-2">{{ pendingCompanies.length }}</span>
            </h5>
            <div v-if="pendingCompanies.length === 0" class="text-center py-4">
              <i class="bi bi-check-circle text-success fs-1"></i>
              <p class="text-secondary mt-2">No pending company approvals</p>
            </div>
            <div v-else>
              <div v-for="company in pendingCompanies.slice(0, 3)" :key="company.id" 
                   class="pending-item d-flex justify-content-between align-items-center p-3 mb-2 bg-light rounded-3">
                <div>
                  <h6 class="text-dark mb-1">{{ company.name }}</h6>
                  <small class="text-secondary">{{ company.industry || 'N/A' }} • {{ company.location || 'N/A' }}</small>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-success rounded-pill" @click="approveCompany(company.id)">
                    <i class="bi bi-check-lg"></i>
                  </button>
                  <button class="btn btn-sm btn-danger rounded-pill" @click="rejectCompany(company.id)">
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>
              </div>
              <div v-if="pendingCompanies.length > 3" class="text-center mt-3">
                <router-link to="/admin/dashboard/companies?status=pending" class="btn btn-link text-primary">
                  View all {{ pendingCompanies.length }} pending →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Drives -->
      <div class="col-lg-6">
        <div class="card border-0">
          <div class="card-body">
            <h5 class="text-dark mb-3">
              <i class="bi bi-briefcase text-primary me-2"></i>Pending Drive Approvals
              <span v-if="pendingDrives.length" class="badge bg-warning ms-2">{{ pendingDrives.length }}</span>
            </h5>
            <div v-if="pendingDrives.length === 0" class="text-center py-4">
              <i class="bi bi-check-circle text-success fs-1"></i>
              <p class="text-secondary mt-2">No pending drive approvals</p>
            </div>
            <div v-else>
              <div v-for="drive in pendingDrives.slice(0, 3)" :key="drive.id" 
                   class="pending-item d-flex justify-content-between align-items-center p-3 mb-2 bg-light rounded-3">
                <div>
                  <h6 class="text-dark mb-1">{{ drive.role }}</h6>
                  <small class="text-secondary">{{ drive.company }} • Deadline: {{ formatDate(drive.deadline) }}</small>
                </div>
                <div class="d-flex gap-2">
                  <button class="btn btn-sm btn-success rounded-pill" @click="approveDrive(drive.id)">
                    <i class="bi bi-check-lg"></i>
                  </button>
                  <button class="btn btn-sm btn-danger rounded-pill" @click="rejectDrive(drive.id)">
                    <i class="bi bi-x-lg"></i>
                  </button>
                </div>
              </div>
              <div v-if="pendingDrives.length > 3" class="text-center mt-3">
                <router-link to="/admin/dashboard/drives?status=pending" class="btn btn-link text-primary">
                  View all {{ pendingDrives.length }} pending →
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Applications -->
    <div class="card border-0">
      <div class="card-body">
        <h5 class="text-dark mb-3">
          <i class="bi bi-file-text text-primary me-2"></i>Recent Applications
        </h5>
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Student</th>
                <th>Company</th>
                <th>Position</th>
                <th>Applied On</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in recentApplications" :key="app.id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="student-avatar-small rounded-circle me-2 d-flex align-items-center justify-content-center"
                         :style="{ background: getAvatarColor(app.student_name) }">
                      {{ getInitials(app.student_name) }}
                    </div>
                    <span>{{ app.student_name }}</span>
                  </div>
                </td>
                <td>{{ app.company }}</td>
                <td>{{ app.position }}</td>
                <td>{{ formatDate(app.applied_on) }}</td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(app.status)">
                    {{ app.status }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-sm btn-outline-primary rounded-pill" @click="viewApplication(app.id)">
                    <i class="bi bi-eye me-1"></i>View
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL } from "@/config";

export default {
  name: 'AdminHome',

  data() {
    return {
      adminName: localStorage.getItem('adminName') || 'Admin',
      stats: [
        { label: 'Total Students', value: 0, icon: 'bi bi-people', color: 'linear-gradient(135deg, #667eea, #764ba2)' },
        { label: 'Total Companies', value: 0, icon: 'bi bi-building', color: 'linear-gradient(135deg, #3b82f6, #1d4ed8)' },
        { label: 'Active Drives', value: 0, icon: 'bi bi-briefcase', color: 'linear-gradient(135deg, #10b981, #059669)' },
        { label: 'Total Placements', value: 0, icon: 'bi bi-trophy', color: 'linear-gradient(135deg, #f59e0b, #d97706)' }
      ],
      pendingCompanies: [],
      pendingDrives: [],
      recentApplications: []
    };
  },

  mounted() {
    this.fetchDashboardData();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchDashboardData() {
      try {
        const [statsRes, companiesRes, drivesRes, appsRes] = await Promise.all([
          axios.get(`${API_URL}/api/admin/dashboard`, this.getAuthHeader()),
          axios.get(`${API_URL}/api/admin/companies?status=pending`, this.getAuthHeader()),
          axios.get(`${API_URL}/api/admin/drives?status=pending`, this.getAuthHeader()),
          axios.get(`${API_URL}/api/admin/applications?limit=5`, this.getAuthHeader())
        ]);

        this.stats = [
          { ...this.stats[0], value: statsRes.data.stats.total_students },
          { ...this.stats[1], value: statsRes.data.stats.total_companies },
          { ...this.stats[2], value: statsRes.data.stats.active_drives },
          { ...this.stats[3], value: statsRes.data.stats.total_placements }
        ];
        
        this.pendingCompanies = companiesRes.data;
        this.pendingDrives = drivesRes.data;
        this.recentApplications = appsRes.data;
      } catch (err) {
        console.error('Failed to fetch dashboard data:', err);
      }
    },

    async approveCompany(id) {
      if (confirm('Approve this company?')) {
        try {
          await axios.put(`${API_URL}/api/admin/companies/${id}/approve`, {}, this.getAuthHeader());
          this.pendingCompanies = this.pendingCompanies.filter(c => c.id !== id);
          alert('Company approved successfully');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to approve company');
        }
      }
    },

    async rejectCompany(id) {
      if (confirm('Reject this company?')) {
        try {
          await axios.put(`${API_URL}/api/admin/companies/${id}/reject`, {}, this.getAuthHeader());
          this.pendingCompanies = this.pendingCompanies.filter(c => c.id !== id);
          alert('Company rejected');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to reject company');
        }
      }
    },

    async approveDrive(id) {
      if (confirm('Approve this drive?')) {
        try {
          await axios.put(`${API_URL}/api/admin/drives/${id}/approve`, {}, this.getAuthHeader());
          this.pendingDrives = this.pendingDrives.filter(d => d.id !== id);
          alert('Drive approved successfully');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to approve drive');
        }
      }
    },

    async rejectDrive(id) {
      if (confirm('Reject this drive?')) {
        try {
          await axios.put(`${API_URL}/api/admin/drives/${id}/reject`, {}, this.getAuthHeader());
          this.pendingDrives = this.pendingDrives.filter(d => d.id !== id);
          alert('Drive rejected');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to reject drive');
        }
      }
    },

    viewApplication(id) {
      this.$router.push(`/admin/dashboard/applications/${id}`);
    },

    getInitials(name) {
      if (!name) return 'U';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },

    getAvatarColor(name) {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!name) return colors[0];
      let hash = 0;
      for (let i = 0; i < name.length; i++) {
        hash = ((hash << 5) - hash) + name.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
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
  }
};
</script>

<style scoped>
.admin-home {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  font-size: 1.5rem;
}

.student-avatar-small {
  width: 35px;
  height: 35px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
}

.pending-item {
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.pending-item:hover {
  background: #ffffff !important;
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.btn-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.btn-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.table th {
  font-weight: 600;
  color: #4b5563;
  border-bottom-width: 2px;
}

.table td {
  vertical-align: middle;
}
</style>