DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django_orm.backends.postgresql_psycopg2',    # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                     	            # Or path to database file if using sqlite3.
        'USER': '',                      				    # Not used with sqlite3.
        'PASSWORD': '',                  			            # Not used with sqlite3.
        'HOST': '',                      	    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      					    # Set to empty string for default. Not used with sqlite3.
        'OPTIONS': {
        'POOL_ENABLED': True,
        }
    }
}

MEDIA_ROOT = '/home/derek/web/media/'

STATIC_ROOT = '/home/derek/web/previewstatic/static/'

# use gmail for sending email
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
SERVER_EMAIL = ''

SECRET_KEY = ''

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_STORAGE_BUCKET_NAME = ''

