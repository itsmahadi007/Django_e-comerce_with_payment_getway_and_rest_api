from datetime import timedelta

from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from django.utils import timezone

from apps.ecommerce.utils.update_admin_about_stock_low import check_stock_and_notify_admins
from apps.notification_management.models import EmailQueue
from backend.utils.sent_mail import sent_mail
from backend.utils.text_choices import EmailSentStatus

logger = get_task_logger(__name__)


@shared_task(name="apps.notification_management.tasks.mail_blast")
def mail_blast():
    logger.info(f"\n ***** Mail_blast Started")

    EmailQueue.objects.filter(
        sent_status=EmailSentStatus.IN_PROGRESS,
        updated_at__lt=timezone.now() - timedelta(hours=1),
    ).update(sent_status=EmailSentStatus.PENDING)

    email_ids = EmailQueue.objects.filter(
        sent_status=EmailSentStatus.PENDING, attempt__lte=EmailQueue.MAX_ATTEMPTS
    )[:20].values_list("id", flat=True)

    EmailQueue.objects.filter(id__in=list(email_ids)).update(
        sent_status=EmailSentStatus.IN_PROGRESS
    )

    pending_emails = EmailQueue.objects.filter(id__in=list(email_ids))

    logger.info(f"\n ***** Mail_blast Pending Emails: {pending_emails.count()}")

    if pending_emails.exists():
        for email in pending_emails:
            print(f"\n ***** Mail_blast Email: {email.id}")

            recipient_list = email.to_email

            email.attempt += 1
            email.save()

            try:
                with transaction.atomic():
                    success = sent_mail(
                        subject=email.subject,
                        message=email.body,
                        to_email=[email],
                        from_email=email.from_email,
                    )

                    if success:
                        email.sent_status = EmailSentStatus.SENT
                        email.sent_at = email.updated_at = timezone.now()
                    else:
                        if email.attempt >= EmailQueue.MAX_ATTEMPTS:
                            email.sent_status = EmailSentStatus.FAILED
                        else:
                            email.sent_status = EmailSentStatus.PENDING
                        email.updated_at = timezone.now()
                    email.save()

            except Exception as e:
                logger.error(
                    f"Message Sending failed for EmailQueue object {email.id}. Reason: {e}"
                )

    logger.info(f"\n ***** Mail_blast Ended")


@shared_task(name="apps.notification_management.tasks.stock_update_mail")
def stock_update_mail():
    logger.info(f"\n ***** stock_update_mail Started")

    try:
        check_stock_and_notify_admins()
    except Exception as e:
        logger.error(f"Error in check_stock_and_notify_admins: {e}")

    logger.info(f"\n ***** stock_update_mail Ended")
