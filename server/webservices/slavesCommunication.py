import json, os
from opencsp.models import Server
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

@csrf_exempt
def checknewjobs(request, server_id):
	server = Server.objects.get(pk=server_id)
	server.finnish_job()
	return HttpResponse(json.dumps( {'result': 'OK'} ), "application/json")
