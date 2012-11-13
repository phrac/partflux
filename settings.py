# Django settings for partfindr project.
import os
DIRNAME = os.path.dirname(__file__)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('Derek Musselmann', 'derek@disflux.com'),
)

INTERNAL_IPS = {
	'192.168.2.2',
	'127.0.0.1',
}

MANAGERS = ADMINS


# ES_HOST should be in a format that pyes understands
ES_HOST = '127.0.0.1:9200'

# User authentication redirect & URL configuration
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/users/login/'
LOGOUT_URL = '/users/logout/'

# Settings for user voting system
# Reputation required before a user can up/down vote items
MINIMUM_VOTE_REPUTATION = 50
# how many reputation points should the user get for a new part
REP_VALUE_NEW_PART = 10
# how many reputation points should the user get for a new buylink
REP_VALUE_NEW_BUYLINK = 4
# how many rep points should user get for new attribute
REP_VALUE_NEW_ATTRIBUTE = 2
# how many rep points should user get for new comment
REP_VALUE_NEW_COMMENT = 3
# how many rep points should user get for new image
REP_VALUE_NEW_IMAGE = 3

GOOGLE_SEARCH_PARTNER_ID = 'partner-pub-3185089159153756:8723235659'
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
#MEDIA_ROOT = '/home/derek/web/media/' # PRODUCTION

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/' # DEVELOPMENT

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

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

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'kr-5zw7w8l9d(9$-r79xjj%dw92d_%(1^@@6g^etp_x(k7z7=)'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "partfindr.context_processors.xref_count",
    "partfindr.context_processors.get_current_path",
    "partfindr.context_processors.get_current_domain",
    "partfindr.context_processors.part_count",
    "partfindr.context_processors.nsn_count",
    #"partfindr.context_processors.user_reputation",
    "flashcookie.flash_context",
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages"
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'flashcookie.FlashMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'partfindr.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
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
    'google_analytics',
    'pure_pagination',
    'registration',
    'sorl.thumbnail',
    'django_gravatar',
    'tastypie',
    'googlesearch',
    # partfindr apps 
    'main',
    'faq',
    'parts',
    'companies',
    'nsn',
    'partgroups',
    'users',
)

# django-registration settings
ACCOUNT_ACTIVATION_DAYS = 7

# custom user profile module
AUTH_PROFILE_MODULE = 'users.UserProfile'

# django-storages settings
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'
AWS_ACCESS_KEY_ID = 'AKIAJEBQFIW46J5LFB3Q'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'partfindr'
from S3 import CallingFormat
AWS_CALLING_FORMAT = CallingFormat.SUBDOMAIN

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 6,
    'MARGIN_PAGES_DISPLAYED': 2,
}

ACCOUNT_ACTIVATION_DAYS = 7
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
