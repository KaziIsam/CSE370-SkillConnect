"""
skillconnect/wsgi.py
====================
WSGI = Web Server Gateway Interface.
This file is the entry point when deploying to a real server.
During development, you don't touch this file.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillconnect.settings')
application = get_wsgi_application()