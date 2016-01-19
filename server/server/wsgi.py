"""import os, sys; sys.path.append('/var/www/opencsp')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()"""


import os
import sys
sys.path.append('/var/www/opencsp')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
