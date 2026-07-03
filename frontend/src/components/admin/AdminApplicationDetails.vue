<template>
  <div class="admin-application-details">
    <!-- Back Button -->
    <button class="btn btn-outline-custom mb-4" @click="goBack">
      <i class="bi bi-arrow-left me-2"></i>Back to Applications
    </button>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading application details...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchApplicationDetails">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Application Details Content -->
    <div v-else-if="application" class="application-details-container">
      <!-- Header Card -->
      <div class="header-card card border-0 mb-4">
        <div class="card-body">
          <div class="row align-items-center">
            <div class="col-auto">
              <div class="student-avatar-large rounded-circle d-flex align-items-center justify-content-center"
                   :style="{ background: studentColor }">
                {{ getInitials(application.student.name) }}
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-1">{{ application.student.name }}</h2>
              <p class="text-primary mb-2">{{ application.student.email }}</p>
              <div class="d-flex gap-3 flex-wrap">
                <span class="badge bg-light text-dark">
                  <i class="bi bi-building me-1"></i>{{ application.student.branch }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-calendar-range me-1"></i>Year {{ application.student.year }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-star me-1"></i>CGPA: {{ application.student.cgpa }}
                </span>
                <span class="badge" :class="getStatusBadgeClass(application.status)">
                  {{ application.status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="row g-4">
        <!-- Left Column - Student Details -->
        <div class="col-lg-4">
          <!-- Student Info Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-person text-primary me-2"></i>Student Information
              </h5>
              <div class="info-list">
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Full Name</div>
                  <div class="info-value text-dark fw-medium">{{ application.student.name }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Email</div>
                  <div class="info-value text-dark">{{ application.student.email }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Branch</div>
                  <div class="info-value text-dark">{{ application.student.branch }}</div>
                </div>
                <div class="info-item d-flex mb-3">
                  <div class="info-label w-50 text-secondary">Year</div>
                  <div class="info-value text-dark">{{ application.student.year }}</div>
                </div>
                <div class="info-item d-flex">
                  <div class="info-label w-50 text-secondary">CGPA</div>
                  <div class="info-value text-dark">{{ application.student.cgpa }}</div>
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
                <span v-for="skill in application.student.skills || []" :key="skill" 
                      class="badge bg-primary p-3 rounded-pill">
                  {{ skill }}
                </span>
                <span v-if="!application.student.skills?.length" class="text-secondary">
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
              <div v-if="application.resume_url" class="document-item d-flex align-items-center p-3 bg-light rounded-3">
                <i class="bi bi-file-pdf text-danger fs-4 me-3"></i>
                <div class="flex-grow-1">
                  <h6 class="text-dark mb-1">Application Resume</h6>
                  <small class="text-secondary">Resume used for this application</small>
                </div>
                <a :href="application.resume_url" target="_blank" class="btn btn-sm btn-outline-primary rounded-pill">
                  <i class="bi bi-eye me-1"></i> View
                </a>
              </div>
              <div v-else class="text-center py-4 bg-light rounded-3">
                <i class="bi bi-file-earmark-x text-secondary fs-1"></i>
                <p class="text-secondary mt-2">No resume available</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Right Column - Job & Application Details -->
        <div class="col-lg-8">
          <!-- Job Information Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-briefcase text-primary me-2"></i>Job Information
              </h5>
              
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Company</small>
                    <strong class="text-dark">{{ application.job.company }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Position</small>
                    <strong class="text-dark">{{ application.job.role }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Salary</small>
                    <strong class="text-dark">{{ application.job.salary || 'Not specified' }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Job Type</small>
                    <strong class="text-dark">{{ application.job.job_type }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Drive Date</small>
                    <strong class="text-dark">{{ formatDate(application.job.drive_date) || 'TBD' }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Drive Location</small>
                    <strong class="text-dark">{{ application.job.drive_location || 'Not specified' }}</strong>
                  </div>
                </div>
              </div>

              <div class="mt-3">
                <p class="text-secondary small mb-1">Job Description:</p>
                <p class="text-dark">{{ application.job.description || 'No description available' }}</p>
              </div>
            </div>
          </div>

          <!-- Application Timeline Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-clock-history text-primary me-2"></i>Application Timeline
              </h5>
              
              <div class="timeline">
                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon bg-primary bg-opacity-10 rounded-circle me-3 d-flex align-items-center justify-content-center"
                       style="width: 40px; height: 40px;">
                    <i class="bi bi-send text-primary"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Applied</h6>
                    <p class="text-secondary small mb-0">{{ formatDateTime(application.applied_on) }}</p>
                  </div>
                </div>

                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon rounded-circle me-3 d-flex align-items-center justify-content-center"
                       :class="application.shortlisted_on ? 'bg-warning bg-opacity-10' : 'bg-light'"
                       style="width: 40px; height: 40px;">
                    <i :class="application.shortlisted_on ? 'bi bi-star text-warning' : 'bi bi-hourglass text-secondary'"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Shortlisted</h6>
                    <p v-if="application.shortlisted_on" class="text-secondary small mb-0">
                      {{ formatDateTime(application.shortlisted_on) }}
                    </p>
                    <p v-else class="text-secondary small mb-0">Not yet shortlisted</p>
                  </div>
                </div>

                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon rounded-circle me-3 d-flex align-items-center justify-content-center"
                       :class="application.selected_on ? 'bg-success bg-opacity-10' : 'bg-light'"
                       style="width: 40px; height: 40px;">
                    <i :class="application.selected_on ? 'bi bi-check-circle text-success' : 'bi bi-hourglass text-secondary'"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Selected</h6>
                    <p v-if="application.selected_on" class="text-secondary small mb-0">
                      {{ formatDateTime(application.selected_on) }}
                    </p>
                    <p v-else class="text-secondary small mb-0">Not yet selected</p>
                  </div>
                </div>

                <div v-if="application.rejected_on" class="timeline-item d-flex">
                  <div class="timeline-icon bg-danger bg-opacity-10 rounded-circle me-3 d-flex align-items-center justify-content-center"
                       style="width: 40px; height: 40px;">
                    <i class="bi bi-x-circle text-danger"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Rejected</h6>
                    <p class="text-secondary small mb-0">{{ formatDateTime(application.rejected_on) }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Interview Details Card -->
          <div v-if="application.interview_date" class="card border-0">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-person-badge text-primary me-2"></i>Interview Details
              </h5>
              
              <div class="row g-3">
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Interview Date & Time</small>
                    <strong class="text-dark">{{ formatDateTime(application.interview_date) }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Interview Mode</small>
                    <strong class="text-dark">{{ application.interview_mode }}</strong>
                  </div>
                </div>
                <div v-if="application.interview_mode === 'Online' && application.meeting_link" class="col-12">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Meeting Link</small>
                    <a :href="application.meeting_link" target="_blank" class="text-primary text-decoration-none">
                      {{ application.meeting_link }}
                    </a>
                  </div>
                </div>
                <div v-if="application.interview_mode === 'In-person' && application.interview_location" class="col-12">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Interview Location</small>
                    <strong class="text-dark">{{ application.interview_location }}</strong>
                  </div>
                </div>
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

export default {
  name: 'AdminApplicationDetails',

  props: {
    applicationId: {
      type: [String, Number],
      required: true
    }
  },

  data() {
    return {
      loading: false,
      error: null,
      application: null
    };
  },

  computed: {
    studentColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.application?.student?.name) return colors[0];
      let hash = 0;
      for (let i = 0; i < this.application.student.name.length; i++) {
        hash = ((hash << 5) - hash) + this.application.student.name.charCodeAt(i);
      }
      return colors[Math.abs(hash) % colors.length];
    }
  },

  mounted() {
    this.fetchApplicationDetails();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchApplicationDetails() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `http://127.0.0.1:5000/api/admin/applications/${this.applicationId}`,
          this.getAuthHeader()
        );
        this.application = res.data;
      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load application details";
      } finally {
        this.loading = false;
      }
    },

    goBack() {
      this.$router.push('/admin/dashboard/applications');
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
    },

    formatDateTime(date) {
      if (!date) return 'N/A';
      return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    }
  }
};
</script>

<style scoped>
.admin-application-details {
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

.info-box {
  transition: all 0.3s ease;
}

.info-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.info-item {
  padding: 0.5rem 0;
  border-bottom: 1px solid #f0f0f0;
}

.info-item:last-child {
  border-bottom: none;
}

.document-item {
  transition: all 0.3s ease;
}

.document-item:hover {
  background: #ffffff !important;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

.timeline-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.timeline-item {
  position: relative;
}

.timeline-item:not(:last-child)::after {
  content: '';
  position: absolute;
  left: 19px;
  top: 45px;
  bottom: -15px;
  width: 2px;
  background: #e0e0e0;
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