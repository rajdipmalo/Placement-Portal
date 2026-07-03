import os
import ssl
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://", "postgresql://"
        )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"sslmode": "require"}
    }

    # ==================== SECURITY ====================
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "fallback_salt")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_EXPIRES_HOURS", 1))
    )

    # ==================== CELERY ====================
    CELERY_BROKER_URL = os.getenv("REDIS_URL")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")

    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "ssl_cert_reqs": ssl.CERT_NONE  # for Upstash
    }

   
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL")

    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "ssl": {
            "ssl_cert_reqs": ssl.CERT_NONE
        }
    }
    CACHE_DEFAULT_TIMEOUT = 300


    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"

    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

    MAIL_DEFAULT_SENDER = (
        "NextGig Placements",
        os.getenv("MAIL_USERNAME", "noreply@nextgig.com")
    )