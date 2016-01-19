from django.conf.urls import patterns, include, url
from masterCommunication import *
from slavesCommunication import *
from virtualSlaveCommunication import *

urlpatterns = patterns('',
	url(r'^updatejob/', updatejob),
	url(r'^getjobs/', getjobs),
	url(r'^syncservers/', syncservers),
	url(r'^downloadfile/', downloadfile),
	url(r'^uploadfile/', uploadfile),
    
    url(r'^checknewjobs/(?P<server_id>\d+)/', checknewjobs),
    

    
    url(r'^virtualslave/exists/',      existsVirtualServer),
    url(r'^virtualslave/register/', 	 registeVirtualServer),
    url(r'^virtualslave/readcommand/', 	 readCommand),
    url(r'^virtualslave/commitcommand/',  commitCommand),
    url(r'^virtualslave/downloadimage/', downloadImage),
    url(r'^virtualslave/uploadimage/', uploadImage),
)