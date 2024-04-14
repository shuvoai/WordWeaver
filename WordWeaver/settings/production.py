from decouple import config

from .base import *
import os
DEBUG = False

SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DB_NAME'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASS')
    }
}
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = []
