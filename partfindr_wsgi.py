import os
import sys

sys.path.append('/home/derek')
sys.path.append('/home/derek/partfindr')

os.environ['DJANGO_SETTINGS_MODULE'] = 'partfindr.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

