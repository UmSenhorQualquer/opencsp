from __init__ import *
import sys, os, shutil

import shutil
import zipfile
os.system('taskset -p 0xff %d' % os.getpid() )

class Transformix(BaseWidget):
	
	def __init__(self):
		super(Transformix,self).__init__('Transformix')

		self._inputpoints 	= ControlFile('Input Points')
		self._transfparam0 	= ControlFile('Transformation Parameters 0')
		self._transfparam1 	= ControlFile('Transformation Parameters 1')
		self._outputfile 	= ControlText('Result file')

		self._formset = [ 
				'_inputpoints',
				('_transfparam0','_transfparam1'),
				'_outputfile',
			]
		self._inputpoints.changed = self.__inputpoints_changed

			
	def __inputpoints_changed(self):  
		if self._outputfile.value==None or self._outputfile.value=='':
			head, tail = os.path.split(self._inputpoints.value)
			self._outputfile.value = "%s_out.ZIP" % os.path.splitext(tail)[0]



	def execute(self):
		#Create the output directory
		if os.path.exists('output'):	  shutil.rmtree('output')
		if not os.path.exists('output'):  os.makedirs('output')

		self.start_progress(2)
		
		head, tail 	= os.path.split(self._transfparam1.value)
		filename 	= os.path.join('output', tail)
		
		with open(self._transfparam1.value) as infile, open(filename, 'w') as outfile:
			for line in infile:
				if '(InitialTransformParametersFileName ' in line:
					outfile.write('(InitialTransformParametersFileName "{0}")\n'.format(self._transfparam0.value) )
				else:
					outfile.write(line)
		

		command = ['transformix','-def',self._inputpoints.value,'-tp',filename,'-out','output'] 
		print self.executeCommand( command )

		self.update_progress()
		
		

			
		workingDirectory = os.getcwd()
		# Zip the resulting files
		os.chdir(workingDirectory)
		tools.zipdir( 'output', os.path.join('output', self._outputfile.value) )
		#Remove all files from the output except the zip file
		for filename in os.listdir( os.path.join(workingDirectory, "output") ):
			path2file = os.path.join('output', filename)
			if os.path.isdir(path2file): shutil.rmtree( path2file )
			elif os.path.splitext(filename)[1].lower()!='.zip': os.remove( path2file )
		##########################################################
		self.update_progress()
		
		self.end_progress()
		self._executing = False
		



##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 pyforms.startApp( Transformix )