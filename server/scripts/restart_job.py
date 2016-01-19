import os, sys; sys.path.append('./');
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from opencsp.models import *


job = Job.objects.get(pk=sys.argv[1])
job.job_started = None
job.job_ended = None
job.job_state = ''
job.ouput = ''
job.save()