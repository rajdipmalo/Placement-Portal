from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity
from models import db, User, Student, Company, Job, Application, Placement
from utils.decorators import role_required
from utils.timezone import ist_now
from extensions import cache 
from sqlalchemy import func
from datetime import datetime

company_bp = Blueprint('company', __name__)

@company_bp.route('/dashboard', methods=['GET'])
@role_required('company')
@cache.cached(timeout=120, key_prefix=lambda: f"company_dashboard_{get_jwt_identity()}")
def company_dashboard():
    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    jobs = Job.query.filter_by(company_id=company.id).all()

    return jsonify({
        "company_name": company.name,
        "total_jobs": len(jobs),
        "jobs": [
            {
                "id": j.id,
                "role": j.role,
                "description": j.description,
                "status": j.status,
                "applications_count": len(j.applications),
                "deadline": j.application_deadline.isoformat() if j.application_deadline else None,
                "created_at": j.created_at.isoformat() if j.created_at else None,
                "drive_date": j.drive_date.isoformat() if j.drive_date else None,
                "drive_location": j.drive_location,
                "eligibility_cgpa": j.eligibility_cgpa,
                "eligibility_year": j.eligibility_year,
                "eligibility_branch": j.eligibility_branch,
                "salary": j.salary,
                "job_type": j.job_type,
                "skills_required": j.skills_required
            }
            for j in jobs
        ]
    })

@company_bp.route('/statistics', methods=['GET'])
@role_required('company')
@cache.cached(timeout=300, key_prefix=lambda: f"company_stats_{get_jwt_identity()}")
def get_company_statistics():

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404


    jobs = Job.query.filter_by(company_id=company.id).all()
    
    total_jobs = len(jobs)
    active_jobs = Job.query.filter_by(company_id=company.id, status='approved').count()
    pending_jobs = Job.query.filter_by(company_id=company.id, status='pending').count()
    

    applications = Application.query.join(Job).filter(Job.company_id == company.id).all()
    
    total_applications = len(applications)
    shortlisted = sum(1 for app in applications if app.status == 'shortlisted')
    selected = sum(1 for app in applications if app.status == 'selected')
    rejected = sum(1 for app in applications if app.status == 'rejected')
    

    placements = Placement.query.filter_by(company_id=company.id).count()

    return jsonify({
        "total_jobs": total_jobs,
        "active_jobs": active_jobs,
        "pending_jobs": pending_jobs,
        "total_applications": total_applications,
        "shortlisted": shortlisted,
        "selected": selected,
        "rejected": rejected,
        "placements": placements
    })

@company_bp.route('/jobs', methods=['POST'])
@role_required('company')
def create_job():

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    if company.approval_status != 'approved':
        return jsonify({"msg": "Company not approved"}), 403

    data = request.json


    required = ['role', 'application_deadline']
    for field in required:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400


    if data.get('eligibility_cgpa') is not None:
        try:
            cgpa = float(data['eligibility_cgpa'])
            if cgpa < 0 or cgpa > 10:
                return jsonify({"msg": "CGPA must be between 0 and 10"}), 400
        except ValueError:
            return jsonify({"msg": "eligibility_cgpa must be a number"}), 400

    if data.get('eligibility_year') is not None:
        try:
            year = int(data['eligibility_year'])
            if year < 1 or year > 4:
                return jsonify({"msg": "Year must be between 1 and 4"}), 400
        except ValueError:
            return jsonify({"msg": "eligibility_year must be a number"}), 400


    if data.get('skills_required') is not None and not isinstance(data['skills_required'], list):
        return jsonify({"msg": "skills_required must be an array"}), 400

    if data.get('eligibility_branch') is not None and not isinstance(data['eligibility_branch'], list):
        return jsonify({"msg": "eligibility_branch must be an array"}), 400


    try:
        deadline = datetime.fromisoformat(data['application_deadline'])
        if deadline < datetime.now():
            return jsonify({"msg": "Application deadline cannot be in the past"}), 400
    except Exception:
        return jsonify({"msg": "Invalid application_deadline format. Use YYYY-MM-DDTHH:MM:SS"}), 400


    drive_date = None
    if data.get('drive_date'):
        try:
            drive_date = datetime.fromisoformat(data['drive_date']).date()
        except Exception:
            return jsonify({"msg": "Invalid drive_date format. Use YYYY-MM-DD"}), 400

    job = Job(
        company_id=company.id,
        role=data['role'],
        description=data.get('description'),
        salary=data.get('salary'),
        job_type=data.get('job_type'),
        skills_required=data.get('skills_required', []),
        eligibility_cgpa=data.get('eligibility_cgpa'),
        eligibility_branch=data.get('eligibility_branch', []),
        eligibility_year=data.get('eligibility_year'),
        application_deadline=deadline,
        drive_date=drive_date,
        drive_location=data.get('drive_location'),
        status='pending'
    )

    db.session.add(job)
    db.session.commit()
    
    cache.clear() 

    return jsonify({
        "msg": "Job created, awaiting admin approval",
        "job_id": job.id
    }), 201

@company_bp.route('/applications', methods=['GET'])  
@role_required('company')
def get_all_applications():

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404


    applications = Application.query.join(Job).filter(Job.company_id == company.id).all()

    return jsonify([
    {
        "application_id": app.id,
        "student_id": app.student.id,
        "student_email": app.student.user.email,
        "full_name": app.student.full_name,
        "branch": app.student.branch,
        "year": app.student.year,
        "cgpa": app.student.cgpa,
        "skills": app.student.skills,
        "resume_url": app.resume_url,
        "application_status": app.status,
        "applied_on": app.applied_on.isoformat() if app.applied_on else None,
        "shortlisted_on": app.shortlisted_on.isoformat() if app.shortlisted_on else None,
        "selected_on": app.selected_on.isoformat() if app.selected_on else None,
        "rejected_on": app.rejected_on.isoformat() if app.rejected_on else None,
        "interview_date": app.interview_date.isoformat() if app.interview_date else None,
        "interview_mode": app.interview_mode,
        "interview_location": app.interview_location,
        "meeting_link": app.meeting_link,  # Add meeting link field
        "job_id": app.job.id,
        "job_role": app.job.role,
        "drive_date": app.job.drive_date.isoformat() if app.job.drive_date else None,
        "drive_location": app.job.drive_location,
        "application_deadline": app.job.application_deadline.isoformat() if app.job.application_deadline else None
    }
    for app in applications
])
    
@company_bp.route('/jobs/<int:job_id>', methods=['GET'])
@role_required('company')
def get_job_details(job_id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    job = Job.query.get_or_404(job_id)

    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403


    applications = Application.query.filter_by(job_id=job_id).all()
    
    stats = {
        "total": len(applications),
        "shortlisted": sum(1 for app in applications if app.status == 'shortlisted'),
        "selected": sum(1 for app in applications if app.status == 'selected'),
        "rejected": sum(1 for app in applications if app.status == 'rejected')
    }

    return jsonify({
        "id": job.id,
        "role": job.role,
        "description": job.description,
        "salary": job.salary,
        "job_type": job.job_type,
        "skills_required": job.skills_required,
        "eligibility_cgpa": job.eligibility_cgpa,
        "eligibility_branch": job.eligibility_branch,
        "eligibility_year": job.eligibility_year,
        "application_deadline": job.application_deadline.isoformat() if job.application_deadline else None,
        "drive_date": job.drive_date.isoformat() if job.drive_date else None,
        "drive_location": job.drive_location,
        "status": job.status,
        "applications_count": len(job.applications),
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "updated_at": job.updated_at.isoformat() if job.updated_at else None,
        "stats": stats 
    })
    
    
@company_bp.route('/jobs/<int:job_id>', methods=['DELETE'])
@role_required('company')
def delete_job(job_id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    job = Job.query.get_or_404(job_id)

    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403


    if job.status != 'pending':
        return jsonify({"msg": "Only pending jobs can be deleted"}), 400

 
    applications_count = Application.query.filter_by(job_id=job_id).count()
    if applications_count > 0:
        return jsonify({"msg": "Cannot delete job with existing applications"}), 400

    db.session.delete(job)
    db.session.commit()
    cache.clear()

    return jsonify({
        "msg": "Job deleted successfully",
        "job_id": job.id
    }), 200

@company_bp.route('/applications/<int:id>/status', methods=['PUT'])
@role_required('company')
def update_application_status(id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    app = Application.query.get_or_404(id)

    if app.job.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403

    data = request.json
    new_status = data.get('status')

    if new_status not in ['shortlisted', 'selected', 'rejected']:
        return jsonify({"msg": "Invalid status"}), 400

    app.status = new_status

    if new_status == 'shortlisted':
        app.shortlisted_on = ist_now()

    elif new_status == 'selected':
        app.selected_on = ist_now()

        existing_placement = Placement.query.filter_by(
            student_id=app.student_id,
            job_id=app.job_id
        ).first()

        if not existing_placement:
            placement = Placement(
                student_id=app.student_id,
                company_id=company.id,
                job_id=app.job_id,
                position=app.job.role,
                salary=app.job.salary,
                joining_date=None
            )
            db.session.add(placement)

    elif new_status == 'rejected':
        app.rejected_on = ist_now()
        app.interview_date = None
        app.interview_mode = None

        existing_placement = Placement.query.filter_by(
            student_id=app.student_id,
            job_id=app.job_id
        ).first()

        if existing_placement:
            db.session.delete(existing_placement)

    db.session.commit()
    cache.clear()
    

    return jsonify({"msg": f"Application status updated to {new_status}"})

@company_bp.route('/profile', methods=['GET'])
@role_required('company')
def get_company_profile():

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    return jsonify({
        "id": company.id,
        "name": company.name,
        "email": company.user.email,  
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "hr_email": company.hr_email,
        "hr_contact": company.hr_contact,
        "approval_status": company.approval_status,
        "created_at": company.created_at.isoformat() if company.created_at else None
    })


@company_bp.route('/placements', methods=['POST'])
@role_required('company')
def create_placement():

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    data = request.json

    job = Job.query.get_or_404(data['job_id'])


    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized"}), 403

    placement = Placement(
        student_id=data['student_id'],
        company_id=company.id,
        job_id=job.id,
        position=data.get('position'),
        salary=data.get('salary'),
        joining_date=datetime.fromisoformat(data['joining_date']).date()
            if data.get('joining_date') else None
    )

    db.session.add(placement)
    db.session.commit()

    return jsonify({"msg": "Placement recorded"})

@company_bp.route('/applications/<int:id>/schedule-interview', methods=['POST'])
@role_required('company')
def schedule_interview(id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    app = Application.query.get_or_404(id)

    if app.job.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403

    data = request.json
    interview_date = data.get('interview_date')
    interview_mode = data.get('interview_mode')
    interview_location = data.get('interview_location')
    meeting_link = data.get('meeting_link')  

    if not interview_date:
        return jsonify({"msg": "Interview date is required"}), 400
        
    if not interview_mode:
        return jsonify({"msg": "Interview mode is required"}), 400
        
    if interview_mode not in ['Online', 'In-person']:
        return jsonify({"msg": "Interview mode must be either 'Online' or 'In-person'"}), 400


    if interview_mode == 'In-person' and not interview_location:
        return jsonify({"msg": "Interview location is required for in-person interviews"}), 400


    try:
        interview_datetime = datetime.fromisoformat(interview_date)
    except Exception:
        return jsonify({"msg": "Invalid interview date format. Use YYYY-MM-DDTHH:MM:SS"}), 400


    job = app.job
    drive_date = job.drive_date


    if drive_date:

        drive_datetime = datetime.combine(drive_date, datetime.min.time())
        
        if interview_datetime.date() <= drive_date:
            return jsonify({
                "msg": f"Interview date must be after the drive date ({drive_date.strftime('%Y-%m-%d')})"
            }), 400
    else:
        return jsonify({"msg": "Drive date is not set for this job"}), 400


    app.interview_date = interview_datetime
    app.interview_mode = interview_mode
    

    if interview_mode == 'Online':
        app.meeting_link = meeting_link
        app.interview_location = None 
    elif interview_mode == 'In-person':
        app.interview_location = interview_location
        app.meeting_link = None

    db.session.commit()

    return jsonify({
        "msg": "Interview scheduled successfully",
        "interview_date": app.interview_date.isoformat() if app.interview_date else None,
        "interview_mode": app.interview_mode,
        "interview_location": app.interview_location,
        "meeting_link": app.meeting_link
    }), 200
    


@company_bp.route('/jobs/<int:job_id>/complete', methods=['POST'])
@role_required('company')
def mark_job_complete(job_id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    job = Job.query.get_or_404(job_id)

    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403

    if job.status != 'approved':
        return jsonify({"msg": "Only approved jobs can be marked as complete"}), 400

    job.status = 'closed'
    db.session.commit()

    return jsonify({
        "msg": "Job marked as complete successfully",
        "job_id": job.id,
        "status": job.status
    }), 200
    
@company_bp.route('/jobs/<int:job_id>/reopen', methods=['POST'])
@role_required('company')
def reopen_job(job_id):

    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    job = Job.query.get_or_404(job_id)

    if job.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403

    if job.status != 'closed':
        return jsonify({"msg": "Only closed jobs can be reopened"}), 400

    job.status = 'approved'
    db.session.commit()

    return jsonify({
        "msg": "Job reopened successfully",
        "job_id": job.id,
        "status": job.status
    }), 200
    

@company_bp.route('/placements', methods=['GET'])
@role_required('company')
def get_placements():
    """
    Get all placements for the company
    """
    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    placements = Placement.query.filter_by(company_id=company.id).all()

    return jsonify([
        {
            "id": p.id,
            "student_id": p.student_id,
            "job_id": p.job_id,
            "position": p.position,
            "salary": p.salary,
            "joining_date": p.joining_date.isoformat() if p.joining_date else None,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in placements
    ]), 200
    
    
    
@company_bp.route('/placements/<int:placement_id>', methods=['PUT'])
@role_required('company')
def update_placement_joining_date(placement_id):
    """
    Update the joining date for an existing placement
    """
    user_id = int(get_jwt_identity())
    company = Company.query.filter_by(user_id=user_id).first()

    if not company:
        return jsonify({"msg": "Company not found"}), 404

    placement = Placement.query.get_or_404(placement_id)


    if placement.company_id != company.id:
        return jsonify({"msg": "Unauthorized access"}), 403

    data = request.json
    joining_date = data.get('joining_date')

    if not joining_date:
        return jsonify({"msg": "Joining date is required"}), 400


    try:
        placement.joining_date = datetime.fromisoformat(joining_date).date()
    except Exception:
        return jsonify({"msg": "Invalid joining date format. Use YYYY-MM-DD"}), 400

    db.session.commit()

    return jsonify({
        "msg": "Joining date updated successfully",
        "placement": {
            "id": placement.id,
            "student_id": placement.student_id,
            "job_id": placement.job_id,
            "joining_date": placement.joining_date.isoformat() if placement.joining_date else None
        }
    }), 200