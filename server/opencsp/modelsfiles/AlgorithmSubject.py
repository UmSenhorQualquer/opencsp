from django.db import models


class AbstractAlgorithmSubject(models.Model):
	algorithmsubject_id = models.AutoField(primary_key=True)
	algorithmsubject_name = models.CharField('Name', max_length=100)
	
	class Meta: abstract = True
	def __unicode__(self): return self.algorithmsubject_name