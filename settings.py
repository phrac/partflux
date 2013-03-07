# Django settings for partfindr project.
import os
DIRNAME = os.path.dirname(__file__)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Derek Musselmann', 'derek@partfindr.net'),
)

INTERNAL_IPS = {
	'192.168.2.2',
	'127.0.0.1',
	'68.13.156.23',
	'68.96.19.120',
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
                'POOL_ENABLED': True,
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


LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
LOGOUT_URL = '/users/logout/'

# Settings for user voting system
# Reputation required before a user can up/down vote items
MINIMUM_VOTE_REPUTATION = 50
# how many reputation points should the user get for a new part
REP_VALUE_NEW_PART = 10
# how many reputation points should the user get for a new buylink
REP_VALUE_NEW_BUYLINK = 1
# how many rep points should user get for new attribute
REP_VALUE_NEW_ATTRIBUTE = 2
# how many rep points should user get for new comment
REP_VALUE_NEW_COMMENT = 3
# how many rep points should user get for new image
REP_VALUE_NEW_IMAGE = 3
# rep points for flagging an attribute (and the inverse if your attr is flagged)
REP_VALUE_FLAG_ATTR = 1
REP_VALUE_FLAGGED_ATTR = -1
# rep points if flag a part (and the inverse if your part is flagged)
REP_VALUE_FLAG_PART = 1
REP_VALUE_FLAGGED_PART = -1
# rep points for cross references
REP_VALUE_NEW_XREF = 5

# Sets the maximum length of a page title
MAX_PAGE_TITLE_LENGTH = 100

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
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/derek/web/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/home/derek/web/partengine/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = 'http://static.partengine.org/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = 'http://partfindr.net/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(DIRNAME, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "context_processors.user_reputation",
    "context_processors.part_count",
    "context_processors.nsn_count",
    "context_processors.get_current_domain",
    "context_processors.get_current_path",
    "context_processors.get_current_version",
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'users.middleware.LastSeen',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'partengine.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#	"/usr/home/derek/pp/partengine/templates",
    os.path.join(DIRNAME, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.sitemaps',
    # external apps
    'pure_pagination',
    'registration',
    'sorl.thumbnail',
    'django_gravatar',
    'faq',
    'tastypie',
    'markdown_deux',
    'haystack',
    'storages',
    'twitter_tag',
    'contact_form',
    # partfindr apps    
    'main',
    'parts',
    'companies',
    'nsn',
    'partgroups',
    'users',
    'reputation',
    'debug_toolbar',
)

# django-registration settings
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 10,
    'MARGIN_PAGES_DISPLAYED': 1,
}

ACCOUNT_ACTIVATION_DAYS = 7

# custom user profile module
AUTH_PROFILE_MODULE = 'users.UserProfile'

# django-storages settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_IS_GZIPPED = True

#Twitter OAuth Settings
# Your access token: Access token
TWITTER_OAUTH_TOKEN = '1228693177-QdV2B5cgs4zM4rt43QgdRH1XcIjBQr8ne32g86I'
# Your access token: Access token secret
TWITTER_OAUTH_SECRET = 'bcDxxq6ocaBNBQRMJyYvQXsbmpCxumTH9BBuhOqmUM'
# OAuth settings: Consumer key
TWITTER_CONSUMER_KEY = 'vGm8CZhCn1T4bbdvL99A'
# OAuth settings: Consumer secret
TWITTER_CONSUMER_SECRET = 'D0oseP8Rg1FXoJycv9qh2lUTAH8sNfGkD8YWEStuL5o'

ABSOLUTE_URL_OVERRIDES = {
    'auth.user': lambda o: "/users/profile/%s/" % o.username,
}

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
