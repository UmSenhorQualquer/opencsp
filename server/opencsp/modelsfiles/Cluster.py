from django.contrib.auth.models import User
from django.db import models

class AbstractCluster(models.Model):
	cluster_id = models.AutoField(primary_key=True)
	cluster_name = models.CharField('Name', max_length=100)
	cluster_uniqueid = models.CharField('Unique id', max_length=255)
	
	satelliteserver = models.ForeignKey('SatelliteServer', null=True, blank=True)
	algorithms = models.ManyToManyField('Algorithm', null=True, blank=True)
	servers = models.ManyToManyField('Server', null=True, blank=True)
	users = models.ManyToManyField(User, null=True, blank=True)

	class Meta: abstract = True
	def __unicode__(self): 
		if self.satelliteserver: return '@'.join( [self.cluster_name,  
			self.satelliteserver.satelliteserver_name] )
		return self.cluster_name


	def syncButton(self):
		return """<a class='btn btn-warning'  href='/plugins/myservers/installcluster/{0}/' ><i class="icon-refresh icon-black"></i>Install</a>""".format(self.cluster_id)
	syncButton.short_description = "Install/Reinstall applications"
	syncButton.allow_tags = True
