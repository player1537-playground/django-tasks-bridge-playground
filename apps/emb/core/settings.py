"""
Minimal Django settings for emb project - AI model tasks only.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Required by Django
SECRET_KEY = 'django-insecure-emb-project-secret-key-change-in-production'

# Minimal installed apps for django-tasks
INSTALLED_APPS = [
    'django.contrib.contenttypes',  # Required by Django
    'django_tasks',
    'django_rq',  # For RQ worker management commands
    'foobar_emb',
    'foobar_w2e',  # Dummy task stubs for cross-project callback references
]

# Minimal database configuration (required by Django)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Tasks Configuration
# emb uses redis-emb (port 6380) for task processing
# w2e backend configured to send callbacks to redis-web (port 6379)
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
        "QUEUES": ["default", "emb"],
    },
    "emb": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
        "QUEUES": ["emb"],
    },
    "w2e": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["w2e"],
    },
}

# RQ_QUEUES configuration for django-rq
RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6380,
        'DB': 0,
    },
    'emb': {
        'HOST': 'localhost',
        'PORT': 6380,
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
