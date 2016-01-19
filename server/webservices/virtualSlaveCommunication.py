import json, os
import Utils.servertools as servertools
from mimetypes import MimeTypes
from django.conf import settings
from django.http import HttpResponse
from opencsp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.core.servers.basehttp import FileWrapper
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from datetime import datetime

@csrf_exempt
def registeVirtualServer(request):
	macaddress 	= request.POST.get('macaddress', None)
	username 	= request.POST.get('username', None)
	password 	= request.POST.get('password', None)
	maxram 		= int(request.POST.get('maxram', 0))
	maxcpus 	= int(request.POST.get('maxcpus', 0))
	version 	= float(request.POST.get('version', -1))
	
	user = authenticate(username=username, password=password)
	if user is not None:

		if VirtualServer.objects.filter(server_mac=macaddress).count()>0:
			server = VirtualServer.objects.get(server_mac=macaddress)
			data = { 'result':'OK', 'uniqueid':server.server_uniqueid }

			server.check_new_jobs()
		else:
			newserver = VirtualServer(
					server_name= "%s %s" %(username, request.META.get('REMOTE_ADDR','') ),
					server_mac=macaddress,
					server_host=request.META.get('REMOTE_ADDR',''),
					server_hostname = request.META.get('REMOTE_HOST', ''),
					server_active = False,
					server_isalive = True,
					server_lastcontact=datetime.now(),
					virtualserver_maxram = maxram,
					virtualserver_maxcores = maxcpus,
					virtualserver_version = version
				)
			newserver.save()
			data = { 'result':'OK', 'uniqueid':newserver.server_uniqueid }
	else:
		data = { 'result':'Login failed' }

	return HttpResponse(json.dumps( data ), "application/json")


@csrf_exempt
def existsVirtualServer(request):
	macaddress 	= request.POST.get('macaddress', None)
	uniqueid 	= request.POST.get('uniqueid', None)
	version 	= float(request.POST.get('version', -1))

	try:
		server = VirtualServer.objects.get(server_mac=macaddress, server_uniqueid=uniqueid)
		server.virtualserver_version = version
		server.save()
		data = { 'result':'OK' }
	except VirtualServer.DoesNotExist:
		data = { 'result':'No server' }

	return HttpResponse(json.dumps( data ), "application/json")



@csrf_exempt
def readCommand(request):
	uniqueid = request.POST.get('uniqueid',None)
	version  = float(request.POST.get('version',None))

	try:
		server = Server.objects.get(server_uniqueid=uniqueid)
		server.server_isalive = True
		server.server_lastcontact = datetime.now()
		server.save()

		if settings.VIRTUALSERVER_VERSION>version and server.virtualserver.virtualserver_update:
			result = {'result': 'OK', 'command': 'update' }
		else:
			instance = server.serverinstance

			if instance:
				data = instance.params
				if  instance.serverinstance_started is None and \
					instance.serverinstance_ended is None and \
					instance.serverinstance_endcommited is None:

					instance.serverinstance_started = datetime.now()
					instance.save()
					result = {'result': 'OK'}
					result.update( data )

				elif instance.serverinstance_ended is not None and \
					instance.serverinstance_endcommited is None:

					result = {'result': 'OK'}
					result.update( data )

				elif instance.serverinstance_started is not None and \
					instance.serverinstance_startcommited is not None and \
					instance.serverinstance_ended is None:

					if instance.job and instance.job.job_started is None and server.checkconnection():
						server.check_new_jobs()

					result = {'result': 'OK'}
				else:
					result = {'result': 'OK'}
			else:
				result = {'result': 'OK'}
		
	except Server.DoesNotExist:
		result = { 'result': 'No server' }
	return HttpResponse(json.dumps( result ), "application/json")


@csrf_exempt
def commitCommand(request):
	
	uniqueid = request.POST.get('uniqueid',None)
	try:
		server = Server.objects.get(server_uniqueid=uniqueid)
		server.server_isalive = True
		server.server_lastcontact = datetime.now()
		server.save()
		command = request.POST.get('command',None)

		if command == 'update':
			server.virtualserver.virtualserver_update=False
			server.virtualserver.save()
			
		instance = server.serverinstance
		
		if instance:

			if command == 'start':
				instance.serverinstance_startcommited = datetime.now()
				instance.save()
			if command == 'stop' or command == 'pause':
				instance.serverinstance_endcommited = datetime.now()
				instance.save()
				server.check_new_jobs()

		result = {'result': 'OK'}
			
	except Server.DoesNotExist:
		result = { 'result': 'No server' }
	return HttpResponse(json.dumps( result ), "application/json")





@csrf_exempt
def downloadImage(request):
	uniqueid = request.POST.get('uniqueid', None)
	try:
		server = Server.objects.get(server_uniqueid=uniqueid)
		instance = server.serverinstance

		image = instance.osimage
		filepath = os.path.join(settings.MEDIA_ROOT, 'machines_images', image.osimage_path)
		mime = MimeTypes()
		mimetype = mime.guess_type(filepath)
		filesize = os.path.getsize(filepath)

		wrapper = FileWrapper(file(filepath, "rb"))
		response = HttpResponse(wrapper, content_type=mimetype)
		response['Content-Length'] = filesize
		return response
	except Server.DoesNotExist:
		pass
	HttpResponse('Nothing')


@csrf_exempt
def uploadImage(request):
	data=request.POST
	uniqueid = data.get('uniqueid', None)
	try:
		server   = Server.objects.get(server_uniqueid=uniqueid)
		instance = server.serverinstance
		
		if instance:
			#Get the install OS command using the reference in the pause command
			user = instance.startuser

			print "instance.startuser", instance.startuser

			
			if 'file' in request.FILES:
				filecontent = request.FILES['file']
				filename = data.get('filename', None)
				print "filecontent", filecontent, 'filename', request.FILES
				filepath = os.path.join( settings.MEDIA_ROOT, 'uploads', user.username, str(server)+'.vdi' )
				fd = open( filepath, 'wb')
				fd.write(filecontent.read())
				fd.close()
	except Server.DoesNotExist:
		pass
		print "Error"

	return HttpResponse('Nothing')