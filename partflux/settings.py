# Django settings for Partflux project.
import os
DIRNAME = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

ADMINS = (
     ('Derek Musselmann', 'derek@partflux.com'),
)

INTERNAL_IPS = {
	'192.168.2.2',
	'127.0.0.1',
	'68.13.156.23',
	'68.96.19.120',
    '192.168.0.9',
}

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 	# Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': '',                     	                # Or path to database file if using sqlite3.
            'USER': '',                      				    # Not used with sqlite3.
            'PASSWORD': '',                  			        # Not used with sqlite3.
            'HOST': 'localhost',                      	        # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '',                      					# Set to empty string for default. Not used with sqlite3.
            'OPTIONS': {
                'autocommit': True,
            }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_KEY_PREFIX = ''


ALLOWED_HOSTS = ['partflux.com',]

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
LOGOUT_URL = '/users/logout/'

# Sets the maximum length of a page title
MAX_PAGE_TITLE_LENGTH = 65

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = 'http://partflux.com/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, '../static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(DIRNAME, '../templates'),
        ],
        'APP_DIRS': True,
        'TEMPLATE_DEBUG': 'DEBUG',
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
        },
    },
]



MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
#    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'partflux.urls'

WSGI_APPLICATION = 'partflux.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',

    # external apps
    'django_hstore',
    'pure_pagination',
    'sorl.thumbnail',
    'haystack',
    'storages',
#    'pingback',
    'taggit',
    'django_xmlrpc',
    'debug_toolbar',
    'django_select2',
    'widget_tweaks',
    'djcelery',

    # partfindr apps
    'parts',
    'companies',
    'distributors',
    'users',
)

# django-registration settings
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 1,
}

ACCOUNT_ACTIVATION_DAYS = 7

# custom user profile module
#AUTH_PROFILE_MODULE = 'users.UserProfile'

# django-storages settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_IS_GZIPPED = True

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/users/profile/%s/" % o.username,
}

AUTH_USER_MODEL = 'auth.User'

# django-select2 settings
SELECT2_BOOTSTRAP = True

# celery / django-celery settings
CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

from settings_local import *
