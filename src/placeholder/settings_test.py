# https://gauravvjn.medium.com/11-tips-for-lightning-fast-tests-in-django-effa87383040
from .settings import *  # noqa: F403

APP_ENV = Environment.TEST  # noqa: F405

# Using sqlite3 DB instead of posgres for testing to speed them up.
# Running it in memory to speed it up even further.
# NOTE: This will not work if we start using ArrayField, will have to remove this setting.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

# Speed up user' password hashing.
PASSWORD_HASHERS = ("django.contrib.auth.hashers.MD5PasswordHasher",)

# Removing all the unnecessary middleware.
MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
)
