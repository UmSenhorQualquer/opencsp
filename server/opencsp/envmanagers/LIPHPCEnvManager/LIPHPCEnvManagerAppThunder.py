import os, paramiko
import opencsp.ApplicationsSettings as ApplicationsSettings
from opencsp.envmanagers.LIPEnvManager import LIPEnvManager
from pyforms.Controls import ControlSlider
from pyforms.Controls import ControlFile
from pyforms.Controls import ControlText
from pyforms.Controls import ControlCombo
from fabric.api import *
from fabric.contrib.files import exists
from django.conf import settings
from LIPHPCEnvManager import LIPHPCEnvManager

paramiko.util.log_to_file("/home/manager/paramiko.log")

class LIPHPCEnvManagerAppThunder(LIPHPCEnvManager):

    def __init__(self):  super(LIPHPCEnvManagerAppThunder, self).__init__()

    

    def remote_script(self, job):
        jobparams = eval(job.job_parameters)
        
        command = """#!/bin/bash
        #######
        # HPC #
        #######
        #$ -pe spark {1}
        #$ -q hpcgrid
        #$ -P HpcGrid
        #$ -l infiniband=y
        #$ -cwd

        #$ -j yes
        #$ -o output.txt

        module load thunder
        thunder-submit {2}

        mkdir output
        echo {0} > busy.no
        """.format(job.pk ,jobparams['_numberofmachines']['position'],'input'+jobparams['_scriptfile']).replace('\t','')

        return command