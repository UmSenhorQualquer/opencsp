from Job import Job


class Application(object):

	def __init__(self, api):
		self._api = api

	def load(self, values):
		self.name 			= values['algorithm_name']
		self.description 	= values['algorithm_desc']
		self.appclass 		= values['algorithm_class']
		self.subjects 		= values['algorithmsubjects']
		self.pk 			= values['algorithm_id']
		
	def __getParameters(self):
		url = "{0}/api/application/{1}/params/".format(self._api._serverUrl, self.appclass)
		r = self._api.session.get(url)  
		return r.json()

	def createJobInstance(self):
		job = Job(self._api)
		job.application = self
		job.parameters = self.__getParameters()
		return job

	def __unicode__(self): 	return "App:{0}:{1}".format(self.appclass, self.pk)
	def __str__(self): 		return self.__unicode__()
	def __repr__(self): 	return self.__unicode__()
