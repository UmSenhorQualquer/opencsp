from django.db import models
from django.contrib.auth.models import User
import uuid, os

def StorageList():
	envsPath = os.path.join('opencsp','storagemanagers')
	return [ (name, name.replace('StorageManager','')) for name in os.listdir(envsPath) if os.path.isdir(os.path.join(envsPath,name))]


class AbstractUserSettings(models.Model):
	user_uniquecode 	= models.CharField('Unique ID', max_length=255, default=uuid.uuid1)
	user_login_attempts = models.SmallIntegerField('Login attempts', default=0)
	user_storage		= models.CharField('Storage manager', max_length=255, 
		choices=StorageList(), default='DefaultStorageManager')

	user = models.ForeignKey(User)
	
	class Meta: abstract = True
	
