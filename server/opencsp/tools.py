


def fromImport(fromModule, importModule):
	moduleclass = __import__(fromModule, fromlist=[importModule])
	moduleclass =  getattr(moduleclass, importModule)
	return moduleclass