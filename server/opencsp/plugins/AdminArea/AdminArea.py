from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin, LayoutPositions, StringArgType, IntArgType
from django.views.decorators.csrf import csrf_exempt
from opencsp.models import AlgorithmSubject
from django.template import RequestContext
from django.shortcuts import render_to_response
import os, csv
from opencsp.models import *
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required, user_passes_test

class AdminArea(OpenCSPPlugin):

	_icon = 'dashboard'
	top_view_url = '/admin/'
	groups = ['Administrator', 'superuser']

	@staticmethod
	def AdminArea(request): return redirect('/admin/')
	AdminArea_argstype 	= []
	AdminArea_position 	= LayoutPositions.NEW_WINDOW
	AdminArea_label 	= 'Admin area'
	AdminArea_groups 	= ['Administrator', 'superuser']
	#AdminArea_js = 'LoadAdminArea();'

