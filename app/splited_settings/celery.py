import os
from celery.schedules import crontab
""" 
Celery
 """

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
# CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Paris'