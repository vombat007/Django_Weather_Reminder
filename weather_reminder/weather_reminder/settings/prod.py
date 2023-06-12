from .base import *

DEBUG = False

INSTALLED_APPS = ['gunicorn'] + INSTALLED_APPS

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('HOST'),
        'PORT': env('PORT'),

    }
}
