from django.db import models

class AbstractTask(models.Model):
	TASKTYPE_SHUTDOWN_SERVER = 'Shutdown server'

	task_id 		= models.AutoField(primary_key=True)
	task_type 		= models.CharField('Type', max_length=30)
	task_parameters = models.TextField('Parameters', null=True, blank=True)
	task_created	= models.DateTimeField('Created', auto_now_add=True)
	task_started 	= models.DateTimeField('Executed on', null=True, blank=True)
	task_ended   	= models.DateTimeField('Ended on', null=True, blank=True)
	task_results 	= models.TextField('Results', null=True, blank=True)

	@property
	def params(self): return eval(self.task_parameters)

	@staticmethod
	def schedule_server_shutdown(server):
		from opencsp.models import Task
		task = Task(
				task_type=Task.TASKTYPE_SHUTDOWN_SERVER,
				task_parameters=str({'server_id': server.pk})
			)
		task.save()
	
	
	class Meta: abstract = True
	def __unicode__(self): return self.task_type 