from opencsp.models import Server

def all_connected_servers(server=None):
	#Return all the related servers
	all_servers = [] if server==None else [server]

	childs = Server.objects.filter(parent=server)
	for child in childs: all_servers.append(child)
	try:
		parent = server.parent
		if parent!=None:
			childs = Server.objects.filter(parent=parent)
			for child in childs: all_servers.append(child)
			all_servers.append( parent )
	except: pass
	return all_servers

