# settings/celery.py
from celery.schedules import crontab

CELERY_TIMEZONE = "Asia/Dhaka"

CELERY_BEAT_SCHEDULE = {

    "mail_blasting": {
        "task": "apps.notification_management.tasks.mail_blast",
        "schedule": crontab(hour="*/3"),
    },
    "stock_update_mail": {
        "task": "apps.notification_management.tasks.stock_update_mail",
        "schedule": crontab(hour="23", minute="50"),
    },

}
