"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

from pyforms.web.django import ApplicationsLoader
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i*2qv#9fp3#@_=!&57dss)r86)gsqedu)5*iq*$lx*5arhr0m4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'suit_redactor',
    'pyforms.web.django',

    'sorl.thumbnail',
    'jfu',
    'opencsp',
    'webservices',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'sekizai.context_processors.sekizai',
    #'django_mobile.context_processors.flavour',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)


TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static", 'plugins'),
    os.path.join(BASE_DIR, "static", 'js'),
    os.path.join(BASE_DIR, "static", 'js', 'cookie'),
    os.path.join(BASE_DIR, "static", 'css'),
    os.path.join(BASE_DIR, "static", 'img'),
    os.path.join(BASE_DIR, "static", 'docs'),
    os.path.join(BASE_DIR, "static", 'bootstrap', 'js'),
    os.path.join(BASE_DIR, "static", 'bootstrap', 'css'),
    os.path.join(BASE_DIR, "static", 'bootstrap', 'fonts'),
)

FILEBROWSER_MAX_UPLOAD_SIZE =  2147483648
ACCOUNT_ACTIVATION_DAYS = 7
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
FILE_UPLOAD_PERMISSIONS = 0777

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'cloudprocessing',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': '123',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Lisbon'
USE_I18N = True
USE_L10N = True
USE_TZ = True

SCRIPTS_ROOT = os.path.join(BASE_DIR, "scripts")
MEDIA_ROOT =  os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'

OPENCSP_UNIQUE_ID           = '35316A35C8E34A3A97AC9947530E0A5D820EA2B9E4F44C7C841D24B5381A0067'
VIRTUALSERVER_VERSION       = 1.0

SUIT_CONFIG = {
    'ADMIN_NAME': 'Open Computational Schedule Platform'
}


PYFORMS_APPLICATIONS_PATH       = 'C:\\Users\\swp\\Documents\\opencsp\\server\\applications\\'
#PYFORMS_APPLICATIONS_PATH       = '/home/ricardo/subversion/applications/'
PYFORMS_APPLICATIONS            = ApplicationsLoader(PYFORMS_APPLICATIONS_PATH)

OPENCSP_JOBS_TERMINALOUTPUT     = os.path.join( MEDIA_ROOT,'jobsoutput' )
#OPENCSP_URL                     = 'http://localhost:8000'
OPENCSP_URL                     = 'http://opencsp.champalimaud.pt'
#OWNCLOUD_LINK                   = 'http://localhost'
OPENCSP_DEFAULT_STORAGE_MANAGER = 'LocalStorageManager'
OWNCLOUD_LINK                   = 'http://storage.champalimaud.pt'
OWNCLOUD_PASSWORD               = '4wNo8JptMWBS5GhMwPeAikUq7iPNShHfkapHR76bF5bPcpv4tHFL'
OPENCSP_STORAGE_AREAS_PATH      = 'C:\\Users\\swp\\Downloads'

LOGIN_URL                       = "/accounts/login/"
LOGIN_REDIRECT_URL              = '/'
#ACCOUNT_EMAIL_REQUIRED          = True
#ACCOUNT_EMAIL_VERIFICATION      = 'mandatory'
#SOCIALACCOUNT_QUERY_EMAIL       = True
SOCIALACCOUNT_AUTO_SIGNUP       = False
#ACCOUNT_CONFIRM_EMAIL_ON_GET    = True
SITE_ID                         = 1
PYFORMS_MODE = 'WEB'


# Time in seconds that OpenCSP will wait for a computer to start up 
# before sending the files for the Job
TIME_WAITTING_FOR_SERVER_TO_STARTUP      = 30
WAITING_TIME_BEFORE_SHUTTING_DOWN_SERVER = 60
WAITING_TIME_BEFORE_UNMOUNT_USER_AREA    = 180
USE_CRON_TO_RUN_JOBS                     = True