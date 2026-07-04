<template>
  <div class="admin-companies">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Companies Management</h1>
      <p class="text-muted">Manage and approve company registrations</p>
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
              <input type="text" v-model="searchQuery" placeholder="Search companies..." 
                     class="form-control border-start-0 rounded-end-pill">
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="statusFilter" class="form-select rounded-pill">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
              <option value="blacklisted">Blacklisted</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Companies Table -->
    <div class="card border-0">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Company</th>
                <th>Industry</th>
                <th>Location</th>
                <th>Contact</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="company in filteredCompanies" :key="company.id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="company-logo-small rounded-circle me-2 d-flex align-items-center justify-content-center"
                         :style="{ background: getCompanyColor(company.name) }">
                      {{ company.name.charAt(0) }}
                    </div>
                    <div>
                      <strong>{{ company.name }}</strong><br>
                      <small class="text-secondary">{{ company.email }}</small>
                    </div>
                  </div>
                </td>
                <td>{{ company.industry || 'N/A' }}</td>
                <td>{{ company.location || 'N/A' }}</td>
                <td>
                  <small>{{ company.hr_email || 'N/A' }}<br>{{ company.hr_contact || 'N/A' }}</small>
                </td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(company.status, company.is_blacklisted)">
                    {{ company.is_blacklisted ? 'Blacklisted' : company.status }}
                  </span>
                </td>
                <td>
                  <div class="btn-group gap-1">
                    <button class="btn btn-sm btn-outline-success rounded-pill" @click="approveCompany(company.id)"
                            :disabled="company.status === 'approved' || company.is_blacklisted">
                      <i class="bi bi-check-lg"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger rounded-pill" @click="rejectCompany(company.id)"
                            :disabled="company.status === 'rejected' || company.is_blacklisted">
                      <i class="bi bi-x-lg"></i>
                    </button>
                    <button class="btn btn-sm rounded-pill" 
                            :class="company.is_blacklisted ? 'btn-outline-warning' : 'btn-outline-secondary'"
                            @click="toggleBlacklist(company)">
                      <i :class="company.is_blacklisted ? 'bi bi-person-up' : 'bi bi-person-down'"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-primary rounded-pill"
                            @click="viewCompany(company.id)">
                      <i class="bi bi-eye"></i>
                    </button>
                  </div>
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
  name: 'AdminCompanies',

  data() {
    return {
      companies: [],
      searchQuery: '',
      statusFilter: ''
    };
  },

  computed: {
    filteredCompanies() {
      let filtered = this.companies;
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(c => 
          c.name.toLowerCase().includes(query) || 
          c.email.toLowerCase().includes(query)
        );
      }
      
      if (this.statusFilter) {
        if (this.statusFilter === 'blacklisted') {
          filtered = filtered.filter(c => c.is_blacklisted);
        } else {
          filtered = filtered.filter(c => c.status === this.statusFilter);
        }
      }
      
      return filtered;
    }
  },

  mounted() {
    this.fetchCompanies();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchCompanies() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/admin/companies", this.getAuthHeader());
        this.companies = res.data;
      } catch (err) {
        console.error('Failed to fetch companies:', err);
      }
    },

    async approveCompany(id) {
      if (confirm('Approve this company?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/companies/${id}/approve`, {}, this.getAuthHeader());
          await this.fetchCompanies();
          alert('Company approved successfully');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to approve company');
        }
      }
    },

    async rejectCompany(id) {
      if (confirm('Reject this company?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/companies/${id}/reject`, {}, this.getAuthHeader());
          await this.fetchCompanies();
          alert('Company rejected');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to reject company');
        }
      }
    },

    async toggleBlacklist(company) {
      const action = company.is_blacklisted ? 'remove from' : 'add to';
      if (confirm(`Are you sure you want to ${action} blacklist?`)) {
        try {
          if (company.is_blacklisted) {
            await axios.put(`http://127.0.0.1:5000/api/admin/companies/${company.id}/unblacklist`, {}, this.getAuthHeader());
          } else {
            await axios.put(`http://127.0.0.1:5000/api/admin/companies/${company.id}/blacklist`, {}, this.getAuthHeader());
          }
          await this.fetchCompanies();
          alert(`Company ${company.is_blacklisted ? 'removed from' : 'added to'} blacklist`);
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to update blacklist');
        }
      }
    },

    viewCompany(id) {
      this.$router.push(`/admin/dashboard/companies/${id}`);
    },

    getCompanyColor(name) {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!name) return colors[0];
      let hash = 0;
      for (let i = 0; i < name.length; i++) {
        hash = ((hash << 5) - hash) + name.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
    },

    getStatusBadgeClass(status, isBlacklisted) {
      if (isBlacklisted) return 'bg-dark';
      const classes = {
        'approved': 'bg-success',
        'pending': 'bg-warning',
        'rejected': 'bg-danger'
      };
      return classes[status] || 'bg-secondary';
    }
  }
};
</script>

<style scoped>
.admin-companies {
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

.company-logo-small {
  width: 40px;
  height: 40px;
  font-size: 1.2rem;
  font-weight: 600;
  color: white;
}

.btn-group {
  gap: 0.25rem;
}

.btn-outline-success,
.btn-outline-danger,
.btn-outline-secondary,
.btn-outline-warning {
  border-width: 2px;
  transition: all 0.3s ease;
}

.btn-outline-success:hover:not(:disabled) {
  background: #10b981;
  color: white;
}

.btn-outline-danger:hover:not(:disabled) {
  background: #ef4444;
  color: white;
}

.btn-outline-warning:hover {
  background: #f59e0b;
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