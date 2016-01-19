from django.db import models
import uuid

class AbstractOSImage(models.Model):
	osimage_id = models.AutoField(primary_key=True)
	osimage_uniquecode = models.CharField('Unique ID', max_length=255, blank=True, null=True)
	osimage_name	 = models.CharField('Name', 	  max_length=255)
	osimage_path	 = models.CharField('Image path', max_length=255)
	osimage_user 	 = models.CharField('User name', max_length=100, null=True, blank=True)
	osimage_pass 	 = models.CharField('Password', max_length=255, null=True, blank=True)
	osimage_remotedir = models.CharField('Directory', max_length=255, null=True, blank=True)
	
	ostype = models.ForeignKey('OSType')
	
	def save(self):
		if self.osimage_uniquecode==None or self.osimage_uniquecode=='': 
			self.osimage_uniquecode=uuid.uuid1().hex+uuid.uuid1().hex+uuid.uuid1().hex+uuid.uuid1().hex
		super(AbstractOSImage,self).save()

	class Meta: abstract = True
	def __unicode__(self): return self.osimage_name