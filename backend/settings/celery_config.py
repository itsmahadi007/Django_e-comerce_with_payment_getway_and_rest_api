# settings/celery.py
from celery.schedules import crontab

CELERY_TIMEZONE = "UTC"

CELERY_BEAT_SCHEDULE = {

    "mail_blasting": {
        "task": "apps.notification_management.tasks.mail_blast",
        "schedule": crontab(hour="*/3"),
    },

}
