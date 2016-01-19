import os
from django.conf import settings
from django.apps import AppConfig
from opencsp.plugins.OpenCSPPluginsManager import *

class OpenCSPAppConfig(AppConfig):
	name = 'opencsp'
	verbose_name = "Open somputational scheduler platform"
	def ready(self):
		print("Updating plugins urls")
		OPENCSP_PLUGINS.export_urls_file(   os.path.join('opencsp','plugins','urls.py') )
		print("Updating plugins scripts")
		OPENCSP_PLUGINS.export_js_file(     os.path.join('static','js','commands.js') )
		OPENCSP_PLUGINS.copy_static_files(settings.STATIC_ROOT)