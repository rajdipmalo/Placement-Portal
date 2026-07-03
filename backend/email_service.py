from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer
from flask import current_app

mail = Mail()


# ==================== VERIFICATION EMAIL ====================
def send_verification_email(user_email, user_name, verification_link):
    try:
        msg = Message(
            subject="Verify Your NextGig Account",
            recipients=[user_email],
            html=f"""
            <h3>Hello {user_name},</h3>
            <p>Click below to verify your account:</p>
            <a href="{verification_link}">Verify Email</a>
            <p>This link expires in 24 hours.</p>
            """
        )

        mail.send(msg)
        print(f"✅ Verification email sent to {user_email}")
        return True

    except Exception as e:
        print(f"❌ Email error: {str(e)}")
        return False


# ==================== GENERIC EMAIL ====================
def send_placement_notification(subject, recipients, html_body):
    try:
        if not recipients or not isinstance(recipients, list):
            return False

        valid_recipients = [r for r in recipients if r and "@" in r]

        if not valid_recipients:
            return False

        msg = Message(
            subject=subject,
            recipients=valid_recipients,
            html=html_body
        )

        mail.send(msg)
        print(f"✅ Email sent to {len(valid_recipients)} users")
        return True

    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False


# ==================== TOKEN ====================
def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def verify_token(token, expiration=86400):
    try:
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )
    except Exception as e:
        print(f"❌ Token error: {str(e)}")
        return None