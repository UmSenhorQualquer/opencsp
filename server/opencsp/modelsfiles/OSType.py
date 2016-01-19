from django.db import models

class AbstractOSType(models.Model):
	ostype_id = models.AutoField(primary_key=True)
	ostype_name = models.CharField('Name', max_length=50)
	ostype_ostype = models.CharField('ostype', max_length=45)

	class Meta: abstract = True
	def __unicode__(self): return self.ostype_name