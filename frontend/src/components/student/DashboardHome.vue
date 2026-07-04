<template>
  <div class="dashboard-home">

    <!-- Welcome Section -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold">
        Welcome back, <span class="text-gradient">{{ userName || 'Student' }}</span>!
      </h1>
      <p class="text-muted">Here's what's happening with your applications today.</p>
    </div>

    <!-- Applications Section -->
    <div class="card applications-card border-0">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-4 flex-wrap gap-3">
          <h5 class="h4 mb-0 text-dark">Your Applications</h5>
          <div class="btn-group" role="group">
            <button 
              class="btn" 
              :class="filterStatus === 'all' ? 'btn-primary-custom' : 'btn-outline-custom'"
              @click="filterStatus = 'all'"
            >All</button>
            <button 
              class="btn" 
              :class="filterStatus === 'shortlisted' ? 'btn-primary-custom' : 'btn-outline-custom'"
              @click="filterStatus = 'shortlisted'"
            >Shortlisted</button>
            <button 
              class="btn" 
              :class="filterStatus === 'selected' ? 'btn-primary-custom' : 'btn-outline-custom'"
              @click="filterStatus = 'selected'"
            >Selected</button>
          </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <p class="text-secondary mt-3">Loading your applications...</p>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="text-center py-5">
          <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
          <p class="text-danger mt-3">{{ error }}</p>
          <button class="btn btn-primary-custom mt-2" @click="fetchAppliedJobs">
            <i class="bi bi-arrow-repeat me-2"></i>Try Again
          </button>
        </div>

        <!-- Applications List -->
        <div v-else>
          <div v-for="job in filteredJobs" :key="job.job_id" 
               class="application-card p-3 mb-3">
            <div class="d-flex justify-content-between align-items-start flex-wrap gap-3">
              <!-- Left Section with Job Info - Clickable -->
              <div class="d-flex gap-3 align-items-start clickable-job" @click="viewJobDetails(job)">
                <div class="company-logo rounded-3 d-flex align-items-center justify-content-center"
                     :style="{ background: getCompanyColor(job.company) }">
                  {{ job.company ? job.company.charAt(0) : 'J' }}
                </div>
                <div>
                  <!-- Job Role - Main Heading -->
                  <h5 class="fw-bold text-dark mb-1">{{ job.job || 'Job Position' }}</h5>
                  <!-- Company Name - Subheading -->
                  <p class="text-primary fw-semibold mb-2">{{ job.company }}</p>
                  
                  <!-- Applied Date -->
                  <div class="d-flex gap-3">
                    <small class="text-secondary">
                      <i class="bi bi-calendar-check me-1"></i>
                      Applied: {{ formatDate(job.applied_on) }}
                    </small>
                  </div>
                </div>
              </div>

              <!-- Right Section with Status and Actions -->
              <div class="d-flex gap-2 align-items-center">
                <span class="badge" :class="getStatusBadgeClass(job.status)">
                  {{ formatStatus(job.status) }}
                </span>
                
                <!-- Eye button to view resume in new tab -->
                <button 
                  v-if="job.resume_url"
                  class="btn btn-outline-custom btn-sm d-flex align-items-center gap-1"
                  @click="viewResumeInNewTab(job.resume_url)"
                  title="View Resume"
                >
                  <i class="bi bi-eye"></i>
                  <span class="d-none d-md-inline">Resume</span>
                </button>
              </div>
            </div>
          </div>

          <div v-if="filteredJobs.length === 0" class="text-center py-5">
            <i class="bi bi-inbox fs-1 text-secondary"></i>
            <p class="text-secondary mt-3">No applications found</p>
            <button class="btn btn-primary-custom" @click="goToCompanies">
              <i class="bi bi-building me-2"></i>Browse Companies
            </button>
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
  name: 'DashboardHome',
  
  emits: ['change-tab', 'update-user-name'],

  data() {
    return {
      loading: false,
      error: null,
      appliedJobs: [],
      filterStatus: 'all',
      userName: localStorage.getItem('userName') || ''
    };
  },

  computed: {
    filteredJobs() {
      if (this.filterStatus === 'all') return this.appliedJobs;
      return this.appliedJobs.filter(job => job.status === this.filterStatus);
    }
  },

  mounted() {
    this.fetchAppliedJobs();
    this.fetchUserProfile();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchUserProfile() {
      try {
        const res = await axios.get(
          `${API_URL}/api/student/profile`,
          this.getAuthHeader()
        );
        
        if (res.data.full_name) {
          this.userName = res.data.full_name;
          this.$emit('update-user-name', res.data.full_name);
        }
      } catch (err) {
        console.error('Failed to fetch user profile:', err);
      }
    },

    async fetchAppliedJobs() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `${API_URL}/api/student/applied-jobs`,
          this.getAuthHeader()
        );

        console.log("Applied jobs response:", res.data); // Debug log

        // Map the response to match our template
        this.appliedJobs = res.data.map(app => ({
          job_id: app.job_id,
          job: app.job, // This is the job role from backend
          company: app.company,
          status: app.status || 'applied',
          applied_on: app.applied_on,
          resume_url: app.resume_url // Add resume URL from the response
        }));

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load applications";
        console.error('Fetch applications error:', err);
      } finally {
        this.loading = false;
      }
    },

    goToCompanies() {
      // Navigate to the companies page
      this.$router.push('/student/dashboard/companies');
    },

    viewJobDetails(job) {
      // Navigate to job details page with company name and job ID
      const encodedCompanyName = encodeURIComponent(job.company);
      this.$router.push(`/student/dashboard/companies/${encodedCompanyName}/job/${job.job_id}`);
    },

    viewResumeInNewTab(resumeUrl) {
      if (resumeUrl) {
        window.open(resumeUrl, '_blank');
      } else {
        alert('No resume available for this application');
      }
    },

    getStatusBadgeClass(status) {
      const classes = {
        selected: 'bg-success',
        shortlisted: 'bg-warning',
        rejected: 'bg-danger',
        applied: 'bg-primary'
      };
      return classes[status] || 'bg-secondary';
    },

    formatStatus(status) {
      if (!status) return 'Applied';
      return status.charAt(0).toUpperCase() + status.slice(1);
    },

    getCompanyColor(company) {
      const colors = [
        'linear-gradient(135deg, #667eea, #764ba2)',
        'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        'linear-gradient(135deg, #10b981, #059669)',
        'linear-gradient(135deg, #f59e0b, #d97706)',
        'linear-gradient(135deg, #8b5cf6, #6d28d9)'
      ];
      
      if (!company) return colors[0];
      
      let hash = 0;
      for (let i = 0; i < company.length; i++) {
        hash = ((hash << 5) - hash) + company.charCodeAt(i);
        hash |= 0;
      }
      return colors[Math.abs(hash) % colors.length];
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
.dashboard-home {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Applications Card */
.applications-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.application-card {
  background: #f8f9fa;
  border-radius: 15px;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.application-card:hover {
  border-color: #667eea;
  box-shadow: 0 5px 20px rgba(102, 126, 234, 0.15);
}

.clickable-job {
  cursor: pointer;
  flex: 1;
  transition: all 0.2s ease;
}

.clickable-job:hover h5 {
  color: #667eea !important;
}

.company-logo {
  width: 50px;
  height: 50px;
  font-size: 22px;
  font-weight: 600;
  color: white;
  transition: all 0.3s ease;
}

.application-card:hover .company-logo {
  transform: scale(1.05);
}

/* Job Title Styling */
.application-card h5 {
  font-size: 1.2rem;
  line-height: 1.4;
  transition: color 0.2s ease;
}

.application-card .text-primary {
  color: #667eea !important;
  font-size: 1rem;
}

/* Button Styles */
.btn-primary-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.5rem 1.5rem;
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
  padding: 0.5rem 1.5rem;
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

.btn-outline-custom.btn-sm {
  padding: 0.4rem 1rem;
  font-size: 0.85rem;
}

.btn-outline-custom.btn-sm i {
  font-size: 1rem;
}

/* Badge Styles */
.badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

.badge.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
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

/* Responsive */
@media (max-width: 768px) {
  .application-card {
    padding: 1rem !important;
  }
  
  .application-card .d-flex.justify-content-between {
    width: 100%;
  }
  
  .application-card .d-flex.gap-3.align-items-start {
    width: 100%;
  }
  
  .company-logo {
    width: 45px;
    height: 45px;
    font-size: 20px;
  }
  
  .application-card h5 {
    font-size: 1.1rem;
  }
  
  .btn-outline-custom.btn-sm span {
    display: none;
  }
  
  .btn-outline-custom.btn-sm i {
    margin: 0;
  }
}
</style>