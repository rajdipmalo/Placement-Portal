import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "../components/LandingPage.vue";
import login from "../components/login.vue";
import registerStudent from "../components/registerStudent.vue";
import registerCompany from "../components/registerCompany.vue";
import EmailVerification from "../components/EmailVerification.vue";  // ✅ NEW


import StudentDashboard from "../components/student/StudentDashboard.vue";
import DashboardHome from "../components/student/DashboardHome.vue";
import CompaniesPage from "../components/student/CompaniesPage.vue";
import CompanyDrivesPage from "../components/student/CompanyDrivesPage.vue";
import ProfilePage from "../components/student/ProfilePage.vue";
import JobDetailsPage from "../components/student/JobDetailsPage.vue";
import StudentPlacements from "../components/student/StudentPlacements.vue";


import CompanyDashboard from "../components/company/CompanyDashboard.vue";
import CompanyHome from "../components/company/CompanyHome.vue";
import CompanyDrives from "../components/company/CompanyDrives.vue";
import CompanyApplications from "../components/company/CompanyApplications.vue";
import CompanyProfile from "../components/company/CompanyProfile.vue";
import CreateDrive from "../components/company/CreateDrive.vue";
import ApplicationDetails from "../components/company/ApplicationDetails.vue";
import DriveDetails from "../components/company/DriveDetails.vue";


import AdminDashboard from "../components/admin/AdminDashboard.vue";
import AdminHome from "../components/admin/AdminHome.vue";
import AdminCompanies from "../components/admin/AdminCompanies.vue";
import AdminStudents from "../components/admin/AdminStudents.vue";
import AdminDrives from "../components/admin/AdminDrives.vue";
import AdminApplications from "../components/admin/AdminApplications.vue";
import AdminReports from "../components/admin/AdminReports.vue";
import AdminStudentDetails from "../components/admin/AdminStudentDetails.vue";
import AdminCompanyDetails from "../components/admin/AdminCompanyDetails.vue";
import AdminDriveDetails from "../components/admin/AdminDriveDetails.vue";
import AdminApplicationDetails from "../components/admin/AdminApplicationDetails.vue";


const routes = [
    { path: "/", name: "LandingPage", component: LandingPage },
    { path: "/login", name: "Login", component: login },
    { path: "/register/student", name: "RegisterStudent", component: registerStudent },
    { path: "/register/company", name: "RegisterCompany", component: registerCompany },
    { path: "/verify-email/:token", name: "verify-email", component: EmailVerification },  // ✅ NEW

    // Student Dashboard Routes
    { 
        path: "/student/dashboard", 
        component: StudentDashboard,
        meta: { requiresAuth: true, role: "student" },
        children: [
            { path: "", name: "StudentDashboardHome", component: DashboardHome },
            { path: "companies", name: "StudentCompanies", component: CompaniesPage },
            { path: "companies/:companyName", name: "StudentCompanyDrives", component: CompanyDrivesPage, props: true },
            { path: "companies/:companyName/job/:jobId", name: "StudentJobDetails", component: JobDetailsPage, props: true },
            { path: "placements", name: "StudentPlacements", component: StudentPlacements },
            { path: "profile", name: "StudentProfile", component: ProfilePage }
        ]
    },

    // Company Dashboard Routes
    { 
        path: "/company/dashboard", 
        component: CompanyDashboard,
        meta: { requiresAuth: true, role: "company" },
        children: [
            { path: "", name: "CompanyHome", component: CompanyHome },
            { path: "drives", name: "CompanyDrives", component: CompanyDrives },
            { path: "applications", name: "CompanyApplications", component: CompanyApplications },
            { path: "applications/:applicationId", name: "ApplicationDetails", component: ApplicationDetails, props: true },
            { path: "profile", name: "CompanyProfile", component: CompanyProfile },
            { path: "create", name: "CreateDrive", component: CreateDrive },
            { path: "drives/:driveId", name: "DriveDetails", component: DriveDetails, props: true }
        ]
    },


    { 
        path: "/admin/dashboard", 
        component: AdminDashboard,
        meta: { requiresAuth: true, role: "admin" },
        children: [
            { path: "", name: "AdminHome", component: AdminHome },
            { path: "companies", name: "AdminCompanies", component: AdminCompanies },
            { path: "students", name: "AdminStudents", component: AdminStudents },
            { path: "drives", name: "AdminDrives", component: AdminDrives },
            { path: "applications", name: "AdminApplications", component: AdminApplications },
            { path: "reports", name: "AdminReports", component: AdminReports },
            { path: "students/:studentId", name: "AdminStudentDetails", component: () => import("../components/admin/AdminStudentDetails.vue"), props: true },
            { path: "companies/:companyId", name: "AdminCompanyDetails", component: () => import("../components/admin/AdminCompanyDetails.vue"), props: true },
            { path: "drives/:driveId", name: "AdminDriveDetails", component: () => import("../components/admin/AdminDriveDetails.vue"), props: true },
            { path: "applications/:applicationId", name: "AdminApplicationDetails", component: () => import("../components/admin/AdminApplicationDetails.vue"), props: true }
        ]
    }



];

export default createRouter({
    history: createWebHistory(),
    routes
});