import httplib, os, random


def htttpPost(hostname, urlpath, parameters, files={}):
	"""
	streaming a file using http post
	"""
	
	boundary  = "----------------------------%s" % random.getrandbits(48)
	separator = '--' + boundary + '\r\n'
	
	total_size = 0
	data = []
	for key, value in parameters.items():
		content = separator+'Content-Disposition: form-data; name="%s"\r\n\r\n%s' % (key, value)
		total_size += len(content)
		data += [ content ]

	for key, value in files.items():
		content = separator+'Content-Disposition: form-data; name="file"; filename="%s"\nContent-Type: application/octet-stream\r\n\r\n' % key
		total_size += len(content)
		total_size += os.path.getsize(value)
	total_size += len('\r\n'+separator)

	conn = httplib.HTTPConnection(hostname)
	conn.connect()
	conn.putrequest('POST', urlpath)
	conn.putheader('Content-Length', str(total_size))
	conn.putheader("Content-Type", "multipart/form-data; boundary=%s" % boundary)
	conn.endheaders()

	for msg in data: conn.send( msg )
	
	for key, value in files.items():
		infile = open(value, 'rb')
		content = separator+'Content-Disposition: form-data; name="file"; filename="%s"\nContent-Type: application/octet-stream\r\n\r\n' % key
		conn.send(content)
		while True:
			chunk = infile.read(1024)
			if not chunk: break
			conn.send(chunk)
	conn.send('\r\n'+separator)

	resp = conn.getresponse()
	return resp