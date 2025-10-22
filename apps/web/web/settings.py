"""
Django settings for web project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-web-project-secret-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django_tasks',
    'django_tasks.backends.database',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'web.urls'

TEMPLATES = []

WSGI_APPLICATION = 'web.wsgi.application'

# Database
# For production, use PostgreSQL as shown in docker-compose.yml
# For testing without Docker, use SQLite
import os
if os.environ.get('USE_POSTGRES'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'webdb',
            'USER': 'webuser',
            'PASSWORD': 'webpass',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Django Tasks Configuration
# For production with Docker, use RQ backend with Redis
# For testing, use database backend
if os.environ.get('USE_REDIS'):
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {
                "url": "redis://localhost:6379/0",
            },
        }
    }
else:
    # For testing, use immediate backend which executes tasks synchronously
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        }
    }

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
