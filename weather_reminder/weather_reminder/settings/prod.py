from .base import *

DEBUG = False

INSTALLED_APPS = ['gunicorn'] + INSTALLED_APPS

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
