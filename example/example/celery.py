import os

import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')

app = celery.Celery('example')  #pylint: disable=invalid-name

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
