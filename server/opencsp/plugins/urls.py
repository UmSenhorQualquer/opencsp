from django.conf.urls import patterns, url
from opencsp.plugins.AppList.AppList import AppList
from opencsp.plugins.JobsList.JobsList import JobsList
from opencsp.plugins.MyServers.MyServers import MyServers
from opencsp.plugins.MyArea.MyArea import MyArea
from opencsp.plugins.AdminArea.AdminArea import AdminArea
from opencsp.plugins.AdminStats.AdminStats import AdminStats
from opencsp.plugins.MySettings.MySettings import MySettings

urlpatterns = patterns('',
	url(r'^applist/loadjob/(?P<application>[a-zA-Z._ 0-9]+)/(?P<job>\d+)/', AppList.LoadJob),
	url(r'^applist/load/(?P<application>[a-zA-Z._ 0-9]+)/', AppList.Load),
	url(r'^applist/applist/', AppList.AppList),
	url(r'^jobslist/check_job_parameters/(?P<job_id>\d+)/', JobsList.check_job_parameters),
	url(r'^jobslist/browsejobs/', JobsList.BrowseJobs),
	url(r'^jobslist/jobslist/', JobsList.JobsList),
	url(r'^jobslist/kill_job/(?P<job_id>\d+)/', JobsList.kill_job),
	url(r'^jobslist/check_output_files/(?P<job_id>\d+)/', JobsList.check_output_files),
	url(r'^jobslist/reset_job/(?P<job_id>\d+)/', JobsList.reset_job),
	url(r'^jobslist/run_job/(?P<job_id>\d+)/', JobsList.run_job),
	url(r'^jobslist/check_job_output/(?P<job_id>\d+)/', JobsList.check_job_output),
	url(r'^myservers/synchronize_server/(?P<server_id>\d+)/', MyServers.synchronize_server),
	url(r'^myservers/browseservers/', MyServers.BrowseServers),
	url(r'^myservers/myservers/', MyServers.MyServers),
	url(r'^myservers/installcluster/(?P<cluster_id>\d+)/', MyServers.InstallCluster),
	url(r'^myarea/myarea/', MyArea.MyArea),
	url(r'^adminarea/adminarea/', AdminArea.AdminArea),
	url(r'^adminstats/adminstats/', AdminStats.AdminStats),
	url(r'^mysettings/mysettings/', MySettings.MySettings),
)