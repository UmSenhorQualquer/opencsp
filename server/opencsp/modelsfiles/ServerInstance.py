from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class AbstractServerInstance(models.Model):
	serverinstance_id 				= models.AutoField(primary_key=True)
	serverinstance_params 			= models.TextField('Command')
	serverinstance_created 			= models.DateTimeField("Created", auto_now_add=True)
	startuser 						= models.ForeignKey(User, related_name='startuser')
	serverinstance_started  		= models.DateTimeField("Started", blank=True, null=True)
	serverinstance_startcommited  	= models.DateTimeField("When the Start operation was commited", blank=True, null=True)
	stopuser 						= models.ForeignKey(User, blank=True, null=True, related_name='stopuser')
	serverinstance_ended  			= models.DateTimeField("Ended", blank=True, null=True)
	serverinstance_endcommited  	= models.DateTimeField("When the End operation was commited", blank=True, null=True)

	server 	= models.ForeignKey('Server')
	osimage = models.ForeignKey('OSImage')
	job		= models.ForeignKey('Job', blank=True, null=True)
	
	class Meta: abstract = True
	def __unicode__(self): return str(self.server)

	@property
	def params(self): 
		if self.serverinstance_params: return eval(self.serverinstance_params)
		return {}
	@params.setter
	def params(self, value): self.serverinstance_params = str(value)
	

	def pause(self, user):
		if self.serverinstance_ended: 		return False
		params = self.params
		params['command'] = 'pause'
		self.params = params
		self.stopuser = user
		self.serverinstance_ended = datetime.now()
		if self.serverinstance_started is None: self.serverinstance_endcommited = datetime.now()
		if self.job and not self.job.job_ended: self.job.kill()
		self.save()
		return True

	def stop(self, user, add_endcommited=False):
		if self.serverinstance_ended: 		return False
		params = self.params
		params['command'] = 'stop'
		self.params = params
		self.stopuser = user
		self.serverinstance_ended = datetime.now()
		if self.serverinstance_started is None or add_endcommited: 
			self.serverinstance_endcommited = datetime.now()

		if self.job and not self.job.job_ended: self.job.kill()
		self.save()
		return True