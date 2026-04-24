import os
from datetime import timedelta

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-v6$@j@0-cvje+wg-)g*!0dm!tfdghf^&%3dfg%+f&5nn^fi0')

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', default='localhost 127.0.0.1 [::1]').split(' ')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    # 'rest_framework.authtoken',
    'channels',

    'apps.core.apps.CoreConfig',
    'apps.car.apps.CarConfig',
    'apps.order.apps.OrderConfig',
    'apps.work.apps.WorkConfig',
    'apps.workstatus.apps.WorkstatusConfig',
    'apps.chatmessage.apps.ChatMessageConfig',
    'apps.api.apps.ApiConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
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

WSGI_APPLICATION = 'config.wsgi.application'

ASGI_APPLICATION = 'config.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                (os.environ.get('REDIS_HOST', 'redis'),
                 int(os.getenv('REDIS_PORT', 6379)))
            ],  # Адрес и порт Redis
        },
    },
}

# В ENV/env.dev прописать все конфиги для подключения к бд
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('SQL_ENGINE',
                                 default='django.db.backends.sqlite3'),
        'NAME': os.environ.get('SQL_NAME', default=BASE_DIR / 'db.sqlite3'),
        'USER': os.environ.get('SQL_USER'),
        'PASSWORD': os.environ.get('SQL_PASSWORD'),
        'HOST': os.environ.get('SQL_HOST'),
        'PORT': os.environ.get('SQL_PORT'),
        'TIME_ZONE': os.environ.get('SQL_TIMEZONE', default='Europe/Moscow')
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = os.environ.get('LANGUAGE_CODE', default='en-us')

TIME_ZONE = os.environ.get('TIMEZONE', default='UTC')

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = 'static'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps/static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'apps/media')

ROOT_URLCONF = 'config.urls.common'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis-caches:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

CACHE_TTL = os.environ.get('CACHE_TTL', 3600)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT аутентификация
        'rest_framework.authentication.SessionAuthentication',         # Сессионная аутентификация для браузера
        # 'apps.api.authentication.CookieJWTAuthentication'
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',  # Разрешения по умолчанию
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',  # Фильтрация
        'rest_framework.filters.SearchFilter',                # Поиск
        'rest_framework.filters.OrderingFilter',              # Сортировка
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',  # Пагинация
    'PAGE_SIZE': 10,  # Размер страницы
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # React dev server
]

CORS_ALLOW_CREDENTIALS = True

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_EXPIRE', 30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('REFRESH_TOKEN_EXPIRE', 7))),
    # 'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

AUTH_USER_MODEL = 'core.User'

PROJECT_NAME = os.environ.get('PROJECT_NAME', 'Django')
