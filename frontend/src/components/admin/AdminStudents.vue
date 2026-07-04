<template>
  <div class="admin-students">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Students Management</h1>
      <p class="text-muted">Manage student profiles and applications</p>
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
              <input type="text" v-model="searchQuery" placeholder="Search students..." 
                     class="form-control border-start-0 rounded-end-pill">
            </div>
          </div>
          <div class="col-md-3">
            <select v-model="branchFilter" class="form-select rounded-pill">
              <option value="">All Branches</option>
              <option value="CSE">Computer Science (CSE)</option>
              <option value="IT">Information Technology (IT)</option>
              <option value="ECE">Electronics (ECE)</option>
              <option value="EEE">Electrical (EEE)</option>
              <option value="MECH">Mechanical (MECH)</option>
              <option value="CIVIL">Civil (CIVIL)</option>
            </select>
          </div>
          <div class="col-md-2">
            <select v-model="yearFilter" class="form-select rounded-pill">
              <option value="">All Years</option>
              <option value="1">1st Year</option>
              <option value="2">2nd Year</option>
              <option value="3">3rd Year</option>
              <option value="4">4th Year</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Students Table -->
    <div class="card border-0">
      <div class="card-body">
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Student</th>
                <th>Branch</th>
                <th>Year</th>
                <th>CGPA</th>
                <th>Applications</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in filteredStudents" :key="student.id">
                <td>
                  <div class="d-flex align-items-center">
                    <div class="student-avatar-small rounded-circle me-2 d-flex align-items-center justify-content-center"
                         :style="{ background: getStudentColor(student.full_name) }">
                      {{ getInitials(student.full_name) }}
                    </div>
                    <div>
                      <strong>{{ student.full_name }}</strong><br>
                      <small class="text-secondary">{{ student.email }}</small>
                    </div>
                  </div>
                </td>
                <td>{{ student.branch }}</td>
                <td>{{ student.year }}</td>
                <td>{{ student.cgpa }}</td>
                <td>
                  <span class="badge bg-primary rounded-pill">{{ student.applications_count }}</span>
                </td>
                <td>
                  <span class="badge" :class="student.is_blacklisted ? 'bg-dark' : 'bg-success'">
                    {{ student.is_blacklisted ? 'Blacklisted' : 'Active' }}
                  </span>
                </td>
                <td>
                  <div class="btn-group gap-1">
                    <button class="btn btn-sm btn-outline-primary rounded-pill" @click="viewStudent(student.id)">
                      <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm rounded-pill" 
                            :class="student.is_blacklisted ? 'btn-outline-warning' : 'btn-outline-secondary'"
                            @click="toggleBlacklist(student)">
                      <i :class="student.is_blacklisted ? 'bi bi-person-up' : 'bi bi-person-down'"></i>
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
  name: 'AdminStudents',

  data() {
    return {
      students: [],
      searchQuery: '',
      branchFilter: '',
      yearFilter: ''
    };
  },

  computed: {
    filteredStudents() {
      let filtered = this.students;
      
      if (this.searchQuery) {
        const query = this.searchQuery.toLowerCase();
        filtered = filtered.filter(s => 
          s.full_name.toLowerCase().includes(query) || 
          s.email.toLowerCase().includes(query)
        );
      }
      
      if (this.branchFilter) {
        filtered = filtered.filter(s => s.branch === this.branchFilter);
      }
      
      if (this.yearFilter) {
        filtered = filtered.filter(s => s.year === parseInt(this.yearFilter));
      }
      
      return filtered;
    }
  },

  mounted() {
    this.fetchStudents();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchStudents() {
      try {
        const res = await axios.get(`${API_URL}/api/admin/students`, this.getAuthHeader());
        this.students = res.data;
      } catch (err) {
        console.error('Failed to fetch students:', err);
      }
    },

    async toggleBlacklist(student) {
      const action = student.is_blacklisted ? 'remove from' : 'add to';
      if (confirm(`Are you sure you want to ${action} blacklist?`)) {
        try {
          if (student.is_blacklisted) {
            await axios.put(`${API_URL}/api/admin/students/${student.id}/unblacklist`, {}, this.getAuthHeader());
          } else {
            await axios.put(`${API_URL}/api/admin/students/${student.id}/blacklist`, {}, this.getAuthHeader());
          }
          await this.fetchStudents();
          alert(`Student ${student.is_blacklisted ? 'removed from' : 'added to'} blacklist`);
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to update blacklist');
        }
      }
    },

    viewStudent(id) {
      this.$router.push(`/admin/dashboard/students/${id}`);
    },

    getInitials(name) {
      if (!name) return 'U';
      return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2);
    },

    getStudentColor(name) {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!name) return colors[0];
      let hash = 0;
      for (let i = 0; i < name.length; i++) {
        hash = ((hash << 5) - hash) + name.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
    }
  }
};
</script>

<style scoped>
.admin-students {
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
  width: 40px;
  height: 40px;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.btn-group {
  gap: 0.25rem;
}

.btn-outline-primary,
.btn-outline-secondary,
.btn-outline-warning {
  border-width: 2px;
  transition: all 0.3s ease;
}

.btn-outline-primary:hover {
  background: #667eea;
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