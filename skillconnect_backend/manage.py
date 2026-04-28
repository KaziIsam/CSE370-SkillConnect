#!/usr/bin/env python
"""
COMMON COMMANDS:
  python manage.py runserver       ← start the web server
  python manage.py check           ← test database connection
  python manage.py shell           ← open Django Python shell
  python manage.py createsuperuser ← create admin login
"""
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillconnect.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and your "
            "virtual environment is activated."
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()