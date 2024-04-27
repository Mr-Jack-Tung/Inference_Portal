"""
Django settings for inferenceportal project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from decouple import config
from pathlib import Path
from datetime import datetime
import os
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['localhost', '127.0.0.1','34.198.186.123', "professorparakeet.com", "www.professorparakeet.com"]
CSRF_TRUSTED_ORIGINS=["http://localhost:8000", "https://34.198.186.123:443", "https://34.198.186.123", "https://professorparakeet.com", "https://www.professorparakeet.com"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'server',
    'django_bleach',
    'captcha',
    "rest_framework_api_key",
    'vectordb',
    'ninja',
    'tinymce',
    'mptt', #tree graph in sql
]
CORS_ORIGIN_ALLOW_ALL = True
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6380)],
            "capacity": 1500,  # default 100
            "expiry": 10,  # default 60
        },
    },
}

DJANGO_VECTOR_DB = {
    "DEFAULT_EMBEDDING_CLASS": "vectordb.embedding_functions.SentenceTransformerEncoder",
    "DEFAULT_EMBEDDING_MODEL": "all-MiniLM-L6-v2",
    "DEFAULT_EMBEDDING_SPACE": "l2", # Can be "cosine" or "l2"
    "DEFAULT_EMBEDDING_DIMENSION": 384, # Default is 384 for "all-MiniLM-L6-v2"
    "DEFAULT_MAX_N_RESULTS": 10, # Number of results to return from search maximum is default is 10
    "DEFAULT_MIN_SCORE": 0.0, # Minimum score to return from search default is 0.0
    "DEFAULT_MAX_BRUTEFORCE_N": 10_000, # Maximum number of items to search using brute force default is 10_000. If the number of items is greater than this number, the search will be done using the HNSW index.
}

CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.math_challenge'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inferenceportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["inferenceportal/server/templates", "frontend/templates",],
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

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://127.0.0.1:6380",
    }
    
}

ASGI_APPLICATION = "inferenceportal.asgi.application"

STATICFILES_DIRS = [BASE_DIR / "static"]

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Stripe
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
BACKEND_DOMAIN = config("BACKEND_DOMAIN")
PAYMENT_SUCCESS_URL = config("PAYMENT_SUCCESS_URL")
PAYMENT_CANCEL_URL = config("PAYMENT_CANCEL_URL")
STRIPE_WEBHOOK_SECRET = config("STRIPE_WEBHOOK_SECRET")

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = config("EMAIL_ADDRESS")
EMAIL_HOST_PASSWORD = config("MAIL")

STATIC_ROOT = 'staticfiles'

CELERY_BROKER_URL = 'redis://127.0.0.1:6380'

REST_FRAMEWORK = {

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'server.api_throttling_rates.KeyCreateRateThrottle',
        'server.api_throttling_rates.CreditCheckRateThrottle',
        'server.api_throttling_rates.XMRConfirmationRateThrottle'
    ],

    'DEFAULT_THROTTLE_RATES': {
        'anon': '20/s',
        'user': '20/s',
        'create_key': '100/day',
        'check_key': '100/hour',
        'confirm_monero': '100/hour'
    }

}
DATA_UPLOAD_MAX_MEMORY_SIZE = None

TINYMCE_DEFAULT_CONFIG = {
    "height": "320px",
    "width": "960px",
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table code help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save print | insertfile image media pageembed template link anchor codesample | tableofcontents | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,

}
