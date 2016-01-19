from PyQt4 import QtCore
from urlparse import urljoin
import  json, os, subprocess, shutil
import subprocess, shlex, mmap
import urllib2
from manager import utils


class LazyFile(object):

    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def read(self):
        with open(self.filename, self.mode) as f:
            return f.read()

class MachineManager(QtCore.QThread):

	def __init__( self, parent, command_id, parameters ):
		QtCore.QThread.__init__(self)
		
		self._parameters 	= parameters
		self._command_id 	= command_id
		self._parent 		= parent
		
		self._user_id 			= parameters.get('user_id', None)
		self._osimage_uniqueid	= parameters.get('osimage_uniqueid', None)
		self._ostype 			= parameters.get('osimage_type', None)
		self._ram 				= int(parameters.get('ram', 512))
		self._cores 			= int(parameters.get('cores', 1))
		self._cpucap 			= int(parameters.get('cpucap', 50))

		self._machine_path 		= os.path.join( 'machines', self._osimage_uniqueid )
		self._image_path 		= os.path.join( 'images', self._osimage_uniqueid )
		
		self._isclosing = False


	def __check_if_image_exists(self): return os.path.isfile( self._image_path )
	def __prepare_machine_2_run(self): pass #shutil.copy2( self._image_path, 'machines' )

	def __download_image(self):
		data2send 	= {'uniqueid': 	self._parent._uniqueid }
		r = utils.htttpPost(
			self._parent._ws_host,
			'/ws/virtualslave/downloadimage/',
			data2send )
		
		f = open( self._image_path , 'wb')
		chunk = r.read(4096)
		while chunk:
			f.write(chunk); f.flush()
			chunk = r.read(4096)
		f.close()

	def __get_machines_list(self):
		f = open('virtualmachines.txt', 'w')
		subprocess.call("vboxmanage list vms".split(), stdout=f); f.close()
		f = open('virtualmachines.txt', 'r')
		virtualmachines = []
		for line in f:
			virtual_machine, uid = line.split('" {')
			virtual_machine = virtual_machine[1:]
			virtualmachines.append(virtual_machine)
		return virtualmachines

	def __setup_machine(self, machinename, machinepath):
		command = ['VBoxManage', 'createvm', '--name', machinename, '--ostype', str(self._ostype), '--register']
		subprocess.call( command )
		#os.system(command)
		command = ['VBoxManage', 'storagectl', machinename, '--name', '"SATA Controller"', '--add', 'sata', '--controller', 'IntelAHCI']
		subprocess.call( command )
		#os.system(command)
		command = ['VBoxManage', 'storageattach', machinename, '--storagectl', '"SATA Controller"', '--port', '0', '--device', '0', '--type', 'hdd', '--medium', str(machinepath)]
		subprocess.call( command )
		#os.system(command)
		command = ['VBoxManage', 'modifyvm', machinename, '--natpf1', 'host2guest-ssh,tcp,,2222,,22']
		subprocess.call( command )
		
  		
	def __run_machine(self, machinename, port=3000):
		command = ['VBoxManage', 'modifyvm', machinename, '--memory', str(self._ram), '--cpuexecutioncap', str(self._cpucap), '--cpus', str(self._cores), '--ioapic', 'on']
		subprocess.call( command )
		#os.system( command )
		self._parent.closeCommand('start')
		os.system('VBoxHeadless -s "%s" -e TCP/Ports=%d' % (machinename,port) )
		

	def run(self):
		if not self.__check_if_image_exists(): self.__download_image()
		self.__prepare_machine_2_run()
		if self._osimage_uniqueid not in self.__get_machines_list():
			self.__setup_machine(self._osimage_uniqueid, self._image_path)

		
		self.__run_machine( self._osimage_uniqueid )
		


	def stopMachine(self):
		if self._isclosing: return
		self._isclosing = True

		command = ['VBoxManage', 'controlvm', self._osimage_uniqueid, 'poweroff']
		subprocess.call( command )
		#command = ['VBoxManage', 'unregistervm', '--delete', self._osimage_uniqueid]
		#subprocess.call( command )
	
		self._parent.closeCommand('stop')
		self.terminate()
		del self._parent._threads[self._command_id]

		
	def pauseMachine(self):
		if self._isclosing: return
		self._isclosing = True

		command = ['VBoxManage', 'controlvm', self._osimage_uniqueid, 'savestate']
		subprocess.call( command )

		
		params = { 'uniqueid': self._parent._uniqueid }
		files  = { os.path.basename(self._image_path): self._image_path }

		utils.htttpPost( self._parent._ws_host, '/ws/virtualslave/uploadimage/', params, files )
		
		#command = ['VBoxManage', 'unregistervm', '--delete', self._osimage_uniqueid]
		#subprocess.call( command )

		self._parent.closeCommand('stop')

		self.terminate()
		del self._parent._threads[self._command_id]

