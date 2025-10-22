"""
Minimal Django settings for web project - tasks and management commands only.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Required by Django
SECRET_KEY = 'django-insecure-web-project-secret-key-change-in-production'

# Minimal installed apps for django-tasks + auth for sensitive data access
INSTALLED_APPS = [
    'django.contrib.contenttypes',  # Required by Django
    'django.contrib.auth',          # For sensitive data access
    'django_tasks',
    'core',
]

# Database configuration
# Production: PostgreSQL with sensitive data
# Testing: SQLite
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
if os.environ.get('USE_REDIS'):
    # Production: Use RQ backend with Redis
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        }
    }
else:
    # Testing: Use immediate backend (synchronous execution)
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        }
    }

# Suppress Django system check warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True

