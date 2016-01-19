import os, sys; sys.path.append('../'); os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from django.conf import settings
from opencsp.models import Job



class OpenCSPManager(object):


	def __init__(self, user):
		self._user = user

	##################################################################################
	##################################################################################
	##################################################################################

	def submitJob(self, application, parameters):
		pass

	def stopJob(self, id):
		pass


	##################################################################################
	##################################################################################
	##################################################################################

	@property
	def jobs(self): pass

	@property
	def servers(self): pass

	@property
	def clusters(self): pass

	@property
	def applications(self): pass