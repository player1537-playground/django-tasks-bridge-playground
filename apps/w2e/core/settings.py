"""
Minimal Django settings for w2e project - web-to-emb bridge, tasks only.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Required by Django
SECRET_KEY = 'django-insecure-w2e-project-secret-key-change-in-production'

# Minimal installed apps for django-tasks
INSTALLED_APPS = [
    'django.contrib.contenttypes',  # Required by Django
    'django_tasks',
    'django_rq',  # For RQ worker management commands
    'foobar_web',  # Dummy task stubs for cross-project references
    'foobar_w2e',
    'foobar_emb',  # Dummy task stubs for cross-project references
]

# Minimal database configuration (required by Django)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Tasks Configuration
# W2E receives tasks from web (redis-web port 6379)
# and forwards to emb aimodel (redis-emb port 6380)
TASKS = {
    "default": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["default", "w2e"],
    },
    "w2e": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        "QUEUES": ["w2e"],
    },
    "emb": {
        "BACKEND": "django_tasks.backends.rq.RQBackend",
        "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
        "QUEUES": ["emb"],
    },
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
    'emb': {
        'HOST': 'localhost',
        'PORT': 6380,
        'DB': 0,
    },
}

# Suppress Django system check warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
