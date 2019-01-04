"""
Django settings for flight_booking project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dotenv

from datetime import timedelta


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# load the .env file
dotenv.load()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = dotenv.get('APP_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = dotenv.get('DEBUG')


ALLOWED_HOSTS = [
    'flight-booking-ap.herokuapp.com/'
    '127.0.0.1',
    'localhost',
    '[::1]',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'flight_booking.apps.bookings',
    'flight_booking.apps.users',
    'storages',
    'django_crontab',
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

ROOT_URLCONF = 'flight_booking.config.urls'

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

WSGI_APPLICATION = 'flight_booking.config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': dotenv.get('DB_NAME'),
        'USER': dotenv.get('DB_USER'),
        'PASSWORD': dotenv.get('DB_PASSWORD'),
        'PORT': dotenv.get('DB_PORT'),
        'HOST': dotenv.get('DB_HOST'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

CRONJOBS = [
    ('0 0 * * *', 'flight_booking.apps.bookings.cron_job.send_flight_reminder_mail')
]

CRONTAB_COMMAND_SUFFIX = '2>&1'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

AUTH_USER_MODEL = 'users.User'

AWS_ACCESS_KEY_ID = dotenv.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = dotenv.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = dotenv.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
AWS_DEFAULT_ACL = 'public-read'

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

DEFAULT_FILE_STORAGE = 'flight_booking.config.custom_s3_storage.MediaStorage'

TOKEN_EXP = timedelta(minutes=dotenv.get('TOKEN_EXP_MIN', default=30))

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = dotenv.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = dotenv.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER