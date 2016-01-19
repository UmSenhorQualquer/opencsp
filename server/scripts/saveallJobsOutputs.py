import sys, os; sys.path.append("./");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from opencsp.models import Job, Server, Task
from common import all_connected_servers


jobs = Job.objects.all()

for job in jobs:
	job.output = job.job_output
	print job