from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin, LayoutPositions, StringArgType, IntArgType
from django.views.decorators.csrf import csrf_exempt
from opencsp.models import AlgorithmSubject
from django.template import RequestContext
from django.shortcuts import render_to_response
import opencsp.ApplicationsSettings as appSettings
import os, simplejson
from django.conf import settings
from django.http import HttpResponse
from opencsp.models import *

class MyArea(OpenCSPPlugin):

	_icon = 'briefcase'
	_menuOrder = 3

	static_files = ['user-area.css']
	
	@staticmethod
	def MyArea(request): 
		data = { 'OWNCLOUD_LINK': settings.OWNCLOUD_LINK }
		return render_to_response(os.path.join('opencsp', 'plugins', 'MyArea', 'myarea.html'), data, context_instance=RequestContext(request) )
	MyArea_argstype = []
	MyArea_position = LayoutPositions.BOTTOM
	MyArea_label = 'My files'
	MyArea_js = 'LoadMyArea();'

	
	