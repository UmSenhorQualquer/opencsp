from opencsp.modelsfiles.Algorithm 			import AbstractAlgorithm
from opencsp.modelsfiles.AlgorithmSubject 	import AbstractAlgorithmSubject
from opencsp.modelsfiles.OSType 			import AbstractOSType
from opencsp.modelsfiles.OSImage 			import AbstractOSImage
from opencsp.modelsfiles.Cluster 			import AbstractCluster
from opencsp.modelsfiles.SatelliteServer 	import AbstractSatelliteServer
from opencsp.modelsfiles.Server 			import AbstractServer
from opencsp.modelsfiles.MasterServer 		import AbstractMasterServer
from opencsp.modelsfiles.UserSettings 		import AbstractUserSettings
from opencsp.modelsfiles.VirtualServer 		import AbstractVirtualServer
from opencsp.modelsfiles.ServerInstance 	import AbstractServerInstance
from opencsp.modelsfiles.Job 				import AbstractJob
from opencsp.modelsfiles.Task 				import AbstractTask

class AlgorithmSubject(AbstractAlgorithmSubject): 	pass
class Algorithm(AbstractAlgorithm): 				pass
class OSType(AbstractOSType): 						pass
class OSImage(AbstractOSImage): 					pass
class Cluster(AbstractCluster): 					pass
class SatelliteServer(AbstractSatelliteServer): 	pass
class Server(AbstractServer): 						pass
class MasterServer(AbstractMasterServer): 			pass
class UserSettings(AbstractUserSettings):			pass			
class VirtualServer(AbstractVirtualServer, Server):	pass
class ServerInstance(AbstractServerInstance):		pass
class Job(AbstractJob):								pass
class Task(AbstractTask):							pass