import os


def _get_database_url():
    url = os.environ.get("DATABASE_URL") or "sqlite:///db.sqlite3"
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    return url


class Config:
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "secret-key")

    # Database
    SQLALCHEMY_DATABASE_URI = _get_database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Forms & Requests
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB

    # Session & Cookies
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    RATELIMIT_STORAGE_URI = "memory://"


class DevConfig(Config):
    DEBUG = True


class ProdConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


config_options = {
    "development": DevConfig,
    "production": ProdConfig,
}