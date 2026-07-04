<template>
  <div class="admin-student-details">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to Students
    </button>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading student details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchStudentDetails">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Student Details Content -->
    <div v-else-if="student" class="student-details-container">
      <!-- Header Card -->
      <div class="header-card card border-0 mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="student-avatar-large rounded-circle d-flex align-items-center justify-content-center"
                   :style="{ background: avatarColor }">
                {{ getInitials(student.full_name) }}
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-1">{{ student.full_name }}</h2>
              <p class="text-primary mb-2">{{ student.email }}</p>
              <div class="d-flex gap-3 flex-wrap">
                <span class="badge bg-light text-dark">
                  <i class="bi bi-building me-1"></i>{{ student.branch }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-calendar-range me-1"></i>Year {{ student.year }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-star me-1"></i>CGPA: {{ student.cgpa }}
                </span>
                <span class="badge" :class="student.is_blacklisted ? 'bg-danger' : 'bg-success'">
                  {{ student.is_blacklisted ? 'Blacklisted' : 'Active' }}
                </span>
              </div>
            </div>
            <div class="col-auto">
              <button class="btn" :class="student.is_blacklisted ? 'btn-outline-warning' : 'btn-outline-danger'"
                      @click="toggleBlacklist">
                <i :class="student.is_blacklisted ? 'bi bi-person-up' : 'bi bi-person-down'" class="me-2"></i>
                {{ student.is_blacklisted ? 'Remove from Blacklist' : 'Blacklist Student' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Details Grid -->
      <div class="row g-4">
        <!-- Left Column - Personal Info & Skills -->
        <div class="col-lg-4">
          <!-- Personal Information -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-person text-primary me-2"></i>Personal Information
              </h5>
              <div class="info-list">
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Full Name</div>
                  <div class="info-value text-dark fw-medium">{{ student.full_name }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Email</div>
                  <div class="info-value text-dark">{{ student.email }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Branch</div>
                  <div class="info-value text-dark">{{ student.branch }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Year</div>
                  <div class="info-value text-dark">{{ student.year }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">CGPA</div>
                  <div class="info-value text-dark">{{ student.cgpa }}</div>
                </div>
                <div class="info-item d-flex">
                  <div class="info-label w-50 text-secondary">Member Since</div>
                  <div class="info-value text-dark">{{ formatDate(student.created_at) }}</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Skills Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-code-square text-primary me-2"></i>Skills
              </h5>
              <div class="d-flex gap-2 flex-wrap">
                <span v-for="skill in student.skills || []" :key="skill" 
                      class="badge bg-primary p-3 rounded-pill">
                  {{ skill }}
                </span>
                <span v-if="!student.skills?.length" class="text-secondary">
                  No skills listed
                </span>
              </div>
            </div>
          </div>

          <!-- Resume Card -->
          <div class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-file-text text-primary me-2"></i>Resume
              </h5>
              <div v-if="student.resume_url" class="document-item d-flex align-items-center p-3 bg-light rounded-3">
                <i class="bi bi-file-pdf text-danger fs-4 me-3"></i>
                <div class="flex-grow-1">
                  <h6 class="text-dark mb-1">Resume</h6>
                  <small class="text-secondary">Student's resume document</small>
                </div>
                <a :href="student.resume_url" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill">
                  <i class="bi bi-eye me-1"></i> View
                </a>
              </div>
              <div v-else class="text-center py-4 bg-light rounded-3">
                <i class="bi bi-file-earmark-x text-secondary fs-1"></i>
                <p class="text-secondary mt-2">No resume uploaded</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Applications & Placements -->
        <div class="col-lg-8">
          <!-- Applications Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-briefcase text-primary me-2"></i>Applications ({{ student.applications?.length || 0 }})
              </h5>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Company</th>
                      <th>Position</th>
                      <th>Applied On</th>
                      <th>Status</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="app in student.applications" :key="app.id">
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
                          <i class="bi bi-eye"></i>
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Placements Card -->
          <div class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-trophy text-primary me-2"></i>Placements ({{ student.placements?.length || 0 }})
              </h5>
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th>Company</th>
                      <th>Position</th>
                      <th>Salary</th>
                      <th>Joining Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="placement in student.placements" :key="placement.company">
                      <td>{{ placement.company }}</td>
                      <td>{{ placement.position }}</td>
                      <td>{{ placement.salary || 'N/A' }}</td>
                      <td>{{ formatDate(placement.joining_date) }}</td>
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
import { API_URL } from "@/config";

export default {
  name: 'AdminStudentDetails',

  props: {
    studentId: {
      type: [String, Number],
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      student: null
    };
  },

  computed: {
    avatarColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.student?.full_name) return colors[0];
      let hash = 0;
      for (let i = 0; i < this.student.full_name.length; i++) {
        hash = ((hash << 5) - hash) + this.student.full_name.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
    }
  },

  mounted() {
    this.fetchStudentDetails();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchStudentDetails() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/admin/students/${this.studentId}`,
          this.getAuthHeader()
        );
        this.student = res.data;
      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load student details";
      } finally {
        this.loading = false;
      }
    },

    async toggleBlacklist() {
      const action = this.student.is_blacklisted ? 'remove from' : 'add to';
      if (confirm(`Are you sure you want to ${action} blacklist?`)) {
        try {
          if (this.student.is_blacklisted) {
            await axios.put(`http://127.0.0.1:5000/api/admin/students/${this.studentId}/unblacklist`, {}, this.getAuthHeader());
          } else {
            await axios.put(`http://127.0.0.1:5000/api/admin/students/${this.studentId}/blacklist`, {}, this.getAuthHeader());
          }
          await this.fetchStudentDetails();
          alert(`Student ${this.student.is_blacklisted ? 'removed from' : 'added to'} blacklist`);
        } catch (err) {
          alert(err.response?.data?.msg || 'Failed to update blacklist');
        }
      }
    },

    viewApplication(id) {
      this.$router.push(`/admin/dashboard/applications/${id}`);
    },

    goBack() {
      this.$router.push('/admin/dashboard/students');
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
  }
};
</script>

<style scoped>
.admin-student-details {
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

.student-avatar-large {
  width: 80px;
  height: 80px;
  font-size: 32px;
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

.info-label {
  color: #6c757d;
}

.info-value {
  font-weight: 500;
}

.document-item {
  transition: all 0.3s ease;
}

.document-item:hover {
  background: #ffffff !important;
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
</style>