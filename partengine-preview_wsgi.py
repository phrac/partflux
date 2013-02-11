import os
import sys

sys.path.append('/home/derek')
sys.path.append('/home/derek/partengine-preview')

os.environ['DJANGO_SETTINGS_MODULE'] = 'partengine-preview.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
