try:
    from config.settings.common import *  # noqa: F401 F403
except ImportError as e:
    print(f"Import error {e}")

DEBUG = False
SECRET_KEY = "django-insecure-ci-key"

STATICFILES_DIRS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_BROKER_URL = "memory://"
CELERY_RESULT_BACKEND = "memory://"

REDIS_URL = None

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.dummy.EmailBackend"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
