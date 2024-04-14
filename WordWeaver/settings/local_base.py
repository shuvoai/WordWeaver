import os
from .base import *
from decouple import config
DEBUG = True

HOST = "http://localhost:8000"

SECRET_KEY = "qweiufgwqifwefwfwefefgq"

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'public/static')

MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
