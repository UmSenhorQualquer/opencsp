from django.db import models

class AbstractSatelliteServer(models.Model):
	satelliteserver_id = models.AutoField(primary_key=True)
	satelliteserver_name = models.CharField('Name', max_length=255)
	satelliteserver_uniqueid = models.CharField('Unique id', max_length=255)

	class Meta: abstract = True
	def __unicode__(self): return self.satelliteserver_name 