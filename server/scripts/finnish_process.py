import sys; reload(sys); sys.setdefaultencoding("utf-8"); sys.path.append('./');
import os; os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from opencsp.models import *
import sys
import os,time
from django.db.models import Q


#f = open('/var/www/opencsp/shutdownlog.txt', 'w')

#check if the jobs ended
servers = [Server.objects.get(pk=sys.argv[1])]
for server in servers: server.unload_files()

