from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin
from django.contrib import messages
from opencsp.models  import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import django.conf as settings
from django.http import HttpResponse
import simplejson, os
from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin, LayoutPositions, StringArgType, IntArgType
from django.db.models import Q
import shlex
from django.shortcuts import redirect
from django.utils import timezone

class JobsList(OpenCSPPlugin):

	_icon = 'cog'
	_menuOrder = 1

	static_files = ['jobs.js', 'jobs.css']

	@staticmethod
	def filter_jobs(request):
		jobs  = Job.objects.all()

		#Implement the filter
		querystring = request.GET.get('q', '')
		for q in shlex.split(querystring):
			jobs  = jobs.filter( (Q(job_application=q) | Q(server__server_name=q) | Q(user__username=q)) )
		
		#Implement the sorting
		sortby = request.GET.get('s', '')
		sorbylist = []
		for col in sortby.split(','):
			if col=='0': 	sorbylist.append('job_application')
			elif col=='-0': sorbylist.append('-job_application')

			if col=='1': 	sorbylist.append('user__username')
			elif col=='-1': sorbylist.append('-user__username')

			if col=='2': 	sorbylist.append('server__server_name')
			elif col=='-2': sorbylist.append('-server__server_name')

			if col=='3': 	sorbylist.append('job_created')
			elif col=='-3': sorbylist.append('-job_created')

			if col=='4': 	sorbylist.append('job_started')
			elif col=='-4': sorbylist.append('-job_started')

			if col=='5': 	sorbylist.append('job_ended')
			elif col=='-5': sorbylist.append('-job_ended')
		if len(sorbylist)>0: jobs = jobs.order_by( *sorbylist )
		else: jobs = jobs.order_by( '-job_created' )

		return jobs


	@staticmethod
	def list_jobs(request):
		jobs = JobsList.filter_jobs(request)
		totaljobs = jobs.count()
		rowslimit = int(request.GET.get('n', 30))
		jobs = jobs[:rowslimit]
		

		rows = []

		for job in jobs:	

			stop_link = ""
			if job.job_ended==None:
				if job.job_state=='loading':
					stop_link = """<img src='/static/wait.gif' />"""
				elif (job.user==request.user or request.user.is_superuser) and job.server.satelliteserver==None :
					stop_link = """<a href='javascript:stopJob(%d);' ><i class="glyphicon glyphicon-remove-sign"></a>""" % job.pk
				elif job.job_state==None:
					stop_link =''
				else: 
					stop_link = job.job_state


			info_link = ''
			if job.job_started!=None and job.job_ended==None and job.job_state=='':
				info_link = """<a href='javascript:jobFiles(%d);' ><i class="glyphicon glyphicon-info-sign"></a>""" % job.pk

			values = {
				'values': [
					"<small>%s</small>" % str(job),
					"<small>%s</small>" % job.user.username,
					"<small>%s</small>" % job.server,
					"<small>%s</small>" % job.job_created.strftime("%Y-%m-%d %H:%M"), 
					"", 
					"",
					"",
					"",
					"""<a href='#view-applist-loadjob|%s+%d' onclick="runApplistLoadjob('%s', %d);" ><i class="glyphicon glyphicon-open"></a>""" % (job.job_application, job.pk, job.job_application, job.pk),
					info_link,
					"""<a href='javascript:jobOutput(%d);' ><i class="glyphicon glyphicon-file"></i></a>""" % job.pk,
					stop_link
				],
				'big_thumb': '/static/work.png'
			}
			if job.job_started: 
				values['values'][4] = "<small>%s</small>" % job.job_started.strftime("%Y-%m-%d %H:%M")
			if job.job_ended: 	
				values['values'][5] = "<small>%s</small>" % job.job_ended.strftime("%Y-%m-%d %H:%M")
				values['values'][6] = "<small>%s</small>" % str(job.job_ended-job.job_created)
				values['values'][7] = "<small>%s</small>" % job.running_time()
			elif job.job_started:
				values['values'][7] = "<small>%s</small>" % str(timezone.now()-job.job_started).split('.')[0]

			rows.append( values )

		if totaljobs>len(rows): rows.append('more') 
		return rows



	@staticmethod
	def kill_job(request, job_id):
		job = Job.objects.get(pk=job_id)
		if job.job_state==None: 
			job.end()
			job.delete()
		else: job.kill()
		return HttpResponse('')
	kill_job_argstype = [IntArgType]

	@staticmethod
	def check_output_files(request, job_id):
		job = Job.objects.get(pk=job_id)	
		if job.job_started!=None and job.job_ended==None:
			output = "<pre>%s</pre>" % str(job.server.server_jobinfo(job))
		elif job.job_started==None:
			output = "The job didn't started yet"
		else:
			output = ""
		return HttpResponse(output)
	check_output_files_argstype = [IntArgType]
	

	@staticmethod
	def reset_job(request, job_id):
		job = Job.objects.get(pk=job_id)
		out = job.reset()
		messages.success(request, 'Job was reseted with success.')
		return redirect( '/admin/opencsp/job/{0}/'.format(job_id) )
	reset_job_argstype = [IntArgType]

	@staticmethod
	def run_job(request, job_id):
		job = Job.objects.get(pk=job_id)
		if not job.server.has_job(): 
			job.run()
			messages.success(request, 'Job submitted with success.')
		else:
			messages.error(request, 'Job not submitted. The server is busy.')
		return redirect( '/admin/opencsp/job/{0}/'.format(job_id) )
	run_job_argstype = [IntArgType]

	@staticmethod
	def check_job_output(request, job_id):
		job = Job.objects.get(pk=job_id)
		out = job.output
		return HttpResponse( "<pre>%s</pre>" % out )
	check_job_output_argstype = [IntArgType]

	@staticmethod
	def check_job_parameters(request, job_id=1):
		job = Job.objects.get(pk=job_id)
		module_class = settings.PYFORMS_APPLICATIONS.createInstance(job.job_application)
		model.httpRequest = request
		
		parameters = eval(job.job_parameters)
		model = module_class()
		model.loadSerializedForm( parameters )		
		return HttpResponse( parameters )
	check_job_parameters_argstype = [IntArgType]
	Load_label = 'Application parameters'
	

	@staticmethod
	def BrowseJobs(request):
		data = simplejson.dumps( JobsList.list_jobs(request) )
		return HttpResponse(data, "application/json")
	BrowseJobs_argstype = []
	BrowseJobs_position = LayoutPositions.JSON

	@staticmethod
	def JobsList(request):
		return render_to_response(
			os.path.join('opencsp', 'plugins', 'JobsList', 'alljobs.html'),
			{}, context_instance=RequestContext(request))
	JobsList_argstype = []
	JobsList_position = LayoutPositions.TOP
	JobsList_label = 'Jobs'

