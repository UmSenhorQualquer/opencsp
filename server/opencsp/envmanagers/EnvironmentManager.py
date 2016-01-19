import inspect, os
from opencsp.tools import fromImport

class EnvironmentManager:

	def __init__(self):
		self._storage = {}

		
	def __importClass(self, moduleclassname):
		if moduleclassname not in self._storage:
			moduleclass = fromImport('opencsp.envmanagers.{0}.{0}'.format(moduleclassname), moduleclassname)
			moduleobj 	= moduleclass()
			self._storage[moduleclassname] = moduleobj
		else:
			moduleobj = self._storage[moduleclassname]
		return moduleobj

	def get(self, moduleclassname, application=None):
		if moduleclassname==None or moduleclassname=='': moduleclassname = 'DefaultEnvManager'

		if application!=None:
			modulename = str(moduleclassname)+"App"+str(application)
			if os.path.exists( os.path.join('opencsp','envmanagers',str(moduleclassname),modulename+'.py') ):
				return self.__importClass(modulename)
				
		modulename = str(moduleclassname)
		if os.path.exists( os.path.join('opencsp','envmanagers',str(moduleclassname),modulename+'.py') ):
			return self.__importClass(modulename)

		return self.__importClass('DefaultEnvManager')

	@property
	def choices(self):
		res = []
		for key, item in self._storage.items():
			res.append( (key, key) )
		return tuple(res)
	
AVAILABLE_ENVIROMENTS = EnvironmentManager()