from __init__ import *


class Testapp(BaseWidget):
	
	def __init__(self):
		super(Testapp,self).__init__('Test')

		self._inputpoints 	= ControlFile('Input Points')
		self._transfparam0 = ControlDate('Transformation Parameters 0')
		self._transfparam1 = ControlPlayer('Bounding')
		self._outputfile 	= ControlText('Result file')
		self._table			= ControlList('Table')
		self._btn			= ControlButton('edit')

		self._formset = [ 
				'_inputpoints',
				('_transfparam0','_transfparam1'),
				('_outputfile','_btn'),
				'_table'
			]

		self._table.horizontalHeaders 	= ['Column 1', 'Column 2']
		self._table.selectEntireRow 	= True
		self._table.readOnly 			= False
		self._table.value 				= [['Row1'],['Row2'],['Row3','Row3-Col1']]


		self._btn.value = self.__clicked

	def __clicked(self):
		self._outputfile.value = 'ricardo'
		self._transfparam1.value = '/Videos Para Ricardo Testar 5.avi'
		
		#self._outputfile.value = self._table.value[self._table.mouseSelectedRowIndex][0]

##################################################################################################################
##################################################################################################################
##################################################################################################################

if __name__ == "__main__":	 pyforms.startApp( Testapp )