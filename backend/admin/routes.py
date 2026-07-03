from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import db, User, Student, Company, Job, Application, Placement
from utils.decorators import role_required
from sqlalchemy import func, or_
from datetime import datetime
from utils.timezone import ist_now
from extensions import cache 

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=120)
def admin_dashboard():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    total_placements = Placement.query.count()
    
    pending_companies = Company.query.filter_by(approval_status='pending').count()
    pending_jobs = Job.query.filter_by(status='pending').count()
    
    recent_applications = Application.query.order_by(Application.applied_on.desc()).limit(5).all()
    
    recent_apps_data = []
    for app in recent_applications:
        recent_apps_data.append({
            "id": app.id,
            "student_name": app.student.full_name,
            "company": app.job.company.name,
            "position": app.job.role,
            "applied_on": app.applied_on.isoformat() if app.applied_on else None,
            "status": app.status
        })

    return jsonify({
        "stats": {
            "total_students": total_students,
            "total_companies": total_companies,
            "active_drives": Job.query.filter_by(status='approved').count(),
            "total_placements": total_placements
        },
        "pending": {
            "companies": pending_companies,
            "drives": pending_jobs
        },
        "recent_applications": recent_apps_data
    })
    
@admin_bp.route('/companies', methods=['GET'])
@role_required('admin')
def get_companies():
    status = request.args.get('status')
    search = request.args.get('search', '')
    blacklisted = request.args.get('blacklisted')  
    
    query = Company.query.join(User).filter(User.role == 'company')
    

    if status:
        query = query.filter(Company.approval_status == status)
    

    if blacklisted == 'true':
        query = query.filter(User.is_blacklisted == True)
    elif blacklisted == 'false':
        query = query.filter(User.is_blacklisted == False)
    

    if search:
        query = query.filter(
            or_(
                Company.name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    companies = query.all()

    return jsonify([
        {
            "id": c.id,
            "name": c.name,
            "email": c.user.email,
            "industry": c.industry,
            "location": c.location,
            "website": c.website,
            "hr_email": c.hr_email,
            "hr_contact": c.hr_contact,
            "status": c.approval_status,
            "is_blacklisted": c.user.is_blacklisted,  
            "created_at": c.created_at.isoformat() if c.created_at else None
        }
        for c in companies
    ])

@admin_bp.route('/companies/<int:id>', methods=['GET'])
@role_required('admin')
def get_company_details(id):
    company = Company.query.get_or_404(id)
    

    jobs = Job.query.filter_by(company_id=id).all()
    

    total_applications = Application.query.join(Job).filter(Job.company_id == id).count()
    
    return jsonify({
        "id": company.id,
        "name": company.name,
        "email": company.user.email,
        "industry": company.industry,
        "location": company.location,
        "website": company.website,
        "hr_email": company.hr_email,
        "hr_contact": company.hr_contact,
        "status": company.approval_status,
        "is_blacklisted": company.user.is_blacklisted,
        "created_at": company.created_at.isoformat() if company.created_at else None,
        "jobs_count": len(jobs),
        "applications_count": total_applications,
        "jobs": [
            {
                "id": j.id,
                "role": j.role,
                "status": j.status,
                "deadline": j.application_deadline.isoformat() if j.application_deadline else None,
                "applications_count": len(j.applications)
            }
            for j in jobs
        ]
    })

@admin_bp.route('/companies/<int:id>/approve', methods=['PUT'])
@role_required('admin')
def approve_company(id):
    company = Company.query.get_or_404(id)
    company.approval_status = 'approved'
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Company approved successfully"})

@admin_bp.route('/companies/<int:id>/reject', methods=['PUT'])
@role_required('admin')
def reject_company(id):
    company = Company.query.get_or_404(id)
    company.approval_status = 'rejected'
    db.session.commit()
    return jsonify({"msg": "Company rejected"})

@admin_bp.route('/companies/<int:id>/blacklist', methods=['PUT'])
@role_required('admin')
def blacklist_company(id):
    company = Company.query.get_or_404(id)
    
    company_name = company.name
    jobs_count = len(company.jobs)
    placements_count = len(company.placements)
    applications_count = Application.query.join(Job).filter(Job.company_id == company.id).count()
    
    try:
        Placement.query.filter_by(company_id=company.id).delete()
        

        Job.query.filter_by(company_id=company.id).delete()
        

        company.user.is_blacklisted = True
        
        db.session.commit()
        
        return jsonify({
            "msg": f"Company '{company_name}' blacklisted. All associated data deleted.",
            "deleted": {
                "jobs": jobs_count,
                "placements": placements_count,
                "applications": applications_count
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to blacklist company: {str(e)}"}), 500

@admin_bp.route('/companies/<int:id>/unblacklist', methods=['PUT'])
@role_required('admin')
def unblacklist_company(id):
    company = Company.query.get_or_404(id)
    company.user.is_blacklisted = False
    
    db.session.commit()
    
    return jsonify({
        "msg": f"Company '{company.name}' removed from blacklist. They can now create new drives.",
        "company": company.name
    }), 200


@admin_bp.route('/students', methods=['GET'])
@role_required('admin')
def get_students():
    branch = request.args.get('branch')
    year = request.args.get('year')
    search = request.args.get('search', '')
    blacklisted = request.args.get('blacklisted') 
    
    query = Student.query.join(User).filter(User.role == 'student')
    

    if branch:
        query = query.filter(Student.branch == branch)
    
    if year:
        query = query.filter(Student.year == int(year))
    

    if blacklisted == 'true':
        query = query.filter(User.is_blacklisted == True)
    elif blacklisted == 'false':
        query = query.filter(User.is_blacklisted == False)
    

    if search:
        query = query.filter(
            or_(
                Student.full_name.ilike(f'%{search}%'),
                User.email.ilike(f'%{search}%')
            )
        )
    
    students = query.all()

    return jsonify([
        {
            "id": s.id,
            "full_name": s.full_name,
            "email": s.user.email,
            "branch": s.branch,
            "year": s.year,
            "cgpa": s.cgpa,
            "skills": s.skills,
            "is_blacklisted": s.user.is_blacklisted,
            "applications_count": len(s.applications),
            "created_at": s.created_at.isoformat() if s.created_at else None
        }
        for s in students
    ])

@admin_bp.route('/students/<int:id>', methods=['GET'])
@role_required('admin')
def get_student_details(id):
    student = Student.query.get_or_404(id)
    

    applications = Application.query.filter_by(student_id=id).all()
    

    placements = Placement.query.filter_by(student_id=id).all()
    
    return jsonify({
        "id": student.id,
        "full_name": student.full_name,
        "email": student.user.email,
        "branch": student.branch,
        "year": student.year,
        "cgpa": student.cgpa,
        "skills": student.skills,
        "resume_url": student.resume_url,
        "is_blacklisted": student.user.is_blacklisted, 
        "created_at": student.created_at.isoformat() if student.created_at else None,
        "applications": [
            {
                "id": app.id,
                "job_id": app.job_id,
                "job_role": app.job.role,
                "company": app.job.company.name,
                "status": app.status,
                "applied_on": app.applied_on.isoformat() if app.applied_on else None
            }
            for app in applications
        ],
        "placements": [
            {
                "company": p.company.name,
                "position": p.position,
                "salary": p.salary,
                "joining_date": p.joining_date.isoformat() if p.joining_date else None
            }
            for p in placements
        ]
    })

@admin_bp.route('/students/<int:id>/blacklist', methods=['PUT'])
@role_required('admin')
def blacklist_student(id):
    student = Student.query.get_or_404(id)
    

    student_name = student.full_name
    applications_count = len(student.applications)
    placements_count = len(student.placements)
    
    try:
        Application.query.filter_by(student_id=student.id).delete()
        Placement.query.filter_by(student_id=student.id).delete()
        student.user.is_blacklisted = True
        
        db.session.commit()
        
        return jsonify({
            "msg": f"Student '{student_name}' blacklisted. All associated data deleted.",
            "deleted": {
                "applications": applications_count,
                "placements": placements_count
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to blacklist student: {str(e)}"}), 500

@admin_bp.route('/students/<int:id>/unblacklist', methods=['PUT'])
@role_required('admin')
def unblacklist_student(id):
    student = Student.query.get_or_404(id)
    student.user.is_blacklisted = False
    
    db.session.commit()
    
    return jsonify({
        "msg": f"Student '{student.full_name}' removed from blacklist. They can now apply for drives.",
        "student": student.full_name
    }), 200




@admin_bp.route('/drives', methods=['GET'])
@role_required('admin')
def get_drives():
    status = request.args.get('status')
    company_id = request.args.get('company_id')
    search = request.args.get('search', '')
    
    query = Job.query
    

    if status:
        query = query.filter(Job.status == status)
    
    if company_id:
        query = query.filter(Job.company_id == int(company_id))
    

    if search:
        query = query.join(Company).filter(
            or_(
                Job.role.ilike(f'%{search}%'),
                Company.name.ilike(f'%{search}%')
            )
        )
    
    drives = query.all()

    return jsonify([
        {
            "id": j.id,
            "role": j.role,
            "company": j.company.name,
            "company_id": j.company_id,
            "job_type": j.job_type,
            "status": j.status,
            "deadline": j.application_deadline.isoformat() if j.application_deadline else None,
            "drive_date": j.drive_date.isoformat() if j.drive_date else None,
            "applications_count": len(j.applications),
            "created_at": j.created_at.isoformat() if j.created_at else None
        }
        for j in drives
    ])

@admin_bp.route('/drives/<int:id>', methods=['GET'])
@role_required('admin')
def get_drive_details(id):
    job = Job.query.get_or_404(id)
    

    applications = Application.query.filter_by(job_id=id).all()
    

    stats = {
        "total": len(applications),
        "shortlisted": sum(1 for a in applications if a.status == 'shortlisted'),
        "selected": sum(1 for a in applications if a.status == 'selected'),
        "rejected": sum(1 for a in applications if a.status == 'rejected')
    }
    
    return jsonify({
        "id": job.id,
        "role": job.role,
        "description": job.description,
        "company": job.company.name,
        "company_id": job.company_id,
        "salary": job.salary,
        "job_type": job.job_type,
        "skills_required": job.skills_required,
        "eligibility_cgpa": job.eligibility_cgpa,
        "eligibility_branch": job.eligibility_branch,
        "eligibility_year": job.eligibility_year,
        "deadline": job.application_deadline.isoformat() if job.application_deadline else None,
        "drive_date": job.drive_date.isoformat() if job.drive_date else None,
        "drive_location": job.drive_location,
        "status": job.status,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "stats": stats,
        "applications": [
            {
                "id": a.id,
                "student_name": a.student.full_name,
                "student_email": a.student.user.email,
                "status": a.status,
                "applied_on": a.applied_on.isoformat() if a.applied_on else None
            }
            for a in applications
        ]
    })

@admin_bp.route('/drives/<int:id>/approve', methods=['PUT'])
@role_required('admin')
def approve_drive(id):
    job = Job.query.get_or_404(id)
    job.status = 'approved'
    db.session.commit()
    cache.clear()
    return jsonify({"msg": "Drive approved successfully"})

@admin_bp.route('/drives/<int:id>/reject', methods=['PUT'])
@role_required('admin')
def reject_drive(id):
    job = Job.query.get_or_404(id)
    job.status = 'rejected'
    db.session.commit()
    return jsonify({"msg": "Drive rejected"})

@admin_bp.route('/applications', methods=['GET'])
@role_required('admin')
def get_all_applications():
    status = request.args.get('status')
    company_id = request.args.get('company_id')
    job_id = request.args.get('job_id')
    limit = request.args.get('limit', type=int)
    
    query = Application.query
    

    if status:
        query = query.filter(Application.status == status)
    
    if company_id:
        query = query.join(Job).filter(Job.company_id == int(company_id))
    
    if job_id:
        query = query.filter(Application.job_id == int(job_id))
    

    query = query.order_by(Application.applied_on.desc())
    

    if limit:
        query = query.limit(limit)
    
    applications = query.all()

    return jsonify([
        {
            "id": a.id,
            "student_id": a.student_id,
            "student_name": a.student.full_name,
            "student_email": a.student.user.email,
            "company": a.job.company.name,
            "company_id": a.job.company_id,
            "job_id": a.job_id,
            "job_role": a.job.role,
            "status": a.status,
            "applied_on": a.applied_on.isoformat() if a.applied_on else None,
            "resume_url": a.resume_url
        }
        for a in applications
    ])

@admin_bp.route('/applications/<int:id>', methods=['GET'])
@role_required('admin')
def get_application_details(id):
    application = Application.query.get_or_404(id)
    
    return jsonify({
        "id": application.id,
        "student": {
            "id": application.student.id,
            "name": application.student.full_name,
            "email": application.student.user.email,
            "branch": application.student.branch,
            "year": application.student.year,
            "cgpa": application.student.cgpa,
            "skills": application.student.skills,
            "resume_url": application.student.resume_url
        },
        "job": {
            "id": application.job.id,
            "role": application.job.role,
            "description": application.job.description,
            "company": application.job.company.name,
            "salary": application.job.salary,
            "job_type": application.job.job_type,
            "drive_date": application.job.drive_date.isoformat() if application.job.drive_date else None,
            "drive_location": application.job.drive_location
        },
        "status": application.status,
        "applied_on": application.applied_on.isoformat() if application.applied_on else None,
        "shortlisted_on": application.shortlisted_on.isoformat() if application.shortlisted_on else None,
        "selected_on": application.selected_on.isoformat() if application.selected_on else None,
        "rejected_on": application.rejected_on.isoformat() if application.rejected_on else None,
        "interview_date": application.interview_date.isoformat() if application.interview_date else None,
        "interview_mode": application.interview_mode,
        "interview_location": application.interview_location,
        "meeting_link": application.meeting_link,
        "resume_url": application.resume_url
    })

@admin_bp.route('/placements', methods=['GET'])
@role_required('admin')
def get_placements():
    placements = Placement.query.order_by(Placement.created_at.desc()).all()
    
    return jsonify([
        {
            "id": p.id,
            "student_name": p.student.full_name,
            "company": p.company.name,
            "position": p.position,
            "salary": p.salary,
            "joining_date": p.joining_date.isoformat() if p.joining_date else None,
            "created_at": p.created_at.isoformat() if p.created_at else None
        }
        for p in placements
    ])

@admin_bp.route('/reports/statistics', methods=['GET'])
@role_required('admin')
@cache.cached(timeout=600)
def get_reports_statistics():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    
    total_students = Student.query.count()
    placed_students = db.session.query(Placement.student_id).distinct().count()
    placement_percentage = (placed_students / total_students * 100) if total_students > 0 else 0
    

    active_companies = db.session.query(Company.id).join(Job).filter(
        Job.status == 'approved'
    ).distinct().count()
    

    blacklisted_users = User.query.filter_by(is_blacklisted=True).count()
    

    top_companies = db.session.query(
        Company.id,
        Company.name,
        func.count(Placement.id).label('placements')
    ).join(Placement).group_by(Company.id).order_by(func.count(Placement.id).desc()).limit(5).all()
    
    top_companies_data = []
    for company in top_companies:
        total_apps = db.session.query(Application.id).join(Job).filter(
            Job.company_id == company.id
        ).count()
        success_rate = (company.placements / total_apps * 100) if total_apps > 0 else 0
        top_companies_data.append({
            'id': company.id,
            'name': company.name,
            'placements': company.placements,
            'successRate': round(success_rate, 1)
        })
    

    monthly_apps = []
    monthly_placements = []
    for month in range(1, 13):
        month_str = f"{datetime.now().year}-{month:02d}"
        

        apps_count = db.session.query(func.count(Application.id)).filter(
            func.strftime('%Y-%m', Application.applied_on) == month_str
        ).scalar() or 0
        monthly_apps.append(apps_count)
        

        placements_count = db.session.query(func.count(Placement.id)).filter(
            func.strftime('%Y-%m', Placement.created_at) == month_str
        ).scalar() or 0
        monthly_placements.append(placements_count)
    

    branch_placements = db.session.query(
        Student.branch,
        func.count(Placement.id)
    ).join(Placement).group_by(Student.branch).all()
    
    branch_labels = [b[0] for b in branch_placements] if branch_placements else []
    branch_counts = [b[1] for b in branch_placements] if branch_placements else []
    

    status_counts = []
    for status in ['applied', 'shortlisted', 'selected', 'rejected']:
        count = Application.query.filter_by(status=status).count()
        status_counts.append(count)
    

    avg_cgpa = db.session.query(func.avg(Student.cgpa)).join(Application).filter(
        Application.status == 'selected'
    ).scalar() or 0
    

    avg_salary_result = db.session.query(
        func.avg(db.cast(Placement.salary, db.Integer))
    ).scalar()
    avg_salary = avg_salary_result or 0
    
    multiple_offers = db.session.query(
        Application.student_id
    ).filter(Application.status == 'selected').group_by(
        Application.student_id
    ).having(func.count(Application.id) > 1).count()
    
    companies_visited = db.session.query(Job.company_id).filter(
        Job.status == 'approved'
    ).distinct().count()
    
    total_applications = Application.query.count()
    
    detailed_stats = [
        {'label': 'Average CGPA of Placed Students', 'value': f'{avg_cgpa:.1f}', 'trend': 'up', 'change': '+0.3'},
        {'label': 'Average Salary Package', 'value': f'₹{avg_salary:.1f} LPA', 'trend': 'up', 'change': '+5.2%'},
        {'label': 'Students with Multiple Offers', 'value': str(multiple_offers), 'trend': 'up', 'change': '+12'},
        {'label': 'Companies Visited', 'value': str(companies_visited), 'trend': 'down', 'change': '-3'},
        {'label': 'Total Applications', 'value': str(total_applications), 'trend': 'up', 'change': '+15.3%'},
        {'label': 'Blacklisted Users', 'value': str(blacklisted_users), 'trend': 'neutral', 'change': '0'}
    ]
    
    return jsonify({
        'total_students': total_students,
        'placed_students': placed_students,
        'placement_percentage': placement_percentage,
        'active_companies': active_companies,
        'blacklisted_users': blacklisted_users,
        'top_companies': top_companies_data,
        'monthly_applications': monthly_apps,
        'monthly_placements': monthly_placements,
        'branch_placements': {
            'labels': branch_labels,
            'counts': branch_counts
        },
        'status_distribution': status_counts,
        'detailed_stats': detailed_stats
    })
    