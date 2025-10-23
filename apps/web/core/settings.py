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
    'foobar_web',
    'foobar_w2e',  # Dummy task stubs for cross-project references
]

# Database configuration - SQLite (for demo purposes)
# In production, this would be PostgreSQL with sensitive data
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Tasks Configuration - RQ backend with Redis
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["default", "w2e"],
    }
}

# RQ_QUEUES configuration for django-rq
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
    'w2e': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
    },
}

# Suppress Django system check warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
