from django.conf.urls import patterns, include, url
from django.contrib import admin



from opencsp.plugins.OpenCSPPluginsManager import OPENCSP_PLUGINS
from opencsp.plugins.JobsList.JobsList import JobsList
from opencsp.plugins.MyServers.MyServers import MyServers
from opencsp.plugins.AppList.AppList import AppList
from django.views.generic.base import RedirectView

from django.conf import settings
from django.conf.urls.static import static
from opencsp.views import *
from filesbrowser.views import *
from webservices import urls as webservices_urls
from opencsp.plugins import urls as opencspPlugins_urls
from opencsp_api import urls as opencsp_api_urls


from opencsp.views import *
from filesbrowser.views import *

admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', index),
	
	url(r'^ws/', include(webservices_urls)),
	url(r'^plugins/', include(opencspPlugins_urls)),
	url(r'^api/', include(opencsp_api_urls)),
    
    url(r'^load/(?P<application>\w+)/batchfile/',AppList.batchfile),
    url(r'^load/(?P<application>\w+)/downloadbatchfile/',AppList.downloadbatchfile),
    url(r'^load/runbatchfile/',AppList.runbatchfile),
    
	url(r'^js/commands.js', commands_js),
    url(r'^load/(?P<application>\w+)/statemachine/diagram/', load_statemachine_image),
	url(r'^load/(?P<application>\w+)/', loadapplicationform),
	url(r'^load/(?P<application>[a-zA-Z._ 0-9]+)/', loadapplicationform),
	

	url(r'^run/(?P<application>\w+)/', runapplication),

	
	url(r'^createfolder/', createfolder ),
	url(r'^removefile/', removefile ),
	url(r'^browsefiles/', browsefiles),
	url(r'^browseservers/(?P<application>[a-zA-Z._ 0-9]+)/', browseappservers),
	#url(r'^browseservers/', browseservers),
	
	url(r'^server/(?P<server_id>\d+)/properties/update/', MyServers.updateServerProperties),
	url(r'^server/(?P<server_id>\d+)/properties/', MyServers.serverProperties),
	
	url(r'^servers/pause/', MyServers.savePauseServers),
	url(r'^servers/release/', MyServers.saveReleaseServers),
	url(r'^servers/start/', MyServers.startServers),

	url(r'^servers/reserve/save/', MyServers.saveReserveServers),
	url(r'^servers/reserve/', MyServers.reserveServers),


	url(r'^queue/(?P<application>[a-zA-Z._ 0-9]+)/(?P<server_id>\d+)/', sendjob2queue),
	

	url(r'^appdoc/(?P<application>[a-zA-Z._ 0-9]+)/(?P<image>[a-zA-Z._ 0-9]+)', load_documentation_image),

	url( r'upload/', upload, name = 'jfu_upload' ),
	url( r'^delete/(?P<filename>[a-zA-Z._ 0-9]+)$', upload_delete, name = 'jfu_delete' ),
	
    

    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^pyforms/', include('pyforms.web.django.urls') ),
)


if settings.DEBUG:
	urlpatterns = patterns('',
	url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
	url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns