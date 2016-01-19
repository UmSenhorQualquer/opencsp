from django.db import models
from datetime import datetime


class AbstractVirtualServer(models.Model):
	virtualserver_id 		= models.AutoField(primary_key=True)
	virtualserver_maxram 	= models.IntegerField('Maximum of RAM', blank=True, null=True)
	virtualserver_maxcores 	= models.IntegerField('Maximum of RAM', blank=True, null=True)
	virtualserver_ram 		= models.IntegerField('RAM', blank=True, null=True)
	virtualserver_cores 	= models.IntegerField('Cores', blank=True, null=True)
	virtualserver_cpucap 	= models.IntegerField('CPU Cap', blank=True, null=True)
	virtualserver_version 	= models.FloatField('Version', blank=True, null=True)
	virtualserver_update	= models.BooleanField('Update server')

	class Meta: abstract = True
	
	def save(self):
		if not self.pk:
			if not self.virtualserver_cpucap: self.virtualserver_cpucap = 60
			if not self.virtualserver_ram: self.virtualserver_ram = 1024
			if not self.virtualserver_cores: self.virtualserver_cores = 1
		super(AbstractVirtualServer,self).save()

	def maxRam(self): 		return self.virtualserver_maxram
	def maxCPUCores(self): 	return self.virtualserver_maxcores

	@property
	def is_alive(self):
		return (datetime.now()-self.server_lastcontact).seconds <= (60*3)

	def updateProperties(self, name, ram, cores, cap):
		if name: self.server_name = name
		if ram: self.virtualserver_ram = int(ram)
		if cores: self.virtualserver_cores = int(cores)
		if cap: self.virtualserver_cpucap = int(cap)
		if ram or cores or cap or name: self.save()
