from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlVisVis
from pyforms.Controls import ControlText
from pyforms.Controls import ControlDate
from pyforms.Controls import ControlCombo
from opencsp.models   import Job, Algorithm, Server
from pyforms 		  import BaseWidget
from django.db.models import Sum, fields

import uuid, datetime

class AdminStatsApp(BaseWidget):

	
	def __init__(self):
		super(AdminStatsApp,self).__init__('Admin stats')
		
		self._totalExec_begin = ControlDate('Starting date', '2014-10-10')
		self._totalExec_end   = ControlDate('Ending date', '2015-10-10')
		self._totalExec_btn   = ControlButton('Refresh')
		
		self._totalExec_graph = ControlVisVis('Total execution time')
		
		self._apps_list 	  = ControlCombo('Filter by application')
		self._totalExecApp_graph = ControlVisVis('Total execution time per application')

		self._servers_list 	  = ControlCombo('Filter by server')
		self._totalExecServer_graph = ControlVisVis('Total execution time per server')


		
		self._formset = [
			('_totalExec_begin','_totalExec_end','_totalExec_btn'),
			'h3:Total execution time',
			'_totalExec_graph',
			'h3:Total execution time per application',
			'_apps_list',
			'_totalExecApp_graph',
			'h3:Total execution time per server',
			'_servers_list',
			'_totalExecServer_graph'
		]

		self._totalExec_btn.value = self.__total_exec_stats
		
		self._apps_list.addItem('--- All ---', '')
		for application in Algorithm.objects.all():
			self._apps_list.addItem(str(application.algorithm_name), str(application.algorithm_class))
		
		self._servers_list.addItem('--- All ---', '')
		for server in Server.objects.all().order_by('server_name'):
			self._servers_list.addItem(str(server.server_name), str(server.pk))
		

	
	def initForm(self):
		self.__total_exec_stats()
		return super(AdminStatsApp,self).initForm()


	def __calc_total_exec_stats(self, begin, end, app=None, server=None):
		values = Job.objects.filter(job_created__range=(begin, end))
		if app is not None: values = values.filter(job_application=app)
		if server is not None: values = values.filter(server=server)
		values = values.extra(select={'created': "DATE(job_created)"})
		values = values.values('created').annotate(job_duration=Sum( F('job_ended')-F('job_created'),output_field=fields.DurationField() ))
		values = values.order_by('created')

		res = []
		for row in values:
			duration = row['job_duration'].total_seconds() if row['job_duration']!=None else 0
			if duration>0: res.append( [row['created'], duration] )
		return res

	def __total_exec_stats(self):
		begin = datetime.datetime.strptime(self._totalExec_begin.value, "%Y-%m-%d").date()
		end   = datetime.datetime.strptime(self._totalExec_end.value,   "%Y-%m-%d").date()
		
		total_exec = self.__calc_total_exec_stats(begin, end)
		self._totalExec_graph.value = [total_exec]

		series = []
		legend = []
		apps = Algorithm.objects.all()
		if self._apps_list.value!='': apps = apps.filter(algorithm_class=self._apps_list.value)
		for application in apps:
			res = self.__calc_total_exec_stats(begin, end, app=application.algorithm_class)
			if len(res)>0: 
				series.append(res)
				legend.append(str(application.algorithm_name))
				

		self._totalExecApp_graph.legend = legend
		self._totalExecApp_graph.value  = series


		series = []
		legend = []
		servers = Server.objects.all()
		if self._servers_list.value!='': servers = servers.filter(pk=self._servers_list.value)
		for server in servers:
			res = self.__calc_total_exec_stats(begin, end, server=server)
			if len(res)>0: 
				series.append(res)
				legend.append(str(server.server_name))
				

		self._totalExecServer_graph.legend = legend
		self._totalExecServer_graph.value  = series

		