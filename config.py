import os
from dotenv import load_dotenv
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, '.env')
APP_DIR = os.path.join(BASE_DIR, 'app')

LOGFILE = 'app/logs/error.log'

if os.path.exists(ENV_FILE):
    load_dotenv(ENV_FILE)

SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')

DATABASES = {
    "default": {
        "DATABASE_HOST": os.getenv("DATABASE_HOST","127.0.0.1"),
        "DATABASE_PORT": os.getenv("DATABASE_PORT", "5432"),
        "DATABASE_USER": os.getenv("DATABASE_USER", "postgres"),
        "DATABASE_PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
        "DATABASE_NAME": os.getenv("DATABASE_NAME", "")
    }
}

BCRYPT_LOG_ROUNDS = 4

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4