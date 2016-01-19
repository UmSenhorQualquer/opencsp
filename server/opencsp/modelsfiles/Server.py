from django.contrib.auth.models import User
from StringIO import StringIO
from datetime import datetime
from django.db import models
import paramiko, os,uuid
from fabric.api import *
from django.conf import settings
from fabric.contrib.files import exists
from django.db.models import Q
from django.utils import timezone
import subprocess
import time, os, sys
import socket
paramiko.util.log_to_file(os.path.join(settings.BASE_DIR, 'paramiko.log'))
#paramiko.util.log_to_file("/home/ricardo/paramiko.log")

import opencsp.envmanagers.EnvironmentManager as EnvironmentManager 

def EnvManagersList():
	envsPath = os.path.join('opencsp','envmanagers')
	return [ (name, name.replace('EnvManager','')) for name in os.listdir(envsPath) if os.path.isdir(os.path.join(envsPath,name))]



class AbstractServer(models.Model):
	
	server_id = models.AutoField(primary_key=True)
	server_uniqueid 	= models.CharField('Unique id', max_length=255, null=True, blank=True)
	server_name 		= models.CharField('Name', max_length=100, null=True, blank=True)
	server_host 		= models.CharField('Address', max_length=100, null=True, blank=True)
	server_user 		= models.CharField('User name', max_length=100, null=True, blank=True)
	server_pass 		= models.CharField('Password', max_length=100, null=True, blank=True)
	server_certificate	= models.CharField('Authentication certificate', max_length=255, null=True, blank=True)
	server_mac			= models.CharField('Mac Address', max_length=64, null=True, blank=True)
	server_hostname		= models.CharField('Host name', max_length=255, null=True, blank=True)
	server_remotedir	= models.CharField('Host directory', max_length=255, null=True, blank=True)
	server_active		= models.BooleanField('Active')
	server_isalive		= models.BooleanField('Is alive')
	server_lastcontact	= models.DateTimeField('Last contact', null=True, blank=True)
	server_envmanager	= models.CharField('Environment manager', max_length=255, 
		choices=EnvManagersList(), default='DefaultEnvManager')
	server_turnoff 		= models.BooleanField('Turn off the computer when is not needed')

	satelliteserver 	= models.ForeignKey('SatelliteServer', null=True, blank=True)
	parent 				= models.ForeignKey('Server', null=True, blank=True)
	
	class Meta: 
		abstract = True
		ordering = ['server_name']
	def __unicode__(self): 
		if self.satelliteserver: return '@'.join( [self.server_name, 
			self.satelliteserver.satelliteserver_name] )
		return str(self.server_name)

	

	###################################################################
	#### Properties ###################################################
	###################################################################

	def environmentManager(self, job=None, app=None): 
		"""
		Retreave the object that will manage the access to this server or job.
		"""
		application = app if job==None else job.job_application
		return EnvironmentManager.AVAILABLE_ENVIROMENTS.get(self.server_envmanager, application)

	@property
	def reservedto(self):
		if hasattr(self, 'virtualserver'): 
			if self.serverinstance:
				return self.serverinstance.startuser
			else:
				return None
		else: 
			return None

	@property
	def osimage(self):
		if hasattr(self, 'virtualserver'): 
			if self.serverinstance:
				return self.serverinstance.osimage
			else:
				return None
		else: 
			return None

	@property
	def state(self):
		instance = self.serverinstance
		if instance is not None: 
			if  instance.serverinstance_started is None and \
				instance.serverinstance_startcommited is None and \
				instance.serverinstance_ended is None and \
				instance.serverinstance_endcommited is None:
				return 'Connecting'
			elif  instance.serverinstance_started is not None and \
				instance.serverinstance_startcommited is None and \
				instance.serverinstance_ended is None and \
				instance.serverinstance_endcommited is None:
				return 'Starting'
			elif instance.serverinstance_started is not None and \
				 instance.serverinstance_startcommited is not None and \
				instance.serverinstance_ended is None and \
				 instance.serverinstance_endcommited is None:
				return 'Running'
			elif instance.serverinstance_ended is not None and \
				 instance.serverinstance_endcommited is None:
				return 'Stoping'
			else:
				return ''
		else: 
			return ''

	@property
	def username(self):
		if hasattr(self, 'virtualserver'): return self.osimage.osimage_user
		else: return self.server_user

	@property
	def password(self):
		if hasattr(self, 'virtualserver'): return self.osimage.osimage_pass
		else: return self.server_pass
	
	@property 
	def remotedir(self):
		if hasattr(self, 'virtualserver'): return self.osimage.osimage_remotedir
		else: return self.server_remotedir
	
	@property
	def is_public(self): return self.cluster_set.filter(users=None).count()>0

	@property
	def is_alive(self):
		if self.satelliteserver!=None: return self.server_isalive
		if hasattr(self, 'virtualserver'): return self.virtualserver.is_alive

		if self.parent!=None: self.parent.is_alive()
	
		now = timezone.now()
		if self.server_lastcontact==None or (now - self.server_lastcontact).seconds>1800:
			self.server_lastcontact = now
			self.server_isalive = self.checkconnection()
			self.save()
			return self.server_isalive
		else:
			return self.server_isalive

	@property
	def db_current_job_id(self):
		"""
		Get the current job described in DB
		"""
		try:
			job = Job.objects.get(server=self, job_ended=None).exclude(job_started=None)
		except:
			return None
		return job.pk


	@property
	def current_job_id(self):
		"""
		Read the current job loaded in the remote server
		"""
		env.host_string 		= self.host_string
		env.password 			= self.password
		env.disable_known_hosts = True
		if self.exists(os.path.join( self.running_env,'busy.yes') ): 
			buf = StringIO(); get(os.path.join( self.running_env,'busy.yes'), buf)
			return int(buf.getvalue())
		if self.exists(os.path.join( self.running_env,'busy.no') ): 
			buf = StringIO(); get(os.path.join( self.running_env,'busy.no'), buf)
			return int(buf.getvalue())
		return None


	@property
	def running_env(self): return os.path.join(self.remotedir, "running_env")

	@property
	def host_string(self): 
		if hasattr(self, 'virtualserver'): return "%s@%s:2222" % (self.username, self.server_host)
		else: return "%s@%s" % (self.username, self.server_host)

	@property
	def algorithms(self):
		#return all the algorithms associated to this server
		from opencsp.models import Algorithm
		return Algorithm.objects.filter(cluster__servers=self).distinct()

	@property
	def serverinstance(self):
		#Return the corrent server instance
		if not hasattr(self, 'virtualserver'): return None
		from opencsp.models import ServerInstance

		try:
			return ServerInstance.objects.exclude(serverinstance_started=None).get(serverinstance_endcommited=None,serverinstance_ended=None, server=self)
		except ServerInstance.DoesNotExist:
			instances = ServerInstance.objects.filter(serverinstance_endcommited=None, server=self).order_by('serverinstance_created')
			if instances.count()>0:
				return instances[0]
			else:
				return None

	@property
	def nextserverinstance(self):
		#Return the corrent server instance
		if not hasattr(self, 'virtualserver'): return None
		from opencsp.models import ServerInstance

		instances = ServerInstance.objects.filter(serverinstance_endcommited=None, server=self).order_by('serverinstance_created')
		if instances.count()>1:
			return instances[1]
		else:
			return None


	###################################################################
	#### Virtual server functions #####################################
	###################################################################

	def pause(self, user):
		if not hasattr(self, 'virtualserver'): return False
		instance = self.serverinstance
		if instance is None: return False
		if instance.pause(user): 
			return True
		return False

	def stop(self, user=None, add_endcommited=False):
		if not hasattr(self, 'virtualserver'): 
			self.environmentManager().turnoff_server(self)
			self.server_isalive = False
			self.server_lastcontact = timezone.now()
			self.save()
			return True
		else:
			instance = self.serverinstance
			if instance is None: return False
			if instance.stop(user, add_endcommited): 
				return True
		return False

	def deployInstance(self, osimage, user, job=None):
		if not hasattr(self, 'virtualserver'): return
		if self.serverinstance is not None: return

		
		data = {
			'user_id': 			user.pk,
			'osimage_uniqueid': osimage.osimage_uniquecode,
			'osimage_name': 	osimage.osimage_name,
			'osimage_type': 	osimage.ostype.ostype_ostype,
			'ram':    			self.virtualserver.virtualserver_ram,
			'cores':  			self.virtualserver.virtualserver_cores,
			'cpucap': 			self.virtualserver.virtualserver_cpucap,
			'command': 			'start'}

		from opencsp.models import ServerInstance
		instance = ServerInstance(
				startuser=user,
				serverinstance_params=str(data),
				server = self,
				job = job,
				osimage = osimage
			)
		instance.save()

	###################################################################
	#### Functions ####################################################
	###################################################################

	def save(self):
		if self.server_uniqueid==None or self.server_uniqueid=='': 
			self.server_uniqueid=uuid.uuid1().hex+uuid.uuid1().hex+uuid.uuid1().hex+uuid.uuid1().hex
		super(AbstractServer,self).save()

	
	
	def checkconnection(self):
		"""
		Verify if the remote server is alive
		"""
		
		return self.environmentManager().server_checkconnection(self)

	#######################################################################################
	##### Unitary operations ##############################################################
	#######################################################################################

	def run(self, command):						return self.environmentManager().run(self, command)
	def sudo(self, command):					return self.environmentManager().sudo(self, command)
	def put(self, origin, destiny): 			return self.environmentManager().put(self, origin, destiny)
	def get(self, origin, destiny): 			return self.environmentManager().get(self, origin, destiny)
	def exists(self, path):						return self.environmentManager().exists(self, path)
	def write(self, filename, content): 		return self.environmentManager().write(self, filename, content)
	def remove_files_in(self, folder): 			return self.environmentManager().remove_files_in(self, folder)

	#######################################################################################
	##### Jobs related ####################################################################
	#######################################################################################
	
	def server_info(self): 					return self.environmentManager().server_info(self)
	def has_job(self): 						return self.environmentManager().has_job(self)
	def is_busy(self): 						return self.environmentManager().is_busy(self)
	def set_busy(self,job):  				return self.environmentManager(job).set_busy(job)
	def read_output(self, job): 			return self.environmentManager(job).read_output(job)
	def output_files(self, job, directories): return self.environmentManager(job).output_files(job, directories)
	def server_jobinfo(self, job): 			return self.environmentManager(job).server_jobinfo(job)
	def run_job(self, job): 				return self.environmentManager(job).run_job(job)

	#######################################################################################
	##### Server related ##################################################################
	#######################################################################################

	def turnon(self):					return self.environmentManager().turnon_server(self)
	def setup_node(self):				return self.environmentManager().setup_node(self)
	def setup_application(self, app): 	return self.environmentManager(app=app.algorithm_class).setup_application(self, app)
	def close_setup_node(self, app):	return self.environmentManager(app=app.algorithm_class).close_setup_node(self, app)


	def prepare_job(self, job):				self.environmentManager(job).prepare_job(job)
	def free_server(self):  				self.remove_files_in( 'running_env' )

	
	def check_new_jobs(self):
		command = "python {1} {0}".format( self.server_id, os.path.join(settings.SCRIPTS_ROOT, 'check_for_new.py') )
		p = subprocess.Popen( command.split(), cwd=settings.BASE_DIR, stdout=subprocess.PIPE );
		p.wait()
		
	def finnish_job(self):
		command = "python {1} {0}".format( self.server_id, os.path.join(settings.SCRIPTS_ROOT, 'finnish_process.py') )
		p = subprocess.Popen( command.split(), cwd=settings.BASE_DIR, stdout=subprocess.PIPE );
		p.wait()


	
	def paramikoRun(self, command):

		s = paramiko.SSHClient();
		s.load_system_host_keys(); 
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy())

		port = 2222 if hasattr(self, 'virtualserver') else 22
		
		for i in range(5):
			try:
				print "try connection", 
				if len(self.password)>0:
					print "1"
					s.connect(self.server_host, port, self.username, self.password, timeout=5.0, look_for_keys=False)
					break
				if len(self.server_certificate)>0:
					print "2"
					s.connect(self.server_host, port, self.username, timeout=20.0, key_filename=self.server_certificate )
					break
				else:
					print "3"
					s.connect(self.server_host, port, self.username, timeout=5.0, look_for_keys=True)
					break
				#except socket.timeout as e:
			except Exception as e:
				print "Timeout error({0}): {1}".format(e.errno, e.strerror)
				if i==4: return "", "Timeout error({0}): {1}".format(e.errno, e.strerror)
				time.sleep(5)

				#paramiko.ssh_exception.NoValidConnectionsError
		
		transport = s.get_transport()
		session = transport.open_session()
		session.request_x11()
		
		session.exec_command(command)
		contents = StringIO()
		data = session.recv(1024)
		# Capturing data from chan buffer.
		while data:
			contents.write(data)
			data = session.recv(1024)

		contents_err = StringIO()
		data_err = session.recv_stderr(1024)
		while data_err:
			contents_err.write(data_err)
			data_err = session.recv_stderr(1024)

		status = session.recv_exit_status();
		session.close();
		s.close()
		

		return contents.getvalue(), contents_err.getvalue()


	


	def unload_files(self):
		job_id = self.current_job_id
		
		if job_id!=None:
			from opencsp.models import Job
			job = Job.objects.get(pk=job_id)
			#try:
			job.log( self.read_output(job) )
			
			if job.job_ended==None:
				if job.masterserver: 
					userpath = os.path.join( settings.MEDIA_ROOT, 'uploads', str(job.user), str(job.pk)+os.path.sep )
				else:
					userpath = os.path.join( settings.MEDIA_ROOT, 'uploads', str(job.user)+os.path.sep )

				self.environmentManager(job).unload_files(job, userpath)
			
			job.info("Cleaning server")

			self.free_server()
			if job.masterserver: job.upload2master()

			job.end()
			job.info("Job ended")

			
			self.check_new_jobs()
			#except:
			#	exceptiontype, value, traceback = sys.exc_info()
			#	job.error( str(exceptiontype) 	)
			#	job.error( str(value) 			)
			#	job.error( str(traceback) 		)
			#	job.end()
			#	self.free_server()

	@staticmethod
	def PickServer(algo, user, server_id):
		if server_id!=None and int(server_id)>0:
			from opencsp.models import Server
			servers = Server.objects.filter( Q(cluster__users=user) | Q(cluster__users=None))
			server = servers.distinct().get(pk=server_id, cluster__algorithms=algo)
		else:
			servers = algo.servers(user)
			servers_count=[]
			server=None
			from opencsp.models import Job
			for s in servers:
				count = Job.objects.filter(job_ended=None, server=s).count()
				if count==0: 
					server = s; 
					break
				servers_count.append( (count,s) )
			if server==None:
				servers_count = sorted(servers_count, key=lambda x: x[0] ) 
				server = servers_count[0][1]
		return server


	def synchronizeServer(self, app=None):
		if app is not None:
			applications = [Algorithm.objects.get(pk=app)]
		else:
			self.setup_node()
			applications = self.algorithms

		for app in applications: self.setup_application(app)