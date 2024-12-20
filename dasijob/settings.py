"""
Django settings for dasijob project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

import environ
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

load_dotenv()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--sw4l!@9*9v56ucygrjw3qqg)sol#6^79**d9*4kpyilzf!t+p"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'dasijob.onrender.com', 'www.dasijob.net','dasijob.net', 'localhost']

CSRF_TRUSTED_ORIGINS = [
    'https://dasijob.onrender.com',
    'https://dasijob.net'
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'widget_tweaks',
    'social_django',
    'rest_framework',
    'channels',
    'django_celery_beat',
    'jobs'
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ]
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

# 권한 관련 설정
AUTH_USER_MODEL = 'auth.User'

# 로그인 관련 설정
LOGIN_URL = 'jobs:login'
LOGIN_REDIRECT_URL = 'jobs:main'
LOGOUT_REDIRECT_URL = 'jobs:main'

ASGI_APPLICATION = 'dasijob.asgi.application'

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'social_django.middleware.SocialAuthExceptionMiddleware',
    'jobs.middleware.ErrorHandlingMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.kakao.KakaoOAuth2',
    'social_core.backends.naver.NaverOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'jobs.backends.CustomAuthBackend',
)

PROTECTED_URLS = [
    'resume_list',
    'resume_create',
    'job_create',
    'application_list',
]

SUBSCRIPTION_REQUIRED_URLS = [
    'analytics_dashboard',
    'resume_builder',
]

COMPANY_ONLY_URLS = [
    'job_create',
    'company_dashboard',
]

# 소셜 로그인 설정
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '6Lehv5EqAAAAAOlp_1_mU4yGxtXHkAxOpuPEBwkh'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '6Lehv5EqAAAAAKP2OARaBMcoiVpX5Wt9o2JZl4_9'

SOCIAL_AUTH_KAKAO_KEY = 'a51a6c85763af38c3b5d2846a921d107'
SOCIAL_AUTH_KAKAO_SECRET = 'your-kakao-secret'

SOCIAL_AUTH_NAVER_KEY = 'cX34CmsM6Bkln8Sh72ug'
SOCIAL_AUTH_NAVER_SECRET = 'DlzjYcDNMw'

ROOT_URLCONF = "dasijob.urls"

# reCAPTCHA 키 (Google reCAPTCHA에서 발급받은 키로 교체 필요)
# RECAPTCHA_PUBLIC_KEY = '6Lehv5EqAAAAAOlp_1_mU4yGxtXHkAxOpuPEBwkh'
# RECAPTCHA_PRIVATE_KEY = '6Lehv5EqAAAAAKP2OARaBMcoiVpX5Wt9o2JZl4_9'

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'jobs' / 'templates'],
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

WSGI_APPLICATION = "dasijob.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LOGIN_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 이메일 설정

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = env('EMAIL_HOST_USER', default='webmaster@localhost')
EMAIL_HOST = env('EMAIL_HOST', default='smtp.naver.com')
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

# Celery 설정
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# Celery Beat 설정
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# API 키 추가
VWORLD_API_KEY = '08FDC254-4A8B-373F-96A4-4864C4468622'

ADMINISTRATIVE_DISTRICT_API_KEY = 'fJtseiwOOFBp9sLzORQxa1RAJl2oI8WCiqwFFZq530S1X0VaIdsHDtUrEc1mjjlf6Y9E%2BMJmCM8%2BO434xejaNw%3D%3D'

NAVER_MAPS_CLIENT_ID = 'ytvynitkhf'
NAVER_MAPS_CLIENT_SECRET = 'j11LhtfOhWEAEy8EhJpLzDhpFmg1jcWXfO3dIXHc'
