import os, paramiko
import opencsp.ApplicationsSettings as ApplicationsSettings
from opencsp.envmanagers.LIPHPCEnvManager import LIPHPCEnvManager
from pyforms.Controls import ControlSlider, ControlFile, ControlText, ControlCombo, ControlCheckBox

from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings

paramiko.util.log_to_file("/home/ricardo/paramiko.log")

class LIPHPCEnvManagerAppImageRegistrationAnts(LIPHPCEnvManager):


	def __init__(self):
		super(LIPHPCEnvManagerAppImageRegistrationAnts, self).__init__()

	def close_setup_node(self, server, application):
		server.run('rsync -av /exper-sw/neuro/ants /exper-sw/neuro/opencsp/applications/imageregistrationants')