<template>
  <div class="company-drives-page">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to Companies
    </button>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading company drives...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchCompanyJobs">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Company Details -->
    <div v-else-if="company">
      <!-- Company Header with more details -->
      <div class="company-detail-header card border-0 mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="company-logo-detail rounded-circle d-flex align-items-center justify-content-center"
                   :style="{ background: getCompanyColor(company.name) }">
                {{ company.name.charAt(0) }}
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-2">{{ company.name }}</h2>
              <div class="d-flex flex-wrap gap-3">
                <span v-if="company.industry" class="text-secondary">
                  <i class="bi bi-building me-1"></i>{{ company.industry }}
                </span>
                <span v-if="company.location" class="text-secondary">
                  <i class="bi bi-geo-alt me-1"></i>{{ company.location }}
                </span>
                <span v-if="company.website" class="text-secondary">
                  <i class="bi bi-link-45deg me-1"></i>
                  <a :href="company.website" target="_blank" class="text-decoration-none">{{ company.website }}</a>
                </span>
              </div>
              <p class="text-secondary mt-2 mb-0">
                <i class="bi bi-briefcase me-2"></i>{{ activeJobs.length }} active placement drive{{ activeJobs.length > 1 ? 's' : '' }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Jobs List for this Company -->
      <h5 class="mb-3 text-dark">Available Drives</h5>
      <div class="row g-4">
        <div v-for="job in company.jobs" :key="job.id" class="col-lg-6">
          <!-- Removed expired-job class conditional -->
          <div class="card job-card border-0">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-start mb-3">
                <h5 class="card-title text-dark mb-0">{{ job.role }}</h5>
                <span v-if="isDeadlinePassed(job.deadline)" class="badge bg-secondary">
                  <i class="bi bi-clock-history me-1"></i>Expired
                </span>
                <span v-else class="badge" :class="getEligibilityBadgeClass(job)">
                  <i :class="getEligibilityIcon(job)" class="me-1"></i>
                  {{ getEligibilityText(job) }}
                </span>
              </div>

              <div class="mb-3">
                <!-- Deadline -->
                <div class="d-flex gap-2 mb-2" :class="{ 'text-danger': isDeadlineNear(job.deadline) && !isDeadlinePassed(job.deadline) }">
                  <i class="bi bi-calendar" :class="isDeadlinePassed(job.deadline) ? 'text-secondary' : 'text-primary'"></i>
                  <small>
                    Deadline: 
                    <strong>{{ formatDeadline(job.deadline) }}</strong>
                    <span v-if="isDeadlinePassed(job.deadline)" class="ms-2 text-secondary">(Closed)</span>
                  </small>
                </div>

                <!-- CGPA Requirement -->
                <div v-if="job.cgpa_required" class="d-flex gap-2 mb-2 text-secondary">
                  <i class="bi bi-star text-primary"></i>
                  <small>Min CGPA: <strong>{{ job.cgpa_required }}</strong></small>
                </div>

                <!-- Year Requirement -->
                <div v-if="job.year_required" class="d-flex gap-2 mb-2 text-secondary">
                  <i class="bi bi-calendar-range text-primary"></i>
                  <small>Year: <strong>{{ job.year_required }}</strong></small>
                </div>

                <!-- Branch Requirements (simplified) -->
                <div v-if="job.branch_required?.length" class="d-flex gap-2 mb-2 text-secondary">
                  <i class="bi bi-diagram-3 text-primary"></i>
                  <small>
                    Branches: 
                    <strong>{{ job.branch_required.slice(0, 2).join(', ') }}{{ job.branch_required.length > 2 ? '...' : '' }}</strong>
                  </small>
                </div>

                <!-- Salary -->
                <div v-if="job.salary" class="d-flex gap-2 text-secondary">
                  <i class="bi bi-cash text-primary"></i>
                  <small>Salary: <strong>{{ formatSalary(job.salary) }}</strong></small>
                </div>
              </div>

              <div class="d-flex gap-2">
                <button class="btn btn-outline-custom flex-grow-1" @click="goToJobDetails(job)">
                  <i class="bi bi-eye me-2"></i>View Details
                </button>
                <button 
                  class="btn" 
                  :class="getApplyButtonClass(job)"
                  @click="applyForJob(job)"
                  :disabled="isApplying || hasApplied(job.id) || !isJobEligible(job) || isDeadlinePassed(job.deadline)"
                  style="flex: 0.5;"
                >
                  <span v-if="applyingJobId === job.id" class="spinner-border spinner-border-sm me-1"></span>
                  <i v-else :class="getApplyButtonIcon(job)" class="me-1"></i>
                  {{ getApplyButtonText(job) }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- No Jobs Message -->
      <div v-if="company && company.jobs.length === 0" class="text-center py-5">
        <i class="bi bi-briefcase text-secondary fs-1"></i>
        <h5 class="text-dark mt-3">No Drives Available</h5>
        <p class="text-secondary">This company doesn't have any placement drives at the moment.</p>
        <button class="btn btn-outline-custom" @click="goBack">
          <i class="bi bi-arrow-left me-2"></i>Back to Companies
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL } from "@/config";

export default {
  name: 'CompanyDrivesPage',

  props: {
    companyName: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      jobs: [],
      appliedJobIds: new Set(),
      userProfile: null,
      isApplying: false,
      applyingJobId: null
    };
  },

  computed: {
    // Get jobs for the selected company with company details
    company() {
      const companyJobs = this.jobs.filter(job => job.company === this.companyName);
      if (companyJobs.length === 0) return null;
      
      // Get company details from the first job (they should be the same for all)
      const firstJob = companyJobs[0];
      
      return {
        name: this.companyName,
        industry: firstJob.company_details?.industry,
        location: firstJob.company_details?.location,
        website: firstJob.company_details?.website,
        jobs: companyJobs
      };
    },

    // Filter active jobs (not expired)
    activeJobs() {
      return this.jobs.filter(job => !this.isDeadlinePassed(job.deadline));
    }
  },

  mounted() {
    this.fetchCompanyJobs();
    this.fetchAppliedJobs();
    this.fetchUserProfile();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchCompanyJobs() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `${API_URL}/api/student/jobs`,
          this.getAuthHeader()
        );

        this.jobs = res.data
          .filter(job => job.company === this.companyName)
          .map(job => ({
            ...job,
            type: job.job_type || 'Full Time',
            location: job.drive_location || 'Not specified',
            description: job.description || 'No description available',
            year_required: job.year_required,
            branch_required: job.branch_required,
            skills_required: job.skills_required
          }));

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load jobs";
      } finally {
        this.loading = false;
      }
    },

    async fetchAppliedJobs() {
      try {
        const res = await axios.get(
          `${API_URL}/api/student/applied-jobs`,
          this.getAuthHeader()
        );
        this.appliedJobIds = new Set(res.data.map(job => job.job_id));
      } catch (err) {
        console.error('Failed to fetch applied jobs:', err);
      }
    },

    async fetchUserProfile() {
      try {
        const res = await axios.get(
          `${API_URL}/api/student/profile`,
          this.getAuthHeader()
        );
        this.userProfile = res.data;
      } catch (err) {
        console.error('Failed to fetch profile:', err);
      }
    },

    goBack() {
      this.$router.push('/student/dashboard/companies');
    },

    goToJobDetails(job) {
      this.$router.push(`/student/dashboard/companies/${this.companyName}/job/${job.id}`);
    },

    // Deadline check methods
    isDeadlinePassed(deadline) {
      if (!deadline) return false;
      const deadlineDate = new Date(deadline);
      const now = new Date();
      return deadlineDate < now;
    },

    isDeadlineNear(deadline) {
      if (!deadline) return false;
      const deadlineDate = new Date(deadline);
      const now = new Date();
      const daysLeft = Math.ceil((deadlineDate - now) / (1000 * 60 * 60 * 24));
      return daysLeft <= 3 && daysLeft > 0;
    },

    // Eligibility check methods
    checkCGPAEligibility(job) {
      if (!job.cgpa_required || !this.userProfile) return true;
      return this.userProfile.cgpa >= job.cgpa_required;
    },

    checkBranchEligibility(job) {
      if (!job.branch_required?.length || !this.userProfile) return true;
      return job.branch_required.includes(this.userProfile.branch);
    },

    checkYearEligibility(job) {
      if (!job.year_required || !this.userProfile) return true;
      return this.userProfile.year === job.year_required;
    },

    isJobEligible(job) {
      if (!this.userProfile) return false;
      return this.checkCGPAEligibility(job) && 
             this.checkBranchEligibility(job) && 
             this.checkYearEligibility(job);
    },

    // Eligibility badge methods
    getEligibilityBadgeClass(job) {
      if (this.isDeadlinePassed(job.deadline)) return 'bg-secondary';
      if (!this.userProfile) return 'bg-secondary';
      if (this.hasApplied(job.id)) return 'bg-success';
      return this.isJobEligible(job) ? 'bg-success' : 'bg-danger';
    },

    getEligibilityIcon(job) {
      if (this.isDeadlinePassed(job.deadline)) return 'bi bi-clock-history';
      if (!this.userProfile) return 'bi bi-question-circle';
      if (this.hasApplied(job.id)) return 'bi bi-check-circle';
      return this.isJobEligible(job) ? 'bi bi-check-circle' : 'bi bi-x-circle';
    },

    getEligibilityText(job) {
      if (this.isDeadlinePassed(job.deadline)) return 'Expired';
      if (!this.userProfile) return 'Login';
      if (this.hasApplied(job.id)) return 'Applied';
      return this.isJobEligible(job) ? 'Eligible' : 'Not Eligible';
    },

    // Apply button methods
    getApplyButtonClass(job) {
      if (this.hasApplied(job.id)) return 'btn-success';
      if (this.isDeadlinePassed(job.deadline)) return 'btn-secondary';
      if (!this.isJobEligible(job)) return 'btn-secondary';
      return 'btn-primary-custom';
    },

    getApplyButtonIcon(job) {
      if (this.hasApplied(job.id)) return 'bi bi-check-circle';
      if (this.isDeadlinePassed(job.deadline)) return 'bi bi-clock-history';
      if (!this.isJobEligible(job)) return 'bi bi-x-circle';
      return 'bi bi-send';
    },

    getApplyButtonText(job) {
      if (this.hasApplied(job.id)) return 'Applied';
      if (this.isDeadlinePassed(job.deadline)) return 'Expired';
      if (!this.isJobEligible(job)) return 'Not Eligible';
      if (this.applyingJobId === job.id) return 'Applying...';
      return 'Apply';
    },

    async applyForJob(job) {
      if (this.hasApplied(job.id)) {
        alert('You have already applied for this job');
        return;
      }

      if (this.isDeadlinePassed(job.deadline)) {
        alert('Application deadline has passed');
        return;
      }

      if (!this.isJobEligible(job)) {
        alert('You are not eligible for this job');
        return;
      }

      this.isApplying = true;
      this.applyingJobId = job.id;

      try {
        await axios.post(
          `${API_URL}/api/student/apply/${job.id}`,
          {},
          this.getAuthHeader()
        );

        alert("Application submitted successfully!");
        this.appliedJobIds.add(job.id);

      } catch (err) {
        console.error('Apply for job error:', err);
        alert(err.response?.data?.msg || "Application failed");
      } finally {
        this.isApplying = false;
        this.applyingJobId = null;
      }
    },

    hasApplied(jobId) {
      return this.appliedJobIds.has(jobId);
    },

    getCompanyColor(company) {
      const colors = [
        'linear-gradient(135deg, #667eea, #764ba2)',
        'linear-gradient(135deg, #3b82f6, #1d4ed8)',
        'linear-gradient(135deg, #10b981, #059669)',
        'linear-gradient(135deg, #f59e0b, #d97706)',
        'linear-gradient(135deg, #8b5cf6, #6d28d9)'
      ];
      
      let hash = 0;
      for (let i = 0; i < company.length; i++) {
        hash = ((hash << 5) - hash) + company.charCodeAt(i);
        hash |= 0;
      }
      return colors[Math.abs(hash) % colors.length];
    },

    formatDeadline(date) {
          if (!date) return 'No deadline';
          const deadline = new Date(date);
          const now = new Date();
          const daysLeft = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));
          
          // Format the actual date and time
          const formattedDate = deadline.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
          });
          
          const formattedTime = deadline.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });
          
          const dateTimeString = `${formattedDate} ${formattedTime}`;
          
          if (daysLeft < 0) return `${dateTimeString} (Expired)`;
          if (daysLeft === 0) return `${dateTimeString} (Today)`;
          if (daysLeft === 1) return `${dateTimeString} (Tomorrow)`;
          return `${dateTimeString} (${daysLeft} days left)`;
        },

    formatDate(date) {
      if (!date) return 'TBD';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatSalary(salary) {
      if (!salary || salary === 'Not disclosed') return 'Not disclosed';
      return `₹${salary.toLocaleString()}`;
    }
  }
};
</script>

<style scoped>
.company-drives-page {
  color: #333;
}

/* Company Detail Header */
.company-detail-header {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.company-logo-detail {
  width: 70px;
  height: 70px;
  font-size: 32px;
  font-weight: 600;
  color: white;
}

/* Job Card - Removed expired-job styles */
.job-card {
  background: white;
  border-radius: 25px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.job-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
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

.btn-primary-custom:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
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

.btn-success {
  background: #10b981;
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-success:hover {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
}

.btn-secondary {
  background: #6c757d;
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
  cursor: not-allowed;
  opacity: 0.65;
}

/* Badge Styles */
.badge.bg-success {
  background: #10b981 !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
}

.badge.bg-danger {
  background: #ef4444 !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
}

.badge.bg-secondary {
  background: #6c757d !important;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
}

.badge.bg-light {
  background: #f3f4f6 !important;
  color: #4b5563;
  padding: 0.5rem 1rem;
  border-radius: 50px;
}

/* Text colors */
.text-danger {
  color: #ef4444 !important;
}

.text-secondary {
  color: #6c757d !important;
}

.text-primary {
  color: #667eea !important;
}

/* Responsive */
@media (max-width: 768px) {
  .row.g-4 {
    --bs-gutter-y: 1rem;
  }
}
</style>