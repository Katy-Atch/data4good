import os
from pages.tasks import hello
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data4good.settings')

app = Celery('data4good')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))