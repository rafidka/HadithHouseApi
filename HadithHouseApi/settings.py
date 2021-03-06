#
# The MIT License (MIT)
#
# Copyright (c) 2018 Rafid Khalid Al-Humaimidi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

"""
Django settings for HadithHouseApi project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import socket

import sys
from enum import Enum

import time

from django.utils.deprecation import MiddlewareMixin

from HadithHouseApi.server_settings import get_db_settings, get_debug, \
    get_allowed_hosts

test_mode = 'test' in sys.argv
collectstatic_mode = 'collectstatic' in sys.argv
migrate_mode = 'migrate' in sys.argv
OFFLINE_MODE = False


class JavaScriptFrameworkMode(Enum):
    """
    Specifies the JS framework to use. This is temporary while I try different
    JS frameworks to replace AngularJS.
    """
    ANGULARJS = 0
    REACTJS = 1
    ANGULAR = 2

    def __int__(self):
        return self.value


JS_FRAMEWORK_MODE = JavaScriptFrameworkMode.ANGULARJS


def is_test_mode():
    """
    Determines whether the applicaiton is being currently running in test mode,
    i.e. python manage.py test.
    :return: True or false.
    """
    return test_mode


def is_offline_mode():
    """
    Determines whether the application is running in offline mode. In this mode,
    the website uses locally fetched JS libraries and uses a sqlite local
    database.
    :return: True or False.
    """
    return OFFLINE_MODE


def is_collectstatic_mode():
    """
    Determines whether the code is being executed during a call to
    "python manage.py collectstatic".
    :return: True or false.
    """
    return collectstatic_mode


def is_migrate_mode():
    """
    Determines whether the code is being executed during a call to
    "python manage.py migrate".
    :return: True or false.
    """
    return migrate_mode


if is_test_mode() or is_collectstatic_mode():
    # We are running in test mode or collecting static files. Hence, avoid using
    # the real log directory to avoid breaking Jenkins build, as there is no
    # log directory on Jenkins.
    import tempfile


    def get_log_dir():
        return tempfile.gettempdir()
else:
    from HadithHouseApi.server_settings import get_log_dir

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(8rs1@c-&_9z(8ur%ydax^gf-p5)58y%94huyaa2&p1b-%1uwj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_debug()
DJANGO_LOG_LEVEL = DEBUG

ALLOWED_HOSTS = get_allowed_hosts()

PRODUCTION_HOSTS = (
    'www.hadithhouse.net',
)

DEVELOPMENT_HOSTS = (
    'dev.hadithhouse.net',
)


def get_environment():
    host = socket.getfqdn().lower()

    if host in PRODUCTION_HOSTS:
        return 'production'
    elif host in DEVELOPMENT_HOSTS:
        return 'development'
    else:
        return 'local'


SERVER_EMAIL = 'noreply@hadithhouse.net'

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_filters',
    'corsheaders',
    'hadiths',
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'HadithHouseApi.urls'

APPEND_SLASH = False

WSGI_APPLICATION = 'HadithHouseApi.wsgi.application'

CORS_ORIGIN_ALLOW_ALL = False
CORS_ORIGIN_REGEX_WHITELIST = [
    '^(https?://)?(\w+\.)?hadithhouse\.net(:(8080|8000))?/?(.+)?$'
]

ADMINS = (
    ('Rafid Al-Humaimidi', 'admin@hadithhouse.net'),
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
# This
if is_test_mode():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'HadithHouse-Test.db'),
        }
    }
elif is_offline_mode():
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'HadithHouse-OfflineMode.db'),
        }
    }
else:
    DATABASES = get_db_settings()

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': get_debug()
        },
    },
]

if is_test_mode() or is_collectstatic_mode() or is_migrate_mode():
    # To separate log files generated during test/db-migration/etc from real
    # log files, we use different names. In addition to the benefit of
    # isolation, the main benefit of this is to avoid permission-related
    # errors caused by trying to access log files with the same
    # name but owned by a different account. For example, during deployment,
    # a log file named 'django.log' would be produced and owned by 'deployer'.
    # Now when apache2 starts and try to access the same file, a permission
    # error is generated. Thus, it is essential to name the files produced by
    # these two scenarios differently.
    mode = 'test' if is_test_mode() \
        else 'migrate' if is_migrate_mode() \
        else 'collectstatic' if is_collectstatic_mode() \
        else 'other'

    timestamp = str(int(time.time() * 1000))
    django_log_filename = os.path.join(
        get_log_dir(), 'django.%s.%s.log' % (mode, timestamp))
    django_requests_log_filename = os.path.join(
        get_log_dir(), 'django.%s.%s.request.log' % (mode, timestamp))
    django_db_backends_log_file = os.path.join(
        get_log_dir(), 'django.%s.%s.db.backends.log' % (mode, timestamp))
else:
    django_log_filename = os.path.join(
        get_log_dir(), 'django.log')
    django_requests_log_filename = os.path.join(
        get_log_dir(), 'django.request.log')
    django_db_backends_log_file = os.path.join(
        get_log_dir(), 'django.db.backends.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'django_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': django_log_filename,
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'utc': True,
            'formatter': 'simple',
            'encoding': 'utf-8'
        },
        'django_requests_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': django_requests_log_filename,
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'utc': True,
            'formatter': 'simple',
            'encoding': 'utf-8'
        },
        'django_db_backends_log_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': django_db_backends_log_file,
            'when': 'D',
            'interval': 1,
            'backupCount': 30,
            'utc': True,
            'formatter': 'simple',
            'encoding': 'utf-8'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['django_log_file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['django_requests_log_file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['django_db_backends_log_file'],
            'propagate': False,
        },
    }
}

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.backends.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'hadiths.pagination.DefaultPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'hadiths.auth.FacebookAuthentication',
    ),
    'EXCEPTION_HANDLER': 'HadithHouseApi.exception_handler.hadithhouse_exception_handler'
}

if OFFLINE_MODE:
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = (
        'hadiths.auth.FacebookOfflineAuthentication',)
