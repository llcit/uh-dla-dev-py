# settings/prod.py

from .base import *



DEBUG = False

TEMPLATE_DEBUG = False

# ! DO NOT EDIT THIS ON LOCAL ENVIRONMENTS! MEANT FOR PRODUCTION (but we want it in the repo).
ALLOWED_HOSTS = ['*.yourhost.com']

# Append apps needed in production.
# (nothing needed at the moment that is not specified in base.py)
# INSTALLED_APPS += ('someapp',)

# ! SACRED -- DO NOT EDIT THIS ON LOCAL ENVIRONMENTS! MEANT FOR PRODUCTION (but we want it in the repo).

SECRET_KEY = ''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

MEDIA_URL = ''

# Disable this when static directories are managed outside of individual apps
# E.g., in the project root as we are doing in this project.
# STATIC_ROOT = PROJECT_DIR.child('static')

STATIC_URL = ''

# END SACRED
