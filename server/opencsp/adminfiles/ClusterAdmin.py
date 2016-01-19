from django.contrib import admin

class ClusterAdmin(admin.ModelAdmin):
	filter_horizontal = ( 'users', 'servers', 'algorithms')
	readonly_fields = ('syncButton','cluster_uniqueid')
	list_display = ('cluster_name',)
	

	fieldsets = (
		(None, {
			'fields': [ 
				('cluster_name','syncButton')
			] 
		}),
		('Configuration', {
			'fields': [ 
				'algorithms', 'servers', 'users'
			] 
		}),
		('Other info', {
			'fields': [ 
				'satelliteserver','cluster_uniqueid',
			] 
		}),
	)
