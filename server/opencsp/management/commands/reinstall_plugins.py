from django.core.management.base import BaseCommand, CommandError
from opencsp.plugins.OpenCSPPluginsManager import *

class Command(BaseCommand):
	help = 'Reinstall all the plugins'

	def handle(self, *args, **options):
		OPENCSP_PLUGINS.export_urls_file(   os.path.join('opencsp','plugins','urls.py') )
		OPENCSP_PLUGINS.export_js_file(     os.path.join('static','js','commands.js') )
