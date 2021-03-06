import os, paramiko
import opencsp.ApplicationsSettings as ApplicationsSettings
from opencsp.envmanagers.LIPEnvManager import LIPEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox

from fabric.api import *
from opencsp.envmanagers.EnvManager import EnvManager
from fabric.contrib.files import exists
from django.conf import settings
from opencsp.envmanagers.DefaultEnvManager.fabproject import rsync_project

paramiko.util.log_to_file("/home/ricardo/paramiko.log")

class LIPEnvManagerAppImageRegistrationAnts(LIPEnvManager):


	def __init__(self):
		super(LIPEnvManagerAppImageRegistrationAnts, self).__init__()

	def setup_application(self, server, application):
		"""
		Setup the node environment in the remote server
		"""
		self.initCredentials(server)
		
		local_dir  = os.path.join(settings.BASE_DIR,'applications',application.algorithm_class.lower() )
		remote_dir = os.path.join(self._base_dir,'applications' )
	
		rsync_project(
			local_dir = local_dir,
			remote_dir= remote_dir,
			exclude=('.svn','*.pyc','output','ants'),
			delete=True,
			sshpass=True
		)

		server.run( """echo "PYFORMS_MODE = 'TERMINAL'" >> {0}""".format( os.path.join(remote_dir, application.algorithm_class.lower(),'settings.py') ))
		

	def close_setup_node(self, server, application):
		server.run('rsync -av /exper-sw/neuro/ants /exper-sw/neuro/opencsp/applications/imageregistrationants')
	

	def remote_script(self, job):
		params = ' '.join( job.consoleparameters)
		appPath = os.path.join('$OPENCSP_HOME',"applications", job.job_application.lower(), job.job_application+'.py' )
		
		command = """#!/bin/bash
			#$ -v SGEIN1=input
			#$ -v SGEIN2=server_id.txt
			#$ -v SGEOUT1=output
			#$ -v SGEOUT2=busy.no

			#$ -j yes
			#$ -o output.txt

			module load gcc-4.6.3
			module load opencsp-1.0

			mkdir output
			echo {2} > busy.no
			python {0} {1} --exec execute 
			""".format( appPath, params, str(job.pk) ).replace('\t\t\t','')

		return command