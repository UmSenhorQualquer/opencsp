import os, sys; sys.path.append('../');os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_processing.settings")
from django.conf import settings
import requests, json
from urlparse import urljoin
from opencsp.models import *
from django.contrib.auth.models import User


servers = {}
for master in MasterServer.objects.all():
	url = urljoin(master.masterserver_url, 'ws/getjobs/')
	headers = {'content-type': 'application/json'}

	data2send = {'uniqueid': settings.OPENCSP_UNIQUE_ID }

	r = requests.post(url, data=json.dumps(data2send), headers=headers)
	retreaveddata = r.json()
	for data in retreaveddata.get('jobs', []):
		if Job.objects.filter(masterserver=master,job_uniqueid=data.get('job_uniqueid', None)).count()==0:
			job = Job()
			job.masterserver = master
			job.dictionary = data
			job.user = master.user
			job.save()
			parameters = eval(job.job_parameters)
			parameters['userpath'] = os.path.join(settings.MEDIA_ROOT,'uploads',master.user.username,str(job.pk) )
			job.job_parameters = str(parameters)
			job.save()
			servers[str(job.server)] = job.server

for server in servers.values():
	os.system("cd %s; python check_for_new.py %d" % (settings.BASE_DIR,server.pk) )