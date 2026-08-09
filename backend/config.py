import os
import ssl
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:

    # ==================== DATABASE ====================

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            "postgres://",
            "postgresql://"
        )

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
        "pool_size": 5,
        "max_overflow": 10,
        "connect_args": {
            "sslmode": "require"
        }
    }

    # ==================== SECURITY ====================

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "fallback_secret"
    )

    SECURITY_PASSWORD_SALT = os.getenv(
        "SECURITY_PASSWORD_SALT",
        "fallback_salt"
    )

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv("JWT_EXPIRES_HOURS", "1"))
    )

    # ==================== CELERY ====================

    CELERY_BROKER_URL = os.getenv("REDIS_URL")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")

    CELERY_BROKER_TRANSPORT_OPTIONS = {
        "ssl": {
            "ssl_cert_reqs": ssl.CERT_NONE
        }
    }

    # ==================== CACHE ====================

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = 300