from django.db import models
from django.contrib.auth.models import User

class AbstractMasterServer(models.Model):
	masterserver_id = models.AutoField(primary_key=True)
	masterserver_name = models.CharField('Name', max_length=255)
	masterserver_uniqueid = models.CharField('Unique id', max_length=255)
	masterserver_url = models.CharField('Url', max_length=255)

	user = models.ForeignKey(User)

	class Meta: abstract = True
	def __unicode__(self): return self.masterserver_name 