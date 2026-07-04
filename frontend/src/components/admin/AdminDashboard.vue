<template>
  <div class="dashboard-wrapper">
    <!-- Topbar -->
    <header class="topbar d-flex justify-content-between align-items-center px-4">
      <div class="left-section">
        <span class="top-title">NextGig Admin</span>
      </div>

      <div class="right-section d-flex align-items-center gap-3">
        <div class="user-info d-flex align-items-center gap-2 px-3 py-2">
          <span class="user-name">{{ adminName || 'Admin' }}</span>
          <span class="badge" :class="roleBadgeClass">
            {{ formattedRole }}
          </span>
        </div>

        <button class="btn btn-outline-custom d-flex align-items-center gap-2" @click="confirmLogout">
          <i class="bi bi-box-arrow-right"></i>
          <span class="d-none d-md-inline">Logout</span>
        </button>
      </div>
    </header>

    <div class="dashboard-container d-flex">
      <!-- Sidebar -->
      <aside class="sidebar p-4 d-flex flex-column">
        <nav class="nav-wrapper flex-grow-1 d-flex flex-column">
          <ul class="nav-list list-unstyled">
            <li
              v-for="item in navItems"
              :key="item.id"
              :class="{ active: isActiveTab(item.id) }"
              @click="navigateToTab(item.id)"
              class="nav-item d-flex align-items-center px-3 py-3 mb-2"
            >
              <i :class="item.icon" class="me-3"></i>
              <span class="nav-label">{{ item.label }}</span>
              <span v-if="item.badge" class="badge ms-auto" :class="badgeClass">{{ item.badge }}</span>
            </li>
          </ul>
        </nav>
      </aside>


      <main class="content p-4 flex-grow-1">
        <router-view 
          @update-admin-name="updateAdminName"
          @token-expired="handleTokenExpired"
        />
      </main>
    </div>


    <div v-if="showLogoutModal" class="modal-overlay" @click.self="closeLogoutModal">
      <div class="modal-content">
        <h3 class="h5 mb-3">Confirm Logout</h3>
        <p class="text-secondary mb-4">Are you sure you want to logout?</p>
        <div class="modal-actions d-flex gap-3 justify-content-end">
          <button class="btn btn-secondary" @click="closeLogoutModal">Cancel</button>
          <button class="btn btn-danger" @click="logout">Logout</button>
        </div>
      </div>
    </div>

    <!-- Session Expired Modal -->
    <div v-if="showSessionExpiredModal" class="modal-overlay" @click.self="redirectToLogin">
      <div class="modal-content">
        <h3 class="h5 mb-3">Session Expired</h3>
        <p class="text-secondary mb-4">Your session has expired. Please login again.</p>
        <div class="modal-actions d-flex gap-3 justify-content-end">
          <button class="btn btn-danger" @click="redirectToLogin">Go to Login</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { API_URL } from "@/config";

export default {
  name: 'AdminDashboard',

  data() {
    return {
      adminName: localStorage.getItem("adminName") || "Admin",
      userRole: "admin",
      showLogoutModal: false,
      showSessionExpiredModal: false,
      navItems: [
        { id: "home", label: "Dashboard", icon: "bi bi-speedometer2", badge: null },
        { id: "companies", label: "Companies", icon: "bi bi-building", badge: null },
        { id: "students", label: "Students", icon: "bi bi-people", badge: null },
        { id: "drives", label: "Placement Drives", icon: "bi bi-briefcase", badge: null },
        { id: "applications", label: "Applications", icon: "bi bi-file-text", badge: null },
        { id: "reports", label: "Reports", icon: "bi bi-graph-up", badge: null }
      ],
      tokenCheckInterval: null
    };
  },

  computed: {
    formattedRole() {
      return 'Admin';
    },

    roleBadgeClass() {
      return 'badge-admin';
    },

    badgeClass() {
      return 'badge-primary';
    }
  },

  watch: {
    '$route.path': {
      handler() {
        // Force re-evaluation of active tab
      },
      immediate: true
    }
  },

  methods: {
    isActiveTab(tabId) {
      const path = this.$route.path;
      
      switch(tabId) {
        case 'home':
          return path === '/admin/dashboard';
        case 'companies':
          return path.startsWith('/admin/dashboard/companies');
        case 'students':
          return path.startsWith('/admin/dashboard/students');
        case 'drives':
          return path.startsWith('/admin/dashboard/drives');
        case 'applications':
          return path.startsWith('/admin/dashboard/applications');
        case 'reports':
          return path === '/admin/dashboard/reports';
        default:
          return false;
      }
    },

    navigateToTab(tabId) {
      if (this.isActiveTab(tabId)) return;

      switch(tabId) {
        case 'home':
          this.$router.push('/admin/dashboard');
          break;
        case 'companies':
          this.$router.push('/admin/dashboard/companies');
          break;
        case 'students':
          this.$router.push('/admin/dashboard/students');
          break;
        case 'drives':
          this.$router.push('/admin/dashboard/drives');
          break;
        case 'applications':
          this.$router.push('/admin/dashboard/applications');
          break;
        case 'reports':
          this.$router.push('/admin/dashboard/reports');
          break;
      }
    },

    updateAdminName(name) {
      this.adminName = name;
      localStorage.setItem("adminName", name);
    },

    confirmLogout() {
      this.showLogoutModal = true;
    },

    closeLogoutModal() {
      this.showLogoutModal = false;
    },

    handleTokenExpired() {
      this.showSessionExpiredModal = true;
      setTimeout(() => {
        if (this.showSessionExpiredModal) {
          this.redirectToLogin();
        }
      }, 3000);
    },

    redirectToLogin() {
      this.clearAuthData();
      this.showSessionExpiredModal = false;
      this.$router.push("/login");
    },

    clearAuthData() {
      localStorage.removeItem("token");
      localStorage.removeItem("role");
      localStorage.removeItem("adminName");
    },

    logout() {
      this.clearAuthData();
      this.showLogoutModal = false;
      this.$router.push("/login");
    },

    setupAxiosInterceptors() {
      axios.interceptors.response.use(
        response => response,
        error => {
          if (error.response && (error.response.status === 401 || error.response.status === 403)) {
            this.handleTokenExpired();
          }
          return Promise.reject(error);
        }
      );
    }
  },

  mounted() {
    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");
    
    if (!token || role !== 'admin') {
      this.$router.push("/login");
      return;
    }
    this.setupAxiosInterceptors();
  },

  beforeDestroy() {
    if (this.tokenCheckInterval) {
      clearInterval(this.tokenCheckInterval);
    }
  }
};
</script>

<style scoped>
.dashboard-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Topbar */
.topbar {
  height: 70px;
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border-bottom: 2px solid rgba(118, 75, 162, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.top-title {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.user-info {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 40px;
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.user-name {
  font-weight: 500;
  color: #ffffff;
}

/* Role Badges */
.badge-admin {
  background: rgba(240, 90, 103, 0.3);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  backdrop-filter: blur(5px);
}

.badge-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.btn-outline-custom {
  background: white;
  border: 2px solid #667eea;
  color: #667eea;
  padding: 6px 16px !important;
  border-radius: 40px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.btn-outline-custom:hover {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
}

/* Layout */
.dashboard-container {
  height: calc(100vh - 70px);
}

/* Sidebar - FIX: Prevent nav items from shrinking */
.sidebar {
  width: 260px;
  background: rgba(255, 255, 255, 0.95);
  color: #333;
  border-right: 1px solid rgba(118, 75, 162, 0.2);
  overflow-y: auto;
  box-shadow: 4px 0 15px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  flex-shrink: 0; /* Prevent sidebar from shrinking */
}

/* Navigation Wrapper - ensures nav doesn't compress */
.nav-wrapper {
  min-height: 0; /* Important for flex containers */
  justify-content: flex-start; /* Items stay at top */
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 0; /* Use margin-bottom on items instead */
}

/* FIX: Nav items maintain consistent size */
.nav-item {
  border-radius: 50px;
  cursor: pointer;
  color: #666;
  transition: all 0.25s ease;
  border: 1px solid transparent;
  flex-shrink: 0; /* Prevent items from shrinking */
  min-height: 50px; /* Maintain minimum height */
  font-size: 0.95rem; /* Keep consistent font size */
}

.nav-item:hover {
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-color: rgba(102, 126, 234, 0.3);
  transform: translateX(3px);
}

.nav-item.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  box-shadow: 0 6px 12px rgba(102, 126, 234, 0.25);
  border-color: #764ba2;
}

.nav-item i {
  font-size: 1.3rem;
  color: #667eea;
  flex-shrink: 0; /* Icon doesn't shrink */
}

.nav-item.active i {
  color: white;
}

.nav-label {
  font-weight: 500;
  white-space: nowrap; /* Prevent text wrapping */
}

/* Content */
.content {
  background: rgba(255, 255, 255, 0.95);
  overflow-y: auto;
  backdrop-filter: blur(10px);
  flex-grow: 1;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 25px;
  max-width: 400px;
  width: 90%;
  border: none;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  animation: slideIn 0.3s ease;
}

.modal-content h3 {
  color: #333;
  font-weight: 600;
}

.modal-content p {
  color: #666;
}

.modal-actions .btn {
  padding: 8px 20px;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.modal-actions .btn-secondary {
  background: #e0e0e0;
  border: none;
  color: #666;
}

.modal-actions .btn-secondary:hover {
  background: #d0d0d0;
  transform: translateY(-2px);
}

.modal-actions .btn-danger {
  background: linear-gradient(135deg, #f05a67 0%, #d94b57 100%);
  border: none;
  color: white;
}

.modal-actions .btn-danger:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(240, 90, 103, 0.4);
}

/* Animation */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Scrollbar */
::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: #f0f0f0;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #5a67d8 0%, #6b3fa0 100%);
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 70px;
    bottom: 0;
    z-index: 100;
    width: 240px;
  }
  
  .btn-outline-custom span {
    display: none;
  }
}
</style>