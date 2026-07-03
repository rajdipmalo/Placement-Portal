from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from models import db, User, Student, Company, Job, Application, Placement
from utils.decorators import role_required
from sqlalchemy import func
from utils.timezone import ist_now
from extensions import cache 
from celery_app import export_applications



student_bp = Blueprint('student', __name__)



@student_bp.route('/companies', methods=['GET'])
@role_required('student')
@cache.cached(timeout=300)
def get_companies():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()


    if student.user.is_blacklisted:
        return jsonify({"msg": "You are blacklisted"}), 403


    companies = Company.query.join(User).filter(
        Company.approval_status == 'approved',
        User.is_blacklisted == False
    ).all()

    companies_data = []
    for company in companies:

        active_jobs_count = Job.query.filter(
            Job.company_id == company.id,
            Job.status == 'approved',
            Job.application_deadline >= ist_now()
        ).count()

        companies_data.append({
            "id": company.id,
            "name": company.name,
            "industry": company.industry,
            "location": company.location,
            "website": company.website,
            "hr_email": company.hr_email,
            "hr_contact": company.hr_contact,
            "active_jobs_count": active_jobs_count
        })

    return jsonify(companies_data)


@student_bp.route('/companies/<int:company_id>', methods=['GET'])
@role_required('student')
@cache.cached(timeout=300)
def get_company_details(company_id):

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()


    if student.user.is_blacklisted:
        return jsonify({"msg": "You are blacklisted"}), 403

    company = Company.query.join(User).filter(
        Company.id == company_id,
        Company.approval_status == 'approved',
        User.is_blacklisted == False
    ).first_or_404()

    return jsonify({
        "id": company.id,
        "name": company.name,
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "hr_email": company.hr_email,
        "hr_contact": company.hr_contact
    })

@student_bp.route('/jobs', methods=['GET'])
@role_required('student')
@cache.cached(timeout=120)
def get_jobs():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()


    if student.user.is_blacklisted:
        return jsonify({"msg": "You are blacklisted"}), 403


    jobs = Job.query.join(Company).join(User).filter(
        Job.status == 'approved',
        User.is_blacklisted == False
    ).all()

    return jsonify([
        {
            "id": job.id,
            "role": job.role,
            "description": job.description,
            "company_id": job.company.id,
            "company": job.company.name,
            "company_details": {
                "industry": job.company.industry,
                "location": job.company.location,
                "website": job.company.website
            },
            "salary": job.salary,
            "job_type": job.job_type,
            "skills_required": job.skills_required,
            "cgpa_required": job.eligibility_cgpa,
            "branch_required": job.eligibility_branch,
            "year_required": job.eligibility_year,
            "deadline": job.application_deadline.isoformat(),
            "drive_date": job.drive_date.isoformat() if job.drive_date else None,
            "drive_location": job.drive_location,
            "status": job.status
        }
        for job in jobs
    ])

@student_bp.route('/apply/<int:job_id>', methods=['POST'])
@role_required('student')
def apply_job(job_id):

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404


    if student.user.is_blacklisted:
        return jsonify({"msg": "You are blacklisted"}), 403

    job = Job.query.get_or_404(job_id)

    if job.status != 'approved':
        return jsonify({"msg": "Job not approved"}), 400

    if job.application_deadline < ist_now():
        return jsonify({"msg": "Deadline passed"}), 400


    if job.company.user.is_blacklisted:
        return jsonify({"msg": "Company is blacklisted"}), 403

    if job.eligibility_cgpa and student.cgpa < job.eligibility_cgpa:
        return jsonify({"msg": "CGPA not eligible"}), 400

    if job.eligibility_branch and student.branch not in job.eligibility_branch:
        return jsonify({"msg": "Branch not eligible"}), 400

    if job.eligibility_year and student.year != job.eligibility_year:
        return jsonify({"msg": "Year not eligible"}), 400

    existing = Application.query.filter_by(
        student_id=student.id,
        job_id=job_id
    ).first()

    if existing:
        return jsonify({"msg": "Already applied"}), 400


    application = Application(
        student_id=student.id,
        job_id=job_id,
        resume_url=student.resume_url
    )

    db.session.add(application)
    db.session.commit()

    return jsonify({
        "msg": "Applied successfully",
        "application_id": application.id,
        "resume_url": application.resume_url
    }), 201

@student_bp.route('/applied-jobs', methods=['GET']) 
@role_required('student')
def applied_jobs():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    apps = Application.query.filter_by(student_id=student.id).all()

    return jsonify([
        {
            "application_id": app.id,
            "job_id": app.job.id,
            "job": app.job.role,
            "company": app.job.company.name,
            "company_id": app.job.company.id,
            "status": app.status,
            "applied_on": app.applied_on.isoformat() if app.applied_on else None,
            "shortlisted_on": app.shortlisted_on.isoformat() if app.shortlisted_on else None,
            "selected_on": app.selected_on.isoformat() if app.selected_on else None,
            "rejected_on": app.rejected_on.isoformat() if app.rejected_on else None,
            "interview_date": app.interview_date.isoformat() if app.interview_date else None,
            "interview_mode": app.interview_mode,
            "interview_location": app.interview_location,
            "meeting_link": app.meeting_link,
            "resume_url": app.resume_url
        }
        for app in apps
    ])
    
@student_bp.route('/placements', methods=['GET'])
@role_required('student')
def placement_history():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()
    
    if not student:
        return jsonify({"msg": "Student not found"}), 404

    placements = Placement.query.filter_by(student_id=student.id).all()

    result = []
    for p in placements:
        application = Application.query.filter_by(
            student_id=student.id,
            job_id=p.job_id
        ).first()
        
        result.append({
            "company": p.company.name,
            "company_id": p.company.id,
            "job_id": p.job_id,
            "position": p.position,
            "salary": p.salary,
            "joining_date": p.joining_date.isoformat() if p.joining_date else None,
            "selected_on": application.selected_on.isoformat() if application and application.selected_on else None
        })

    return jsonify(result)

@student_bp.route('/profile', methods=['GET'])
@role_required('student')
def get_profile():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    return jsonify({
        "id": student.id,
        "full_name": student.full_name,
        "email": student.user.email,
        "branch": student.branch,
        "year": student.year,
        "cgpa": student.cgpa,
        "skills": ", ".join(student.skills or []),
        "resume_url": student.resume_url,
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "updated_at": student.updated_at.isoformat() if student.updated_at else None
    })

@student_bp.route('/profile', methods=['PUT'])
@role_required('student')
def update_profile():

    user_id = int(get_jwt_identity())
    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return jsonify({"msg": "Student not found"}), 404

    data = request.json

    student.full_name = data.get("full_name", student.full_name)
    student.branch = data.get("branch", student.branch)
    student.year = data.get("year", student.year)
    student.cgpa = data.get("cgpa", student.cgpa)
    student.resume_url = data.get("resume_url", student.resume_url)

    if data.get("skills"):
        student.skills = [
            skill.strip()
            for skill in data["skills"].split(",")
            if skill.strip()
        ]

    db.session.commit()
    cache.clear()

    return jsonify({"msg": "Profile updated successfully"})


@student_bp.route("/export-applications", methods=["POST"])
@role_required("student")
def export_applications_route():

    user_id = int(get_jwt_identity())

    student = Student.query.filter_by(user_id=user_id).first()

    if not student:
        return {"message": "Student not found"}, 404

    export_applications.delay(student.id)

    return {
        "message": "Your export job has started. You will receive an email once the CSV is ready."
    }, 200
    