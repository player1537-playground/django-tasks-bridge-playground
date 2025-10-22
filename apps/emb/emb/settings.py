"""
Django settings for emb project.
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-emb-project-secret-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django_tasks',
    'django_tasks.backends.database',
    'bridge',
    'aimodel',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'emb.urls'

TEMPLATES = []

WSGI_APPLICATION = 'emb.wsgi.application'

# Database - emb doesn't need a database, using dummy backend
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Tasks Configuration
# bridge uses redis-web (port 6379) to receive tasks from web project
# aimodel uses redis-emb (port 6380) for internal task processing
# For production with Docker and Redis, set USE_REDIS=1
# For testing, uses database backend
import os
if os.environ.get('USE_REDIS'):
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {
                "url": "redis://localhost:6380/0",
            },
        },
        "bridge": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {
                "url": "redis://localhost:6379/0",
            },
        },
        "aimodel": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {
                "url": "redis://localhost:6380/0",
            },
        },
    }
else:
    # For testing, use immediate backend which executes tasks synchronously
    # This allows testing without running workers
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
        "bridge": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
        "aimodel": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
    }

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
