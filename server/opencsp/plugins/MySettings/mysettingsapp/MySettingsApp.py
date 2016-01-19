from django.core.exceptions import ObjectDoesNotExist
from pyforms import BaseWidget
from pyforms.Controls import ControlText
from pyforms.Controls import ControlButton
from opencsp.models import UserSettings
import uuid

class MySettingsApp(BaseWidget):
	
	def __init__(self):
		super(MySettingsApp,self).__init__('My settings')
		
		self._user_uid = ControlText('API password')
		self._new_uid_btn = ControlButton('New password')
		self._save_btn = ControlButton('Save')

		self._formset = [
			('_user_uid','_new_uid_btn'), 
			('_save_btn', ' ')]

		self._save_btn.value = self.__save_form
		self._new_uid_btn.value = self.__new_uid

	def initForm(self):
		try:
			usersettings = UserSettings.objects.get(user=self.httpRequest.user)
		except ObjectDoesNotExist:
			usersettings = UserSettings(user=self.httpRequest.user)
			usersettings.save()
		self._user_uid.value = usersettings.user_uniquecode

		return super(MySettingsApp, self).initForm()

	def __new_uid(self):
		self._user_uid.value = str(uuid.uuid1())

	def __save_form(self):
		try:
			usersettings = UserSettings.objects.get(user=self.httpRequest.user)
		except ObjectDoesNotExist:
			usersettings = UserSettings(user=self.httpRequest.user)

		usersettings.user_uniquecode = self._user_uid.value

		usersettings.save()

			