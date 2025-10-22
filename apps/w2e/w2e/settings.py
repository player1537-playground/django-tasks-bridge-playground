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
    'bridge',
]

# Minimal database configuration (required by Django)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Django Tasks Configuration
# Bridge receives tasks from web (redis-web port 6379)
# and forwards to emb aimodel (redis-emb port 6380)
if os.environ.get('USE_REDIS'):
    # Production: Use RQ backend with Redis
    TASKS = {
        "default": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        },
        "bridge": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {"url": "redis://localhost:6379/0"},
        },
        "aimodel": {
            "BACKEND": "django_tasks.backends.rq.RQBackend",
            "BACKEND_OPTIONS": {"url": "redis://localhost:6380/0"},
        },
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
        "bridge": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
        "aimodel": {
            "BACKEND": "django_tasks.backends.immediate.ImmediateBackend",
        },
    }

# Suppress Django system check warnings
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
