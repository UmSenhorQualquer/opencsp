import sys, os; sys.path.append("./");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from django.utils import timezone
from dateutil import parser
from opencsp import AVAILABLE_STORAGES
from django.contrib.auth.models import User

infodir = os.path.join( settings.MEDIA_ROOT, 'mounts', 'mountsinfo' )
for subdir, dirs, files in os.walk(infodir):
	for filename in files:
		username = filename[:-4]
		infofile = os.path.join(infodir, filename)

		try:
			with open( infofile, 'r') as f: lastmount = parser.parse(f.read())
			timediff = (timezone.now()-lastmount).total_seconds()
			if timediff>settings.WAITING_TIME_BEFORE_UNMOUNT_USER_AREA:
				user = User.objects.get(username=username)
				storage = AVAILABLE_STORAGES.get(user)
				storage.umount()
		except: pass