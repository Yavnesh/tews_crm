from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.beat
# from crm.tasks import sub
# from datetime import timedelta
# from celery.schedules import crontab
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tews_crm.settings')

# Create a Celery instance
app = Celery('tews_crm')
# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

# app.config_update({
#     'imports': ('crm.tasks',),  # Add 'crm.tasks' to imports
# })

# app.conf.beat_schedule = {
#     'every-10-second': {
#     'task':'crm.tasks.add1',
#     'schedule' :10,                  # timedelta(seconds=10),    #crontab(minute='*/1'),
#     'args' : (100,)
#     }
# }
# app.conf.beat_schedule = {
#     'every-10-second': {
#     'task':'crm.tasks.sub',
#     'schedule' :10,                  # timedelta(seconds=10),    #crontab(minute='*/1'),
#     'args' : (['100', '91'])
#     }
# }