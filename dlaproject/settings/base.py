"""
Django settings for dlaproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)  # Points to <repository root>


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 'oaiharvests', IN DEVOLOPMENT
    # 'dlasite', IN DEVELOPMENT

    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dlaproject.urls'

WSGI_APPLICATION = 'dlaproject.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_DIR.child('media')

# Disable this when static directories are managed outside of individual apps
# E.g., in the project root as we are doing in this project.
# STATIC_ROOT = PROJECT_DIR.child('static')

STATICFILES_DIRS = (
    PROJECT_DIR.child('static'),
)

STATIC_URL = '/static/'

TEMPLATE_DIRS = PROJECT_DIR.child('templates')
