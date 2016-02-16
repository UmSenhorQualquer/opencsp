from jfu.http import upload_receive, UploadResponse, JFUResponse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from opencsp import AVAILABLE_STORAGES
from django.http import HttpResponse, HttpResponseServerError
import simplejson, json, glob, os
from django.conf import settings
import Utils.tools as tools
import time, shlex



def sizeof_fmt(num):
	for x in ['bytes','KB','MB','GB']:
		if num < 1000.0: return "%3.1f%s" % (num, x)
		num /= 1000.0
	return "%3.1f%s" % (num, 'TB')






def createfolder(request):
	try:
		path = request.POST.get('path', '.')
		storage = AVAILABLE_STORAGES.get(request.user)
		success = storage.mkdir(path)
	except: success = False
	return HttpResponse(simplejson.dumps(success), "application/json")



@never_cache
@csrf_exempt
def browsefiles(request):
	path = request.REQUEST.get('p', '/')
	backfolder = request.REQUEST.get('backfolder', 'true') == 'true'
	
	storage = AVAILABLE_STORAGES.get(request.user)


	rows = []
	if path!='/' and path!='//' and backfolder:
		link = """<a href='javascript:openFolder("/{0}")' >..</a>""".format( os.path.split(path[1:-1])[0] )
		rows.append({'values': [
			link,'','','',], 
			'small_thumb': '', 
			'big_thumb': '', 
			'url': '',
			'file': '..'
		})		
	

	for index, f in enumerate(storage.list(path)):
		rows.append({'values': [
				"""<a target='_blank' href='{0}' >{1}</a>""".format( f.open_link, f.filename ),
				sizeof_fmt( f.size ), 
				f.lastmodified,
				"""<a href='javascript:removeFile("{0}",{1});' ><i class="glyphicon glyphicon-trash remove-button"></i></a>""".format( f.fullpath, index )
			], 
			'small_thumb': 	f.small_thumb, 
			'big_thumb': 	f.big_thumb, 
			'url': 			f.fullpath,
			'file': 		f.fullpath,
			'filename': 	f.filename
		})
	
	#Implement the filter
	querystring = request.REQUEST.get('q', '')
	for q in shlex.split(querystring):
		rows  = filter(lambda x: q in x['values'][0], rows)
	
	#Implement the sorting
	sortby = request.REQUEST.get('s', '')
	sorbylist = []
	for col in sortby.split(','):
		if col=='0': 	rows = sorted(rows, key=lambda x: x['values'][0])
		elif col=='-0': rows = sorted(rows, key=lambda x: x['values'][0], reverse=True)

		if col=='1': 	rows = sorted(rows, key=lambda x: x['values'][1])
		elif col=='-1': rows = sorted(rows, key=lambda x: x['values'][1], reverse=True)

		if col=='2': 	rows = sorted(rows, key=lambda x: x['values'][2])
		elif col=='-2': rows = sorted(rows, key=lambda x: x['values'][2], reverse=True)

	data = simplejson.dumps(rows)
	return HttpResponse(data, "application/json")

@never_cache
@csrf_exempt
def removefile(request):
	filename = request.POST.get('filename', None)
	if filename!=None:
		storage = AVAILABLE_STORAGES.get(request.user)
		success = storage.delete(filename)
	data = simplejson.dumps({})
	return HttpResponse(data, "application/json")


@never_cache
@require_POST
def upload_delete( request, filename ):
	success = True
	try:
		storage = AVAILABLE_STORAGES.get(request.user)
		success = storage.delete(filename)
	except: success = False
	return JFUResponse( request, success )

@never_cache
@require_POST
def upload( request ):
	path = request.REQUEST.get('path','/')

	files = upload_receive( request )
	if not isinstance(files, list): files = [files]
	data = files[0]; filename = os.path.join(path, str(data))

	storage = AVAILABLE_STORAGES.get(request.user)
	storage.put_file_contents(filename, data)
	fileinfo = storage.file_info( filename )
	
	file_dict = {
		'name' : 			fileinfo.filename,
		'size' : 			sizeof_fmt(fileinfo.size),
		'thumbnail_url': 	fileinfo.small_thumb,
		'url': 				fileinfo.open_link,
		'delete': 			'', #'delete_url': reverse('jfu_delete', kwargs = {'filename': str(data) }),
		'delete_type': 		'POST',
	}
	return UploadResponse( request, file_dict )