"""
Django settings for udemy project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gkl4pfn$lv^($x7acwd@6+e6_@@(jl3i-&=in&@-v1%zu*e(pu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
AUTH_USER_MODEL = "user.User"

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app.apps.AppConfig',
    'user.apps.UserConfig',
    'crispy_forms',
    'mathfilters',
    'rest_framework',
    'rest_framework.authtoken',
    'django_rest_passwordreset',
    'django_elasticsearch_dsl',

]
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': ['http://localhost:9231']
    }
}

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend',
#     'allauth.account.auth_backends.AuthenticationBackend'
# ]

# SITE_ID = 2

# LOGIN_REDIRECT_URL = '/'
# LOGOUT_REDIRECT_URL = '/'
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='230827856265-062bm2fgjfl24qqbdnqkastuue59nmmt.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='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'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'udemy.urls'

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
                'app.cart_context_processor.get_cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'udemy.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'udemy',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = 'static/'
STATICFILE_DIRS = [
    os.path.join(BASE_DIR, 'udemy/static')
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CRISPY_TEMPLATE_PACK = 'bootstrap4'


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'mahmoudatefff07@gmail.com'
EMAIL_HOST_PASSWORD = 'iwwyinompvtrcsru'


CELERY_BROKER_URL = 'redis://127.0.0.1:6379'

CELERY_BEAT_SCHEDULE = {
    "SendHello": {
        'task': 'user.tasks.test',
        'schedule': 10  # every 10 secound
    }
}
