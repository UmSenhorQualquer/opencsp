from opencspapi import OpenCSP




api = OpenCSP('http://localhost:8000', 'root', '123')

#for f in api.storage.list('/'): print f
#exit()


apps = api.list_applications()

#jobs = api.list_jobs(username='root', created=['2015-12-25', '2016-12-29'])
#jobs[0].update()


for app in apps:
	if app.appclass=='Elastix':
		break

job = app.createJobInstance()

print job.parameters
print job.submit()

print job.kill()