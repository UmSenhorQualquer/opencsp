import opencsp.envmanagers.EnvironmentManager as EnvironmentManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox, ControlDir


import glob,shutil, os, uuid, requests, json
from django.contrib.auth.models import User
from fabric.contrib.files import exists
from django.conf import settings
from django.utils import timezone
from django.db import models
from urlparse import urljoin
from opencsp import AVAILABLE_STORAGES
import time, sys
from smartencoding import smart_unicode, smart_unicode_with_replace

class AbstractJob(models.Model):
	job_id 			= models.AutoField(primary_key=True)
	job_uniqueid 	= models.CharField('Unique id', max_length=255, blank=True, null=True)
	job_application = models.CharField('Application', max_length=200)
	job_state 		= models.CharField('State', max_length=30, blank=True, null=True)
	job_parameters 		= models.TextField('Parameters')
	job_outparameters 	= models.TextField('Out parameters')
	job_created 	= models.DateTimeField("Created",auto_now_add=True,)
	job_started 	= models.DateTimeField("Started", blank=True, null=True)
	job_ended 		= models.DateTimeField("Ended", blank=True, null=True)
	job_output 		= models.TextField('Output', blank=True, null=True)

	job_startUpload 	= models.DateTimeField("Start upload", blank=True, null=True)
	job_endUpload 		= models.DateTimeField("End upload", blank=True, null=True)
	job_inputSize 		= models.PositiveIntegerField('Total input size', blank=True, null=True)
	job_uploadedBytes 	= models.PositiveIntegerField('Uploaded bytes', blank=True, null=True)
	
	job_startDownload 	= models.DateTimeField("Start download", blank=True, null=True)
	job_endDownload 	= models.DateTimeField("End download", blank=True, null=True)
	job_outputSize 		= models.PositiveIntegerField('Total output size', blank=True, null=True)
	job_downloadedBytes = models.PositiveIntegerField('Uploaded bytes', blank=True, null=True)

	masterserver 	= models.ForeignKey('MasterServer', blank=True, null=True)
	server 			= models.ForeignKey('Server')
	user 			= models.ForeignKey(User)
	
	class Meta: abstract = True

	def __unicode__(self): return "%s" % (str(self.job_application))

	def running_time(self):
		if self.job_ended==None or self.job_started==None: return ''
		return str(self.job_ended-self.job_started)

	def save(self):
		
		if self.job_uniqueid==None or self.job_uniqueid=='':
			self.job_uniqueid=uuid.uuid1().hex+uuid.uuid1().hex+uuid.uuid1().hex+uuid.uuid1().hex

		#Find the total size of the input data ########################
		if self.pk==None:
			storage = AVAILABLE_STORAGES.get(self.user)

			self.job_inputSize = 0
			for filename in self.inputfiles: 
				fileinfo = storage.file_info( filename )
				self.job_inputSize += fileinfo.size
		#################################################################

		super(AbstractJob,self).save()


	def __dirFileNames(self, storage, dirname, files):
		for f in storage.list(dirname):
			if f.type=='dir': 
				self.__dirFileNames(storage, f.fullpath, files)
			else:
				files.append( f.fullpath )

	@property
	def inputfiles(self):
		files = []
		application = settings.PYFORMS_APPLICATIONS.createInstance(self.job_application); 
		application.storage = storage = AVAILABLE_STORAGES.get(self.user)
		

		params = eval(str(self.job_parameters));
		application.loadSerializedForm( params )

		try:
			for key, item in application.__dict__.items():
				
				if 	isinstance(item, ControlFile) and item._value!=None:
					filename = item._value
					if 	len(filename.strip())>1	and \
						not (
							item._value.startswith('http://') or item._value.startswith('https://')
						):
							files.append( filename )
				
				if 	isinstance(item, ControlDir) and item._value!=None:
					dirname = item._value
					if len(dirname.strip())>=1: self.__dirFileNames(storage, dirname, files)
		except:
			pass
		return files

	@property
	def consoleparameters(self):
		application = settings.PYFORMS_APPLICATIONS.createInstance(self.job_application); 
		application.storage = AVAILABLE_STORAGES.get(self.user)
		
		params = eval(str(self.job_parameters));
		application.loadSerializedForm( params )
		params = []
		for key, item in application.__dict__.items():
			if isinstance(item, (ControlSlider, ControlText, ControlCombo, ControlCheckBox) ) and \
				item._value!=None and item._value!='':
				params.append("--{0} '{1}'".format(key, item._value) )

			if isinstance(item, (ControlFile, ControlDir) ) and item._value!=None and item._value!='' and len(item._value)>0:
				#value = os.path.join('input',item._value[1:])
				#if item._value.startswith('http://') or item._value.startswith('https://'): value = item._value
				
				filename = item._value#[len(application.storage.localpath):]
				if len(filename)>1:
					filename = 'input'+filename
					params.append( "--{0} '{1}'".format(key, filename) )
			
		return params

	@property
	def dictionary(self):
		res =  {'job_id'		:self.job_id  ,
				'job_uniqueid'		:self.job_uniqueid  ,
				'job_application'	:self.job_application,
				'job_state'			:self.job_state 	,
				'job_started'		:self.job_started 	,
				'job_ended'			:self.job_ended 	,
				'job_parameters'	:self.job_parameters,
				'job_created'		:str(self.job_created) 	,
				'server'			:self.server.server_uniqueid 	}
		if self.job_started: res.update({'job_started':str(self.job_started)})
		if self.job_ended: res.update({'job_ended':str(self.job_ended)})
		return res

	@dictionary.setter
	def dictionary(self, value):
		self.job_uniqueid		= value.get('job_uniqueid', 	None)
		self.job_application	= value.get('job_application', 	None)
		self.job_state			= value.get('job_state', 		None)
		self.job_parameters		= value.get('job_parameters', 	None)
		self.job_ended			= value.get('job_ended', 		None)
		self.job_created		= value.get('job_created', 		None)
		self.job_started		= value.get('job_started', 		None)
		self.job_ended			= value.get('job_ended', 		None)
		if 'output' in value: self.output = value.get('ouput')
		
		server 					= value.get('server',	 	None)
		if self.pk==None and server: self.server = Server.objects.get(satelliteserver=None,server_uniqueid=server)
	
	@property
	def output(self):
		if self.job_ended!=None: 
			outFilename = os.path.join(settings.OPENCSP_JOBS_TERMINALOUTPUT, str(self.pk)+'.txt')
			if os.path.isfile(outFilename):
				infile = open(outFilename, "r")
				content = infile.read()
				infile.close()
				return content
			else:
				return self.job_output
		elif self.job_started!=None:
			return self.server.read_output(self)
		else: return "The job didn't started yet."

	@output.setter
	def output(self, value):
		outFilename = os.path.join(settings.OPENCSP_JOBS_TERMINALOUTPUT, str(self.pk)+'.txt')
		outfile = open(outFilename, "w")
		outfile.write(value.encode('ascii', 'ignore'))
		outfile.close()

	def log(self, value): 	
		if self.output==None: self.output=''
		self.output += "%s\n" % value

	def warning(self, value, color='orange'): 	
		if self.output==None: self.output=''
		value = smart_unicode_with_replace(value).encode('ascii', errors='ignore')
		self.output += "<b style='color:{0};'>{1}</b>\n".format(color, value )
		self.save()
	def info(self, value): self.warning(value, color='orange')
	def error(self, value): self.warning("Error: %s" % value, color='red')

	def upload2master(self):
		application = settings.PYFORMS_APPLICATIONS.createInstance(self.job_application); 
		application.storage = AVAILABLE_STORAGES.get(self.user)
		params = eval(str(self.job_parameters));
		application.loadSerializedForm(params)
		
		url = urljoin( self.masterserver.masterserver_url, 'ws/uploadfile/' )
		for f in glob.glob(os.path.join( parameters['userpath'], '*') ):
			data = {
				'uniqueid': settings.OPENCSP_UNIQUE_ID,
				'job_uniqueid': self.job_uniqueid,
				'filename': os.path.basename(f)
				}
			files = { 'file': open(f, 'rb') }
			r = requests.post(url, data, files=files)
		shutil.rmtree( params['userpath'] )

	def downloadFromMaster(self):
		self.info("Downloading files from the Master server")

		application = settings.PYFORMS_APPLICATIONS.createInstance(self.job_application); 
		application.storage = AVAILABLE_STORAGES.get(self.user)
		params = eval(str(self.job_parameters));
		application.loadSerializedForm( params )
		userpath = params['userpath']

		url = urljoin( self.masterserver.masterserver_url, 'ws/downloadfile/' )

		for key, item in application.__dict__.items():
			if isinstance(item, ControlFile) and item._value!='' and item._value!=None: 
				filename = item.value.replace(userpath+"/", '')
				data2send = {
					'uniqueid': settings.OPENCSP_UNIQUE_ID,
					'job_uniqueid': self.job_uniqueid,
					'filename': filename
					}
				headers = {'content-type': 'application/json'}
				r = requests.post(url, data=json.dumps(data2send), headers=headers)
				jobpath = os.path.join(settings.MEDIA_ROOT, 'uploads',self.user.username, str(self.pk) )
				if not os.path.exists(jobpath): os.makedirs(jobpath)
				f = open( item.value , 'wb')
				for chunk in r.iter_content(chunk_size=1024): 
					if chunk: f.write(chunk); f.flush()
				f.close()


	def __load_files(self):
		if self.masterserver: self.downloadFromMaster()

		self.job_startUpload = timezone.now()
		self.server.prepare_job(self)
		self.job_endUpload = timezone.now()
		self.save()

		if self.masterserver: 
			jobpath = os.path.join(settings.MEDIA_ROOT, 'uploads',self.user.username, str(self.pk), '*' )
			files = glob.glob(jobpath)
			for f in files: os.remove(f)
	
	@property
	def jobinstance(self):
		from opencsp.models import ServerInstance

		try:
			return ServerInstance.objects.get(job=self)
		except ServerInstance.DoesNotExist:
			return None

	def is_finnished(self): return self.server.exists( os.path.join( self.server.running_env,'busy.no') )
		
	def run(self):
		wait = not self.server.checkconnection()

		if hasattr(self.server, 'virtualserver'):
			if self.jobinstance==None:
				from opencsp.models import Algorithm
				algo = Algorithm.objects.get(algorithm_class=self.job_application)
				self.server.deployInstance(algo.osimage, self.user, self)
				return
			elif self.jobinstance.serverinstance_startcommited==None: 
				return
			else:
				wait = True
		else:
			if wait: self.server.turnon()


		
		self.job_state = 'loading'
		self.info("Preparing job...")
		self.start()
		if wait:  time.sleep(settings.TIME_WAITTING_FOR_SERVER_TO_STARTUP)
		#try:

		self.server.free_server()
		self.server.set_busy(self)
		
		self.__load_files()
		self.job_state=''
		self.save()

		self.info("Starting...")
		self.server.run_job(self)
	
			
		"""except Exception as e:
			import traceback
			tb = traceback.format_exc()
			self.error( tb )

			self.info("The job was aborted...")
			self.end()
			self.server.free_server()"""


	def kill(self):
		if self.job_started==None: 
			self.start(); self.warning('Job killed before starting')
		elif hasattr(self.server, 'virtualserver'):
			self.job_ended = timezone.now(); 
			self.save()
			return
		else:
			self.warning("Sending kill signal")
			try:
				if self.server.current_job_id==self.pk:
					self.warning('Contacting server ...')
					self.server.environmentManager(self).kill(self)
					self.log( self.server.read_output(self) )
					self.server.free_server()				
					self.warning("Job killed")
			except: self.warning("Error on killing the job")
		self.end()
		self.server.check_new_jobs()

	def updateMaster(self):
		url = urljoin(self.masterserver.masterserver_url, 'ws/updatejob/')
		headers = {'content-type': 'application/json'}
		data2send = {'uniqueid': settings.OPENCSP_UNIQUE_ID, 'job': self.dictionary }
		r = requests.post(url, data=json.dumps(data2send), headers=headers)
		result = r.json()

	def start(self): 
		self.job_started = timezone.now(); 
		if self.masterserver: self.updateMaster()
		self.save()

	def end(self): 

		if hasattr(self.server, 'virtualserver'):
			currentinstance = self.server.serverinstance
			
			from opencsp.models import Job
			nextjob = Job.objects.exclude(pk=self.pk)
			nextjob = nextjob.filter(server=self.server)
			nextjob = nextjob.filter(job_started=None, job_ended=None).order_by('job_created')

			if nextjob.count()>0:
				nextjob = nextjob[0]
				from opencsp.models import Algorithm
				algo = Algorithm.objects.get(algorithm_class=nextjob.job_application)
				if algo.osimage==currentinstance.osimage:
					#If the next job is set for the same image, do not shutdown the virtual server
					self.server.stop( self.user, True )
				else:
					#if the image is diferent, shutdown the server to start a new image
					self.server.stop( self.user )	
			else:
				self.server.stop( self.user )

		self.job_ended = timezone.now(); 
		if self.masterserver: self.updateMaster()
		self.save()


	def reset(self):
		self.job_started 	= None
		self.job_ended 		= None
		self.job_state 		= ''
		self.output 		= ''
		self.save()