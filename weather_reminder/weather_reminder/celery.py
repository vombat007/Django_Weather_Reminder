import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weather_reminder.settings.prod')

app = Celery('weather_reminder')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule_filename = '/tmp/celerybeat-schedule'

app.conf.beat_schedule = {
    'fetch-weather-data': {
        'task': 'reminder.tasks.send_weather_notifications',
        'schedule': crontab(minute=0, hour='*'),
    },
}
