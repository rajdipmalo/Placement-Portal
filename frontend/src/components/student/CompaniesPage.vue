<template>
  <div class="companies-page">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Companies</h1>
      <p class="text-muted">Browse companies hiring for placement drives</p>
    </div>

    <!-- Search Filter -->
    <div class="card filters-card border-0 mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-12">
            <div class="input-group">
              <span class="input-group-text bg-white text-secondary border-end-0">
                <i class="bi bi-search"></i>
              </span>
              <input 
                type="text" 
                v-model="searchQuery" 
                placeholder="Search for companies..."
                class="form-control border-start-0 rounded-end-pill"
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="text-secondary mt-3">Loading companies...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-5">
      <i class="bi bi-exclamation-triangle text-danger fs-1"></i>
      <p class="text-danger mt-3">{{ error }}</p>
      <button class="btn btn-primary-custom mt-2" @click="fetchCompanies">
        <i class="bi bi-arrow-repeat me-2"></i>Try Again
      </button>
    </div>

    <!-- Companies Grid View -->
    <div v-else>
      <div class="row g-4">
        <div v-for="company in filteredCompanies" :key="company.id" class="col-lg-4 col-md-6">
          <div class="card company-card border-0 h-100" @click="goToCompanyDrives(company.name)">
            <div class="card-body text-center">
              <div class="company-logo-large rounded-circle mx-auto mb-3 d-flex align-items-center justify-content-center"
                   :style="{ background: getCompanyColor(company.name) }">
                {{ company.name.charAt(0) }}
              </div>
              <h5 class="card-title text-dark mb-2">{{ company.name }}</h5>
              
              <!-- Company Details -->
              <div class="text-start mb-3">
                <p v-if="company.industry" class="text-secondary mb-1 small">
                  <i class="bi bi-building me-2"></i>{{ company.industry }}
                </p>
                <p v-if="company.location" class="text-secondary mb-1 small">
                  <i class="bi bi-geo-alt me-2"></i>{{ company.location }}
                </p>
                <p v-if="company.website" class="text-secondary mb-1 small">
                  <i class="bi bi-link-45deg me-2"></i>
                  <a :href="company.website" target="_blank" class="text-decoration-none" @click.stop>{{ truncateUrl(company.website) }}</a>
                </p>
              </div>

              <p class="text-secondary mb-3">
                <i class="bi bi-briefcase me-2"></i>{{ company.active_jobs_count }} active drive{{ company.active_jobs_count > 1 ? 's' : '' }}
              </p>
              <button class="btn btn-outline-custom w-100">
                View Drives <i class="bi bi-arrow-right ms-2"></i>
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredCompanies.length === 0" class="text-center py-5">
        <i class="bi bi-inbox fs-1 text-secondary"></i>
        <h5 class="text-dark mt-3">No companies found</h5>
        <p class="text-secondary">Try adjusting your search</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { API_URL } from "@/config";

export default {
  name: 'CompaniesPage',

  data() {
    return {
      loading: false,
      error: null,
      companies: [],
      searchQuery: '',
      userProfile: null
    };
  },

  computed: {
    filteredCompanies() {
      if (!this.searchQuery) return this.companies;
      
      const query = this.searchQuery.toLowerCase();
      return this.companies.filter(company => 
        company.name.toLowerCase().includes(query) ||
        (company.industry && company.industry.toLowerCase().includes(query)) ||
        (company.location && company.location.toLowerCase().includes(query))
      );
    }
  },

  mounted() {
    this.fetchCompanies();
    this.fetchUserProfile();
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    async fetchCompanies() {
      this.loading = true;
      this.error = null;

      try {
        const res = await axios.get(
          `${API_URL}/api/student/companies`,
          this.getAuthHeader()
        );

        this.companies = res.data;

      } catch (err) {
        this.error = err.response?.data?.msg || "Failed to load companies";
      } finally {
        this.loading = false;
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

    truncateUrl(url) {
      if (!url) return '';
      return url.replace(/^https?:\/\//, '').substring(0, 25) + (url.length > 25 ? '...' : '');
    },

    goToCompanyDrives(companyName) {
      this.$router.push(`/student/dashboard/companies/${companyName}`);
    }
  }
};
</script>

<style scoped>
.companies-page {
  color: #333;
}

.text-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Filters Card */
.filters-card {
  background: white;
  border-radius: 25px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Company Card */
.company-card {
  background: white;
  border-radius: 25px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  cursor: pointer;
}

.company-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.company-logo-large {
  width: 80px;
  height: 80px;
  font-size: 36px;
  font-weight: 600;
  color: white;
}

/* Form Controls */
.form-control, .form-select {
  border: 2px solid #e0e0e0;
  padding: 0.6rem 1.2rem;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 0.2rem rgba(118, 75, 162, 0.25);
}

.form-control.rounded-pill, .form-select.rounded-pill {
  padding: 0.6rem 1.2rem;
}

.input-group-text {
  background: white;
  border: 2px solid #e0e0e0;
  border-right: none;
  border-radius: 50px 0 0 50px;
}

.input-group .form-control {
  border-left: none;
  border-radius: 0 50px 50px 0;
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

.btn-primary-custom:hover {
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

/* Responsive */
@media (max-width: 768px) {
  .company-logo-large {
    width: 60px;
    height: 60px;
    font-size: 28px;
  }
  
  .row.g-4 {
    --bs-gutter-y: 1rem;
  }
}
</style>