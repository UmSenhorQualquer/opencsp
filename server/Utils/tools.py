import os,sys, cv2, math, zipfile, numpy as np
from django.conf import settings



def getFileInSameDirectory(file, name):
	module_path = os.path.abspath(os.path.dirname(file))
	return os.path.join(module_path, name)


def groupImagesHorizontally( images, color=False ):
	final_width, final_height = sum([ x.shape[1] for x in images ]), max([ x.shape[0] for x in images ])
	if color:
	    final_image = np.zeros( (final_height, final_width, 3), dtype=np.uint8 )
	else:
	    final_image = np.zeros( (final_height, final_width), dtype=np.uint8 )
	cursor = 0
	for image in images:
	    final_image[0:image.shape[0],cursor:cursor+image.shape[1]] = image
	    cursor += image.shape[1]
	return final_image


def groupImagesVertically( images, color=False ):
	final_width, final_height = max([ x.shape[1] for x in images ]), sum([ x.shape[0] for x in images ])
	if color:
	    final_image = np.zeros( (final_height, final_width, 3), dtype=np.uint8 )
	else:
	    final_image = np.zeros( (final_height, final_width), dtype=np.uint8 )
	cursor = 0
	for image in images:
	    final_image[cursor:cursor+image.shape[0],0:image.shape[1]] = image
	    cursor += image.shape[0]
	return final_image


def groupImage( images,color=False ):
	himages = []
	for group in images:
	    if isinstance(group, list):
	        himages.append( groupImagesVertically(group,color) )
	    else:
	        himages.append( group )

	return groupImagesHorizontally(himages,color)


def get_object_class_path(obj):
	path = os.path.abspath(sys.modules[obj.__module__].__file__)
	head, tail = os.path.split(path)
	return head


def get_thumb(user, filename, size=32):
	filepath_without_extention, file_extension = os.path.splitext( filename )
	path_without_extention, _ = os.path.splitext( filename )
	_, file_without_extention = os.path.split( path_without_extention )

	if os.path.exists(path_without_extention+'.thumb%d' % size): 
		return os.path.join(settings.MEDIA_URL,'uploads',str(user),file_without_extention+'.thumb%d' % size)
	
	if file_extension=='.avi' or file_extension=='.mpg' or file_extension=='.mp4':
		os.system("ffmpegthumbnailer -i %s -s %d -o %s.thumb%d" % (filename, size, filepath_without_extention, size) )
		return os.path.join(settings.MEDIA_URL,'uploads',str(user),file_without_extention+'.thumb%d' % size)
	elif file_extension=='.png' or file_extension=='.jpg':
		os.system("convert -thumbnail %d %s %s.thumb%d" % (size, filename, filepath_without_extention, size) )
		return os.path.join(settings.MEDIA_URL,'uploads',str(user),file_without_extention+'.thumb_%d' % size)

	return '/static/data%d.png' % size


def lin_dist(p0, p1):   return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)


def zipdir(path, zippath):
	walkfiles = os.walk(path)
	zippath = zipfile.ZipFile(zippath, 'w')
	for root, dirs, files in walkfiles:
		print "ZIP64 ", os.path.join(root, filename), "->", zippath
		for filename in files: zippath.write(os.path.join(root, filename))