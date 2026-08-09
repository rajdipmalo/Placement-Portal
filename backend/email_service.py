import os
import resend

from itsdangerous import URLSafeTimedSerializer
from flask import current_app


# ==================== RESEND CONFIG ====================

resend.api_key = os.getenv("RESEND_API_KEY")


# ==================== VERIFICATION EMAIL ====================

def send_verification_email(user_email, user_name, verification_link):
    try:
        if not resend.api_key:
            print("❌ RESEND_API_KEY is not configured")
            return False

        from_email = os.getenv(
            "RESEND_FROM_EMAIL",
            "onboarding@resend.dev"
        )

        params = {
            "from": from_email,
            "to": [user_email],
            "subject": "Verify Your NextGig Account",
            "html": f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Verify Your NextGig Account</title>
                </head>

                <body style="
                    margin: 0;
                    padding: 0;
                    background-color: #f4f6f8;
                    font-family: Arial, sans-serif;
                ">

                    <div style="
                        max-width: 600px;
                        margin: 40px auto;
                        background: white;
                        padding: 40px;
                        border-radius: 12px;
                        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
                    ">

                        <h2 style="
                            color: #667eea;
                            margin-bottom: 20px;
                        ">
                            Welcome to NextGig!
                        </h2>

                        <p style="font-size: 16px; color: #333;">
                            Hello <strong>{user_name}</strong>,
                        </p>

                        <p style="
                            font-size: 15px;
                            color: #555;
                            line-height: 1.6;
                        ">
                            Thank you for registering with NextGig.
                            Please verify your email address to activate
                            your account.
                        </p>

                        <div style="text-align: center; margin: 30px 0;">
                            <a href="{verification_link}"
                               style="
                                   display: inline-block;
                                   padding: 14px 28px;
                                   background: #667eea;
                                   color: white;
                                   text-decoration: none;
                                   border-radius: 8px;
                                   font-size: 16px;
                                   font-weight: bold;
                               ">
                                Verify Email
                            </a>
                        </div>

                        <p style="
                            font-size: 14px;
                            color: #777;
                            line-height: 1.5;
                        ">
                            This verification link will expire in
                            <strong>24 hours</strong>.
                        </p>

                        <hr style="
                            border: none;
                            border-top: 1px solid #eee;
                            margin: 30px 0;
                        ">

                        <p style="
                            font-size: 13px;
                            color: #999;
                        ">
                            If you did not create a NextGig account,
                            you can safely ignore this email.
                        </p>

                        <p style="
                            font-size: 14px;
                            color: #555;
                        ">
                            Regards,<br>
                            <strong>NextGig Team</strong>
                        </p>

                    </div>

                </body>
                </html>
            """
        }

        response = resend.Emails.send(params)

        print(f"✅ Verification email sent to {user_email}")
        print(f"✅ Resend response: {response}")

        return True

    except Exception as e:
        print(f"❌ Resend verification email error: {str(e)}")
        return False


# ==================== GENERIC EMAIL ====================

def send_placement_notification(subject, recipients, html_body):
    try:
        if not resend.api_key:
            print("❌ RESEND_API_KEY is not configured")
            return False

        if not recipients or not isinstance(recipients, list):
            print("❌ Recipients must be a non-empty list")
            return False

        valid_recipients = [
            email
            for email in recipients
            if email and isinstance(email, str) and "@" in email
        ]

        if not valid_recipients:
            print("❌ No valid recipients found")
            return False

        from_email = os.getenv(
            "RESEND_FROM_EMAIL",
            "onboarding@resend.dev"
        )

        params = {
            "from": from_email,
            "to": valid_recipients,
            "subject": subject,
            "html": html_body
        }

        response = resend.Emails.send(params)

        print(
            f"✅ Email sent to "
            f"{len(valid_recipients)} users"
        )

        print(f"✅ Resend response: {response}")

        return True

    except Exception as e:
        print(f"❌ Resend email error: {str(e)}")
        return False


# ==================== TOKEN ====================

def generate_verification_token(email):
    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt=current_app.config["SECURITY_PASSWORD_SALT"]
    )


# ==================== VERIFY TOKEN ====================

def verify_token(token, expiration=86400):
    try:
        serializer = URLSafeTimedSerializer(
            current_app.config["SECRET_KEY"]
        )

        return serializer.loads(
            token,
            salt=current_app.config["SECURITY_PASSWORD_SALT"],
            max_age=expiration
        )

    except Exception as e:
        print(f"❌ Token error: {str(e)}")
        return None