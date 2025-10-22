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
    'aimodel',
]

# Minimal database configuration (required by Django)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Tasks Configuration
# aimodel uses redis-emb (port 6380) for task processing
if os.environ.get('USE_REDIS'):
    # Production: Use RQ backend with Redis
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
            "QUEUES": ["default", "aimodel"],
        },
        "aimodel": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
            "QUEUES": ["aimodel"],
        },
    }

    # RQ_QUEUES configuration for django-rq
    RQ_QUEUES = {
        'default': {
            'HOST': 'localhost',
            'PORT': 6380,
            'DB': 0,
        },
        'aimodel': {
            'HOST': 'localhost',
            'PORT': 6380,
            'DB': 0,
        },
    }
else:
    # Testing: Use immediate backend (synchronous execution)
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
        "aimodel": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
    }

# Suppress Django system check warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True

