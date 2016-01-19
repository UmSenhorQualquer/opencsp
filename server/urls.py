from django.conf.urls import patterns, url
from AppList import AppList
from JobsList import JobsList
from MyServers import MyServers
from MyArea import MyArea

urlpatterns = patterns('',
	url(r'^applist/load/(?P<application>[a-zA-Z._ 0-9]+)/', AppList.Load),
	url(r'^applist/applist/', AppList.AppList),
	url(r'^applist/loadjob/(?P<application>[a-zA-Z._ 0-9]+)/(?P<job>\d+)/', AppList.LoadJob),
	url(r'^jobslist/browsejobs/', JobsList.BrowseJobs),
	url(r'^jobslist/jobslist/', JobsList.JobsList),
	url(r'^myservers/browseservers/', MyServers.BrowseServers),
	url(r'^myservers/myservers/', MyServers.MyServers),
	url(r'^myarea/myarea/', MyArea.MyArea),
)