
from django.db import models
from django.db.models import Q

class AbstractAlgorithm(models.Model):
	algorithm_id 		= models.AutoField(primary_key=True)
	algorithm_name 		= models.CharField('Name', max_length=255)
	algorithm_class 	= models.CharField('Class name', max_length=100)
	algorithm_image 	= models.ImageField('Icon',upload_to='algorithm_image', max_length=255)
	algorithm_desc 		= models.TextField('Description', blank=True, null=True)
	algorithmsubjects 	= models.ManyToManyField('AlgorithmSubject')
	osimage 			= models.ForeignKey('OSImage', blank=True, null=True)

	class Meta: 
		abstract = True
		ordering = ['algorithm_name']
	def __unicode__(self): return self.algorithm_name

	def servers(self, user=None): 
		from opencsp.models import Server
		
		servers = Server.objects.filter(cluster__algorithms=self)
		if user!=None: servers = servers.filter( Q(cluster__users=user) | Q(cluster__users=None))
		servers = servers.distinct().order_by('server_name')
		return servers


	