from django.views.decorators.csrf import csrf_exempt
from opencsp.models import AlgorithmSubject, Algorithm, Job
from opencsp.plugins.JobsList.JobsList import JobsList
from django.http import HttpResponse
from django.conf import settings
import simplejson

def applications_list(request): 
	res = []
	for algo in Algorithm.objects.all():
		a = {
			'algorithm_id':algo.algorithm_id, 
			'algorithm_name':algo.algorithm_name,
			'algorithm_class':algo.algorithm_class,
			'algorithm_desc':algo.algorithm_desc,
			'algorithmsubjects':';'.join([str(x) for x in algo.algorithmsubjects.all()]),
		}
		res.append(a)
	data = simplejson.dumps( res )
	return HttpResponse(data, "application/json")

def application_params(request, application): 
	model_path = settings.PYFORMS_APPLICATIONS.moduleClassPath(application)
	model = settings.PYFORMS_APPLICATIONS.createInstance(application)
	data = simplejson.dumps( model.serializeForm() )
	return HttpResponse(data, "application/json")

@csrf_exempt
def jobs_list(request):
	res = []
	jobs 		= Job.objects.all()
	
	if request.POST.get('username', None): 		jobs = jobs.filter(user__username=request.POST.get('username'))
	if request.POST.get('application', None): 	jobs = jobs.filter(job_application=request.POST.get('application'))
	if request.POST.get('state', None): 		jobs = jobs.filter(job_state=request.POST.get('state'))
	if request.POST.get('created', None):
		value = request.POST.get('created').split(';')
		if len(value)>1:
			jobs = jobs.filter(job_created__range=tuple(value))
		else:
			jobs = jobs.filter(job_created=value[0])
	if request.POST.get('started', None):
		value = request.POST.get('started').split(';')
		if len(value)>1:
			jobs = jobs.filter(job_started__range=tuple(value))
		else:
			jobs = jobs.filter(job_started=value[0])
	if request.POST.get('ended', None):
		value = request.POST.get('ended').split(';')
		if len(value)>1:
			jobs = jobs.filter(job_ended__range=tuple(value))
		else:
			jobs = jobs.filter(job_ended=value[0])

	rowslimit = int(request.POST.get('limit', 30))
	jobs = jobs[:rowslimit]

	for job in jobs:
		j = job.dictionary
		res.append(j)

	data = simplejson.dumps( res )
	return HttpResponse(data, "application/json")

def job_output(request, job_id): 
	return HttpResponse( Job.objects.get(pk=job_id).output )

def job_get(request, job_id):
	job = Job.objects.get(pk=job_id) 
	data = simplejson.dumps( job.dictionary )
	return HttpResponse(data, "application/json")

def job_kill(request, job_id):
	job = Job.objects.get(pk=job_id)
	if job.job_state==None: 
		job.end()
		job.delete()
	else: job.kill()
	data = simplejson.dumps( job.dictionary )
	return HttpResponse(data, "application/json")

def storate_url(request): 
	data = simplejson.dumps( settings.OWNCLOUD_LINK )
	return HttpResponse(data, "application/json")
