<template>
  <div class="admin-drives">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Placement Drives</h1>
      <p class="text-muted">Manage and approve placement drives</p>
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
              <input type="text" v-model="searchQuery" placeholder="Search drives..." 
                     class="form-control border-start-0 rounded-end-pill">
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="statusFilter" class="form-select rounded-pill">
              <option value="">All Status</option>
              <option value="pending">Pending</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
              <option value="closed">Closed</option>
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

    <!-- Drives Table -->
    <div class="card border-0">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Drive Details</th>
                <th>Company</th>
                <th>Deadline</th>
                <th>Drive Date</th>
                <th>Applications</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in filteredDrives" :key="drive.id">
                <td>
                  <strong>{{ drive.role }}</strong><br>
                  <small class="text-secondary">{{ drive.job_type }}</small>
                </td>
                <td>{{ drive.company }}</td>
                <td>{{ formatDate(drive.deadline) }}</td>
                <td>{{ formatDate(drive.drive_date) || 'TBD' }}</td>
                <td>
                  <span class="badge bg-primary rounded-pill">{{ drive.applications_count }}</span>
                </td>
                <td>
                  <span class="badge" :class="getStatusBadgeClass(drive.status)">
                    {{ drive.status }}
                  </span>
                </td>
                <td>
                  <div class="btn-group gap-1">
                    <button class="btn btn-sm btn-outline-success rounded-pill" @click="approveDrive(drive.id)"
                            :disabled="drive.status === 'approved'">
                      <i class="bi bi-check-lg"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger rounded-pill" @click="rejectDrive(drive.id)"
                            :disabled="drive.status === 'rejected'">
                      <i class="bi bi-x-lg"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-primary rounded-pill" @click="viewDrive(drive.id)">
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
  name: 'AdminDrives',

  data() {
    return {
      drives: [],
      companies: [],
      searchQuery: '',
      statusFilter: '',
      companyFilter: ''
    };
  },

  computed: {
    filteredDrives() {
      let filtered = this.drives;
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(d => 
          d.role.toLowerCase().includes(query) || 
          d.company.toLowerCase().includes(query)
        );
      }
      
      if (this.statusFilter) {
        filtered = filtered.filter(d => d.status === this.statusFilter);
      }
      
      if (this.companyFilter) {
        filtered = filtered.filter(d => d.company_id === parseInt(this.companyFilter));
      }
      
      return filtered;
    }
  },

  mounted() {
    this.fetchDrives();
    this.fetchCompanies();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchDrives() {
      try {
        const res = await axios.get("http://127.0.0.1:5000/api/admin/drives", this.getAuthHeader());
        this.drives = res.data;
      } catch (err) {
        console.error('Failed to fetch drives:', err);
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

    async approveDrive(id) {
      if (confirm('Approve this drive?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/drives/${id}/approve`, {}, this.getAuthHeader());
          await this.fetchDrives();
          alert('Drive approved successfully');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to approve drive');
        }
      }
    },

    async rejectDrive(id) {
      if (confirm('Reject this drive?')) {
        try {
          await axios.put(`http://127.0.0.1:5000/api/admin/drives/${id}/reject`, {}, this.getAuthHeader());
          await this.fetchDrives();
          alert('Drive rejected');
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to reject drive');
        }
      }
    },

    viewDrive(id) {
      this.$router.push(`/admin/dashboard/drives/${id}`);
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
.admin-drives {
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

.btn-group {
  gap: 0.25rem;
}

.btn-outline-success,
.btn-outline-danger,
.btn-outline-primary {
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

.btn-outline-primary:hover {
  background: #667eea;
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