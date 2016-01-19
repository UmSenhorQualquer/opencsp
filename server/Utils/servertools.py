from django.contrib.auth.models import User
from django.conf import settings
import os

def userFilePath(user, filename):
	userfolder = os.path.join(settings.MEDIA_ROOT,'uploads', user.username)
	if not os.path.exists(userfolder): os.makedirs(userfolder)
	return os.path.join( userfolder, filename)

