from __future__ import with_statement
from fabric.api import *
from fabric.contrib.files import exists
from fabproject import rsync_project
import paramiko; paramiko.util.log_to_file("paramiko.log")
from fabric.network import ssh; ssh.util.log_to_file("paramiko.log", 10)
import os, config
import argparse

env.user = 'manager'
env.hosts = ['10.40.11.123']
env.password = '123456'


def setup_master(installation_path):
	sudo(	"mkdir 	-p %s" % installation_path )
	sudo(	"chmod 	-R 777 %s" % installation_path )
	sudo(	"chown 	-R %s %s" % (env.user, installation_path) )
	sudo(	"chgrp 	-R %s %s" % (env.user, installation_path) )
	
	current_path = os.path.dirname(__file__)
	local_dir  = os.path.join(current_path,'server','*')
	remote_dir = installation_path

	rsync_project(
		local_dir=local_dir,
		remote_dir=remote_dir,
		exclude=('.svn', '*.pyc','output'),
		delete=True,
		sshpass=True
	)
	sudo(	"chown 	-R manager %s" % installation_path )
	sudo(	"chgrp 	-R manager %s" % installation_path )
	sudo(	"chmod -R 777 %s" % installation_path )

	sudo(	"mkdir 	-p /var/opencsp/media/uploads")
	sudo(	"chmod 	-R 777 /var/opencsp/media/uploads")
	sudo(	"chown 	-R manager /var/opencsp/media/uploads")
	sudo(	"chgrp 	-R manager /var/opencsp/media/uploads")

	run(	"rm -R %s" % os.path.join(installation_path,'media'), warn_only=True )
	sudo(	"ln -s /var/opencsp/media %s " % os.path.join(installation_path,'media') )
	
	sudo(	"mkdir 	-p /var/opencsp/applications")
	sudo(	"chmod 	-R 755 /var/opencsp/applications")
	sudo(	"chown 	-R manager /var/opencsp/applications")
	sudo(	"chgrp 	-R manager /var/opencsp/applications")
	run(	"rm -R %s" % os.path.join(installation_path,'applications'), warn_only=True )
	sudo(	"ln -s /var/opencsp/applications %s " % os.path.join(installation_path,'applications') )
	
	#sudo('/etc/init.d/apache2 restart')

	





def sync_master_code(installation_path):
	"""
	Syncs the master with the local
	"""
	current_path = os.path.dirname(__file__)
	
	for local_path, remote_path in config.SYNC_CONF:
		
		objectpath = os.path.join(installation_path, remote_path)

		try:
			sudo(	"chown 	-Rf %s %s" % (env.user, objectpath) )
			sudo(	"chgrp 	-Rf %s %s" % (env.user, objectpath) )
		except:pass
		
		rsync_project(
			local_dir = os.path.join(current_path, 		local_path	),
			remote_dir= os.path.join(installation_path, remote_path	),
			exclude=('.svn', '*.pyc', 'output'),
			delete=True,
			sshpass=True
		)
		try:
			sudo(	"chown 	-Rf manager %s" % objectpath )
			sudo(	"chgrp 	-Rf manager %s" % objectpath )
			sudo(	"chmod 	-Rf 777 %s" % installation_path )
		except:pass
	
	#sudo('/etc/init.d/apache2 restart')

