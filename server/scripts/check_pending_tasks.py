import os, sys; sys.path.append('./');
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from opencsp.models import Job, Server, Task
from django.utils import timezone
from common import all_connected_servers

tasks = Task.objects.filter(task_started=None)

for task in tasks:

	if task.task_type==Task.TASKTYPE_SHUTDOWN_SERVER:
		diffseconds = (timezone.now()-task.task_created).total_seconds()
		#wait for WAITING_TIME_BEFORE_SHUTTING_DOWN_SERVER seconds before trying a shutdown again
		if diffseconds>=settings.WAITING_TIME_BEFORE_SHUTTING_DOWN_SERVER:
			task.task_started = timezone.now()
			params = task.params
			server = Server.objects.get(pk=params['server_id'])
			jobs = Job.objects.filter(server__in=all_connected_servers(server), server__satelliteserver=None)
			jobs = jobs.filter(job_ended=None)
			if not jobs.exists(): 
				try: server.stop()
				except: pass
			task.task_ended = timezone.now()
			task.save()