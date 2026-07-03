import smtplib
from email.mime.text import MIMEText
from config import Config


def send_email(subject, recipients, message):
    """
    Send email with comprehensive validation and error handling.
    
    Args:
        subject (str): Email subject
        recipients (list): List of recipient email addresses
        message (str): Email body (can be HTML)
    
    Returns:
        bool: True if email sent successfully, False otherwise
    """
    
    try:
        # ✅ Validate SMTP configuration FIRST
        if not Config.SMTP_USER:
            print("❌ SMTP_USER not configured in .env")
            return False
        
        if not Config.SMTP_PASSWORD:
            print("❌ SMTP_PASSWORD not configured in .env")
            return False
        
        if not Config.SMTP_HOST:
            print("❌ SMTP_HOST not configured in .env")
            return False
        
        # ✅ Validate inputs
        if not subject or not isinstance(subject, str):
            print("❌ Invalid subject")
            return False
        
        if not message or not isinstance(message, str):
            print("❌ Invalid message")
            return False
        
        if not recipients or not isinstance(recipients, list):
            print("❌ Recipients must be a non-empty list")
            return False
        
        # ✅ Validate each recipient
        valid_recipients = []
        for recipient in recipients:
            if recipient and isinstance(recipient, str) and "@" in recipient:
                valid_recipients.append(recipient)
            else:
                print(f"⚠️  Invalid recipient email: {recipient}")
        
        if not valid_recipients:
            print("❌ No valid recipients found")
            return False
        
        # ✅ Create and send email
        msg = MIMEText(message, "html")
        msg["Subject"] = subject
        msg["From"] = Config.SMTP_USER
        msg["To"] = ", ".join(valid_recipients)
        
        # Connect and send
        if Config.SMTP_PORT == 465:
            server = smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT)
        else:
            server = smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT)
            server.starttls()
        
        server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
        server.sendmail(Config.SMTP_USER, valid_recipients, msg.as_string())
        server.quit()
        
        print(f"✅ Email sent successfully to {len(valid_recipients)} recipient(s)")
        return True

    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication failed - check SMTP_USER and SMTP_PASSWORD in .env")
        return False
    
    except smtplib.SMTPException as e:
        print(f"❌ SMTP error: {str(e)}")
        return False
    
    except Exception as e:
        print(f"❌ Failed to send email: {str(e)}")
        return False