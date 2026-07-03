from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.timezone import ist_now
from sqlalchemy.dialects.postgresql import JSONB

db = SQLAlchemy()


class User(db.Model):
    __tablename__='users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)


    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(500), unique=True, nullable=True)
    verification_sent_at = db.Column(db.DateTime, nullable=True)
    verified_at = db.Column(db.DateTime, nullable=True)
    
    created_at = db.Column(db.DateTime, default=ist_now)
    updated_at = db.Column(db.DateTime, onupdate=ist_now)
    
    company = db.relationship('Company', backref='user', uselist=False, cascade="all, delete")
    student = db.relationship('Student', backref='user', uselist=False, cascade="all, delete")


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    industry = db.Column(db.String(200))
    location = db.Column(db.String(200))
    website = db.Column(db.String(200))
    hr_email = db.Column(db.String(200))
    hr_contact = db.Column(db.String(20))
    
    approval_status = db.Column(db.String(30), default='pending') 
    created_at = db.Column(db.DateTime, default=ist_now)
    updated_at = db.Column(db.DateTime, onupdate=ist_now)
    
    jobs = db.relationship('Job', backref='company', lazy=True, cascade="all, delete")
    placements = db.relationship('Placement', backref='company', lazy=True, cascade="all, delete")  


class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    full_name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), index=True)
    year = db.Column(db.Integer, index=True)
    cgpa = db.Column(db.Float, index=True)

    skills = db.Column(JSONB)

    resume_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=ist_now)
    updated_at = db.Column(db.DateTime, onupdate=ist_now)

    applications = db.relationship('Application', backref='student', lazy=True, cascade="all, delete")
    placements = db.relationship('Placement', backref='student', lazy=True, cascade="all, delete") 


class Job(db.Model):
    __tablename__='jobs'

    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    role = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    salary = db.Column(db.String(100))
    job_type = db.Column(db.String(50))


    skills_required = db.Column(JSONB)
    eligibility_branch = db.Column(JSONB)

    eligibility_cgpa = db.Column(db.Float)
    eligibility_year = db.Column(db.Integer)
    application_deadline = db.Column(db.DateTime, nullable=False)
    drive_date = db.Column(db.Date)
    drive_location = db.Column(db.String(150))
    status = db.Column(db.String(30), default='pending')

    created_at = db.Column(db.DateTime, default=ist_now)
    updated_at = db.Column(db.DateTime, onupdate=ist_now)

    applications = db.relationship('Application', backref='job', lazy=True, cascade="all, delete")


class Application(db.Model):
    __tablename__='applications'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False, index=True)
    status = db.Column(db.String(30), default='applied')
    
    resume_url = db.Column(db.String(500))  
    
    interview_date = db.Column(db.DateTime)
    interview_mode = db.Column(db.String(50))
    interview_location = db.Column(db.String(200))
    meeting_link = db.Column(db.String(200))
    
    applied_on = db.Column(db.DateTime, default=ist_now)
    shortlisted_on = db.Column(db.DateTime)
    selected_on = db.Column(db.DateTime)
    rejected_on = db.Column(db.DateTime)
    
    updated_at = db.Column(db.DateTime, onupdate=ist_now)
    
    __table_args__ = (
        db.UniqueConstraint('student_id', 'job_id', name='unique_application'),
    )


class Placement(db.Model):
    __tablename__ = 'placements'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False, index=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False, index=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    
    position = db.Column(db.String(100))
    salary = db.Column(db.String(100))
    joining_date = db.Column(db.Date)
    
    created_at = db.Column(db.DateTime, default=ist_now)