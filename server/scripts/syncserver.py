import os, sys; sys.path.append('../');os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cloud_processing.settings")
from django.conf import settings
import requests, json
from urlparse import urljoin
from opencsp.models import *


for master in MasterServer.objects.all():
	url = urljoin(master.masterserver_url, 'ws/syncservers/')
	headers = {'content-type': 'application/json'}

	# SERVERS #######################################
	servers = []
	for server in Server.objects.filter(satelliteserver=None).exclude(server_uniqueid=None).distinct():
		data = {'server_uniqueid': server.server_uniqueid, 
				'server_name': server.server_name,
				'server_isalive': server.server_isalive,
				'server_lastcontact': str(server.server_lastcontact) }
		servers.append( data )
	# CLUSTERS #######################################
	clusters = []
	for cluster in Cluster.objects.filter(satelliteserver=None).exclude(cluster_uniqueid=None):
		data = {'cluster_uniqueid': cluster.cluster_uniqueid, 
				'cluster_name': cluster.cluster_name,
				'servers': [x.server_uniqueid for x in cluster.servers.all() if x.server_uniqueid!=None] }

		clusters.append( data )
	##################################################
	data2send = {
		'uniqueid': settings.OPENCSP_UNIQUE_ID, 
		'servers': servers,
		'clusters': clusters }

	r = requests.post(url, data=json.dumps(data2send), headers=headers)
	print r.text