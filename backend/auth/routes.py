"""
Authentication Routes - with Email Verification
Location: auth/routes.py
"""
import os
from flask import Blueprint, request, jsonify, url_for, redirect
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Student, Company
from utils.timezone import ist_now
from email_service import (
    send_verification_email,
    generate_verification_token,
    verify_token
)

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register/student', methods=['POST'])
def register_student():
    data = request.json

    required = ['email', 'password', 'full_name', 'branch', 'year', 'cgpa']
    for field in required:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400

    try:
        verification_token = generate_verification_token(data['email'])

        user = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='student',
            is_active=True,
            is_verified=False,
            verification_token=verification_token,
            verification_sent_at=ist_now()
        )

        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            full_name=data['full_name'],
            branch=data['branch'],
            year=data['year'],
            cgpa=data['cgpa'],
            skills=data.get('skills', []),
            resume_url=data.get('resume_url')
        )

        db.session.add(student)
        db.session.commit()


        verification_link = f"{os.getenv('FRONTEND_URL')}/verify-email/{verification_token}"

        send_verification_email(
            user_email=data['email'],
            user_name=data['full_name'],
            verification_link=verification_link
        )

        return jsonify({
            "msg": "Registration successful! Check email for verification."
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400



@auth_bp.route('/register/company', methods=['POST'])
def register_company():
    data = request.json

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400

    try:
        verification_token = generate_verification_token(data['email'])

        user = User(
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='company',
            is_active=True,
            is_verified=False,
            verification_token=verification_token,
            verification_sent_at=ist_now()
        )

        db.session.add(user)
        db.session.flush()

        company = Company(
            user_id=user.id,
            name=data['name'],
            industry=data.get('industry'),
            location=data.get('location'),
            website=data.get('website'),
            hr_email=data.get('hr_email'),
            hr_contact=data.get('hr_contact'),
            approval_status='pending'
        )

        db.session.add(company)
        db.session.commit()


        verification_link = f"{os.getenv('FRONTEND_URL')}/verify-email/{verification_token}"

        send_verification_email(
            user_email=data['email'],
            user_name=data['name'],
            verification_link=verification_link
        )

        return jsonify({
            "msg": "Company registered! Verify email first."
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400


# ================== VERIFY EMAIL ==================
@auth_bp.route('/verify-email/<token>', methods=['GET'])
def verify_email(token):
    email = verify_token(token)

    if not email:
        return jsonify({"msg": "Invalid or expired token"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.is_verified:
        return jsonify({"msg": "Already verified"}), 200

    try:
        user.is_verified = True
        user.verified_at = ist_now()
        user.verification_token = None
        db.session.commit()

        return jsonify({
            "msg": "Email verified successfully",
            "role": user.role
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Verification failed"}), 500


@auth_bp.route('/resend-verification', methods=['POST'])
def resend_verification():
    """Resend verification email"""
    data = request.json
    email = data.get('email')

    if not email:
        return jsonify({"msg": "Email is required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if user.is_verified:
        return jsonify({"msg": "Email is already verified"}), 400

    try:
        verification_token = generate_verification_token(email)
        
        if not verification_token:
            return jsonify({"msg": "Could not generate verification token"}), 500

        user.verification_token = verification_token
        user.verification_sent_at = ist_now()
        db.session.commit()

        verification_link = url_for(
            'auth.verify_email',
            token=verification_token,
            _external=True
        )
        
        if user.role == 'student' and user.student:
            user_name = user.student.full_name
        elif user.role == 'company' and user.company:
            user_name = user.company.name
        else:
            user_name = user.email
        
        send_verification_email(
            user_email=email,
            user_name=user_name,
            verification_link=verification_link
        )

        return jsonify({
            "msg": "Verification email sent. Please check your inbox."
        }), 200

    except Exception as e:
        print(f"❌ Resend verification error: {str(e)}")
        return jsonify({"msg": f"Error sending email: {str(e)}"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login with email verification check"""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()

    # Check credentials
    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    # ✅ NEW: Check if email is verified
    if not user.is_verified:
        return jsonify({
            "msg": "Please verify your email before logging in",
            "requires_verification": True,
            "email": email
        }), 403

    # Check if active
    if not user.is_active:
        return jsonify({"msg": "Account deactivated"}), 403

    # Check if blacklisted
    if user.is_blacklisted:
        return jsonify({"msg": "Account blacklisted"}), 403

    # Check company approval
    if user.role == 'company':
        if not user.company or user.company.approval_status != 'approved':
            return jsonify({"msg": "Company not approved by admin"}), 403

    # Generate JWT token
    token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": token,
        "role": user.role
    }), 200