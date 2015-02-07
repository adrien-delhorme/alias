"""
Django settings for alias project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import json
import os
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Secrets handling
# --------------------------------------

# JSON-based secrets module
with open(os.path.join(BASE_DIR, 'settings/secrets.json')) as f:
    secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets, optional=False):
    """
    Get the secret variable or return explicit exception.
    """
    try:
        return secrets[setting]
    except KeyError:
        if not optional:
            error_msg = 'Set the {} environment variable'.format(setting)
            raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = get_secret("ALLOWED_HOSTS")
ADMINS = get_secret("ADMINS")

SECRET_KEY = get_secret("SECRET_KEY")

# Email setup

EMAIL_USE_TLS = True
EMAIL_HOST = get_secret('EMAIL_HOST')
EMAIL_HOST_USER = get_secret('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_secret('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_secret('EMAIL_PORT')
DEFAULT_FROM_EMAIL = get_secret('DEFAULT_FROM_EMAIL')

# Database setup

DATABASES = get_secret('DATABASES')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'widget_tweaks',
    'alias_app.webapp',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'alias_app.urls'

WSGI_APPLICATION = 'alias_app.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '../public/static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Template directories

TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]

LOGIN_REDIRECT_URL = reverse_lazy('wizard')
