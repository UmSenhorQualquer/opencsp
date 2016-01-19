import simplejson, os, shlex
from django.db.models import Q
from django.template import RequestContext
from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin
from opencsp.models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.shortcuts import redirect
from opencsp.plugins.OpenCSPPlugin import OpenCSPPlugin, LayoutPositions, StringArgType, IntArgType
from django.conf import settings

class MyServers(OpenCSPPlugin):

	_icon = 'tasks'
	_menuOrder = 2
	groups = ['Administrator', 'superuser']
	

	static_files = ['servers.js']

	@staticmethod
	def MyServers(request):
		return render_to_response(
			os.path.join('opencsp', 'plugins', 'MyServers', 'myservers.html'),
			{}, context_instance=RequestContext(request))
		
	MyServers_argstype = []
	MyServers_position = LayoutPositions.TOP
	MyServers_label = 'Servers'





	@staticmethod
	def BrowseServers(request):
		servers = Server.objects.exclude(server_active=False)
		servers = servers.filter( Q(cluster__users=request.user) | Q(cluster__users=None) )
		servers = servers.filter(satelliteserver=None)
		servers = servers.filter(parent=None).order_by('server_name').distinct()

		#Implement the filter
		querystring = request.REQUEST.get('q', '')
		for q in shlex.split(querystring):
			servers  = servers.filter( (Q(server_name=q) | Q(server_host=q) | Q(osimage__osimage_name=q) | Q(reservedto__username=q)) )
			
		#Implement the sorting
		sortby = request.REQUEST.get('s', '')
		sorbylist = []
		for col in sortby.split(','):
			if col=='0': 	sorbylist.append('server_name')
			elif col=='-0': sorbylist.append('-server_name')

			if col=='5': 	sorbylist.append('server_host')
			elif col=='-5': sorbylist.append('-server_host')

		if len(sorbylist)>0: servers = servers.order_by( *sorbylist )

		totaljobs = servers.count()
		rowslimit = int(request.REQUEST.get('n', 30))
		
		rows = []
		for server in servers:
			small_thumb = '/static/power_on.png' if server.is_alive else '/static/power_off.png'
						
			properties, host = '', server.server_host
			if hasattr( server,'virtualserver'):
				properties = '<a title="Properties" href="javascript:serverProperty(%d);" ><i class="glyphicon glyphicon-wrench"></i></a>' % server.pk
				if server.reservedto==request.user: host=server.server_host

			s = {
				'small_thumb': small_thumb,
				'id': server.pk,
				'values': [
						str(server), 
						host,
						'Virtual' if hasattr(server, 'virtualserver') else '',
						server.state, 
						str(server.osimage) if server.osimage else '',
						str(server.reservedto) if server.reservedto else '',
						properties
					] 
				}
			rows.append(s)
		if totaljobs>len(rows): rows.append('more') 
		data = simplejson.dumps( rows )
		return HttpResponse(data, "application/json")
	BrowseServers_argstype = []
	BrowseServers_position = LayoutPositions.JSON





	@staticmethod
	def serverProperties(request, server_id):
		server = Server.objects.get(pk=server_id)
		return render_to_response(
			os.path.join('opencsp', 'plugins', 'MyServers', 'serverProperties.html'),
			{ 'server': server }, 
			context_instance=RequestContext(request))

	@staticmethod
	@csrf_exempt
	def updateServerProperties(request, server_id):
		server = Server.objects.get(pk=server_id)
		ram = request.POST.get('ram', None)
		cores = request.POST.get('cores', None)
		cap = request.POST.get('cap', None)
		name = request.POST.get('name', None)
		server.virtualserver.updateProperties( name, ram, cores, cap )

		data = simplejson.dumps( {'result': 'OK'} )
		return HttpResponse(data, "application/json")


	@staticmethod
	@csrf_exempt
	def reserveServers(request):
		servers_ids = request.POST.get('servers', None)
		if len(servers_ids)==0:	ids = []
		else: ids = servers_ids.split(',')
			
		servers = Server.objects.exclude(virtualserver=None).filter(pk__in=ids)
		images = OSImage.objects.all()

		return render_to_response(
			os.path.join('opencsp', 'plugins', 'MyServers', 'reserveServers.html'),
			{'servers':servers, 'images':images},
			context_instance=RequestContext(request) )

	@staticmethod
	@csrf_exempt
	def startServers(request):
		servers_ids = request.POST.get('servers', None)
		if len(servers_ids)==0:	ids = []
		else: ids = servers_ids.split(',')
		
		data = simplejson.dumps( {'result': 'OK'} )	
		servers = Server.objects.filter(pk__in=ids)

		for server in servers: 
			try:
				server.turnon()
			except:
				data = simplejson.dumps( {'result': 'Error'} )
		return HttpResponse(data, "application/json")

	@staticmethod
	@csrf_exempt
	def saveReserveServers(request):
		servers_ids = request.POST.get('servers', None)
		if len(servers_ids)==0:	ids = []
		else: ids = servers_ids.split(',')
		
		servers = Server.objects.filter(pk__in=ids)
		osimage = OSImage.objects.get(pk=request.POST.get('osimage', None))
		for server in servers:
			server.deployInstance(osimage, request.user)
			
		data = simplejson.dumps( {'result': 'OK'} )
		return HttpResponse(data, "application/json")

	@staticmethod
	@csrf_exempt
	def saveReleaseServers(request):
		servers_ids = request.POST.get('servers', None)
		if len(servers_ids)==0:	ids = []
		else: ids = servers_ids.split(',')

		servers = Server.objects.filter(pk__in=ids).distinct()
		for server in servers: 
			Task.schedule_server_shutdown(server);
			server.stop(request.user)
			
		data = simplejson.dumps( {'result': 'OK'} )
		return HttpResponse(data, "application/json")

	@staticmethod
	@csrf_exempt
	def savePauseServers(request):
		servers_ids = request.POST.get('servers', None)
		if len(servers_ids)==0:	ids = []
		else: ids = servers_ids.split(',')
		
		servers = Server.objects.filter(pk__in=ids)
		for server in servers: server.pause(request.user)
			
		data = simplejson.dumps( {'result': 'OK'} )
		return HttpResponse(data, "application/json")


	@staticmethod
	def InstallCluster(request, cluster_id):
		os.system("cd {0}; fab sync_cluster_code:{1}".format(settings.BASE_DIR,cluster_id) )
		return redirect( '/admin/opencsp/cluster/{0}/'.format(cluster_id) )
	InstallCluster_argstype = [IntArgType]
	

	@staticmethod
	def synchronize_server(request, server_id):
		server = Server.objects.get(pk=server_id)
		out = server.reset()
		messages.success(request, 'Server was synchronized with success.')
		return redirect( '/admin/opencsp/server/{0}/'.format(server_id) )
	synchronize_server_argstype = [IntArgType]


	@staticmethod
	def check_new_jobs(request, server_id):
		server = Server.objects.get(pk=server_id)
		out = server.check_new_jobs()
		messages.success(request, 'New jobs checked with success.')
		return redirect( '/admin/opencsp/server/{0}/'.format(server_id) )
	synchronize_server_argstype = [IntArgType]