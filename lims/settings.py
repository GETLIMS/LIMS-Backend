"""
Django settings for lims project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from ast import literal_eval
import datetime

TESTMODE = sys.argv[1:2] == ['test']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=112i0p+%m&d(l8v#1mu*@j*as%7@e!&*nw90@ghy((d-6ynd4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_docs',
    'corsheaders',
    'gm2m',
    'django_countries',
    'ordered_model',
    'django_extensions',
    'channels',
    'guardian',
    'lims.shared',
    'lims.users',
    'lims.orders',
    'lims.addressbook',
    'lims.pricebook',
    'lims.crm',
    'lims.inventory',
    'lims.codonusage',
    'lims.projects',
    'lims.workflows',
    'lims.dashboard',
    'lims.equipment',
    'lims.filetemplate',
    'lims.datastore',
    'lims.drivers',
    'lims.plugins.apps.PluginsConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'reversion.middleware.RevisionMiddleware'
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # default
    'guardian.backends.ObjectPermissionBackend',
)

ROOT_URLCONF = 'lims.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'lims/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'lims.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME', 'lims'),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', 5432)
    }
}

ATOMIC_REQUESTS = True

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR + '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "lims/static"),
)

# Media location (for quotes etc.)
MEDIA_ROOT = BASE_DIR + '/files/'
MEDIA_URL = '/files/'

#
# Email settings
#
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '465')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', True)
EMAIL_FROM = os.environ.get('EMAIL_FROM', 'Leaf LIMS')

#
# Async/queue settings
#
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'asgi_redis.RedisChannelLayer',
        'ROUTING': 'lims.urls.channel_routing',
        'CONFIG': {
            'hosts': [os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379')]
        }
    },
}

#
# Logging
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

#
# Per webapp permissions
#
WEBAPP_STAFF_ONLY = {
    'customerportal': False,
    'EquipmentReservations': False,
    'lims': True,
}

#
# REST framework settings
#
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'lims.shared.pagination.PageNumberOnlyPagination',
}

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'Identifier'
)

#
# Token settings
#
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(hours=12),
}

#
# App configuration
#
ORGANISATION_NAME = os.environ.get('ORGANISATION_NAME', 'Leaf LIMS')

#
# CRM Settings
#
ENABLE_CRM = literal_eval(os.environ.get('ENABLE_CRM', 'True'))

#
# Salesforce settings
#
SALESFORCE_URL = os.environ.get('SALESFORCE_URL', 'https://login.salesforce.com')
SALESFORCE_USERNAME = os.environ.get('SALESFORCE_USERNAME', '')
SALESFORCE_PASSWORD = os.environ.get('SALESFORCE_PASSWORD', '')
SALESFORCE_TOKEN = os.environ.get('SALESFORCE_TOKEN', '')

#
# Project configurations
#
PROJECT_IDENTIFIER_PREFIX = os.environ.get('PROJECT_IDENTIFIER_PREFIX', 'P')
PROJECT_IDENTIFIER_START = os.environ.get('PROJECT_IDENTIFIER_START', 100)

#
# Admin user defaults
#
SETUP_ADMIN_EMAIL = os.environ.get('SETUP_ADMIN_EMAIL', '')
SETUP_ADMIN_PASSWORD = os.environ.get('SETUP_ADMIN_PASSWORD', None)

#
# Default groups and permissions
#
DEFAULT_GROUPS = ('user', 'staff', 'admin',)
DEFAULT_USER_PERMISSIONS = (
    "Can add equipment reservation",
    "Can change equipment reservation",
    "Can delete equipment reservation",
    "Can add trigger subscription",
    "Can change trigger subscription",
    "Can delete trigger subscription",
)
DEFAULT_STAFF_PERMISSIONS = (
    "Can add order",
    "Can change order",
    "Can delete order",
    "Can add address",
    "Can change address",
    "Can delete address",
    "Can add tag",
    "Can change tag",
    "Can delete tag",
    "Can add set",
    "Can change set",
    "Can delete set",
    "Can add item",
    "Can change item",
    "Can delete item",
    "Can add item property",
    "Can change item property",
    "Can delete item property",
    "Can add project",
    "Can change project",
    "Can delete project",
    "View project",
    "Can add product",
    "Can change product",
    "Can delete product",
    "View product",
    "Can add comment",
    "Can change comment",
    "Can delete comment",
    "Can add work log",
    "Can change work log",
    "Can delete work log",
    "View workflow",
    "Can add equipment reservation",
    "Can change equipment reservation",
    "Can delete equipment reservation",
    "Access LIMS system",
    "View item",
    "View item type",
    "View measure",
    "View location",
    "View item set",
    "View product status",
    "View comment",
    "View workflow task template",
    "Can add run",
    "Can change run",
    "Can delete run",
    "View run",
    "View CRM Project",
    "View CRM Quote",
    "View CRM Account",
    "Can add crm account",
    "Can change crm account",
    "Can delete crm account",
    "Can add crm project",
    "Can change crm project",
    "Can delete crm project",
    "Can add crm quote",
    "Can change crm quote",
    "Can delete crm quote",
)

#
# API DOCS SETTINGS
#
SWAGGER_SETTINGS = {
    'is_authenticated': True,
}


# ALERTS
ALERT_EMAIL_FROM = 'Leaf LIMS <LeafLIMS@localhost>'
