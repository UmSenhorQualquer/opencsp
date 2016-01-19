from models 								import *
from django.db.models 						import Q
from django.conf 							import settings
from multiprocessing 						import Process
from django.http 							import HttpResponse, HttpResponseServerError
from django.contrib.auth.forms 				import *
from django.template 						import RequestContext
from django.http 							import HttpResponseRedirect
from django.core.urlresolvers 				import reverse
from django.shortcuts 						import render_to_response
from django.utils.encoding 					import smart_unicode
from django.contrib.auth 					import REDIRECT_FIELD_NAME
from django.views.decorators.csrf 			import csrf_exempt
from django.views.decorators.cache 			import never_cache
from django.contrib.auth.decorators 		import login_required
from jfu.http 								import upload_receive, UploadResponse, JFUResponse
from opencsp.plugins.OpenCSPPluginsManager 	import OPENCSP_PLUGINS


import simplejson, json, glob, inspect, mimetypes, os



@login_required
def index(request):
	context = {'user': request.user}
	context.update({ 'plugins':OPENCSP_PLUGINS.menu(request.user) })
	return render_to_response('authenticated_base.html', context )



def commands_js(request):
	plugins = OPENCSP_PLUGINS.plugins
	return render_to_response(
		os.path.join('opencsp', 'commands.js',),
		{'plugins': plugins}, context_instance=RequestContext(request))




@csrf_exempt
def browseappservers(request, application):
	algo = Algorithm.objects.get(algorithm_class=application)
	res = [ (server.pk, str(server) ) for server in algo.servers(request.user) ]
	data = simplejson.dumps( res )
	return HttpResponse(data, "application/json")




@csrf_exempt
def sendjob2queue(request, application, server_id):
	try:
		parms = json.loads(request.body)
		
		algo 	= Algorithm.objects.get(algorithm_class=application)
		try:
			print algo, server_id, request.user
			server 	= Server.PickServer(algo, request.user, server_id)
		except IndexError as e:
			return HttpResponseServerError('Error when choosing the server.')
				
		job = Job(job_application=application, job_parameters=parms, server=server, user=request.user )
		job.save()
		
		#If the server is local, it will launch the job.
		#Otherwise the job will wait until someone pull it.
		if server.satelliteserver==None and job!=None: server.check_new_jobs()
			
		data = simplejson.dumps({ 'result': 'OK', 'msg':'Job scheduled with success', 'job_id':job.pk })
		return HttpResponse(data, "application/json")
	except Exception as e:
		return HttpResponseServerError(str(e))


@csrf_exempt
def load_statemachine_image(request, application):
	image_file = os.path.join( settings.MEDIA_ROOT, 'statesmachines', '{0}.png'.format(application) )
	print image_file
	try:
		with open(image_file, "rb") as f:
			mmtype = mimetypes.guess_type(image_file)
			return HttpResponse(f.read(), content_type=mmtype[0])
	except IOError:
		response = HttpResponse("Error")
		return response


@csrf_exempt
def load_documentation_image(request, application, image):
	model_path = settings.PYFORMS_APPLICATIONS.moduleClassPath(application)
	model_directory, model_file = os.path.split(model_path)
	image_file = os.path.join( model_directory, 'docs', image )
	print image_file
	try:
		with open(image_file, "rb") as f:
			mmtype = mimetypes.guess_type(image_file)
			return HttpResponse(f.read(), content_type=mmtype[0])
	except IOError:
		response = HttpResponse("Error")
		return response



@csrf_exempt
def loadapplicationform(request, application):
	model_path = settings.PYFORMS_APPLICATIONS.moduleClassPath(application)
	model = settings.PYFORMS_APPLICATIONS.createInstance(application)
	model.httpRequest = request
	canqueue = False
	try: 
		getattr(model, 'execute') 
		canqueue=True
	except: pass

	job_params = None
	job_id = request.REQUEST.get('job', None)

	if job_id!=None:
		job = Job.objects.get(pk=job_id)
		job_params = eval(job.job_parameters)
		model.loadSerializedForm(job_params, False)
	
	params = { 'application': application, 'canqueue':  canqueue, 'appInstance': model}
	params.update( model.initForm() )

	model_directory, model_file = os.path.split(model_path)
	readme_file = os.path.join( model_directory, 'docs', 'readme.html' )
	
	if os.path.isfile(readme_file):
		readme_content = open(readme_file, 'r').read()
		readme_content = readme_content.replace('src="', 'src="/appdoc/%s/' % application)
		readme_content = readme_content.replace("src='", "src='/appdoc/%s/" % application)
		params.update( { 'readme': readme_content } )

	return render_to_response(
		os.path.join('opencsp', 'plugins', 'AppList', 'framework.html'),
		params, context_instance=RequestContext(request))

@never_cache
@csrf_exempt
def updateapplicationform(request, application):
	#try:
	module = settings.PYFORMS_APPLICATIONS.createInstance(application)
	module.httpRequest = request
	parms = json.loads(request.body)
	module.loadSerializedForm( parms )
	result = module.serializeForm()
	data = simplejson.dumps(result)
	return HttpResponse(data, "application/json")
	#except Exception as e:
	#	return HttpResponseServerError(str(e))


@csrf_exempt
def runapplication(request, application):
	module = settings.PYFORMS_APPLICATIONS.createInstance(application)
	model.httpRequest = request
	parameters = request.POST
	module.loadSerializedForm( parameters )
	results = module.update()
	return HttpResponse(results)



@csrf_exempt
def browseservers(request):
	servers = Server.objects.filter( Q(cluster__users=request.user) | Q(cluster__users=None) )
	servers = servers.filter(parent=None).order_by('server_name').distinct()
	res = []
	for server in servers:
		is_alive = server.is_alive
		status_link = ''
		if is_alive: 
			status_link = "<a href='javascript:serverStatus(%d);' ><img src='/static/info.png' /></a>""" % server.pk

		s = {
			'values': [
					server.server_name, 
					'Public' if server.is_public else 'Private', 
					'<img src="/static/power_on.png" />' if is_alive else '<img src="/static/power_off.png" />',
					status_link 
				] 
			}
		res.append(s)

	data = simplejson.dumps( res )
	return HttpResponse(data, "application/json")


@csrf_exempt
def server_info(request, server_id):
	server = Server.objects.get(pk=server_id)	
	output = str(server.server_info())
	return HttpResponse(output)

@login_required
def register_server(request, macaddress):
	server = Server()







from allauth.account.utils import perform_login
from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver

from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.utils import get_user_model
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings
import json


@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    email_address = sociallogin.account.extra_data['email']
    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id)))
