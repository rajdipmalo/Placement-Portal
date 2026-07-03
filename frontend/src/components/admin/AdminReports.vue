<template>
  <div class="admin-reports">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="display-5 fw-bold text-gradient">Reports & Statistics</h1>
      <p class="text-muted">View placement analytics and generate reports</p>
    </div>

    <!-- Date Range Filter -->
    <div class="card filters-card border-0 mb-4">
      <div class="card-body">
        <div class="row g-3 align-items-end">
          <div class="col-md-3">
            <label class="form-label text-dark">From Date</label>
            <input type="date" v-model="dateRange.from" class="form-control rounded-pill">
          </div>
          <div class="col-md-3">
            <label class="form-label text-dark">To Date</label>
            <input type="date" v-model="dateRange.to" class="form-control rounded-pill">
          </div>
          <div class="col-md-3">
            <button class="btn btn-primary-custom w-100" @click="fetchReportData">
              <i class="bi bi-filter me-2"></i>Apply Filter
            </button>
          </div>
          <div class="col-md-3">
            <button class="btn btn-outline-custom w-100" @click="exportReport">
              <i class="bi bi-download me-2"></i>Export Report
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary Cards -->
    <div class="row g-4 mb-4">
      <div class="col-md-3 col-sm-6" v-for="stat in summaryStats" :key="stat.label">
        <div class="stat-card card border-0">
          <div class="card-body">
            <div class="d-flex align-items-center">
              <div class="stat-icon rounded-circle me-3 d-flex align-items-center justify-content-center"
                   :style="{ background: stat.color }">
                <i :class="stat.icon" class="text-white"></i>
              </div>
              <div>
                <h3 class="h2 mb-0 text-dark">{{ stat.value }}</h3>
                <small class="text-secondary">{{ stat.label }}</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row -->
    <div class="row g-4 mb-4">
      <!-- Monthly Applications Chart -->
      <div class="col-lg-6">
        <div class="card border-0 h-100">
          <div class="card-body">
            <h5 class="text-dark mb-3">
              <i class="bi bi-graph-up text-primary me-2"></i>Monthly Applications
            </h5>
            <div class="chart-container">
              <canvas ref="monthlyApplicationsChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Branch-wise Placements Chart -->
      <div class="col-lg-6">
        <div class="card border-0 h-100">
          <div class="card-body">
            <h5 class="text-dark mb-3">
              <i class="bi bi-pie-chart text-primary me-2"></i>Branch-wise Placements
            </h5>
            <div class="chart-container">
              <canvas ref="branchPlacementsChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Second Row Charts -->
    <div class="row g-4 mb-4">
      <!-- Company-wise Placements -->
      <div class="col-lg-6">
        <div class="card border-0">
          <div class="card-body">
            <h5 class="text-dark mb-3">
              <i class="bi bi-bar-chart text-primary me-2"></i>Top Companies by Placements
            </h5>
            <div class="table-responsive">
              <table class="table table-hover">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Placements</th>
                    <th>Success Rate</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="company in topCompanies" :key="company.id">
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="company-logo-small rounded-circle me-2 d-flex align-items-center justify-content-center"
                             :style="{ background: getCompanyColor(company.name) }">
                          {{ company.name.charAt(0) }}
                        </div>
                        {{ company.name }}
                      </div>
                    </td>
                    <td><strong>{{ company.placements }}</strong></td>
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="progress flex-grow-1 me-2" style="height: 6px;">
                          <div class="progress-bar" :style="{ width: company.successRate + '%', background: 'linear-gradient(135deg, #667eea, #764ba2)' }"></div>
                        </div>
                        <span>{{ company.successRate }}%</span>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Application Status Distribution -->
      <div class="col-lg-6">
        <div class="card border-0">
          <div class="card-body">
            <h5 class="text-dark mb-3">
              <i class="bi bi-diagram-3 text-primary me-2"></i>Application Status Distribution
            </h5>
            <div class="chart-container" style="height: 250px;">
              <canvas ref="statusDistributionChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Detailed Statistics Table -->
    <div class="card border-0">
      <div class="card-body">
        <h5 class="text-dark mb-3">
          <i class="bi bi-table text-primary me-2"></i>Detailed Statistics
        </h5>
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th>Metric</th>
                <th>Value</th>
                <th>Trend</th>
                <th>Change</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="metric in detailedStats" :key="metric.label">
                <td>{{ metric.label }}</td>
                <td><strong>{{ metric.value }}</strong></td>
                <td>
                  <span class="badge" :class="metric.trend === 'up' ? 'bg-success' : metric.trend === 'down' ? 'bg-danger' : 'bg-secondary'">
                    <i :class="metric.trend === 'up' ? 'bi bi-arrow-up' : metric.trend === 'down' ? 'bi bi-arrow-down' : 'bi bi-dash'"></i>
                  </span>
                </td>
                <td :class="metric.trend === 'up' ? 'text-success' : metric.trend === 'down' ? 'text-danger' : ''">
                  {{ metric.change }}
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
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'AdminReports',

  data() {
    return {
      dateRange: {
        from: this.getDefaultFromDate(),
        to: this.getDefaultToDate()
      },
      summaryStats: [
        { label: 'Total Students', value: 0, icon: 'bi bi-people', color: 'linear-gradient(135deg, #667eea, #764ba2)' },
        { label: 'Placed Students', value: 0, icon: 'bi bi-trophy', color: 'linear-gradient(135deg, #10b981, #059669)' },
        { label: 'Placement Rate', value: '0%', icon: 'bi bi-percent', color: 'linear-gradient(135deg, #f59e0b, #d97706)' },
        { label: 'Active Companies', value: 0, icon: 'bi bi-building', color: 'linear-gradient(135deg, #3b82f6, #1d4ed8)' }
      ],
      topCompanies: [],
      detailedStats: [],
      charts: {
        monthlyApplications: null,
        branchPlacements: null,
        statusDistribution: null
      },
      monthlyData: {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        applications: [],
        placements: []
      },
      branchData: {
        labels: [],
        counts: []
      },
      statusData: {
        labels: ['Applied', 'Shortlisted', 'Selected', 'Rejected'],
        counts: [0, 0, 0, 0]
      }
    };
  },

  mounted() {
    this.fetchReportData();
  },

  beforeDestroy() {
    // Destroy charts to prevent memory leaks
    Object.values(this.charts).forEach(chart => {
      if (chart) chart.destroy();
    });
  },

  methods: {
    getAuthHeader() {
      const token = localStorage.getItem("token");
      return token ? { headers: { Authorization: `Bearer ${token}` } } : {};
    },

    getDefaultFromDate() {
      const date = new Date();
      date.setMonth(date.getMonth() - 11);
      return date.toISOString().split('T')[0];
    },

    getDefaultToDate() {
      return new Date().toISOString().split('T')[0];
    },

    async fetchReportData() {
      try {
        const params = {
          from: this.dateRange.from,
          to: this.dateRange.to
        };

        const res = await axios.get("http://127.0.0.1:5000/api/admin/reports/statistics", { 
          ...this.getAuthHeader(),
          params 
        });

        const data = res.data;
        
        // Update summary stats
        this.summaryStats[0].value = data.total_students;
        this.summaryStats[1].value = data.placed_students;
        this.summaryStats[2].value = data.placement_percentage.toFixed(1) + '%';
        this.summaryStats[3].value = data.active_companies;

        // Update top companies
        this.topCompanies = data.top_companies;

        // Update detailed stats
        this.detailedStats = data.detailed_stats;

        // Update chart data
        this.monthlyData.applications = data.monthly_applications;
        this.monthlyData.placements = data.monthly_placements;
        this.branchData = data.branch_placements;
        this.statusData.counts = data.status_distribution;

        // Render charts
        this.$nextTick(() => {
          this.renderCharts();
        });

      } catch (err) {
        console.error('Failed to fetch report data:', err);
        // Use dummy data for demo
        this.loadDummyData();
      }
    },

    loadDummyData() {
      // Dummy data for demonstration
      this.summaryStats = [
        { label: 'Total Students', value: 450, icon: 'bi bi-people', color: 'linear-gradient(135deg, #667eea, #764ba2)' },
        { label: 'Placed Students', value: 320, icon: 'bi bi-trophy', color: 'linear-gradient(135deg, #10b981, #059669)' },
        { label: 'Placement Rate', value: '71.1%', icon: 'bi bi-percent', color: 'linear-gradient(135deg, #f59e0b, #d97706)' },
        { label: 'Active Companies', value: 28, icon: 'bi bi-building', color: 'linear-gradient(135deg, #3b82f6, #1d4ed8)' }
      ];

      this.topCompanies = [
        { id: 1, name: 'Google', placements: 45, successRate: 85 },
        { id: 2, name: 'Microsoft', placements: 38, successRate: 82 },
        { id: 3, name: 'Amazon', placements: 32, successRate: 78 },
        { id: 4, name: 'TCS', placements: 28, successRate: 75 },
        { id: 5, name: 'Infosys', placements: 25, successRate: 72 }
      ];

      this.detailedStats = [
        { label: 'Average CGPA of Placed Students', value: '8.2', trend: 'up', change: '+0.3' },
        { label: 'Average Salary Package', value: '₹8.5 LPA', trend: 'up', change: '+5.2%' },
        { label: 'Students with Multiple Offers', value: '85', trend: 'up', change: '+12' },
        { label: 'Companies Visited', value: '32', trend: 'down', change: '-3' },
        { label: 'Total Applications', value: '1,284', trend: 'up', change: '+15.3%' }
      ];

      this.monthlyData = {
        labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        applications: [65, 78, 92, 108, 125, 142, 158, 172, 188, 195, 210, 225],
        placements: [12, 18, 24, 28, 32, 38, 42, 48, 52, 58, 62, 68]
      };

      this.branchData = {
        labels: ['CSE', 'IT', 'ECE', 'EEE', 'MECH', 'CIVIL'],
        counts: [120, 85, 62, 48, 35, 22]
      };

      this.statusData = {
        labels: ['Applied', 'Shortlisted', 'Selected', 'Rejected'],
        counts: [450, 280, 320, 130]
      };

      this.$nextTick(() => {
        this.renderCharts();
      });
    },

    renderCharts() {
      // Destroy existing charts
      Object.values(this.charts).forEach(chart => {
        if (chart) chart.destroy();
      });

      // Monthly Applications Chart
      const monthlyCtx = this.$refs.monthlyApplicationsChart?.getContext('2d');
      if (monthlyCtx) {
        this.charts.monthlyApplications = new Chart(monthlyCtx, {
          type: 'line',
          data: {
            labels: this.monthlyData.labels,
            datasets: [
              {
                label: 'Applications',
                data: this.monthlyData.applications,
                borderColor: '#667eea',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
              },
              {
                label: 'Placements',
                data: this.monthlyData.placements,
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                fill: true
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }

      // Branch Placements Chart
      const branchCtx = this.$refs.branchPlacementsChart?.getContext('2d');
      if (branchCtx) {
        this.charts.branchPlacements = new Chart(branchCtx, {
          type: 'doughnut',
          data: {
            labels: this.branchData.labels,
            datasets: [{
              data: this.branchData.counts,
              backgroundColor: [
                '#667eea',
                '#3b82f6',
                '#10b981',
                '#f59e0b',
                '#8b5cf6',
                '#ef4444'
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                position: 'bottom'
              }
            }
          }
        });
      }

      // Status Distribution Chart
      const statusCtx = this.$refs.statusDistributionChart?.getContext('2d');
      if (statusCtx) {
        this.charts.statusDistribution = new Chart(statusCtx, {
          type: 'bar',
          data: {
            labels: this.statusData.labels,
            datasets: [{
              label: 'Number of Applications',
              data: this.statusData.counts,
              backgroundColor: [
                '#3b82f6',
                '#f59e0b',
                '#10b981',
                '#ef4444'
              ]
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: {
                display: false
              }
            },
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      }
    },

    exportReport() {
      // Prepare report data
      const reportData = {
        generatedOn: new Date().toLocaleString(),
        dateRange: this.dateRange,
        summary: this.summaryStats,
        topCompanies: this.topCompanies,
        monthlyData: this.monthlyData,
        branchData: this.branchData
      };

      // Convert to CSV
      const csv = this.convertToCSV(reportData);
      
      // Download CSV
      const blob = new Blob([csv], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `placement-report-${this.dateRange.from}-to-${this.dateRange.to}.csv`;
      a.click();
      window.URL.revokeObjectURL(url);
    },

    convertToCSV(data) {
      let csv = 'Report Generated On,' + data.generatedOn + '\n\n';
      
      csv += 'Summary Statistics\n';
      csv += 'Metric,Value\n';
      data.summary.forEach(stat => {
        csv += `${stat.label},${stat.value}\n`;
      });

      csv += '\nTop Companies\n';
      csv += 'Company,Placements,Success Rate\n';
      data.topCompanies.forEach(company => {
        csv += `${company.name},${company.placements},${company.successRate}%\n`;
      });

      return csv;
    },

    getCompanyColor(name) {
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
.admin-reports {
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

.stat-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  font-size: 1.5rem;
}

.chart-container {
  height: 300px;
  position: relative;
}

.card {
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

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

.form-control, .form-select {
  border: 2px solid #e0e0e0;
  padding: 0.6rem 1.2rem;
  border-radius: 50px;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  border-color: #764ba2;
  box-shadow: 0 0 0 0.2rem rgba(118, 75, 162, 0.25);
}

.company-logo-small {
  width: 35px;
  height: 35px;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.progress {
  background-color: #e9ecef;
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}

.table th {
  font-weight: 600;
  color: #4b5563;
  border-bottom-width: 2px;
}

.table td {
  vertical-align: middle;
}

.badge {
  padding: 0.5rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* Responsive */
@media (max-width: 768px) {
  .chart-container {
    height: 250px;
  }
  
  .stat-card {
    margin-bottom: 1rem;
  }
}
</style>