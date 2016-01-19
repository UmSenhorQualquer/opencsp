import json
import Utils.servertools as servertools
from mimetypes import MimeTypes
from django.conf import settings
from django.http import HttpResponse
from opencsp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper

@csrf_exempt
def syncservers(request):
	data=json.loads(request.body)
	uniqueid = data.get('uniqueid',None)
	try:
		satellite = SatelliteServer.objects.get(satelliteserver_uniqueid=uniqueid)

		# SYNC SERVERS ############################################################
		serverslist = data.get('servers',[])
		servers_added = 0
		existing_servers = 0
		for serverdata in serverslist:
			try:
				server = Server.objects.get(server_uniqueid=serverdata['server_uniqueid'], satelliteserver=satellite)
				server.server_name = serverdata['server_name']
				server.server_isalive = serverdata['server_isalive']
				if serverdata.get('server_lastcontact', None)!='None':
					server.server_lastcontact = serverdata.get('server_lastcontact', None)
				server.save()
				existing_servers += 1
			except Server.DoesNotExist:
				server = Server(
					satelliteserver=satellite, 
					server_name=serverdata['server_name'],
					server_uniqueid=serverdata['server_uniqueid'],
					server_isalive=serverdata['server_isalive'],
					server_lastcontact=serverdata['server_lastcontact'],)
				server.save()
				servers_added += 1
		# SYNC CLUSTERS ############################################################
		clusterslist = data.get('clusters',[])
		clusters_added = 0
		existing_clusters = 0
		for clusterdata in clusterslist:
			try:
				cluster = Cluster.objects.get(cluster_uniqueid=clusterdata['cluster_uniqueid'], satelliteserver=satellite)
				cluster.cluster_name = clusterdata['cluster_name']
				cluster.save()
				existing_clusters += 1
			except Cluster.DoesNotExist:
				cluster = Cluster(
					satelliteserver=satellite, 
					cluster_name=clusterdata['cluster_name'],
					cluster_uniqueid=clusterdata['cluster_uniqueid'])
				cluster.save()
				clusters_added += 1

			for serverui in clusterdata['servers']:
				s = Server.objects.get(server_uniqueid=serverui, satelliteserver=satellite)
				if s not in cluster.servers.all(): cluster.servers.add(s)
		############################################################################
		data = { 'result': 'OK', 
				 'Added servers': servers_added, 'Existing servers': existing_servers,
				 'Added clusters': clusters_added, 'Existing clusters': existing_clusters  }
	except SatelliteServer.DoesNotExist:
		data = { 'result': 'No server' }
	return HttpResponse(json.dumps( data ), "application/json")



@csrf_exempt
def getjobs(request):
	data=json.loads(request.body)
	uniqueid = data.get('uniqueid',None)
	try:
		satellite = SatelliteServer.objects.get(satelliteserver_uniqueid=uniqueid)
		servers = Server.objects.filter( satelliteserver=satellite )
		jobs = Job.objects.filter( server=servers, job_started=None ).exclude(job_uniqueid=None)
		
		data = { 'result': 'OK', 
				 'jobs': [x.dictionary for x in jobs] }

	except SatelliteServer.DoesNotExist:
		data = { 'result': 'No server' }

	return HttpResponse(json.dumps( data ), "application/json")

@csrf_exempt
def updatejob(request):
	data=json.loads(request.body)
	uniqueid = data.get('uniqueid', None)
	try:
		satellite = SatelliteServer.objects.get(satelliteserver_uniqueid=uniqueid)
		jobdata = data.get('job', None)
		if jobdata:
			job_uniqueid = jobdata.get('job_uniqueid', None)
			job = Job.objects.get(job_uniqueid=job_uniqueid, server__satelliteserver=satellite)
			job.dictionary = jobdata
			job.save()
		data = { 'result': 'OK' }
	except Job.DoesNotExist or SatelliteServer.DoesNotExist:
		data = { 'result': 'No server' }

	print "update job"
	return HttpResponse(json.dumps( data ), "application/json")


@csrf_exempt
def uploadfile(request):
	print "-------********* UPLOADFILE"
	data=request.POST
	uniqueid = data.get('uniqueid', None)
	job_uniqueid = data.get('job_uniqueid', None)

	print "uniqueid", uniqueid, 'job_uniqueid', job_uniqueid
	try:
		satellite = SatelliteServer.objects.get(satelliteserver_uniqueid=uniqueid)
		job = Job.objects.get(job_uniqueid=data.get('job_uniqueid', None), server__satelliteserver=satellite)
		
		if 'file' in request.FILES:
			filecontent = request.FILES['file']
			filename = data.get('filename', None)
			filepath = os.path.join( settings.MEDIA_ROOT, 'uploads', job.user.username, filename )
			fd = open( filepath, 'wb')
			fd.write(filecontent.read())
			fd.close()
	except Job.DoesNotExist or SatelliteServer.DoesNotExist:
		pass

	return HttpResponse('Nothing')

@csrf_exempt
def downloadfile(request):
	data=json.loads(request.body)
	uniqueid = data.get('uniqueid', None)
	try:
		satellite = SatelliteServer.objects.get(satelliteserver_uniqueid=uniqueid)
		job = Job.objects.get(job_uniqueid=data.get('job_uniqueid', None), server__satelliteserver=satellite)
		filename = data.get('filename', None)
		if filename:			
			filepath = servertools.userFilePath(job.user, filename)
			mime = MimeTypes()
			mimetype = mime.guess_type(filepath)
			filesize = os.path.getsize(filepath)

			wrapper = FileWrapper(file(filepath))
			response = HttpResponse(wrapper, content_type=mimetype)
			response['Content-Length'] = filesize
			return response

	except Job.DoesNotExist or SatelliteServer.DoesNotExist:
		pass
	HttpResponse('Nothing')
