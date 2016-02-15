import sys, os; sys.path.append("./");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from opencsp.models import Server
from crontab import CronTab


cron = CronTab(user=True)
cron.remove_all(comment='checkserver')


scripts_path = os.path.dirname(os.path.abspath(__file__))

for server in Server.objects.filter(server_active=True):
	command = os.path.join(scripts_path, 'check_for_new.py {0}'.format(server.pk))
	#print 'Install', command
	job = cron.new(command=command, comment='checkserver' )	
	job.setall('* * * * *')
	job.enable(True)


cron.write()
#print cron.render()