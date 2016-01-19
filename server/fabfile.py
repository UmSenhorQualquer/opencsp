import os, sys; 
sys.path.append('./');
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from django.db.models import Q

from fabric.api import *
from fabric.contrib.files import exists


from opencsp.models import Server,Algorithm, Job, Cluster

import os
import argparse



def sync_slaves_code(serverid, app=None):
	"""
	Syncs the slaves with the local
	"""
	try:
		server = Server.objects.get(pk = serverid)
	except Exception as detail:
		print "Error: no server found", detail
		return

	server.synchronizeServer()


def sync_cluster_code(clusterid):
	cluster = Cluster.objects.get(pk=clusterid)
	print "\n\n******************* SETUP NODE ********************\n\n"
	for server in cluster.servers.all(): server.setup_node()

	print "\n\n******************* SYNC APPS ********************\n\n"
	for server in cluster.servers.all():
		for application in cluster.algorithms.all():
			sync_slaves_code(server.pk, application.pk)

	print "\n\n******************* CLOSE SETUP ********************\n\n"
	listofserversandapps = []
	for server in cluster.servers.all():
		for application in cluster.algorithms.all():
			key = str(server) + str(application)
			if key not in listofserversandapps:
				server.close_setup_node(application)
				listofserversandapps.append( key )