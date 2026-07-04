<template>
  <div class="job-details-page">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to {{ companyName }}
    </button>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading job details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchJobDetails">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Job Details Content -->
    <div v-else-if="job" class="job-details-container">
      <!-- Company Header with more details -->
      <div class="company-header-card card border-0 mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="company-logo-large rounded-circle d-flex align-items-center justify-content-center"
                   :style="{ background: getCompanyColor(job.company) }">
                {{ job.company.charAt(0) }}
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-1">{{ job.role }}</h2>
              <p class="text-primary mb-2">{{ job.company }}</p>
              
              <!-- Company Details -->
              <div v-if="job.company_details" class="d-flex flex-wrap gap-3 mb-2">
                <span v-if="job.company_details.industry" class="text-secondary small">
                  <i class="bi bi-building me-1"></i>{{ job.company_details.industry }}
                </span>
                <span v-if="job.company_details.location" class="text-secondary small">
                  <i class="bi bi-geo-alt me-1"></i>{{ job.company_details.location }}
                </span>
                <span v-if="job.company_details.website" class="text-secondary small">
                  <i class="bi bi-link-45deg me-1"></i>
                  <a :href="job.company_details.website" target="_blank" class="text-decoration-none">{{ job.company_details.website }}</a>
                </span>
              </div>

              <div class="d-flex gap-3 flex-wrap">
                <span class="badge bg-light text-dark">
                  <i class="bi bi-briefcase me-1"></i>{{ job.job_type  }}
                </span>
                <span v-if="isDeadlinePassed(job.deadline)" class="badge bg-secondary">
                  <i class="bi bi-clock-history me-1"></i>Expired
                </span>
                <span v-else class="badge" :class="getEligibilityBadgeClass()">
                  <i :class="getEligibilityIcon()" class="me-1"></i>
                  {{ getEligibilityText() }}
                </span>
              </div>
            </div>
            <div class="col-auto">
              <button 
                class="btn btn-lg" 
                :class="getApplyButtonClass()"
                @click="applyForJob"
                :disabled="hasApplied || !isJobEligible() || applying || isDeadlinePassed(job.deadline)"
              >
                <span v-if="applying" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else :class="getApplyButtonIcon()" class="me-2"></i>
                {{ getApplyButtonText() }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Interview Details Card - Show at top if interview is scheduled -->
      <div v-if="hasApplied && job.interview_date" class="interview-card card border-0 mb-4">
        <div class="card-body">
          <div class="row">
            <div class="col-12">
              <h5 class="text-dark mb-3">
                <i class="bi bi-person-badge text-primary me-2"></i>Interview Schedule
              </h5>
            </div>
          </div>
          <div class="row g-4">
            <div class="col-md-3">
              <div class="interview-info-item">
                <small class="text-secondary d-block">Date</small>
                <strong class="text-dark fs-6">{{ formatDate(job.interview_date) }}</strong>
              </div>
            </div>
            <div class="col-md-3">
              <div class="interview-info-item">
                <small class="text-secondary d-block">Time</small>
                <strong class="text-dark fs-6">{{ formatTime(job.interview_date) }}</strong>
              </div>
            </div>
            <div class="col-md-3">
              <div class="interview-info-item">
                <small class="text-secondary d-block">Mode</small>
                <strong class="text-dark fs-6">{{ job.interview_mode }}</strong>
              </div>
            </div>
            <div class="col-md-3">
              <div class="interview-info-item">
                <small class="text-secondary d-block">Status</small>
                <span class="badge" :class="getInterviewStatusClass()">
                  <i :class="getInterviewStatusIcon()" class="me-1"></i>
                  {{ getInterviewStatusText() }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Show meeting link for online interviews -->
          <div v-if="job.interview_mode === 'Online' && job.meeting_link" class="row mt-3">
            <div class="col-12">
              <div class="interview-info-item">
                <small class="text-secondary d-block">Meeting Link</small>
                <a :href="job.meeting_link" target="_blank" class="text-primary text-decoration-none">
                  <i class="bi bi-camera-video me-1"></i>{{ job.meeting_link }}
                </a>
              </div>
            </div>
          </div>

          <!-- Show location for in-person interviews -->
          <div v-if="job.interview_mode === 'In-person' && job.interview_location" class="row mt-3">
            <div class="col-12">
              <div class="interview-info-item">
                <small class="text-secondary d-block">Location</small>
                <strong class="text-dark">
                  <i class="bi bi-geo-alt me-1"></i>{{ job.interview_location }}
                </strong>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Job Details Grid -->
      <div class="row g-4">
        <!-- Left Column - Main Details -->
        <div class="col-lg-8">
          <!-- Description -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-file-text text-primary me-2"></i>Job Description
              </h5>
              <p class="text-secondary">{{ job.description || 'No description available' }}</p>
            </div>
          </div>

          <!-- Requirements -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-list-check text-primary me-2"></i>Requirements
              </h5>
              
              <div class="row g-4">
                <div class="col-md-6">
                  <div class="requirement-item">
                    <small class="text-secondary d-block mb-1">Minimum CGPA</small>
                    <strong class="text-dark fs-5">{{ job.cgpa_required || 'Not specified' }}</strong>
                    <span v-if="userProfile && job.cgpa_required" class="d-block small mt-1" 
                          :class="checkCGPAEligibility() ? 'text-success' : 'text-danger'">
                      <i :class="checkCGPAEligibility() ? 'bi bi-check-circle' : 'bi bi-x-circle'" class="me-1"></i>
                      Your CGPA: {{ userProfile.cgpa }}
                    </span>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="requirement-item">
                    <small class="text-secondary d-block mb-1">Eligible Year</small>
                    <strong class="text-dark fs-5">{{ job.year_required ? job.year_required + 'th Year' : 'Any Year' }}</strong>
                    <span v-if="userProfile && job.year_required" class="d-block small mt-1" 
                          :class="checkYearEligibility() ? 'text-success' : 'text-danger'">
                      <i :class="checkYearEligibility() ? 'bi bi-check-circle' : 'bi bi-x-circle'" class="me-1"></i>
                      Your Year: {{ userProfile.year }}
                    </span>
                  </div>
                </div>
              </div>

              <div class="mt-4">
                <h6 class="text-dark mb-3">Eligible Branches</h6>
                <div class="d-flex gap-2 flex-wrap">
                  <span v-for="branch in job.branch_required || []" :key="branch"
                        class="badge" 
                        :class="userProfile && branch === userProfile.branch ? 'bg-success' : 'bg-light text-dark'"
                        style="padding: 0.6rem 1rem;">
                    {{ branch }}
                    <i v-if="userProfile && branch === userProfile.branch" class="bi bi-check-circle ms-1"></i>
                  </span>
                  <span v-if="!job.branch_required?.length" class="text-secondary">
                    All branches eligible
                  </span>
                </div>
                <span v-if="userProfile && job.branch_required?.length" class="d-block small mt-2" 
                      :class="checkBranchEligibility() ? 'text-success' : 'text-danger'">
                  <i :class="checkBranchEligibility() ? 'bi bi-check-circle' : 'bi bi-x-circle'" class="me-1"></i>
                  Your Branch: {{ userProfile.branch }}
                </span>
              </div>

              <!-- Skills section - just display -->
              <div class="mt-4">
                <h6 class="text-dark mb-3">Required Skills</h6>
                <div class="d-flex gap-2 flex-wrap">
                  <span v-for="skill in job.skills_required || []" :key="skill"
                        class="badge bg-primary"
                        style="padding: 0.6rem 1rem;">
                    {{ skill }}
                  </span>
                  <span v-if="!job.skills_required?.length" class="text-secondary">
                    No specific skills required
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Key Information -->
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
                  <strong class="text-dark">{{ formatSalary(job.salary) }}</strong>
                </div>
              </div>

              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-geo-alt text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Location</small>
                  <strong class="text-dark">{{ job.drive_location || 'Not specified' }}</strong>
                </div>
              </div>

              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-calendar text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Deadline</small>
                  <strong class="text-dark" :class="{ 'text-danger': isDeadlineNear && !isDeadlinePassed(job.deadline) }">
                    {{ formatDeadline(job.deadline) }}
                  </strong>
                </div>
              </div>

              <div class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-calendar-event text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Drive Date</small>
                  <strong class="text-dark">{{ formatDate(job.drive_date) || 'TBD' }}</strong>
                </div>
              </div>

              <!-- Joining Date - Show if placement exists -->
              <div v-if="job.joining_date" class="key-info-item d-flex align-items-center mb-3">
                <div class="info-icon bg-light rounded-circle p-2 me-3">
                  <i class="bi bi-calendar-check text-primary"></i>
                </div>
                <div>
                  <small class="text-secondary d-block">Joining Date</small>
                  <strong class="text-dark">{{ formatDate(job.joining_date) }}</strong>
                </div>
              </div>
            </div>
          </div>

          <!-- Apply Button (Mobile) -->
          <div class="d-lg-none">
            <button 
              class="btn w-100 py-3" 
              :class="getApplyButtonClass()"
              @click="applyForJob"
              :disabled="hasApplied || !isJobEligible() || applying || isDeadlinePassed(job.deadline)"
            >
              <span v-if="applying" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else :class="getApplyButtonIcon()" class="me-2"></i>
              {{ getApplyButtonText() }}
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
  name: 'JobDetailsPage',

  props: {
    jobId: {
      type: [String, Number],
      required: true
    },
    companyName: {
      type: String,
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      job: null,
      appliedJobIds: new Set(),
      applicationsData: {},
      placementsData: [],
      applying: false,
      userProfile: null
    };
  },

  computed: {
    hasApplied() {
      return this.appliedJobIds.has(Number(this.jobId));
    },

    isDeadlineNear() {
      if (!this.job?.deadline) return false;
      const deadline = new Date(this.job.deadline);
      const now = new Date();
      const daysLeft = Math.ceil((deadline - now) / (1000 * 60 * 60 * 24));
      return daysLeft <= 3 && daysLeft > 0;
    }
  },

  mounted() {
    this.fetchJobDetails();
    this.fetchUserProfile();
    this.fetchPlacements();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    // Deadline check methods
    isDeadlinePassed(deadline) {
      if (!deadline) return false;
      const deadlineDate = new Date(deadline);
      const now = new Date();
      return deadlineDate < now;
    },

    async fetchJobDetails() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `${API_URL}/api/student/jobs`,
          this.getAuthHeader()
        );

        const job = res.data.find(j => j.id === Number(this.jobId));
        
        if (!job) {
          this.error = "Job not found";
          return;
        }

        this.job = {
          ...job,
          type: job.job_type || 'Full Time',
          location: job.drive_location || 'Not specified',
          description: job.description || 'No description available',
          year_required: job.year_required,
          branch_required: job.branch_required,
          skills_required: job.skills_required,
          drive_location: job.drive_location,
          drive_date: job.drive_date,
          joining_date: null,
          interview_date: null,
          interview_mode: null,
          interview_location: null,
          meeting_link: null
        };

        await this.fetchAppliedJobs();
        
        if (this.hasApplied) {
          await this.fetchInterviewDetails();
        }

        // Check for placement after we have all data
        setTimeout(() => {
          this.checkPlacementForJob();
        }, 100);

      } catch (err) {
        console.error('Fetch job details error:', err);
        this.error = err.response?.data?.msg || "Failed to load job details";
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
        
        console.log("Applied jobs response:", res.data);
        
        this.appliedJobIds = new Set(res.data.map(app => app.job_id));
        
        this.applicationsData = res.data.reduce((acc, app) => {
          acc[app.job_id] = app;
          return acc;
        }, {});
        
      } catch (err) {
        console.error('Failed to fetch applied jobs:', err);
      }
    },

    async fetchPlacements() {
      try {
        const res = await axios.get(
          `${API_URL}/api/student/placements`,
          this.getAuthHeader()
        );
        this.placementsData = res.data;
        console.log("Placements data:", res.data);
      } catch (err) {
        console.error('Failed to fetch placements:', err);
      }
    },

    checkPlacementForJob() {
      console.log("Checking placement for job:", this.job?.id);
      console.log("Placements data:", this.placementsData);
      
      if (!this.job || !this.placementsData.length) {
        console.log("No job or placements data");
        return;
      }
      
      // Try to find a placement that matches this job by company and position
      const placement = this.placementsData.find(p => 
        p.company === this.job.company && 
        p.position === this.job.role
      );
      
      if (placement && placement.joining_date) {
        this.job.joining_date = placement.joining_date;
        console.log("Found joining date for job:", placement.joining_date);
      } else {
        console.log("No matching placement found for this job");
      }
    },

    async fetchInterviewDetails() {
      try {
        if (this.applicationsData && this.applicationsData[this.jobId]) {
          const application = this.applicationsData[this.jobId];
          
          console.log("Application data:", application);
          
          this.job.interview_date = application.interview_date;
          this.job.interview_mode = application.interview_mode;
          this.job.interview_location = application.interview_location;
          this.job.meeting_link = application.meeting_link;
          
          console.log("Updated job with interview data:", {
            date: this.job.interview_date,
            mode: this.job.interview_mode,
            location: this.job.interview_location,
            link: this.job.meeting_link
          });
        }
      } catch (err) {
        console.error('Failed to fetch interview details:', err);
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
      this.$router.push(`/student/dashboard/companies/${this.companyName}`);
    },

    checkCGPAEligibility() {
      if (!this.job?.cgpa_required || !this.userProfile) return true;
      return this.userProfile.cgpa >= this.job.cgpa_required;
    },

    checkBranchEligibility() {
      if (!this.job?.branch_required?.length || !this.userProfile) return true;
      return this.job.branch_required.includes(this.userProfile.branch);
    },

    checkYearEligibility() {
      if (!this.job?.year_required || !this.userProfile) return true;
      return this.userProfile.year === this.job.year_required;
    },

    isJobEligible() {
      if (!this.userProfile) return false;
      if (this.isDeadlinePassed(this.job?.deadline)) return false;
      return this.checkCGPAEligibility() && 
             this.checkBranchEligibility() && 
             this.checkYearEligibility();
    },

    getEligibilityBadgeClass() {
      if (this.isDeadlinePassed(this.job?.deadline)) return 'bg-secondary';
      if (!this.userProfile) return 'bg-secondary';
      if (this.hasApplied) return 'bg-success';
      return this.isJobEligible() ? 'bg-success' : 'bg-danger';
    },

    getEligibilityIcon() {
      if (this.isDeadlinePassed(this.job?.deadline)) return 'bi bi-clock-history';
      if (!this.userProfile) return 'bi bi-question-circle';
      if (this.hasApplied) return 'bi bi-check-circle';
      return this.isJobEligible() ? 'bi bi-check-circle' : 'bi bi-x-circle';
    },

    getEligibilityText() {
      if (this.isDeadlinePassed(this.job?.deadline)) return 'Expired';
      if (!this.userProfile) return 'Login to check';
      if (this.hasApplied) return 'Applied';
      return this.isJobEligible() ? 'Eligible' : 'Not Eligible';
    },

    getApplyButtonClass() {
      if (this.hasApplied) return 'btn-success';
      if (this.isDeadlinePassed(this.job?.deadline)) return 'btn-secondary';
      if (!this.isJobEligible()) return 'btn-secondary';
      return 'btn-primary-custom';
    },

    getApplyButtonIcon() {
      if (this.hasApplied) return 'bi bi-check-circle';
      if (this.isDeadlinePassed(this.job?.deadline)) return 'bi bi-clock-history';
      if (!this.isJobEligible()) return 'bi bi-x-circle';
      return 'bi bi-send';
    },

    getApplyButtonText() {
      if (this.hasApplied) return 'Already Applied';
      if (this.isDeadlinePassed(this.job?.deadline)) return 'Expired';
      if (!this.isJobEligible()) return 'Not Eligible';
      return this.applying ? 'Applying...' : 'Apply Now';
    },

    async applyForJob() {
      if (this.hasApplied) {
        alert('You have already applied for this job');
        return;
      }

      if (this.isDeadlinePassed(this.job?.deadline)) {
        alert('Application deadline has passed');
        return;
      }

      if (!this.isJobEligible()) {
        alert('You are not eligible for this job');
        return;
      }

      this.applying = true;

      try {
        await axios.post(
          `${API_URL}/api/student/apply/${this.job.id}`,
          {},
          this.getAuthHeader()
        );

        alert("Application submitted successfully!");
        this.appliedJobIds.add(this.job.id);
        await this.fetchJobDetails();

      } catch (err) {
        console.error('Apply for job error:', err);
        alert(err.response?.data?.msg || "Application failed");
      } finally {
        this.applying = false;
      }
    },

    getInterviewStatusClass() {
      if (!this.job?.interview_date) return 'bg-secondary';
      
      const interviewDate = new Date(this.job.interview_date);
      const now = new Date();
      
      if (interviewDate < now) return 'bg-secondary';
      if (interviewDate - now < 24 * 60 * 60 * 1000) return 'bg-warning';
      return 'bg-success';
    },

    getInterviewStatusIcon() {
      if (!this.job?.interview_date) return 'bi bi-calendar';
      
      const interviewDate = new Date(this.job.interview_date);
      const now = new Date();
      
      if (interviewDate < now) return 'bi bi-calendar-check';
      if (interviewDate - now < 24 * 60 * 60 * 1000) return 'bi bi-exclamation-triangle';
      return 'bi bi-calendar-event';
    },

    getInterviewStatusText() {
      if (!this.job?.interview_date) return 'No Interview Scheduled';
      
      const interviewDate = new Date(this.job.interview_date);
      const now = new Date();
      
      if (interviewDate < now) return 'Interview Passed';
      if (interviewDate - now < 24 * 60 * 60 * 1000) return 'Interview Tomorrow!';
      return 'Interview Scheduled';
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
      
      if (daysLeft < 0) return 'Expired';
      if (daysLeft === 0) return 'Today';
      if (daysLeft === 1) return 'Tomorrow';
      return `${daysLeft} days left`;
    },

    formatDate(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    },

    formatTime(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    formatInterviewDateTime(date) {
      if (!date) return 'Not scheduled';
      return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
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
.job-details-page {
  color: #333;
}

/* Back Button */
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

/* Company Header */
.company-header-card {
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

/* Interview Card */
.interview-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border-left: 4px solid #667eea;
}

.interview-info-item {
  padding: 0.75rem;
  background: #f8f9fa;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.interview-info-item:hover {
  background: #ffffff;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

/* Cards */
.card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
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
.badge.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 50px;
}

.badge.bg-light {
  background: #f3f4f6 !important;
  color: #4b5563;
  padding: 0.6rem 1rem;
  border-radius: 50px;
}

.badge.bg-success {
  background: #10b981 !important;
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 50px;
}

.badge.bg-danger {
  background: #ef4444 !important;
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 50px;
}

.badge.bg-secondary {
  background: #6c757d !important;
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 50px;
}

.badge.bg-warning {
  background: #f59e0b !important;
  color: white;
  padding: 0.6rem 1rem;
  border-radius: 50px;
}

/* Key Info */
.info-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.info-icon i {
  font-size: 1.2rem;
}

.key-info-item {
  padding: 0.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.key-info-item:hover {
  background: #f8f9fa;
}

/* Responsive */
@media (max-width: 768px) {
  .company-header-card .row {
    flex-direction: column;
    text-align: center;
  }
  
  .company-header-card .col-auto:last-child {
    margin-top: 1rem;
    width: 100%;
  }
  
  .company-header-card .btn-lg {
    width: 100%;
  }
  
  .company-logo-large {
    width: 60px;
    height: 60px;
    font-size: 28px;
    margin-bottom: 1rem;
  }

  .interview-card .row {
    flex-direction: column;
  }
  
  .interview-card .col-md-3 {
    margin-bottom: 0.5rem;
  }
}
</style>