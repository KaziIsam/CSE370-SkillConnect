"""
skillconnect/settings.py
========================
Django settings for BRAC SkillConnect project.

HOW TO USE:
  - This file is the brain of your Django project.
  - It tells Django: where the database is, which apps exist,
    where templates live, etc.
"""

from pathlib import Path

# ─────────────────────────────────────────────────
# BASE DIRECTORY
# Path(__file__) = this file (settings.py)
# .resolve().parent.parent = go up 2 folders → project root
# ─────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent


# ─────────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────────
# IMPORTANT: Change this to a random string in production!
SECRET_KEY = 'django-insecure-brac-skillconnect-cse370-change-in-production'

# Set to False before deploying live
DEBUG = True

# Allow requests from anywhere during development
ALLOWED_HOSTS = ['*']


# ─────────────────────────────────────────────────
# INSTALLED APPS
# Django needs to know which apps exist in your project.
# 'students' is YOUR app — the one you created.
# ─────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',          # Admin panel at /admin/
    'django.contrib.auth',           # Built-in user authentication
    'django.contrib.contenttypes',   # Required by Django
    'django.contrib.sessions',       # Session management (login state)
    'django.contrib.messages',       # Flash messages (success/error popups)
    'django.contrib.staticfiles',    # Serve CSS/JS files
    'students',                      # YOUR APP ← Member 1's module
]


# ─────────────────────────────────────────────────
# MIDDLEWARE
# These run on EVERY request/response.
# Think of them as filters the request passes through.
# ─────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ─────────────────────────────────────────────────
# URL CONFIGURATION
# Tells Django where the main URL file is.
# ─────────────────────────────────────────────────
ROOT_URLCONF = 'skillconnect.urls'


# ─────────────────────────────────────────────────
# TEMPLATES
# Tells Django where to find your HTML files.
# ─────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # Global templates folder
        'APP_DIRS': True,                   # Also look inside each app's templates/
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'skillconnect.wsgi.application'


# ─────────────────────────────────────────────────
# DATABASE — MySQL Connection
#
# HOW TO SET UP:
# 1. Open MySQL Workbench
# 2. Make sure brac_skillconnect database exists:
#    CREATE DATABASE IF NOT EXISTS brac_skillconnect;
# 3. Fill in your MySQL password below.
#
# WHY MySQL instead of SQLite?
#   SQLite is the default but only works as a local file.
#   MySQL is a real database server — what professionals use.
#   Your tables are already created in MySQL from Step 3.
# ─────────────────────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     'skill_connect',    # ← lowercase, matches your actual DB
        'USER':     'root',
        'PASSWORD': '',                 # ← empty, no password
        'HOST':     '127.0.0.1',        # ← use IP instead of localhost
        'PORT':     '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}


# ─────────────────────────────────────────────────
# PASSWORD VALIDATORS (Django built-in)
# ─────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─────────────────────────────────────────────────
# INTERNATIONALISATION
# ─────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'Asia/Dhaka'   # Bangladesh time
USE_I18N      = True
USE_TZ        = True


# ─────────────────────────────────────────────────
# STATIC FILES (CSS, JS, Images)
# When you run the server, Django serves these automatically.
# ─────────────────────────────────────────────────
STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / 'static']


# ─────────────────────────────────────────────────
# DEFAULT PRIMARY KEY FIELD TYPE
# ─────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─────────────────────────────────────────────────
# MESSAGE TAGS (for flash messages in templates)
# ─────────────────────────────────────────────────
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG:   'debug',
    messages.INFO:    'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR:   'danger',
}