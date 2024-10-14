"""
Django settings for placeholder project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import enum
import os
from pathlib import Path

from dotenv import load_dotenv

from core.middleware.logging import correlation_id

from .logging import get_logging_config

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class Environment(enum.StrEnum):
    LOCAL = "local"
    TEST = "test"
    DEV = "dev"
    STG = "stg"
    PROD = "production"


APP_ENV = Environment(os.getenv("ENVIRONMENT", "production"))
DEBUG = os.getenv("DEBUG", "False") == "True"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = []

# Application definition
# Logging.
CORRELATION_ID_HEADER = "X-Request-ID"
LOGGING = get_logging_config(log_level=LOG_LEVEL, correlation_id_var=correlation_id)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party apps.
    "rest_framework",
    "rest_framework.authtoken",
    # Our apps.
    "core.apps.CoreConfig",
    "authentication.apps.AuthenticationConfig",
    "api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.logging.CorrelationIDMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "placeholder.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "placeholder.wsgi.application"


################ DATABASE SETUP.
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASE_CONN_MAX_AGE = 0
if APP_ENV in (Environment.STG, Environment.PROD):
    DATABASE_CONN_MAX_AGE = 600

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", "placeholder"),
        "USER": os.getenv("DATABASE_USER", "placeholder"),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
        "HOST": os.getenv("DATABASE_HOST", ""),
        "PORT": os.getenv("DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": DATABASE_CONN_MAX_AGE,
        "OPTIONS": {
            "application_name": "placeholder-default",
            "connect_timeout": 10,
        },
        "TEST": {
            "NAME": "placeholdertest",
        },
    }
}


################ AUTH SETTINGS.
AUTH_USER_MODEL = "authentication.User"
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
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

################ API settings.
DRF_RENDERER_CLASSES = ("rest_framework.renderers.JSONRenderer",)
if APP_ENV not in (Environment.PROD,):  # Disable browsable API in prod.
    DRF_RENDERER_CLASSES = DRF_RENDERER_CLASSES + ("rest_framework.renderers.BrowsableAPIRenderer",)

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": DRF_RENDERER_CLASSES,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.utils.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.utils.pagination.PageNumberPagination",
    "EXCEPTION_HANDLER": "api.utils.exceptions.placeholder_exception_handler",
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
