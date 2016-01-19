import os, paramiko
import opencsp.ApplicationsSettings as ApplicationsSettings
from opencsp.envmanagers.DefaultEnvManager.DefaultEnvManager import DefaultEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox
from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings
import ping
from django.utils import timezone

paramiko.util.log_to_file("/home/ricardo/paramiko.log")

class DefaultEnvManagerAppBackupVideo(DefaultEnvManager):

	BACKUP_PATH = os.path.join('/', 'home', 'manager', 'backup')

	def __init__(self):  super(DefaultEnvManagerAppBackupVideo, self).__init__()

	def unload_files(self, job, userpath):
		"""
		Unload the files from the remote output directory from a previous Job
		"""
		server = job.server
		outputFolder = os.path.join( server.running_env, 'output')

		job.job_startDownload = timezone.now()
		job.job_downloadedBytes = 0

		try:
			job.info("Downloading job's output:")
			if server.exists( outputFolder ):
				job.job_outputSize = self.remote_path_size(server, outputFolder)
				job.info("du -sb {0}".format(outputFolder))
				job.save()

				client = paramiko.SSHClient()
				client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				client.load_system_host_keys()
				client.connect( server.server_host, username=server.server_user, password=server.server_pass)
				sftp_client = client.open_sftp()

				mainpath = self.BACKUP_PATH
				outpath = os.path.join(mainpath, job.user.email)
				
				for f in server.output_files(job):
					job.info( "\t{0} <- {1}".format( outpath, f) )	
					filepath = os.path.join( outpath, f )

					self.get(job.server, os.path.join( outputFolder, f ), filepath)

					job.job_downloadedBytes += os.path.getsize(filepath)
		except Exception, e: 
			job.error( str(e) )

		job.job_endDownload = timezone.now()
		job.save()