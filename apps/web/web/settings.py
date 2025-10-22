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
    'django_rq',  # For RQ worker management commands
    'core',
]

# Database configuration - PostgreSQL with sensitive data
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

# Django Tasks Configuration - RQ backend with Redis
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["default", "bridge"],
    }
}

# RQ_QUEUES configuration for django-rq
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'bridge': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
}

# Suppress Django system check warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True

