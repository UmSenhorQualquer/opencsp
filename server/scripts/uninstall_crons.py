import sys, os; sys.path.append("./");
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
import django; django.setup()
from opencsp.models import Server
from crontab import CronTab


cron = CronTab(user=True)
cron.remove_all(comment='checkserver')
cron.write()
#print cron.render()