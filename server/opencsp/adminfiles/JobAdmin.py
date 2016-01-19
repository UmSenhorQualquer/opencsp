from django.contrib import admin

def resetjobs(modeladmin, request, queryset):
	for job in queryset: job.reset()
		
resetjobs.short_description = "Reset jobs"

class JobAdmin(admin.ModelAdmin):
	actions = [resetjobs]
	list_display = ('job_application','server','user','job_created', 'job_started', 'job_ended', 'running_time')
	list_filter = ['job_application', 'server','user','job_created', 'job_started', 'job_ended']
	search_fields = ['job_application',]
	readonly_fields = ['job_uniqueid', 'job_application', 'job_state',
		'job_created', 'job_started', 'job_ended', 'job_startUpload', 
		'job_startDownload','job_inputSize', 'job_uploadedBytes',
		'job_startDownload', 'job_endDownload', 'job_outputSize', 'job_downloadedBytes',
		'resetButton','gotoServer']
	
	

	fieldsets = (
		(None, {
			'fields': [ 'job_application', 
			('gotoServer','resetButton'),
			('user', 'server' ), ]
		}),
		('Parameters', {
			'fields': ('job_parameters','job_outparameters')
		}),
		('Running info', {
			'fields': ['job_created', ('job_started', 'job_ended')]
		}),
		('Upload', {
			'fields': [('job_startUpload', 'job_endUpload'), ('job_inputSize', 'job_uploadedBytes'),]
		}),
		('Download', {
			'fields': [('job_startDownload', 'job_endDownload'), ('job_outputSize', 'job_downloadedBytes'),]
		}),
		('Extra info', {
			'fields': ('job_uniqueid','job_state', )
		}),
	)


	def resetButton(self, job):
		if job.job_started==None:
			return """<a class='btn btn-success'  href='/plugins/jobslist/run_job/{0}/' ><i class="icon-play-circle icon-white"></i> Run</a>""".format(job.job_id)
		else:
			return """<a class='btn btn-danger'  href='/plugins/jobslist/reset_job/{0}/' ><i class="icon-retweet icon-white"></i> Reset</a>""".format(job.job_id)
	resetButton.short_description = "Reset/Run job"
	resetButton.allow_tags = True

	def gotoServer(self, job):
		return """<a class='btn btn-primary'  href='/admin/opencsp/server/{0}/' ><i class="icon-tasks icon-white"></i> Server</a>""".format(job.server.server_id)
	gotoServer.short_description = "Got to server"
	gotoServer.allow_tags = True