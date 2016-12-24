import os
import sys
import django
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'analytics.settings'
from django.conf import settings

from threading import Timer


from datetime import datetime

from django.core.mail.message import EmailMessage

django.setup()
from analyticsApi.tasks.analyticsTask import syncAllProfilesPost,syncProfiles


def shedular_of_post():
    syncProfiles()
    syncAllProfilesPost()


class RepeatedTimer(object):

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


# it auto-starts, no need of rt.start()
runScheduler = RepeatedTimer(3600/2, shedular_of_post)
# shedular_of_post()
