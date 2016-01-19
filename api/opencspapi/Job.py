import simplejson

class Job(object):

    def __init__(self, api): 
        self._api           = api
        self.application    = None
        self.parameters     = None
        self.started        = None
        self.ended          = None
        self.state          = None
        self.uniqueid       = None
        self.pk             = None
        self.server         = None
        self.created        = None

    def load(self, values):
        self.application    = values['job_application']
        self.parameters     = values['job_parameters']
        self.started        = values['job_started']
        self.ended          = values['job_ended']
        self.state          = values['job_state']
        self.uniqueid       = values['job_uniqueid']
        self.pk             = values['job_id']
        self.server         = values['server']
        self.created        = values['job_created']

    def update(self): 
        if self.pk:
            url = "{0}/api/job/{1}/".format(self._api._serverUrl, self.pk)
            r = self._api.get(url)
            values = r.json()
            self.load(values)

    def kill(self):
        if self.pk:
            url = "{0}/api/job/{1}/kill/".format(self._api._serverUrl, self.pk)
            r = self._api.get(url)
            values = r.json()
            self.load(values)

            self.created        = None
            self.started        = None
            self.ended          = None
            self.state          = None
            self.uniqueid       = None
            self.pk             = None

            return True
        else:
            return False

    @property
    def isTerminated(self):
        if self.ended!=None:
            return True
        else:
            self.update()
            return self.ended!=None
    


    def submit(self, server=None):
        server = self.server.pk if self.server!=None else 0
        url = "{0}/queue/{1}/{2}/".format(self._api._serverUrl, self.application.appclass, server)
        r = self._api.post(url, data=simplejson.dumps(self.parameters))
        res = r.json()
        self.pk = res['job_id']
        return res
        
        
    @property
    def output(self):
        url = "{0}/api/job/{1}/output/".format(self._api._serverUrl, self.pk)
        r = self._api.session.get(url)
        return r.text
    
    def __unicode__(self):  return "job:"+str(self.pk)
    def __str__(self):      return self.__unicode__()
    def __repr__(self):     return self.__unicode__()
