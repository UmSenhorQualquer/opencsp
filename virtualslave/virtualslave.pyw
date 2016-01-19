from uuid import getnode as get_mac
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import Qt
import psutil, mmap, urllib, subprocess
import sys, hashlib, json, os, zipfile
from urlparse import urljoin
from manager.MachineManager import MachineManager, utils

#from Crypto.Cipher import XOR


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    __version__ = 0.00
    
    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
      
        self.setIcon(QtGui.QIcon("icon.png"))
        self.iconMenu = QtGui.QMenu(parent)
        self.appabout = self.iconMenu.addAction("About")
        self.appexit = self.iconMenu.addAction("Exit")
        self.setupEvents()
        self.setContextMenu(self.iconMenu)

        self._ws_host = 'opencsp'
        self._ws_host = 'localhost:8000'
        self._ws_http = 'http://%s/' % self._ws_host
        self.__initConfiguration()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.__readCommand)
        self._timer.start(5000)

        self._threads = {}
    


    def __registerServer(self, macaddress, user, password, maxram, maxcpus):
        data2send = {
            'macaddress': get_mac(), 
            'username': user,
            'password': password, 
            'maxram': int(maxram),
            'maxcpus': int(maxcpus),
            'version': self.__version__
        }

        r = utils.htttpPost(
            self._ws_host,
            '/ws/virtualslave/register/',
            data2send )

        retreaveddata = json.loads(r.read())
        if retreaveddata.get('result', None)=='OK':
            return retreaveddata.get('uniqueid', None), None
        else:
            return None, retreaveddata.get('result', None)

    def __checkServerExists(self, uniqueid):
        data2send = {
            'macaddress': get_mac(), 
            'uniqueid': uniqueid,
            'version': self.__version__
        }
        r = utils.htttpPost(
            self._ws_host,
            '/ws/virtualslave/exists/',
            data2send )

        retreaveddata = json.loads( r.read() )
        return retreaveddata.get('result', None)=='OK'



    def __initConfiguration(self):
        if not self.__loadConfiguration():
            username, ok = QtGui.QInputDialog.getText(None, 'Login',  'Username:')
            if not ok: exit()
            password, ok = QtGui.QInputDialog.getText(None, 'Login',  'Password:', mode=QtGui.QLineEdit.Password)
            if not ok: exit()

            mem = psutil.virtual_memory()
            ram = (mem.total / 1024 / 1024)*0.8
            maxcups = psutil.NUM_CPUS
            if maxcups>1: maxcups = maxcups-1

            self._uniqueid, msg = self.__registerServer( get_mac(), str(username), str(password), ram, maxcups)
            if self._uniqueid==None:
                QtGui.QMessageBox.about(None, "Login failed", "Sorry, it was not possible to register this server.\nError message: %s" % msg)
                exit()
            
            self.__saveConfiguration()
        
    def __saveConfiguration(self):
		f = open('config.txt', 'wb'); 
		data = {'uniqueid': self._uniqueid, 'checksum':''}
		
		checksum = hashlib.md5(str(data).encode('utf-8')).hexdigest()
		data['checksum'] = checksum

		#key = str(get_mac()) + str(get_mac()) + str(get_mac())
		#key = key[:32]
		#obj = XOR.new( key )
		
		
		data = str(data)
		#data = obj.encrypt( data )

		f.write(data); f.flush();
		f.close()

    def __loadConfiguration(self):
        try:
            f = open('config.txt', 'rb'); txtdata = f.read(); f.close()
            #key = str(get_mac()) + str(get_mac()) + str(get_mac())
            #key = key[:32]
            #obj = XOR.new( key )
            #txtdata = obj.decrypt(txtdata)
            data = eval(txtdata)
            configFileCheckSum = data['checksum']
            data['checksum'] = ''
            checksum = hashlib.md5(str(data).encode('utf-8')).hexdigest()

            if configFileCheckSum!=checksum: return False
            self._uniqueid = data['uniqueid']
            return self.__checkServerExists(self._uniqueid)
        except:
            return False

    def __readCommand(self):
        print "Readcommand"

        data2send = {'uniqueid': self._uniqueid, 'version': self.__version__ }
        #try:
        r = utils.htttpPost(
            self._ws_host,
            '/ws/virtualslave/readcommand/',
            data2send )


        data = json.loads( r.read() )

        if data.get('result', None)=='OK':
            command = data.get('command', None)
            if command: 
                command_id = data.get('command_id', None)
                self.__executeCommand(command_id, command, data )
            
        #except Exception, e:
        #    print "error", e


    def closeCommand(self, command):
        data2send = {'uniqueid': self._uniqueid, 'command': command}
        r = utils.htttpPost(
            self._ws_host,
            '/ws/virtualslave/commitcommand/',
            data2send )

    def __downloadNewCode(self):
        url = urljoin(self._ws_http, '/static/virtualserver.zip')
        if not os.path.exists('tmp'): os.makedirs('tmp')
        zipfilename = os.path.join('tmp', 'virtualserver.zip')
        urllib.urlretrieve(url, zipfilename)
        with zipfile.ZipFile(zipfilename, "r") as z:
            z.extractall(".")

    def __restart(self):
        command = ['python', 'virtualslave.pyw']
        subprocess.Popen( command )
        exit()

    def __executeCommand(self,command_id, command_name, data):

        if command_name=='update':
            self.__downloadNewCode()
            self.closeCommand('update')
            self.__restart()
       
        if command_name=='start':
            print "command_id", command_id
            thread = MachineManager(self, command_id, data)
            self._threads[command_id] = thread
            thread.start()
            #The installOSImage will not be closed until the image stops running
            self._timer.setInterval(5000)
        else:

            refering_2_command_id = data.get('refering_2_command_id', None)
            thread = self._threads.get(refering_2_command_id, None)

            if thread is not None:
                if command_name=='stop':
                    thread.stopMachine()
                    self._timer.setInterval(60000)
                elif command_name=='pause':
                    thread.pauseMachine()
                    self._timer.setInterval(60000)
            else:
                self.closeCommand('stop')
        


    def activated(activationReason):
        QtGui.QSystemTrayIcon.activated(self, activationReason)

    def setupEvents(self):
        self.appabout.triggered.connect(self.showAbout)
        self.appexit.triggered.connect(self.appExit)
        
    def showAbout(self):
        QtGui.QMessageBox.information(QtGui.QWidget(), 
            self.tr("Fly DB printer."), self.tr("Developed in 2014 by CNP Software Platform"))
   
    def appExit(self):
        for key, thread in self._threads.items():
            print "closing job", key
            thread.stopMachine()
            thread.terminate()
        sys.exit()














if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv); trayIcon = SystemTrayIcon(); trayIcon.show()
    while True: app.exec_()
