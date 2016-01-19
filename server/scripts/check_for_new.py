import sys, os; sys.path.append("./");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from opencsp.models import Job, Server, Task
from common import all_connected_servers


server = Server.objects.get(pk=sys.argv[1])

jobs = Job.objects.filter( job_started=None )
jobs = jobs.filter(server__in=all_connected_servers(server), server__satelliteserver=None)
jobs = jobs.order_by('job_created')

tested_servers = []
for job in jobs:
	if job.server in tested_servers: continue
	if job.server.has_job(): continue
	tested_servers.append( job.server )
	job.run()
	


if server.server_turnoff:
	#check if there are still jobs to run, otherwise turn the computer off
	jobs = Job.objects.filter( job_ended=None )
	jobs = jobs.filter( server__in=all_connected_servers(server) )
	if not jobs.exists():
		#if there are no jobs, stop the server
		#For some reason the server restart after the first shutdown
		#this function place a future task for opencsp to shutdown the compute again
		Task.schedule_server_shutdown(server); 
		try: server.stop()
		except: pass
