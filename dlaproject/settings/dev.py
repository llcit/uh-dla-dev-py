# dev.py
from .base import *

# Secret key stored in your local environment variable not here.
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'oaitestdb',
        'USER': 'djangodbuser',
        'PASSWORD': '1',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Append apps used in development not production.
INSTALLED_APPS += (
    'debug_toolbar',
)