# Django settings for museic project.

import os

CUR_DIRECTORY = os.path.dirname(__file__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = '/tmp/museic.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

EMAIL_SUBJECT_PREFIX = '[MUSEiC] '
EMAIL_HOST = 'localhost'
EMAIL_PORT = '1025'

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

SITE_ID = 1

SITE_PREFIX = ''
MEDIA_ROOT = os.path.join(CUR_DIRECTORY, os.path.pardir, 'static')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static-admin/'
MUSEIC_CONTENT_ROOT = os.path.join(CUR_DIRECTORY, os.pardir, "dynamic")
MUSEIC_CONTENT_PREFIX = '/dynamic/'
LOGIN_REDIRECT_URL = '/accounts/profile/'
LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'

for i in ('MEDIA_URL', 'ADMIN_MEDIA_PREFIX', 'MUSEIC_CONTENT_PREFIX',
        'LOGIN_REDIRECT_URL', 'LOGIN_URL', 'LOGOUT_URL'):
    globals()[i] = SITE_PREFIX + globals()[i]

SECRET_KEY = '0mn**5qi^6=+xlr_q2(1+^6agwx2ua&37m=(4+cfz(n8g4r78t'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
                                "django.core.context_processors.debug",
                                "django.core.context_processors.i18n",
                                "django.core.context_processors.media",
                                "django.core.context_processors.request",
                                )


ROOT_URLCONF = 'museic.urls'

AUTH_PROFILE_MODULE = 'accounts.userprofile'
ABSOLUTE_URL_OVERRIDES = {
        'auth.user': lambda o: '/accounts/profile/%s' % o.username,
        }

TEMPLATE_DIRS = (
    os.path.join(CUR_DIRECTORY, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.comments',

    'userprofile',
    'djangoratings',
    'messages',

    'museic.accounts',
    'museic.content',
    'museic.navigation',
    'museic.microformats',
    'museic.ajax',
)
