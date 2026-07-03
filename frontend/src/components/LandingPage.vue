<template>
  <div class="landing-page">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg fixed-top">
      <div class="container">
        <router-link to="/" class="navbar-brand">
          <span class="brand-text">NextGig</span>
        </router-link>
        
        <button class="navbar-toggler" type="button" @click="isMenuOpen = !isMenuOpen">
          <i class="bi bi-list fs-1"></i>
        </button>
        
        <div class="collapse navbar-collapse" :class="{ 'show': isMenuOpen }">
          <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <a class="nav-link" href="#features">Features</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#how-it-works">How It Works</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#companies">For Companies</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#students">For Students</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#contact">Contact</a>
            </li>
            <li class="nav-item ms-lg-3">
              <router-link to="/login" class="btn btn-outline-custom me-2">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register/student" class="btn btn-primary-custom">Get Started</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
      <div class="container">
        <div class="row align-items-center min-vh-100">
          <div class="col-lg-6 hero-content">
            <h1 class="display-3 fw-bold mb-4">
              <span class="gradient-text">NextGig</span>
              <br>Your Gateway to
              <span class="gradient-text">Dream Careers</span>
            </h1>
            <p class="lead text-secondary mb-4">
              The ultimate placement management platform connecting talented students 
              with leading companies. Streamline your recruitment process and land your dream job.
            </p>
            <div class="d-flex gap-3 flex-wrap">
              <router-link to="/register/student" class="btn btn-primary-custom btn-lg">
                <i class="bi bi-person-plus me-2"></i>Join as Student
              </router-link>
              <router-link to="/register/company" class="btn btn-outline-custom btn-lg">
                <i class="bi bi-building me-2"></i>Register Company
              </router-link>
            </div>
            <div class="mt-5">
              <div class="row g-4">
                <div class="col-4">
                  <div class="stat-item">
                    <h3 class="h2 fw-bold gradient-text">500+</h3>
                    <p class="text-secondary">Companies</p>
                  </div>
                </div>
                <div class="col-4">
                  <div class="stat-item">
                    <h3 class="h2 fw-bold gradient-text">10k+</h3>
                    <p class="text-secondary">Students</p>
                  </div>
                </div>
                <div class="col-4">
                  <div class="stat-item">
                    <h3 class="h2 fw-bold gradient-text">1000+</h3>
                    <p class="text-secondary">Placements</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-lg-6 hero-image">
            <div class="hero-illustration">
              <i class="bi bi-briefcase-fill floating-icon"></i>
              <i class="bi bi-people-fill floating-icon"></i>
              <i class="bi bi-building floating-icon"></i>
              <i class="bi bi-trophy-fill floating-icon"></i>
            </div>
          </div>
        </div>
      </div>
      <div class="hero-shape">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320">
          <path fill="#667eea" fill-opacity="0.1" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,122.7C672,117,768,139,864,154.7C960,171,1056,181,1152,170.7C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path>
        </svg>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="display-5 fw-bold mb-3">Why Choose <span class="gradient-text">NextGig</span></h2>
          <p class="lead text-secondary">Powerful features that make placement management effortless</p>
        </div>
        
        <div class="row g-4">
          <div v-for="feature in features" :key="feature.title" class="col-lg-4 col-md-6">
            <div class="feature-card card border-0 h-100">
              <div class="card-body text-center p-4">
                <div class="feature-icon mb-4">
                  <i :class="feature.icon"></i>
                </div>
                <h5 class="card-title fw-bold mb-3">{{ feature.title }}</h5>
                <p class="card-text text-secondary">{{ feature.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how-it-works" class="how-it-works-section py-5 bg-light">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="display-5 fw-bold mb-3">How It <span class="gradient-text">Works</span></h2>
          <p class="lead text-secondary">Simple steps to start your placement journey</p>
        </div>

        <div class="row">
          <div v-for="(step, index) in steps" :key="step.title" class="col-lg-3 col-md-6 mb-4">
            <div class="step-card text-center">
              <div class="step-number mb-3">{{ index + 1 }}</div>
              <div class="step-icon mb-3">
                <i :class="step.icon"></i>
              </div>
              <h5 class="fw-bold mb-2">{{ step.title }}</h5>
              <p class="text-secondary small">{{ step.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- For Companies Section -->
    <section id="companies" class="companies-section py-5">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 mb-4 mb-lg-0">
            <div class="companies-illustration text-center">
              <i class="bi bi-building fs-1 text-primary"></i>
              <i class="bi bi-briefcase fs-1 text-success mx-3"></i>
              <i class="bi bi-bar-chart fs-1 text-warning"></i>
            </div>
          </div>
          <div class="col-lg-6">
            <h2 class="display-5 fw-bold mb-4">
              For <span class="gradient-text">Companies</span>
            </h2>
            <p class="lead text-secondary mb-4">
              Streamline your campus recruitment process with our comprehensive placement management system.
            </p>
            
            <div class="benefits-list">
              <div v-for="benefit in companyBenefits" :key="benefit" class="benefit-item d-flex mb-3">
                <i class="bi bi-check-circle-fill text-success me-3"></i>
                <span>{{ benefit }}</span>
              </div>
            </div>
            
            <router-link to="/register/company" class="btn btn-primary-custom btn-lg mt-4">
              <i class="bi bi-building me-2"></i>Register Your Company
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- For Students Section -->
    <section id="students" class="students-section py-5 bg-light">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 order-lg-2 mb-4 mb-lg-0">
            <div class="students-illustration text-center">
              <i class="bi bi-person-circle fs-1 text-primary"></i>
              <i class="bi bi-journal-bookmark-fill fs-1 text-success mx-3"></i>
              <i class="bi bi-trophy-fill fs-1 text-warning"></i>
            </div>
          </div>
          <div class="col-lg-6 order-lg-1">
            <h2 class="display-5 fw-bold mb-4">
              For <span class="gradient-text">Students</span>
            </h2>
            <p class="lead text-secondary mb-4">
              Discover your dream career with access to top companies and personalized job recommendations.
            </p>
            
            <div class="benefits-list">
              <div v-for="benefit in studentBenefits" :key="benefit" class="benefit-item d-flex mb-3">
                <i class="bi bi-check-circle-fill text-success me-3"></i>
                <span>{{ benefit }}</span>
              </div>
            </div>
            
            <router-link to="/register/student" class="btn btn-primary-custom btn-lg mt-4">
              <i class="bi bi-person-plus me-2"></i>Join as Student
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Testimonials Section -->
    <section class="testimonials-section py-5">
      <div class="container">
        <div class="text-center mb-5">
          <h2 class="display-5 fw-bold mb-3">What People <span class="gradient-text">Say</span></h2>
          <p class="lead text-secondary">Success stories from our community</p>
        </div>

        <div class="row">
          <div v-for="testimonial in testimonials" :key="testimonial.name" class="col-lg-4 col-md-6 mb-4">
            <div class="testimonial-card card border-0 h-100">
              <div class="card-body p-4">
                <div class="rating mb-3">
                  <i v-for="star in 5" :key="star" class="bi bi-star-fill text-warning me-1"></i>
                </div>
                <p class="testimonial-text text-secondary mb-4">"{{ testimonial.text }}"</p>
                <div class="d-flex align-items-center">
                  <div class="testimonial-avatar me-3">
                    {{ getInitials(testimonial.name) }}
                  </div>
                  <div>
                    <h6 class="fw-bold mb-1">{{ testimonial.name }}</h6>
                    <small class="text-secondary">{{ testimonial.role }}</small>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-5">
      <div class="container">
        <div class="cta-card card border-0">
          <div class="card-body text-center p-5">
            <h2 class="display-5 fw-bold mb-4 text-white">Ready to Start Your Journey?</h2>
            <p class="lead text-white-50 mb-4">Join thousands of students and companies already on NextGig</p>
            <div class="d-flex justify-content-center gap-3 flex-wrap">
              <router-link to="/register/student" class="btn btn-light btn-lg">
                <i class="bi bi-person-plus me-2"></i>Join as Student
              </router-link>
              <router-link to="/register/company" class="btn btn-outline-light btn-lg">
                <i class="bi bi-building me-2"></i>Register Company
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer id="contact" class="footer py-5 bg-dark">
      <div class="container">
        <div class="row g-4">
          <div class="col-lg-4">
            <h5 class="text-white mb-3">NextGig</h5>
            <p class="text-secondary">Your gateway to dream careers. Connecting talented students with leading companies.</p>
            <div class="social-links">
              <a href="#" class="text-secondary me-3"><i class="bi bi-facebook fs-5"></i></a>
              <a href="#" class="text-secondary me-3"><i class="bi bi-twitter fs-5"></i></a>
              <a href="#" class="text-secondary me-3"><i class="bi bi-linkedin fs-5"></i></a>
              <a href="#" class="text-secondary"><i class="bi bi-instagram fs-5"></i></a>
            </div>
          </div>
          <div class="col-lg-2 col-md-6">
            <h6 class="text-white mb-3">Quick Links</h6>
            <ul class="list-unstyled">
              <li class="mb-2"><a href="#features" class="text-secondary text-decoration-none">Features</a></li>
              <li class="mb-2"><a href="#how-it-works" class="text-secondary text-decoration-none">How It Works</a></li>
              <li class="mb-2"><a href="#companies" class="text-secondary text-decoration-none">For Companies</a></li>
              <li class="mb-2"><a href="#students" class="text-secondary text-decoration-none">For Students</a></li>
            </ul>
          </div>
          <div class="col-lg-3 col-md-6">
            <h6 class="text-white mb-3">Contact Us</h6>
            <ul class="list-unstyled">
              <li class="mb-2 text-secondary"><i class="bi bi-envelope me-2"></i>info@nextgig.com</li>
              <li class="mb-2 text-secondary"><i class="bi bi-telephone me-2"></i>+1 234 567 890</li>
              <li class="mb-2 text-secondary"><i class="bi bi-geo-alt me-2"></i>123 Tech Street, Silicon Valley</li>
            </ul>
          </div>
          <div class="col-lg-3">
            <h6 class="text-white mb-3">Newsletter</h6>
            <p class="text-secondary small">Subscribe to get updates about new features and opportunities</p>
            <div class="input-group">
              <input type="email" class="form-control rounded-pill" placeholder="Your email">
              <button class="btn btn-primary-custom rounded-pill">Subscribe</button>
            </div>
          </div>
        </div>
        <hr class="my-4 bg-secondary">
        <div class="text-center">
          <p class="text-secondary mb-0">&copy; 2024 NextGig. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',

  data() {
    return {
      isMenuOpen: false,
      features: [
        {
          icon: 'bi bi-briefcase fs-1',
          title: 'Smart Job Matching',
          description: 'AI-powered algorithm matches students with the most relevant job opportunities based on their skills and preferences.'
        },
        {
          icon: 'bi bi-building fs-1',
          title: 'Company Dashboard',
          description: 'Comprehensive dashboard for companies to manage drives, track applications, and schedule interviews efficiently.'
        },
        {
          icon: 'bi bi-people fs-1',
          title: 'Student Portal',
          description: 'Intuitive portal for students to browse jobs, track applications, and receive personalized recommendations.'
        },
        {
          icon: 'bi bi-calendar-check fs-1',
          title: 'Drive Management',
          description: 'End-to-end management of placement drives from creation to completion with automated workflows.'
        },
        {
          icon: 'bi bi-file-text fs-1',
          title: 'Application Tracking',
          description: 'Real-time tracking of applications with status updates and interview scheduling capabilities.'
        },
        {
          icon: 'bi bi-graph-up fs-1',
          title: 'Analytics & Reports',
          description: 'Detailed analytics and reports for administrators to track placement statistics and trends.'
        }
      ],
      steps: [
        {
          icon: 'bi bi-person-plus fs-2',
          title: 'Create Account',
          description: 'Sign up as a student or company to get started'
        },
        {
          icon: 'bi bi-briefcase fs-2',
          title: 'Browse Opportunities',
          description: 'Explore available drives and job opportunities'
        },
        {
          icon: 'bi bi-send fs-2',
          title: 'Apply',
          description: 'Submit applications with your profile and resume'
        },
        {
          icon: 'bi bi-trophy fs-2',
          title: 'Get Placed',
          description: 'Get selected and start your dream career'
        }
      ],
      companyBenefits: [
        'Post unlimited job openings',
        'Access to qualified student database',
        'Advanced filtering and search',
        'Schedule and manage interviews',
        'Track application progress',
        'Generate placement reports'
      ],
      studentBenefits: [
        'Browse jobs from top companies',
        'Personalized job recommendations',
        'Track application status',
        'Receive interview notifications',
        'Build professional profile',
        'Access placement statistics'
      ],
      testimonials: [
        {
          name: 'John Smith',
          role: 'HR Manager at Google',
          text: 'NextGig has revolutionized our campus recruitment process. The platform is intuitive and helped us find exceptional talent.'
        },
        {
          name: 'Sarah Johnson',
          role: 'Software Engineer at Microsoft',
          text: 'I found my dream job through NextGig. The platform made it easy to apply and track my applications throughout the process.'
        },
        {
          name: 'Michael Chen',
          role: 'Placement Coordinator',
          text: 'Managing placements has never been easier. The analytics and reporting features are incredibly helpful for our department.'
        }
      ]
    };
  },

  methods: {
    getInitials(name) {
      return name.split(' ').map(n => n[0]).join('').toUpperCase();
    }
  }
};
</script>

<style scoped>
.landing-page {
  overflow-x: hidden;
}

/* Navigation */
.navbar {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  padding: 1rem 0;
}

.brand-text {
  font-size: 1.8rem;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-link {
  color: #333;
  font-weight: 500;
  margin: 0 0.5rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #667eea;
}

/* Buttons */
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
  color: white;
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

.btn-lg {
  padding: 0.8rem 2rem;
  font-size: 1.1rem;
}

/* Hero Section */
.hero-section {
  position: relative;
  background: linear-gradient(135deg, #f5f7ff 0%, #ffffff 100%);
  overflow: hidden;
  min-height: 100vh;
  padding-top: 80px;
}

.hero-content {
  padding: 2rem 0;
}

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-illustration {
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2rem;
}

.floating-icon {
  font-size: 4rem;
  color: #667eea;
  opacity: 0.8;
  animation: float 3s ease-in-out infinite;
}

.floating-icon:nth-child(1) { animation-delay: 0s; }
.floating-icon:nth-child(2) { animation-delay: 0.5s; }
.floating-icon:nth-child(3) { animation-delay: 1s; }
.floating-icon:nth-child(4) { animation-delay: 1.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
}

.hero-shape {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  line-height: 0;
}

.hero-shape svg {
  width: 100%;
  height: auto;
}

.stat-item {
  text-align: center;
}

/* Companies & Students Illustrations */
.companies-illustration i,
.students-illustration i {
  font-size: 5rem;
  margin: 0 1rem;
  animation: bounce 2s ease-in-out infinite;
}

.companies-illustration i:nth-child(2),
.students-illustration i:nth-child(2) {
  animation-delay: 0.3s;
}

.companies-illustration i:nth-child(3),
.students-illustration i:nth-child(3) {
  animation-delay: 0.6s;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-15px); }
}

/* Features Section */
.feature-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

/* Steps Section */
.step-card {
  padding: 2rem 1rem;
}

.step-number {
  width: 40px;
  height: 40px;
  margin: 0 auto;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 1.2rem;
}

.step-icon {
  color: #667eea;
}

/* Benefits */
.benefit-item {
  font-size: 1.1rem;
}

/* Testimonials */
.testimonial-card {
  background: white;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.testimonial-avatar {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 1.1rem;
}

.testimonial-text {
  font-style: italic;
}

/* CTA Section */
.cta-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 30px;
}

.text-white-50 {
  color: rgba(255, 255, 255, 0.7) !important;
}

.btn-light {
  background: white;
  color: #667eea;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-light:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.3);
  color: #667eea;
}

.btn-outline-light {
  border: 2px solid white;
  color: white;
  padding: 0.8rem 2rem;
  border-radius: 50px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-outline-light:hover {
  background: white;
  color: #667eea;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 255, 255, 0.3);
}

/* Footer */
.footer {
  background: #1a1a2e !important;
}

.footer a:hover {
  color: white !important;
}

.form-control.rounded-pill {
  border: none;
  padding: 0.6rem 1.2rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero-content {
    text-align: center;
    padding-top: 4rem;
  }
  
  .navbar-collapse {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin-top: 1rem;
  }
  
  .display-3 {
    font-size: 2.5rem;
  }
  
  .display-5 {
    font-size: 2rem;
  }
  
  .btn-lg {
    width: 100%;
    margin-bottom: 0.5rem;
  }
  
  .hero-illustration {
    height: 300px;
  }
  
  .floating-icon {
    font-size: 3rem;
  }
  
  .companies-illustration i,
  .students-illustration i {
    font-size: 3rem;
    margin: 0 0.5rem;
  }
}
</style>