from django.http import HttpResponse
from django.forms import ModelForm
from pyforms.web.django import ApplicationsLoader

from django import forms
from opencsp.models import *
import simplejson, uuid, os
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin, LayoutPositions, StringArgType

from django.conf import settings



class MySettings(OpenCSPPlugin):

	_icon = 'cog'
	_app_loader = ApplicationsLoader(os.path.dirname(os.path.abspath(__file__)))
	
	@staticmethod
	def MySettings(request):
		app = MySettings._app_loader.createInstance('MySettingsApp')
		app.httpRequest = request
		
		params = { 'application': 'MySettingsApp', 'appInstance': app}
		params.update( app.initForm() )

		return render_to_response(
			os.path.join('opencsp', 'plugins', 'pyforms-template.html'),
			params, context_instance=RequestContext(request))

	MySettings_argstype = []
	MySettings_position = LayoutPositions.TOP
	MySettings_label = 'Settings'