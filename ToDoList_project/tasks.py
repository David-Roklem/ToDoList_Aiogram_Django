from datetime import timedelta
from celery.schedules import crontab
from django.utils import timezone
from api.models import Task
from . import celery_app
from .telegram_api import Telegram


celery_app.conf.beat_schedule = {
    "remind-every-5-min": {
        "task": "ToDoList_project.tasks.send_reminder",
        "schedule": crontab(minute="*/5"),
    },
}


def get_users_with_due_tasks():
    now = timezone.localtime()
    five_minutes_later = now + timedelta(minutes=5)
    users_with_due_tasks = list(
        Task.objects.filter(due_date__lte=five_minutes_later, due_date__gte=now)
        .values("user")
        .distinct()
    )
    return users_with_due_tasks


@celery_app.task(bind=True, max_retries=3, countdown=1)
def send_reminder(self):
    bot = Telegram()
    users_to_notify = get_users_with_due_tasks()
    for user in users_to_notify:
        telegram_id = user.get("user", 0)
        if telegram_id:
            bot.send_message(telegram_id, "У вас есть задачи с наступившим сроком выполнения!")
