from os import getenv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = getenv('STORE_IO_SECRET_KEY')
ALLOWED_HOSTS = getenv('STORE_IO_ALLOWED_HOSTS', 'localhost').split(',')
DEBUG = bool(getenv('STORE_IO_DEBUG'))



INSTALLED_APPS = [
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.contrib.migrations',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'store_io.urls'

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

WSGI_APPLICATION = 'store_io.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': getenv('STORE_IO_DB_NAME'),
        'USER': getenv('STORE_IO_DB_USERNAME'),
        'PASSWORD': getenv('STORE_IO_DB_PASSWORD'),
        'HOST': getenv('STORE_IO_DB_HOST'),
        'PORT': getenv('STORE_IO_DB_PORT'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': getenv('STORE_IO_CACHE_LOCATION'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    'token-cache': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': getenv('STORE_IO_TOKEN_CACHE_LOCATION'),
        'TIMEOUT': 86400,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'storeioauth',
    },
    'idempotent': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': getenv('STORE_IO_IDEMPOTENT_CACHE_URL'),
    },
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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{BASE_DIR}/app.log',
            'formatter': 'simple',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        }
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'core.handlers.exception_handler',
    'DEFAULT_RENDERER_CLASSES': ['core.renderers.DefaultJsonRenderer'],
    'DEFAULT_PAGINATION_CLASS': 'core.paginations.DefaultPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': ['accounts.backends.Authentication'],
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
