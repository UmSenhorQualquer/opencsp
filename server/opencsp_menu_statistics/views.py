from django.template 				import RequestContext
from django.views.decorators.csrf 	import csrf_exempt
from django.shortcuts 				import render_to_response
from django.conf 					import settings




def admin_stats(request):
	app = AdminStats._app_loader.createInstance('AdminStatsApp')
	app.httpRequest = request
	
	params = { 'application': 'AdminStatsApp', 'appInstance': app}
	params.update( app.initForm() )

	return render_to_response(
		os.path.join('opencsp', 'plugins', 'pyforms-template.html'),
		params, context_instance=RequestContext(request))

AdminStats_argstype = []
AdminStats_position = LayoutPositions.TOP
AdminStats_label 	= 'Statistics'
AdminStats_groups 	= ['Administrator', 'superuser']