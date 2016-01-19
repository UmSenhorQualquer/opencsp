from django.contrib import admin

class ServerAdmin(admin.ModelAdmin):
	list_display = ( 'server_name','server_host', 'parent','server_isalive')
	search_fields = ['server_name',]
	readonly_fields = ['server_uniqueid','server_isalive','server_lastcontact',
		'gotoJob','syncServer','checkJobs']

	fieldsets = (
		(None, {
			'fields': [ ('server_active','gotoJob','syncServer','checkJobs'),
				'server_name',('server_isalive','server_lastcontact') ]
		}),
		('Network', {
			'fields': ('server_host','server_user','server_pass', 'server_certificate','server_mac')
		}),
		('Configurations', {
			'fields': ['server_turnoff','server_remotedir', 'server_envmanager',]
		}),
		('Other configurations', {
			'fields': ['parent','satelliteserver']
		}),
	)

	def gotoJob(self, server):
		job_id=server.db_current_job_id
		if job_id==None: return "No job running"
		return """<a class='btn btn-primary'  href='/admin/opencsp/job/{0}/' ><i class="icon-tasks icon-white"></i> Got to</a>""".format(server.current_job_id)
	gotoJob.short_description = "Current job"
	gotoJob.allow_tags = True

	def syncServer(self, server):
		return """<a class='btn btn-warning'  href='/plugins/myservers/synchronize_server/{0}/' ><i class="icon-refresh icon-white"></i> Synchronize</a>""".format(server.server_id)
	syncServer.short_description = "Sync server"
	syncServer.allow_tags = True

	def checkJobs(self, server):
		return """<a class='btn btn-primary'  href='/plugins/myservers/check_new_jobs/{0}/' ><i class="icon-tasks icon-white"></i> Check</a>""".format(server.server_id)
	checkJobs.short_description = "Check for pedding jobs"
	checkJobs.allow_tags = True