"""
WSGI config for emb project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emb.settings')

application = get_wsgi_application()
