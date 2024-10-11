import os

from dotenv import load_dotenv

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Determine the environment and load appropriate .env file
environment = os.environ.get("DJANGO_RUNNING_IN_DOCKER", "False")
env_file = ".env.server" if environment == "True" else ".env.local"

# Load the environment file
load_dotenv(env_file)

# Debug
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")

# AWS RDS
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# CELERY settings
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"
CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/0"

# Email
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")

# Secret_key
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
