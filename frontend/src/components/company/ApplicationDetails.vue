<template>
  <div class="application-details-page">
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
                   :style="{ background: avatarColor }">
                {{ getInitials(application.full_name) }}
              </div>
            </div>
            <div class="col">
              <h2 class="h3 text-dark mb-1">{{ application.full_name }}</h2>
              <p class="text-primary mb-2">{{ application.student_email }}</p>
              <div class="d-flex gap-3 flex-wrap">
                <span class="badge bg-light text-dark">
                  <i class="bi bi-building me-1"></i>{{ application.branch }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-calendar-range me-1"></i>Year {{ application.year }}
                </span>
                <span class="badge bg-light text-dark">
                  <i class="bi bi-star me-1"></i>CGPA: {{ application.cgpa }}
                </span>
                <span class="badge" :class="getStatusBadgeClass(application.application_status)">
                  {{ application.application_status }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="row g-4">
        <!-- Left Column - Student Details -->
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
                    <small class="text-secondary d-block">Job Role</small>
                    <strong class="text-dark fs-5">{{ application.job_role }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Applied On</small>
                    <strong class="text-dark">{{ formatDate(application.applied_on) }}</strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Drive Date</small>
                    <strong class="text-dark">
                      {{ formatDate(application.drive_date) }}
                    </strong>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Application ID</small>
                    <strong class="text-dark">#{{ application.application_id }}</strong>
                  </div>
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
                <span v-for="skill in application.skills || []" :key="skill" 
                      class="badge bg-primary p-3">
                  {{ skill }}
                </span>
                <span v-if="!application.skills?.length" class="text-secondary">
                  No skills listed
                </span>
              </div>
            </div>
          </div>

          <!-- Timeline Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-clock-history text-primary me-2"></i>Application Timeline
              </h5>
              
              <div class="timeline">
                <!-- Applied - Always shown -->
                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon bg-primary bg-opacity-10 rounded-circle me-3 d-flex align-items-center justify-content-center"
                       :class="{ 'completed': true }"
                       style="width: 40px; height: 40px;">
                    <i class="bi bi-send text-primary"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Applied</h6>
                    <p class="text-secondary small mb-0">{{ formatDateTime(application.applied_on) }}</p>
                  </div>
                </div>
                
                <!-- Shortlisted -->
                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon rounded-circle me-3 d-flex align-items-center justify-content-center"
                       :class="getTimelineIconClass('shortlisted')"
                       style="width: 40px; height: 40px;">
                    <i :class="getTimelineIcon('shortlisted')"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Shortlisted</h6>
                    <p v-if="isStatusAtLeast('shortlisted')" class="text-secondary small mb-0">
                      {{ formatDateTime(application.shortlisted_on) }}
                    </p>
                    <p v-else class="text-secondary small mb-0">Pending</p>
                  </div>
                </div>
                
                <!-- Selected -->
                <div class="timeline-item d-flex mb-3">
                  <div class="timeline-icon rounded-circle me-3 d-flex align-items-center justify-content-center"
                       :class="getTimelineIconClass('selected')"
                       style="width: 40px; height: 40px;">
                    <i :class="getTimelineIcon('selected')"></i>
                  </div>
                  <div>
                    <h6 class="text-dark mb-1">Selected</h6>
                    <p v-if="isStatusAtLeast('selected')" class="text-secondary small mb-0">
                      {{ formatDateTime(application.selected_on) }}
                    </p>
                    <p v-else class="text-secondary small mb-0">Pending</p>
                  </div>
                </div>
                
                <!-- Rejected -->
                <div v-if="application.application_status === 'rejected'" class="timeline-item d-flex">
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
        </div>

        <!-- Right Column - Actions & Documents -->
        <div class="col-lg-4">
          <!-- Status Update Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-arrow-repeat text-primary me-2"></i>Update Status
              </h5>
              
              <div class="d-flex gap-2">
                <button 
                  class="btn btn-outline-warning flex-fill" 
                  @click="updateStatus('shortlisted')"
                  :disabled="application.application_status === 'shortlisted' || application.application_status === 'selected' || application.application_status === 'rejected'"
                >
                  <i class="bi bi-star me-2"></i>Shortlist
                </button>
                <button 
                  class="btn btn-outline-success flex-fill" 
                  @click="updateStatus('selected')"
                  :disabled="application.application_status === 'selected' || application.application_status === 'rejected'"
                >
                  <i class="bi bi-check-circle me-2"></i>Select
                </button>
                <button 
                  class="btn btn-outline-danger flex-fill" 
                  @click="updateStatus('rejected')"
                  :disabled="application.application_status === 'rejected'"
                >
                  <i class="bi bi-x-circle me-2"></i>Reject
                </button>
              </div>
            </div>
          </div>

          <!-- Documents Card -->
          <div class="card border-0 mb-4">
            <div class="card-body">
              <h5 class="text-dark mb-3">
                <i class="bi bi-file-text text-primary me-2"></i>Documents
              </h5>
              
              <div class="document-item d-flex align-items-center p-3 bg-light rounded-3 mb-2">
                <i class="bi bi-file-pdf text-danger fs-4 me-3"></i>
                <div class="flex-grow-1">
                  <h6 class="text-dark mb-1">Resume</h6>
                  <small class="text-secondary">Application-specific resume</small>
                </div>
                <a :href="application.resume_url" target="_blank" class="btn btn-sm btn-outline-primary">
                  <i class="bi bi-eye"></i> View
                </a>
              </div>
            </div>
          </div>

          <!-- Interview/Joining Card - Conditional based on status -->
          <div class="card border-0">
            <div class="card-body">
              <!-- Show Joining Date for Selected Students -->
              <div v-if="application.application_status === 'selected'">
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="text-dark mb-0">
                    <i class="bi bi-calendar-check text-primary me-2"></i>
                    Joining Details
                  </h5>
                </div>
                
                <!-- Display Joining Date if exists -->
                <div v-if="application.joining_date" class="joining-info mb-3">
                  <div class="scheduled-interview bg-light p-3 rounded-3">
                    <div class="d-flex align-items-center">
                      <i class="bi bi-calendar text-primary me-2"></i>
                      <span class="text-dark">Joining Date: <strong>{{ formatDate(application.joining_date) }}</strong></span>
                    </div>
                  </div>
                </div>
                
                <!-- Joining Date Form -->
                <form @submit.prevent="submitJoiningDate">
                  <div class="mb-3">
                    <label class="form-label text-dark">Joining Date <span class="text-danger">*</span></label>
                    <input 
                      type="date" 
                      v-model="joiningDate"
                      class="form-control rounded-pill"
                      :min="minJoiningDate"
                      required
                    >
                    <small class="text-secondary">Select the date when the student will join</small>
                  </div>
                  
                  <button type="submit" class="btn btn-primary-custom w-100" :disabled="submitting">
                    <span v-if="submitting" class="spinner-border spinner-border-sm me-2"></span>
                    <i v-else class="bi bi-calendar-check me-2"></i>
                    {{ submitting ? 'Saving...' : (application.joining_date ? 'Update Joining Date' : 'Set Joining Date') }}
                  </button>
                </form>
              </div>

              <!-- Show Interview Schedule for Shortlisted/Applied Students -->
              <div v-else>
                <!-- Show Schedule Interview Form when no interview is scheduled OR when editing -->
                <div v-if="!application.interview_date || showEditForm">
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-dark mb-0">
                      <i class="bi bi-calendar-plus text-primary me-2"></i>
                      {{ showEditForm ? 'Edit Interview' : 'Schedule Interview' }}
                    </h5>
                    <button v-if="showEditForm" class="btn btn-sm btn-outline-secondary rounded-pill" @click="cancelEdit">
                      <i class="bi bi-x me-1"></i> Cancel
                    </button>
                  </div>
                  
                  <form @submit.prevent="scheduleInterview">
                    <div class="mb-3">
                      <label class="form-label text-dark">Interview Date & Time <span class="text-danger">*</span></label>
                      <input 
                        type="datetime-local" 
                        v-model="interview.date" 
                        class="form-control rounded-pill"
                        :min="minDateTime"
                        required
                      >
                    </div>
                    
                    <div class="mb-3">
                      <label class="form-label text-dark">Interview Mode <span class="text-danger">*</span></label>
                      <select v-model="interview.mode" class="form-select rounded-pill" required @change="handleModeChange">
                        <option value="">Select mode</option>
                        <option value="Online">Online</option>
                        <option value="In-person">In-person</option>
                      </select>
                    </div>
                    
                    <!-- Location field for In-person mode -->
                    <div v-if="interview.mode === 'In-person'" class="mb-3">
                      <label class="form-label text-dark">Interview Location <span class="text-danger">*</span></label>
                      <input 
                        type="text" 
                        v-model="interview.location" 
                        class="form-control rounded-pill" 
                        placeholder="e.g., Conference Room, Company Office"
                        required
                      >
                      <small class="text-secondary">Enter the complete address/location for the interview</small>
                    </div>
                    
                    <!-- Meeting link for Online mode -->
                    <div v-if="interview.mode === 'Online'" class="mb-3">
                      <label class="form-label text-dark">Meeting Link</label>
                      <input 
                        type="url" 
                        v-model="interview.meeting_link" 
                        class="form-control rounded-pill" 
                        placeholder="e.g., https://meet.google.com/xxx"
                      >
                      <small class="text-secondary">Share Google Meet or other video call link</small>
                    </div>
                    
                    <div class="d-flex gap-2">
                      <button type="submit" class="btn btn-primary-custom flex-grow-1" :disabled="scheduling || !isInterviewFormValid">
                        <span v-if="scheduling" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="bi bi-calendar-check me-2"></i>
                        {{ scheduling ? 'Scheduling...' : (showEditForm ? 'Update Interview' : 'Schedule Interview') }}
                      </button>
                    </div>
                  </form>
                </div>

                <!-- Show Scheduled Interview Details when interview is scheduled and not editing -->
                <div v-else>
                  <div class="d-flex justify-content-between align-items-center mb-3">
                    <h5 class="text-dark mb-0">
                      <i class="bi bi-info-circle text-primary me-2"></i>Scheduled Interview
                    </h5>
                    <button class="btn btn-sm btn-outline-primary rounded-pill" @click="startEdit">
                      <i class="bi bi-pencil me-1"></i> Edit
                    </button>
                  </div>
                  
                  <div class="scheduled-interview bg-light p-3 rounded-3">
                    <div class="d-flex align-items-center mb-2">
                      <i class="bi bi-calendar text-primary me-2"></i>
                      <span class="text-dark">{{ formatDateTime(application.interview_date) }}</span>
                    </div>
                    
                    <div class="d-flex align-items-center mb-2">
                      <i class="bi bi-laptop text-primary me-2"></i>
                      <span class="text-dark">Mode: {{ application.interview_mode }}</span>
                    </div>
                    
                    <!-- Show meeting link for online interviews -->
                    <div v-if="application.interview_mode === 'Online' && application.meeting_link" class="d-flex align-items-center mb-2">
                      <i class="bi bi-camera-video text-primary me-2"></i>
                      <a :href="application.meeting_link" target="_blank" class="text-primary text-decoration-none">
                        {{ application.meeting_link }}
                      </a>
                    </div>
                    
                    <!-- Show location for in-person interviews -->
                    <div v-if="application.interview_mode === 'In-person' && application.interview_location" class="d-flex align-items-center">
                      <i class="bi bi-geo-alt text-primary me-2"></i>
                      <span class="text-dark">{{ application.interview_location }}</span>
                    </div>
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
import { useRouter } from 'vue-router';

export default {
  name: 'ApplicationDetails',

  props: {
    applicationId: {
      type: [String, Number],
      required: true
    }
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  emits: ['back-to-applications', 'update-status', 'token-expired'],

  data() {
    return {
      loading: false,
      error: null,
      application: null,
      scheduling: false,
      submitting: false,
      showEditForm: false,
      interview: {
        date: '',
        mode: '',
        location: '',
        meeting_link: ''
      },
      joiningDate: '',
      placementId: null, // Add this to store placement ID
      statusOrder: ['applied', 'shortlisted', 'selected', 'rejected']
    };
  },

  computed: {
    avatarColor() {
      const colors = ['#667eea', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'];
      if (!this.application?.full_name) return colors[0];
      const hash = this.application.full_name.split('').reduce((a, b) => {
        a = ((a << 5) - a) + b.charCodeAt(0);
        return a & a;
      }, 0);
      return colors[Math.abs(hash) % colors.length];
    },

    minDateTime() {
      const now = new Date();
      now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
      return now.toISOString().slice(0, 16);
    },

    minJoiningDate() {
      const tomorrow = new Date();
      tomorrow.setDate(tomorrow.getDate() + 1);
      return tomorrow.toISOString().split('T')[0];
    },

    isInterviewFormValid() {
      if (!this.interview.date || !this.interview.mode) return false;
      if (this.interview.mode === 'In-person' && !this.interview.location) return false;
      return true;
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
        // Fetch application details
        const res = await axios.get(
          "http://127.0.0.1:5000/api/company/applications",
          this.getAuthHeader()
        );

        const application = res.data.find(
          app => app.application_id === Number(this.applicationId)
        );

        if (!application) {
          this.error = "Application not found";
          return;
        }

        this.application = application;

        // Fetch placements to get joining date if selected
        if (application.application_status === 'selected') {
          try {
            const placementsRes = await axios.get(
              "http://127.0.0.1:5000/api/company/placements",
              this.getAuthHeader()
            );
            
            const placement = placementsRes.data.find(
              p => p.student_id === application.student_id && p.job_id === application.job_id
            );
            
            if (placement) {
              this.application.joining_date = placement.joining_date;
              this.placementId = placement.id;
              this.joiningDate = placement.joining_date || '';
            }
          } catch (err) {
            console.error('Failed to fetch placements:', err);
          }
        }

        // Populate interview form if interview is scheduled (for editing)
        if (application.interview_date) {
          this.interview.date = application.interview_date.slice(0, 16);
          this.interview.mode = application.interview_mode || '';
          
          // Set fields based on mode
          if (application.interview_mode === 'Online') {
            this.interview.meeting_link = application.meeting_link || '';
            this.interview.location = '';
          } else if (application.interview_mode === 'In-person') {
            this.interview.location = application.interview_location || '';
            this.interview.meeting_link = '';
          }
        }

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load application details";
        if (err.response?.status === 401) {
          this.$emit('token-expired');
        }
      } finally {
        this.loading = false;
      }
    },

    isStatusAtLeast(targetStatus) {
      if (!this.application) return false;
      
      const currentIndex = this.statusOrder.indexOf(this.application.application_status);
      const targetIndex = this.statusOrder.indexOf(targetStatus);
      
      return currentIndex >= targetIndex;
    },

    getTimelineIconClass(status) {
      if (this.isStatusAtLeast(status)) {
        return status === 'shortlisted' ? 'bg-warning bg-opacity-10 completed' :
               status === 'selected' ? 'bg-success bg-opacity-10 completed' : '';
      }
      return 'bg-light';
    },

    getTimelineIcon(status) {
      if (this.isStatusAtLeast(status)) {
        return status === 'shortlisted' ? 'bi bi-star text-warning' :
               status === 'selected' ? 'bi bi-check-circle text-success' : 'bi bi-hourglass text-secondary';
      }
      return 'bi bi-hourglass text-secondary';
    },

    async updateStatus(status) {
      if (!confirm(`Are you sure you want to mark this application as ${status}?`)) return;

      try {
        await axios.put(
          `http://127.0.0.1:5000/api/company/applications/${this.application.application_id}/status`,
          { status },
          this.getAuthHeader()
        );

        alert(`Application marked as ${status} successfully!`);
        await this.fetchApplicationDetails();
        this.$emit('update-status');

      } catch (err) {
        alert(err.response?.data?.msg || "Failed to update status");
      }
    },

    handleModeChange() {
      this.interview.location = '';
      this.interview.meeting_link = '';
    },

    startEdit() {
      this.showEditForm = true;
    },

    cancelEdit() {
      this.showEditForm = false;
      if (this.application.interview_date) {
        this.interview.date = this.application.interview_date.slice(0, 16);
        this.interview.mode = this.application.interview_mode || '';
        
        if (this.application.interview_mode === 'Online') {
          this.interview.meeting_link = this.application.meeting_link || '';
          this.interview.location = '';
        } else if (this.application.interview_mode === 'In-person') {
          this.interview.location = this.application.interview_location || '';
          this.interview.meeting_link = '';
        }
      }
    },

    async scheduleInterview() {
      if (!this.interview.date) {
        alert('Please select interview date and time');
        return;
      }

      if (!this.interview.mode) {
        alert('Please select interview mode');
        return;
      }

      if (this.interview.mode === 'In-person' && !this.interview.location) {
        alert('Please enter interview location for in-person interview');
        return;
      }

      this.scheduling = true;

      try {
        const payload = {
          interview_date: this.interview.date,
          interview_mode: this.interview.mode
        };

        if (this.interview.mode === 'In-person') {
          payload.interview_location = this.interview.location;
        } else if (this.interview.mode === 'Online') {
          payload.meeting_link = this.interview.meeting_link;
        }

        await axios.post(
          `http://127.0.0.1:5000/api/company/applications/${this.application.application_id}/schedule-interview`,
          payload,
          this.getAuthHeader()
        );

        alert('Interview scheduled successfully!');
        this.showEditForm = false;
        await this.fetchApplicationDetails();

      } catch (err) {
        alert(err.response?.data?.msg || "Failed to schedule interview");
      } finally {
        this.scheduling = false;
      }
    },

    async submitJoiningDate() {
      if (!this.joiningDate) {
        alert('Please select a joining date');
        return;
      }

      if (!this.placementId) {
        alert('Placement record not found. Please ensure the student is selected first.');
        return;
      }

      this.submitting = true;

      try {
        const payload = {
          joining_date: this.joiningDate
        };

        // Update existing placement using the new PUT endpoint
        await axios.put(
          `http://127.0.0.1:5000/api/company/placements/${this.placementId}`,
          payload,
          this.getAuthHeader()
        );

        alert('Joining date updated successfully!');
        await this.fetchApplicationDetails();

      } catch (err) {
        alert(err.response?.data?.msg || "Failed to update joining date");
      } finally {
        this.submitting = false;
      }
    },

    goBack() {
      this.router.push('/company/dashboard/applications');
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
.application-details-page {
  color: #333;
  min-height: 100%;
  background: #f8f9fa;
  padding: 1.5rem;
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

/* Header Card */
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

/* Cards */
.card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  border: none;
}

.info-box {
  transition: all 0.3s ease;
}

.info-box:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

/* Timeline */
.timeline-icon {
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.timeline-icon.completed {
  transform: scale(1.05);
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

/* Joining Info */
.joining-info {
  margin-bottom: 1rem;
}

.scheduled-interview {
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
}

.scheduled-interview:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
}

/* Responsive */
@media (max-width: 768px) {
  .application-details-page {
    padding: 1rem;
  }
  
  .header-card .row {
    flex-direction: column;
    text-align: center;
  }
  
  .student-avatar-large {
    margin-bottom: 1rem;
  }
  
  .timeline-item:not(:last-child)::after {
    left: 15px;
  }
  
  .d-flex.gap-2 {
    flex-direction: column;
  }
}
</style>