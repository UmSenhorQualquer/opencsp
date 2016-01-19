from opencsp.models import *
from django.contrib import admin
from opencsp.adminfiles.JobAdmin import JobAdmin
from opencsp.adminfiles.ServerAdmin import ServerAdmin
from opencsp.adminfiles.ClusterAdmin import ClusterAdmin





class ServerInstanceAdmin(admin.ModelAdmin):
	list_display = ('server', 'job', 'serverinstance_created','startuser', 'serverinstance_started', 'serverinstance_startcommited', 'stopuser', 'serverinstance_ended', 'serverinstance_endcommited')


def update_version(modeladmin, request, queryset):
	for server in queryset:
		server.virtualserver_update = True
		server.save()
		
update_version.short_description = "Update version"

class VirtualServerAdmin(admin.ModelAdmin):
	actions = [update_version]

admin.site.register(AlgorithmSubject)
admin.site.register(UserSettings)
admin.site.register(Algorithm)
admin.site.register(VirtualServer,VirtualServerAdmin)
admin.site.register(ServerInstance,ServerInstanceAdmin)
admin.site.register(MasterServer)
admin.site.register(Server, ServerAdmin)
admin.site.register(SatelliteServer)
admin.site.register(Cluster, ClusterAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(OSImage)
admin.site.register(Task)