<template>
  <div class="admin-applications">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Applications Management</h1>
      <p class="text-muted">View all student applications</p>
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
              <input type="text" v-model="searchQuery" placeholder="Search applications..." 
                     class="form-control border-start-0 rounded-end-pill">
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="statusFilter" class="form-select rounded-pill">
              <option value="">All Status</option>
              <option value="applied">Applied</option>
              <option value="shortlisted">Shortlisted</option>
              <option value="selected">Selected</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="companyFilter" class="form-select rounded-pill">
              <option value="">All Companies</option>
              <option v-for="company in companies" :key="company.id" :value="company.id">
                {{ company.name }}
              </option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Applications Table -->
    <div class="card border-0">
      <div class="card-body">
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
              <tr v-for="app in filteredApplications" :key="app.id">
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
                <td>{{ app.job_role }}</td>
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
  name: 'AdminApplications',

  data() {
    return {
      applications: [],
      companies: [],
      searchQuery: '',
      statusFilter: '',
      companyFilter: ''
    };
  },

  computed: {
    filteredApplications() {
      let filtered = this.applications;
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(a => 
          a.student_name.toLowerCase().includes(query) || 
          a.company.toLowerCase().includes(query) ||
          a.job_role.toLowerCase().includes(query)
        );
      }
      
      if (this.statusFilter) {
        filtered = filtered.filter(a => a.status === this.statusFilter);
      }
      
      if (this.companyFilter) {
        filtered = filtered.filter(a => a.company_id === parseInt(this.companyFilter));
      }
      
      return filtered;
    }
  },

  mounted() {
    this.fetchApplications();
    this.fetchCompanies();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchApplications() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/admin/applications", this.getAuthHeader());
        this.applications = res.data;
      } catch (err) {
        console.error('Failed to fetch applications:', err);
      }
    },

    async fetchCompanies() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/admin/companies?status=approved", this.getAuthHeader());
        this.companies = res.data;
      } catch (err) {
        console.error('Failed to fetch companies:', err);
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
.admin-applications {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.filters-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.student-avatar-small {
  width: 35px;
  height: 35px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
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