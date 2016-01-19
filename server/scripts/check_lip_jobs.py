import os, sys; sys.path.append('./');
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from django.db.models import Q
from opencsp.models import *


CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
FLAG_FILE 	= os.path.join(CURRENT_DIR, 'flags', 'LIP_SCRIPT_RUNNING.txt')


if os.path.exists(FLAG_FILE): exit()

try:
	f = open(FLAG_FILE, 'w'); f.close()

	serversQuery = Server.objects.filter( Q(server_envmanager='LIPHPCEnvManager') | Q(server_envmanager='LIPEnvManager') )
	servers = []
	for server in serversQuery:
		if server.has_job(): servers.append(server)

	jobs = Job.objects.exclude(job_started=None).filter(
		job_ended=None, 
		server__satelliteserver=None, 
		server__in=servers )
	jobs = jobs.order_by('job_created')

	tested_servers = []
	for job in jobs:
		if job.server in tested_servers: continue
		if job.server.has_job() and job.is_finnished():
			job.job_state = 'unloading'
			job.save()
			job.server.unload_files()
		tested_servers.append( job.server )

finally: 
	try:
		os.remove(FLAG_FILE)
	except:
		print "log"
	