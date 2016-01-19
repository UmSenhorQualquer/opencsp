from django.conf.urls import patterns, url
from opencsp_api import views

urlpatterns = patterns('',
	url(r'^applications/list/', views.applications_list),
	url(r'^application/(?P<application>\w+)/params/', views.application_params),
	url(r'^jobs/list/', views.jobs_list),
	url(r'^job/(?P<job_id>\d+)/kill/', views.job_kill),
	url(r'^job/(?P<job_id>\d+)/output/', views.job_output),
	url(r'^job/(?P<job_id>\d+)/', views.job_get),
	url(r'^storage/url/', views.storate_url),
)