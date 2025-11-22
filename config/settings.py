# config/settings.py
from pathlib import Path
import os
import os
DEBUG = os.getenv("DEBUG", "True") == "True"


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: change this to an env var in real production
SECRET_KEY = "django-insecure-bt7!f#g=!-!e&$75li=n^ma1o-87s)n%-puya379fa5y5vpqke"

# For now: read from env, default True for local dev
DEBUG = os.getenv("DEBUG", "True") == "True"

# Railway gives dynamic hostnames, easiest for now:
ALLOWED_HOSTS = ["*"]

# -------------------------------------------------------------------
# Apps
# -------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "channels",   # you already had this
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# -------------------------------------------------------------------
# Database – Railway Postgres
# -------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "railway",
        "USER": "postgres",
        "PASSWORD": "HaLABdtYjFiuaGdHBDMmYWWfDeOPhsXA",
        "HOST": "shuttle.proxy.rlwy.net",
        "PORT": "22790",
    }
}

# -------------------------------------------------------------------
# Password validation
# -------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# -------------------------------------------------------------------
# Internationalization
# -------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------------------
# Static & Media
# -------------------------------------------------------------------
STATIC_URL = "/static/"

# where your project-level static folder is (CSS, JS, etc.)
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# where collectstatic will dump files for production
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -------------------------------------------------------------------
# Auth redirects
# -------------------------------------------------------------------
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "feed"
LOGOUT_REDIRECT_URL = "login"

# -------------------------------------------------------------------
# Default primary key field type
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# -------------------------------------------------------------------
# Channels – simple in-memory layer (OK on a single Railway container)
# -------------------------------------------------------------------
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    }
}
