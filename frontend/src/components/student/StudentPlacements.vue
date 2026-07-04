<template>
  <div class="student-placements">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">My Placements</h1>
      <p class="text-muted">View all your selected jobs and placement details</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading your placements...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchPlacements">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- No Placements State -->
    <div v-else-if="placements.length === 0" class="text-center py-5">
      <div class="empty-state">
        <i class="bi bi-trophy text-secondary fs-1"></i>
        <h5 class="text-dark mt-3">No Placements Yet</h5>
        <p class="text-secondary">You haven't been selected for any jobs yet.</p>
        <router-link to="/student/dashboard/companies" class="btn-sm btn-primary-custom mt-3">
          <i class="bi-building building-icon me-2"></i>Browse Companies
        </router-link>
      </div>
    </div>

    <!-- Placements Grid -->
    <div v-else class="placements-grid">
      <!-- Placements List - Medium sized cards -->
      <div class="row g-4">
        <div v-for="placement in placements" :key="placement.company_id + placement.position" class="col-md-6 col-lg-4">
          <div class="placement-card card border-0 h-100">
            <div class="card-body p-4">
              <!-- Header with Company Logo -->
              <div class="d-flex align-items-center mb-3">
                <div class="company-logo rounded-circle me-3 d-flex align-items-center justify-content-center"
                     :style="{ background: getCompanyColor(placement.company) }">
                  {{ placement.company.charAt(0) }}
                </div>
                <div class="flex-grow-1">
                  <h5 class="text-dark mb-1 fw-bold">{{ placement.company }}</h5>
                  <span class="badge bg-success">Selected</span>
                </div>
              </div>

              <!-- Position and Salary -->
              <div class="row g-3 mb-3">
                <div class="col-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Position</small>
                    <strong class="text-dark">{{ placement.position }}</strong>
                  </div>
                </div>
                <div class="col-6">
                  <div class="info-box bg-light p-3 rounded-3">
                    <small class="text-secondary d-block">Salary</small>
                    <strong class="text-dark">{{ placement.salary || 'Not specified' }}</strong>
                  </div>
                </div>
              </div>

              <!-- Joining Date Section -->
              <div v-if="placement.joining_date" class="joining-section bg-light p-3 rounded-3 mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <div>
                    <small class="text-secondary d-block">Joining Date</small>
                    <strong class="text-success">{{ formatDate(placement.joining_date) }}</strong>
                  </div>
                  <span class="badge" :class="getJoiningStatusClass(placement)">
                    {{ getJoiningStatus(placement) }}
                  </span>
                </div>
                
                <!-- Countdown Timer -->
                <div class="countdown-timer">
                  <div class="d-flex justify-content-between align-items-center mb-1">
                    <small class="text-secondary">Days left:</small>
                    <strong class="text-primary">{{ getDaysUntilJoining(placement) }}</strong>
                  </div>
                  <div class="progress" style="height: 6px;">
                    <div class="progress-bar" 
                         :class="getProgressBarClass(placement)"
                         :style="{ width: getJoiningProgress(placement) + '%' }"></div>
                  </div>
                  <!-- Optional: Show selection date info -->
                  <div v-if="placement.selected_on" class="d-flex justify-content-between mt-2">
                    <small class="text-secondary">Selected on:</small>
                    <small class="text-dark">{{ formatDate(placement.selected_on) }}</small>
                  </div>
                </div>
              </div>

              <!-- No Joining Date Message -->
              <div v-else class="no-joining bg-light p-3 rounded-3 mb-3">
                <div class="text-center">
                  <i class="bi bi-clock-history text-secondary fs-5"></i>
                  <p class="text-secondary mt-2 mb-0">Joining date not set</p>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="d-flex gap-2">
                <button class="btn btn-outline-custom flex-grow-1" @click="viewJobDetails(placement)">
                  <i class="bi bi-eye me-2"></i>View Details
                </button>
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
  name: 'StudentPlacements',

  data() {
    return {
      loading: false,
      error: null,
      placements: []
    };
  },

  mounted() {
    this.fetchPlacements();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchPlacements() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `${API_URL}/api/student/placements`,
          this.getAuthHeader()
        );
        this.placements = res.data;
        console.log("Placements data:", res.data);
      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load placements";
        console.error('Fetch placements error:', err);
      } finally {
        this.loading = false;
      }
    },

    viewJobDetails(placement) {
      if (placement.job_id) {
        this.$router.push(`/student/dashboard/companies/${placement.company}/job/${placement.job_id}`);
      } else {
        alert('Job details not available');
      }
    },

    downloadOffer(placement) {
      if (placement.offer_letter) {
        window.open(placement.offer_letter, '_blank');
      }
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

    getDaysUntilJoining(placement) {
      if (!placement.joining_date) return 'TBD';
      const joiningDate = new Date(placement.joining_date);
      const today = new Date();
      const diffTime = joiningDate - today;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays < 0) return 'Passed';
      if (diffDays === 0) return 'Today!';
      return `${diffDays} days`;
    },

    getJoiningStatus(placement) {
      if (!placement.joining_date) return 'Not Set';
      const joiningDate = new Date(placement.joining_date);
      const today = new Date();
      
      if (joiningDate < today) return 'Joined';
      if (joiningDate.toDateString() === today.toDateString()) return 'Today';
      return 'Upcoming';
    },

    getJoiningStatusClass(placement) {
      if (!placement.joining_date) return 'bg-secondary';
      const joiningDate = new Date(placement.joining_date);
      const today = new Date();
      
      if (joiningDate < today) return 'bg-secondary';
      if (joiningDate.toDateString() === today.toDateString()) return 'bg-warning';
      return 'bg-success';
    },

    getJoiningProgress(placement) {
      // If no joining date or selection date, return 0
      if (!placement.joining_date || !placement.selected_on) return 0;
      
      const joiningDate = new Date(placement.joining_date);
      const selectedDate = new Date(placement.selected_on);
      const today = new Date();
      
      // If joining date is in the past, progress is 100%
      if (joiningDate < today) return 100;
      
      // Calculate total duration from selection to joining (in milliseconds)
      const totalDuration = joiningDate - selectedDate;
      
      // If total duration is zero or negative, return 0
      if (totalDuration <= 0) return 0;
      
      // Calculate time elapsed since selection
      const timeElapsed = today - selectedDate;
      
      // Calculate progress percentage
      let progress = (timeElapsed / totalDuration) * 100;
      
      // Ensure progress is between 0 and 100
      progress = Math.min(100, Math.max(0, progress));
      
      return Math.round(progress * 10) / 10; // Round to 1 decimal place
    },

    getProgressBarClass(placement) {
      if (!placement.joining_date) return 'bg-secondary';
      
      const joiningDate = new Date(placement.joining_date);
      const today = new Date();
      
      if (joiningDate < today) return 'bg-secondary';
      if (joiningDate.toDateString() === today.toDateString()) return 'bg-warning';
      
      // Get progress to determine color intensity
      const progress = this.getJoiningProgress(placement);
      if (progress >= 75) return 'bg-success';
      if (progress >= 50) return 'bg-info';
      if (progress >= 25) return 'bg-primary';
      return 'bg-success'; // Default
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
.student-placements {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Placement Card - Medium size */
.placement-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.placement-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.company-logo {
  width: 50px;
  height: 50px;
  font-size: 22px;
  font-weight: 600;
  color: white;
  flex-shrink: 0;
}

.info-box {
  transition: all 0.3s ease;
}

.info-box:hover {
  background: #ffffff !important;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
}

/* Joining Section */
.joining-section {
  border-left: 4px solid #10b981;
  transition: all 0.3s ease;
}

.joining-section:hover {
  background: #ffffff !important;
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
}

.no-joining {
  border-left: 4px solid #6c757d;
  transition: all 0.3s ease;
}

.no-joining:hover {
  background: #ffffff !important;
  box-shadow: 0 4px 12px rgba(108, 117, 125, 0.1);
}

/* Progress Bar */
.progress {
  background-color: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.3s ease;
}

.progress-bar.bg-success {
  background: linear-gradient(135deg, #10b981, #059669) !important;
}

.progress-bar.bg-warning {
  background: linear-gradient(135deg, #f59e0b, #d97706) !important;
}

.progress-bar.bg-info {
  background: linear-gradient(135deg, #3b82f6, #1d4ed8) !important;
}

.progress-bar.bg-primary {
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
}

.progress-bar.bg-secondary {
  background: linear-gradient(135deg, #6c757d, #5a6268) !important;
}

/* Countdown Timer */
.countdown-timer {
  font-size: 0.9rem;
}

/* Empty State */
.empty-state {
  padding: 3rem;
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.empty-state i {
  font-size: 4rem;
}

/* Button Styles */
.btn-primary-custom {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
  padding: 0.6rem 1.5rem;
  border-radius: 50px;
  font-weight: 500;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.btn-primary-custom:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  color: white;
}

.btn-primary-custom .building-icon {
  font-size: 0.8rem;
  vertical-align: middle;
}

.btn-outline-custom {
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  padding: 0.5rem 1.2rem;
  border-radius: 50px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.btn-outline-custom:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

.btn-outline-success {
  border: 2px solid #10b981;
  color: #10b981;
  background: white;
  border-radius: 50px;
  padding: 0.5rem 1rem;
  font-size: 0.95rem;
  transition: all 0.3s ease;
}

.btn-outline-success:hover {
  background: #10b981;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(16, 185, 129, 0.4);
}

/* Badge Styles */
.badge.bg-success {
  background: #10b981 !important;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.8rem;
}

.badge.bg-warning {
  background: #f59e0b !important;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.8rem;
}

.badge.bg-secondary {
  background: #6c757d !important;
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 50px;
  font-size: 0.8rem;
}

/* Responsive */
@media (max-width: 768px) {
  .company-logo {
    width: 45px;
    height: 45px;
    font-size: 20px;
  }
  
  .placement-card {
    margin-bottom: 1rem;
  }
}
</style>