import json
from datetime import datetime, timedelta

from django_celery_beat.models import PeriodicTask, IntervalSchedule

def set_schedule(*args, **kwargs):
    '''Установка расписания задачи для деактевирования пользователя'''
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=60,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name='Importing contacts',
        task='ed_platform.tasks.user_deactivate',
        args=json.dumps(['arg1', 'arg2']),
        kwargs=json.dumps({
            'be_careful': True,
        }),
        expires=datetime.utcnow() + timedelta(seconds=60)
    )
