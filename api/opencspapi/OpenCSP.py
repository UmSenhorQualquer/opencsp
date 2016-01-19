import requests, owncloud
from Job import Job
from Application import Application


class OpenCSP(object):


	def __init__(self, serverUrl, username, password):
		self._serverUrl = serverUrl
		self._username 	= username
		self._password 	= password
		self._storage 	= None

	@property
	def session(self):
		url = "{0}/accounts/login/".format(self._serverUrl)
		session = requests.session()
		session.keep_alive = True
		r0 = session.get(url)
		csrfmiddlewaretoken = session.cookies['csrftoken']

		payload = {'login': self._username, 'password': self._password, 'csrfmiddlewaretoken':csrfmiddlewaretoken.strip() }
		self._r1 = session.post(url, data=payload,cookies=r0.cookies)
		return session

	def get(self, url):
		return self.session.get(url,cookies=self._r1.cookies)

	def post(self, url, data):
		return self.session.post(url,cookies=self._r1.cookies, data=data)
	
	def list_applications(self):
		url = "{0}/api/applications/list/".format(self._serverUrl)
		r = self.get(url) 
		res = []
		for values in r.json():
			app = Application(self);
			app.load(values)
			res.append(app)
		return res

	def list_jobs(self, limit=30, username=None, application=None, state=None, 
			created=None, started=None, ended=None):
		url = "{0}/api/jobs/list/".format(self._serverUrl)

		data = { 'username':username, 'application':application, 'state':state }
		if created: data.update({'created':';'.join(created) })
		if started: data.update({'started':';'.join(started) })
		if ended: data.update({'ended':';'.join(ended)		 })
		r = self.post(url, data=data)
		res = []

		for values in r.json():
			job = Job(self)
			job.load(values)
			res.append(job)
		return res

	def __storage_url(self):
		url = "{0}/api/storate_url/".format(self._serverUrl)
		r = self.get(url)  
		return r.json()

	@property
	def storage(self):
		if self._storage is None:
			self._storage = oc = owncloud.Client(self.__storage_url())
			oc.login(self._username, self._password)
		return self._storage