from django.shortcuts import render_to_response
from django.template import RequestContext
from opencsp.models import AlgorithmSubject
from django.core.urlresolvers import reverse
from  django.core.urlresolvers import NoReverseMatch
import inspect, sys

class LayoutPositions:
	TOP = 0
	BOTTOM = 1
	WINDOW = 2
	JSON = 3
	NEW_WINDOW = 4
	NEW_TAB = 1
	HOME = 0

class StringArgType(object):
	@staticmethod
	def argument(name): return "(?P<%s>[a-zA-Z._ 0-9]+)" % name

class IntArgType(object):
	@staticmethod
	def argument(name): return "(?P<%s>\d+)" % name





class OpenCSPPlugin(object):
	_menuOrder = 1000

	static_files = []

	@staticmethod
	def top_view(request): return None

	@staticmethod
	def bottom_view(request): return None

	@property
	def label(self): return getattr(self.__class__, '%s_label' % self.__class__.__name__)

	@property
	def hash(self): return self._hash

	@property
	def top_url(self): 
		try:
			if hasattr(self,'top_view_url'): return reverse("%s-top" % self._hash )
		except NoReverseMatch: pass
		return None

	@property
	def bottom_url(self): 
		try:
			if hasattr(self,'bottom_view_url'): return reverse("%s-bottom" % self.hash )
		except NoReverseMatch: pass
		return None

	@property
	def views(self):
		result = []
		for name, item in inspect.getmembers(self.__class__, inspect.isfunction):
			if hasattr(self, '%s_argstype' % name ): result.append( item )
		result = list(set(result))
		return result


	@property
	def icon(self):
		if hasattr(self, '_icon'): return self._icon
		else: return None



	@property
	def JsFunction(self): return "run%s();" % self.__class__.__name__.capitalize()

	@property
	def anchor(self): return self.__class__.__name__.lower()

	@staticmethod
	def viewName(plugin, view): return "%s.%s" % (plugin.__name__, view.__name__)

	@staticmethod
	def viewURL(plugin, view):
		argstype 	= getattr(plugin, '%s_argstype' % view.__name__)
		args 		= [x for x in inspect.getargspec(view)[0][1:]]

		arguments = [view.__name__.lower()]
		for argtype, arg in zip(argstype, args):
			arguments.append( argtype.argument(arg) )
		url = "/".join(arguments)

		return "%s/%s/" % ( plugin.__name__.lower(), url )

	@staticmethod
	def viewJsURL(plugin, view):
		args 		= [x for x in inspect.getargspec(view)[0][1:]]

		arguments = [view.__name__.lower()]
		for arg in args:
			arguments.append( '"+%s+"' % arg )
		url = "/".join(arguments)

		return "%s/%s/" % ( plugin.__name__.lower(), url )

	@staticmethod
	def viewJsAnchor(plugin, view):
		prefix 	= plugin.__name__.lower()
		sufix 	= view.__name__.lower()
		if prefix==sufix: return prefix
		return "%s-%s" % (prefix, sufix)

	@staticmethod
	def viewBreadcrumbs(plugin, view):
		breadcrumbs = []
		function = getattr(plugin, plugin.__class__.__name__)
		linkname = getattr(plugin, '%s_label' % function.__name__) if hasattr(plugin, '%s_label' % function.__name__ ) else function.__name__

		if view.__name__!=plugin.__class__.__name__:
			breadcrumb = [
				linkname, 
				OpenCSPPlugin.viewJsAnchor(plugin.__class__, function), 
				plugin.JsFunction
			]
			breadcrumbs.append(breadcrumb)

		if hasattr(plugin, '%s_breadcrumbs' % view.__name__ ):
			for function in getattr(plugin, '%s_breadcrumbs' % view.__name__ ):
				linkname = getattr(plugin, '%s_label' % function.__name__) if hasattr(plugin, '%s_label' % function.__name__ ) else function.__name__
				breadcrumb = [
					linkname, 
					OpenCSPPlugin.viewJsAnchor(plugin.__class__, view), 
					plugin.JsFunction
				]
				breadcrumbs.append(breadcrumb)
		
		return breadcrumbs
		#if plugin.__name__!=view.__name__:

				