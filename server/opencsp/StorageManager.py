from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
import inspect, os

class StorageManager:

	def __init__(self):
		self._classes = {}
		self._storage = {}	

	def __importClass(self, moduleclassname):
		if moduleclassname not in self._classes:
			modulename = '.'.join( ['opencsp','storagemanagers',moduleclassname, moduleclassname] )
			moduleclass = __import__(modulename, fromlist=[moduleclassname])
			moduleclass =  getattr(moduleclass, moduleclassname)
			self._classes[moduleclassname] = moduleclass
		else:
			moduleclass = self._classes[moduleclassname]
		return moduleclass

	def get(self, user):
		if user.username not in self._storage:
			from opencsp.models import UserSettings
			try:
				user_settings = UserSettings.objects.get(user=user)
				storage_manager = user_settings.user_storage
			except ObjectDoesNotExist:
				storage_manager = settings.OPENCSP_DEFAULT_STORAGE_MANAGER

			classdef = self.__importClass(storage_manager)
			self._storage[user.username] = classdef(user)
		
		return self._storage[user.username]
