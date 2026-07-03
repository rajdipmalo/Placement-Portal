"""
Celery Background Tasks for NextGig Placement Portal
Location: celery_app.py (project root)
"""

from dotenv import load_dotenv
load_dotenv()

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from celery import Celery
from datetime import timedelta
import csv
from sqlalchemy import func
from celery.schedules import crontab

from models import db, User, Job, Student, Application, Company
from utils.timezone import ist_now
from email_service import send_placement_notification  

BASE_URL = "http://localhost:5000"

celery = Celery(
    "tasks",
    broker=os.getenv("REDIS_URL"),
    backend=os.getenv("REDIS_URL")
)

celery.conf.update(
    timezone="Asia/Kolkata",
    enable_utc=False,
    broker_transport_options={
        "ssl_cert_reqs": "CERT_NONE"
    }
)

celery.conf.beat_schedule = {
    "daily-reminder-job": {
        "task": "celery_app.daily_reminders",
        "schedule": crontab(hour=16, minute=45),
    },
    "monthly-report-job": {
        "task": "celery_app.monthly_report",
        "schedule": crontab(day_of_month=18, hour=16, minute=45),
    },
}


@celery.task(name="celery_app.daily_reminders")
def daily_reminders():
    """Send daily reminder emails to students about approaching deadlines"""
    from app import app

    with app.app_context():
        try:
            now = ist_now()
            deadline_limit = now + timedelta(days=10)

            jobs = Job.query.filter(Job.application_deadline <= deadline_limit).all()
            students = Student.query.all()

            if not jobs:
                print("ℹ️  No jobs with approaching deadlines")
                return

            if not students:
                print("ℹ️  No students found")
                return

            email_count = 0
            failed_count = 0

            for job in jobs:
                for student in students:
                    user = User.query.get(student.user_id)

                    if not user or not user.email:
                        failed_count += 1
                        continue

                    # ✅ Only send to verified users
                    if not user.is_verified:
                        continue

                    subject = f"Application Deadline Reminder - {job.role} at {job.company.name}"

                    html_body = f"""
                    <html>
                        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                                <h2 style="margin: 0;">NextGig Placements</h2>
                                <p style="margin: 10px 0 0 0;">Application Deadline Reminder</p>
                            </div>
                            <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                                <p>Hi <strong>{student.full_name}</strong>,</p>
                                <p>A placement application deadline is approaching!</p>
                                
                                <div style="background: white; border-left: 4px solid #667eea; padding: 15px; margin: 20px 0; border-radius: 4px;">
                                    <p><strong>Company:</strong> {job.company.name}</p>
                                    <p><strong>Position:</strong> {job.role}</p>
                                    <p><strong>Deadline:</strong> {job.application_deadline.strftime('%Y-%m-%d %H:%M')}</p>
                                    {f'<p><strong>Drive Date:</strong> {job.drive_date.strftime("%Y-%m-%d")}</p>' if job.drive_date else ''}
                                </div>
                                
                                <p>Don't miss this opportunity! Apply now to be considered for this position.</p>
                                
                                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                                
                                <p style="color: #999; font-size: 12px;">
                                    NextGig Placement Cell
                                </p>
                            </div>
                        </body>
                    </html>
                    """

                    # ✅ NEW: Use send_placement_notification
                    if send_placement_notification(subject, [user.email], html_body):
                        email_count += 1
                    else:
                        failed_count += 1

            print(f"✅ Daily reminders completed: {email_count} sent, {failed_count} failed")

        except Exception as e:
            print(f"❌ Error in daily_reminders: {str(e)}")


@celery.task(name="celery_app.monthly_report")
def monthly_report():
    """Send monthly placement report to admin"""
    from app import app

    with app.app_context():
        try:
            admin = User.query.filter_by(role="admin").first()
            
            if not admin:
                print("❌ Admin user not found")
                return

            if not admin.email:
                print("❌ Admin email not configured")
                return

            now = ist_now()
            first_day = now.replace(day=1, hour=0, minute=0, second=0)
            last_month_end = first_day
            last_month_start = (first_day - timedelta(days=1)).replace(day=1)

            drives_count = Job.query.filter(
                Job.drive_date >= last_month_start.date(),
                Job.drive_date <= last_month_end.date()
            ).count()

            applied_count = db.session.query(func.count()).select_from(Application).filter(
                Application.applied_on >= last_month_start,
                Application.applied_on < last_month_end
            ).scalar()

            selected_count = db.session.query(func.count()).select_from(Application).filter(
                Application.status == "selected",
                Application.selected_on >= last_month_start,
                Application.selected_on < last_month_end
            ).scalar()

            month_name = last_month_start.strftime('%B %Y')

            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                        <h2 style="margin: 0;">NextGig Placements</h2>
                        <p style="margin: 10px 0 0 0;">Monthly Placement Report - {month_name}</p>
                    </div>
                    <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                        <h3>Monthly Metrics</h3>
                        
                        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                            <tr style="background: #f0f0f0;">
                                <td style="border: 1px solid #ddd; padding: 10px; font-weight: bold;">Metric</td>
                                <td style="border: 1px solid #ddd; padding: 10px; font-weight: bold;">Count</td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #ddd; padding: 10px;">Drives Conducted</td>
                                <td style="border: 1px solid #ddd; padding: 10px;"><strong>{drives_count}</strong></td>
                            </tr>
                            <tr style="background: #f9f9f9;">
                                <td style="border: 1px solid #ddd; padding: 10px;">Student Applications</td>
                                <td style="border: 1px solid #ddd; padding: 10px;"><strong>{applied_count}</strong></td>
                            </tr>
                            <tr>
                                <td style="border: 1px solid #ddd; padding: 10px;">Students Selected</td>
                                <td style="border: 1px solid #ddd; padding: 10px;"><strong>{selected_count}</strong></td>
                            </tr>
                        </table>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #999; font-size: 12px;">
                            This is an automated report generated on {now.strftime('%Y-%m-%d %H:%M:%S')} IST
                        </p>
                    </div>
                </body>
            </html>
            """

            # ✅ NEW: Use send_placement_notification
            if send_placement_notification(f"Monthly Placement Report - {month_name}", [admin.email], html):
                print("✅ Monthly report sent successfully")
            else:
                print("❌ Failed to send monthly report")

        except Exception as e:
            print(f"❌ Error in monthly_report: {str(e)}")


@celery.task(name="celery_app.export_applications")
def export_applications(student_id):
    """Export student's applications to CSV and email the link"""
    from app import app

    with app.app_context():
        try:
            student = Student.query.get(student_id)

            if not student:
                print("❌ Student not found")
                return

            user = User.query.get(student.user_id)

            if not user:
                print("❌ User not found for student")
                return

            if not user.email:
                print("❌ User email not configured")
                return

            applications = Application.query.filter_by(student_id=student_id).all()

            if not applications:
                print("ℹ️  No applications found for this student")
                return

            os.makedirs("static/exports", exist_ok=True)

            filename = f"applications_{student_id}.csv"
            filepath = f"static/exports/{filename}"

            with open(filepath, "w", newline="") as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow([
                    "Student ID",
                    "Student Name",
                    "Company Name",
                    "Position",
                    "Status",
                    "Applied On",
                    "Shortlisted On",
                    "Selected On",
                    "Rejected On"
                ])

                for app_data in applications:
                    job = Job.query.get(app_data.job_id)
                    company = Company.query.get(job.company_id)

                    writer.writerow([
                        student.id,
                        student.full_name,
                        company.name,
                        job.role,
                        app_data.status,
                        app_data.applied_on.strftime('%Y-%m-%d %H:%M') if app_data.applied_on else '',
                        app_data.shortlisted_on.strftime('%Y-%m-%d %H:%M') if app_data.shortlisted_on else '',
                        app_data.selected_on.strftime('%Y-%m-%d %H:%M') if app_data.selected_on else '',
                        app_data.rejected_on.strftime('%Y-%m-%d %H:%M') if app_data.rejected_on else ''
                    ])

            download_link = f"{BASE_URL}/static/exports/{filename}"

            subject = "Your Placement Application Export"

            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; text-align: center; color: white; border-radius: 10px 10px 0 0;">
                        <h2 style="margin: 0;">NextGig Placements</h2>
                        <p style="margin: 10px 0 0 0;">Application Export Ready</p>
                    </div>
                    <div style="background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px;">
                        <p>Hi <strong>{student.full_name}</strong>,</p>
                        <p>Your placement application export is ready to download.</p>
                        
                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{download_link}" 
                               style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; display: inline-block; font-weight: bold;">
                                Download CSV (All Applications)
                            </a>
                        </div>
                        
                        <p>The CSV file contains:</p>
                        <ul>
                            <li>Student information</li>
                            <li>All companies you applied to</li>
                            <li>Position details</li>
                            <li>Application status</li>
                            <li>Important dates (applied, selected, rejected)</li>
                        </ul>
                        
                        <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                        
                        <p style="color: #999; font-size: 12px;">
                            NextGig Placement Cell
                        </p>
                    </div>
                </body>
            </html>
            """

            # ✅ NEW: Use send_placement_notification
            if send_placement_notification(subject, [user.email], html_body):
                print(f"✅ Export completed and email sent to {user.email}")
            else:
                print(f"❌ Export created but failed to send email")

        except Exception as e:
            print(f"❌ Error in export_applications: {str(e)}")