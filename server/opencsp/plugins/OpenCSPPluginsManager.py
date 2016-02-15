from django.conf.urls import patterns, url
from opencsp.plugins.OpenCSPPlugin import LayoutPositions, OpenCSPPlugin
import inspect, os, shutil
from django.template.loader import render_to_string
from opencsp.tools import fromImport

class OpenCSPPluginsManager(object):

	def __init__(self):
		self._plugins_list = []

	def append(self, plugin):
		self._plugins_list.append(plugin)

	def urls(self):
		params = ['']

		for plugin in self._plugins_list:
			if hasattr(plugin,'top_view_url'):
				params.append( 
					url( plugin.top_view_url, plugin.top_view, name="%s-top" % plugin._hash ) 
				)
			if hasattr(plugin,'bottom_view_url'):
				params.append( 
					url( plugin.bottom_view_url, plugin.bottom_view, name="%s-bottom" % plugin._hash )
				)
		
		return patterns( *params )

	@property
	def plugins(self): return [ plugin for plugin in self._plugins_list ]

	
	def menu(self, user=None): 
		res = []
		for plugin in self._plugins_list:
			add = False
			if hasattr(plugin, 'groups'):
				if 'superuser' in plugin.groups and user.is_superuser:  add = True
				if user.groups.filter(name__in=plugin.groups).exists():  add = True
			else:
				add = True

			if add: res.append(plugin)

		return res


	def copy_static_files(self, static_folder):

		static_folder = os.path.join(static_folder, 'plugins')
		if not os.path.exists(static_folder): os.makedirs(static_folder)

		for p in self.plugins:
			class_file = inspect.getfile(p)
			print os.path.realpath(class_file), '-'
			plugin_folder = os.path.dirname(os.path.realpath(class_file))
			print plugin_folder
			for filename in p.static_files:
				shutil.copyfile( os.path.join(plugin_folder, filename),os.path.join(static_folder, filename))


	def export_urls_file(self, filename):
		out = open(filename, 'w')

		out.write( "from django.conf.urls import patterns, url\n" )
		for p in self.plugins:
			out.write( "from opencsp.plugins.{0}.{0} import {0}\n".format(p.__name__) )
		out.write( "\n" )
		out.write( "urlpatterns = patterns('',\n" )
		for pluginClass in self.plugins:
			plugin = pluginClass()
			
			for view in plugin.views:
				if not hasattr(plugin, '%s_argstype' % view.__name__): continue

				out.write( "\turl(r'^%s', %s),\n" % ( 
					OpenCSPPlugin.viewURL(pluginClass, view), 
					OpenCSPPlugin.viewName(pluginClass, view) ) )
		out.write( ")" )

		out.close()

	def export_js_file(self, filename):
		out = open(filename, 'w')
		
		for pluginClass in self.plugins:
			plugin = pluginClass()
			for view in plugin.views:
				if not hasattr(plugin, '%s_position' % view.__name__): continue
				if not hasattr(plugin, '%s_argstype' % view.__name__): continue

				prefix = pluginClass.__name__.capitalize()
				sufix = view.__name__.capitalize()
				if prefix==sufix: sufix=''
				params = [x for x in inspect.getargspec(view)[0][1:]]
				out.write( "function run%s%s(%s){\n" % ( prefix, sufix, ','.join(params) ) )
				out.write( "\tloading();\n" )
				out.write( "\tactivateMenu('menu-%s');\n" % plugin.anchor )

				position = getattr(plugin, '%s_position' % view.__name__)
				
				label_attr = '{0}_label'.format(view.__name__)
				label = getattr(plugin, label_attr) if hasattr(plugin, label_attr) else view.__name__
				
				breadcrumbs = OpenCSPPlugin.viewBreadcrumbs(plugin, view)
				if position==LayoutPositions.TOP:
					out.write( "\tshowBreadcrumbs(%s, '%s');\n" % (breadcrumbs, label) )
				
				
				if hasattr(plugin, '%s_js' % view.__name__):
					javascript = getattr(plugin, '%s_js' % view.__name__)
					out.write( """\t%s\n""" % javascript )
				else:		
					if position==LayoutPositions.HOME:
						out.write( "\tclearInterval(refreshEvent);\n")
						out.write( """
						select_main_tab();
						$('#top-pane').load("/plugins/%s", function(response, status, xhr){
							if(status=='error') error_msg(xhr.status+" "+xhr.statusText+": "+xhr.responseText);
							not_loading();
						});\n""" % OpenCSPPlugin.viewJsURL(pluginClass, view) )
					
					if position==LayoutPositions.NEW_TAB:

						out.write('add_tab("{0}", "{1}", "/plugins/{2}");'.format(view.__name__, label, OpenCSPPlugin.viewJsURL(pluginClass, view)) )

					if position==LayoutPositions.WINDOW:
						out.write( "\tloading();" )
						out.write( "\t$('#opencsp-window').dialog('open');\n" )
						out.write( """\t$('#opencsp-window').load("/plugins/%s",function() {\n"""  %  OpenCSPPlugin.viewJsURL(pluginClass, view) )
						out.write( """\t\tnot_loading();$(this).scrollTop($(this)[0].scrollHeight);\n""" )
						out.write( """\t});\n""" )
					if position==LayoutPositions.NEW_WINDOW:
						out.write( """window.open('/plugins/%s');""" % OpenCSPPlugin.viewJsURL(pluginClass, view) )

				out.write( "}\n" )
				out.write( "\n" )
			
		views_ifs = []
		for pluginClass in self.plugins:
			plugin = pluginClass()
			for view in plugin.views:
				prefix = pluginClass.__name__.capitalize()
				sufix = view.__name__.capitalize()
				if prefix==sufix: sufix=''
				params = [x for x in inspect.getargspec(view)[0][1:]]
				views_ifs.append( "\tif(view=='%s') run%s%s.apply(null, params);\n" % ( OpenCSPPlugin.viewJsAnchor(pluginClass, view), prefix, sufix) )


		out.write( render_to_string( os.path.join('opencsp','commands.js'), {'views_ifs': views_ifs} ) )
		out.close()




###### Find the available plugins ####################################################
fileDirPath = os.path.dirname( os.path.abspath(__file__) )
availablePlugins = [ name for name in os.listdir(fileDirPath) if os.path.isdir(os.path.join(fileDirPath,name))]
plugins2Import = []
for plugin in availablePlugins:
	pluginClass = fromImport('opencsp.plugins.{0}.{0}'.format(plugin), plugin)
	plugins2Import.append(pluginClass)

###### Sort the plugins ##############################################################
plugins2Import = sorted(plugins2Import, key=lambda x: x._menuOrder)
###### Import the plugins ############################################################
OPENCSP_PLUGINS = OpenCSPPluginsManager()
for pluginClass in plugins2Import: OPENCSP_PLUGINS.append( pluginClass )
