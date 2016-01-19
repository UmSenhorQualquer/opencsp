from uuid import getnode as get_mac
from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4 import QtWebKit
from PyQt4 import Qt
import sys, hashlib, requests, json
from urlparse import urljoin
from manager.MachineManager import MachineManager


class SystemTrayIcon(QtGui.QSystemTrayIcon):

    _server = None
    _queue = []

    def __init__(self, parent=None):
        QtGui.QSystemTrayIcon.__init__(self, parent)
      
        self.setIcon(QtGui.QIcon("icon.png"))
        self.iconMenu = QtGui.QMenu(parent)
        self.appabout = self.iconMenu.addAction("About")
        self.appexit = self.iconMenu.addAction("Exit")
        self.setupEvents()
        self.setContextMenu(self.iconMenu)

        self.__initConfiguration()

        self._timer = QtCore.QTimer()
        self._timer.timeout.connect(self.__readCommand)
        self._timer.start(10000)

        self._thread = None
        self._currentVM = None

    def stop(self): self._timer.stop()
    def start(self): self._timer.start()

    def __initConfiguration(self):
        if not self.__loadConfiguration():
            url = urljoin('http://localhost:8000/', 'ws/virtualslave/register/')
            headers = {'content-type': 'application/json'}
            data2send = {'macaddress': get_mac()}
            r = requests.post(url, data=json.dumps(data2send), headers=headers)
            retreaveddata = r.json()
            if retreaveddata.get('result', None)=='OK':
                self._uniqueid = retreaveddata['uniqueid']
                self.__saveConfiguration()
        
    def __saveConfiguration(self):
        f = open('config.txt', 'w'); 
        data = {'uniqueid': self._uniqueid, 'checksum':''}
        checksum = hashlib.md5(str(data).encode('utf-8')).hexdigest()
        data['checksum'] = checksum
        f.write(str(data)); f.close()

    def __loadConfiguration(self):
        try:
            f = open('config.txt', 'r'); txtdata = f.read(); f.close()
            data = eval(txtdata)
            configFileCheckSum = data['checksum']
            data['checksum'] = ''
            checksum = hashlib.md5(str(data).encode('utf-8')).hexdigest()
            if configFileCheckSum!=checksum: return False
            self._uniqueid = data['uniqueid']
            return True
        except:
            return False

    def __readCommand(self):
        url = urljoin('http://localhost:8000/', 'ws/virtualslave/readcommand/')
        headers = {'content-type': 'application/json'}
        data2send = {'uniqueid': self._uniqueid}
        r = requests.post(url, data=json.dumps(data2send), headers=headers)
        data = r.json()
        if data.get('result', None)=='OK':
            command = data.get('command', None)
            if command: 
                command_id = data.get('command_id', None)
                command_name = data.get('command_name', None)
                command = eval(command)
                self.__executeCommand(command_id, command_name, command )

    def closeCommand(self, command_id):
        url = urljoin('http://localhost:8000/', 'ws/virtualslave/closecommand/')
        headers = {'content-type': 'application/json'}
        data2send = {'uniqueid': self._uniqueid, 'command_id': command_id}
        r = requests.post(url, data=json.dumps(data2send), headers=headers)
        self._thread = None
        self.start()

    def __executeCommand(self,command_id, command_name, command):
        if command_name=='installOSImage':
            print "-------------------"
            self._thread = MachineManager(self, command_id, command)
            print self._thread

        elif    command_name=='stop':
            
            if self._thread: 
            
                self._thread.terminated()
                self._thread.quit()
                self._thread = None

        elif    command_name=='pause':
            
            if self._thread: 
                self._thread.pause( command.get('user', None), self._uniqueid )    
                self._thread = None

        if self._thread: self._thread.start()
       


    def activated(activationReason):
        QtGui.QSystemTrayIcon.activated(self, activationReason)

    def setupEvents(self):
        self.appabout.triggered.connect(self.showAbout)
        self.appexit.triggered.connect(self.appExit)
        
    def showAbout(self):
        QtGui.QMessageBox.information(QtGui.QWidget(), 
            self.tr("Fly DB printer."), self.tr("Developed in 2014 by CNP Software Platform"))
   
    def appExit(self):
        if self._thread: 
            self._thread.quit()
            self._thread.terminated()
        sys.exit()














if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv); trayIcon = SystemTrayIcon(); trayIcon.show()
    while True: app.exec_()
