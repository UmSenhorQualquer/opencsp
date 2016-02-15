from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin, LayoutPositions, StringArgType, IntArgType
from django.views.decorators.csrf import csrf_exempt
from opencsp.models import AlgorithmSubject, Algorithm
from django.template import RequestContext
from django.shortcuts import render_to_response
import os, csv
import simplejson, os
from opencsp.models import *
from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt

def detectDelimiter(csvFile):
	with open(csvFile, 'r',encoding='utf8') as myCsvfile:
		header=myCsvfile.readline()
		if header.find(";")!=-1: return ";"
		if header.find(",")!=-1: return ","
	#default delimiter (MS Office export)
	return ";"

class AppList(OpenCSPPlugin):

	_icon = 'th-large'
	_menuOrder = 0


	@staticmethod
	def AppList(request): 
		subjects = AlgorithmSubject.objects.all()
		params ={ 'subjects':subjects }
		return render_to_response(
			os.path.join('opencsp', 'plugins', 'AppList', 'applications_list.html'),
			params, context_instance=RequestContext(request) )
	AppList_argstype = []
	AppList_position = LayoutPositions.TOP
	AppList_label = 'Applications'

	@staticmethod
	def LoadJob(request, application, job):
		return AppList.__load(request, application, job)
	LoadJob_argstype = [StringArgType, IntArgType]
	LoadJob_position = LayoutPositions.TOP
	LoadJob_label = 'Application parameters'
	

	@staticmethod
	def Load(request, application):
		return AppList.__load(request, application)
	Load_argstype = [StringArgType]
	Load_position = LayoutPositions.TOP
	Load_label = 'Application parameters'
	Load_breadcrumbs = []


	@staticmethod
	def __load(request, application, job_id=None):
		#try:
		model_path = settings.PYFORMS_APPLICATIONS.moduleClassPath(application)
		model = settings.PYFORMS_APPLICATIONS.createInstance(application)
		model.httpRequest = request
		canqueue = False
		try: 
			getattr(model, 'execute') 
			canqueue=True
		except: pass

		job_params = None
		

		if job_id!=None:
			job = Job.objects.get(pk=job_id)
			job_params = eval(job.job_parameters)
			model.loadSerializedForm(job_params)
		
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
		#except Exception as e:
		#	return HttpResponseServerError(str(e))
		
	
	@staticmethod
	@csrf_exempt
	def runbatchfile(request):
		csvfile = request.FILES['batchfilename']
		dialect = csv.Sniffer().sniff(csvfile.read(1024), delimiters=";,")
		csvfile.seek(0)

		spamreader = csv.reader(csvfile, dialect)
		model, application, rowdesc = None, None, None
		for row in spamreader:
			if len(row)==0: 
				model   = None
				application = None
				rowdesc = None
			elif row[0]=='APPLICATION':
				model   = None
				application = None
				rowdesc = None
				application = row[1]
				model       = settings.PYFORMS_APPLICATIONS.createInstance(application)
				model.httpRequest = request
			elif model!=None and rowdesc==None:
				rowdesc = [ model.findParameterByLabel(col) for col in row]
			elif model!=None and rowdesc!=None:
				params = {}
				for i, col in enumerate(row[:-1]):
					params[rowdesc[i]]=col
				params['userpath'] = os.path.join( settings.MEDIA_ROOT, 'uploads', str(request.user) )
				
				algo = Algorithm.objects.get(algorithm_class=application)
				try:
					server = Server.objects.get(server_name=row[-1])
				except Server.DoesNotExist:
					server = Server.PickServer(algo, request.user, None)
	
				job = Job( job_application=application, job_parameters=params, server=server, user=request.user )
				job.save()

		if server.satelliteserver==None and job!=None: server.check_new_jobs()
		
		params = {}
		return HttpResponse('Ok')


	@staticmethod
	def downloadbatchfile(request, application):
		model = settings.PYFORMS_APPLICATIONS.createInstance(application)
		model.httpRequest = request
		
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="%s_batchfile.csv"' % application

		writer = csv.writer(response)
		titles = [a._label for a in model.formControls.values()]
		titles.append('Server')
		writer.writerow(['APPLICATION', application])
		writer.writerow(titles)

		return response
	

	@staticmethod
	def batchfile(request, application):
		params = { 'application': application}
		return render_to_response(
			os.path.join('opencsp', 'plugins', 'AppList', 'batchfile.html'),
			params, context_instance=RequestContext(request))


		