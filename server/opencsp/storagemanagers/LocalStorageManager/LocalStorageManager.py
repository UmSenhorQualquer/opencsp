import Utils.owncloud as owncloud, os,shutil
from django.conf import settings
from RemoteFile import RemoteFile
from django.utils import timezone
import subprocess

def get_thumb(fileinfo, size=32):
	if fileinfo.file_type=='dir': return "/static/icons/folder{0}.png".format(size)

	file_extension = os.path.splitext( fileinfo.path )[1]

	if 	file_extension=='.avi' or \
		file_extension=='.mpg' or \
		file_extension=='.mp4': return '/static/icons/movie%d.png' % size

	if 	file_extension=='.png' or \
		file_extension=='.jpg' or \
		file_extension=='.jpeg':
		return '/static/icons/image%d.png' % size
	
	return '/static/icons/file%d.png' % size




class DefaultStorageManager(object):

	def __init__(self, user): self._user = user

	def __parseFile(self, f):
		fileobj = RemoteFile()
		fileobj.filename 		= f.get_name()
		fileobj.fullpath 		= f.path[:-1] if f.file_type=='dir' else f.path
		fileobj.size 			= int(f.attributes.get('{http://owncloud.org/ns}size', f.attributes.get('{DAV:}getcontentlength', 0) ))
		fileobj.lastmodified 	= f.attributes.get('{DAV:}getlastmodified', None)
		fileobj.type 			= f.file_type
		fileobj.small_thumb 	= get_thumb(f, 32)
		fileobj.big_thumb 		= get_thumb(f, 180)
		fileobj.download_link 	= 'javascript:openFolder("{0}")'.format(fileobj.fullpath) if f.file_type=='dir' else "{0}/index.php/apps/files/ajax/download.php?dir={1}&files={2}".format(settings.OWNCLOUD_LINK, f.get_path(), f.get_name() )
		fileobj.open_link 		= 'javascript:openFolder("{0}")'.format(fileobj.fullpath) if f.file_type=='dir' else "{0}/index.php/apps/files/ajax/download.php?dir={1}&files={2}".format(settings.OWNCLOUD_LINK, f.get_path(), f.get_name() )
		return fileobj

	def __user_path(self, path):
		return path
		
	def put_file_contents(self, remote_path, data):
		infile = open(self.__user_path(remote_path), 'wb')
		infile.write(data)
		infile.close()
		return True

	def put_file(self, remote_path, local_source_file, **kwargs):
		shutil.copy2(local_source_file, self.__user_path(remote_path) )
		return True

	def get_file_handler(self, path):
		infile = open(self.__user_path(path), 'rb')
		return infile

	def delete(self, path):
		if os.path.isfile( self.__user_path(path) ):
			os.remove( self.__user_path(path) )
		else:
			os.rmdir( self.__user_path(path) )
		return True

	def list(self, path):
		for f in os.listdir( self.__user_path(path) ):  yield self.file_info(f)

	def file_info(self, path):
		return self.__parseFile( os.stat( self.__user_path(path) ) )
		

	def mkdir(self, path):
		os.mkdir( self.__user_path( path) )
		return True

	def public_link(self, path): return None
		