# Import the necessary Django database transaction management
import json

from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from apps.notification_management.models.email_queue_models import EmailQueue

# Import the EmailQueue model and the mail_blast task function
from .sent_mail import sent_mail
from .text_choices import EmailPriorityStatus, EmailSentStatus


# email to user --> email_queue_overhauler --> mail_blast
# use this function from all the apis or places where you want to send email
def email_queue_overhauler(
    subject=None,  # Subject of the email
    body=None,  # Body of the email
    from_email=None,  # Email address the email will be sent from
    to_email=None,  # Email address the email will be sent to
    priority=None,  # Priority status of the email in the queue
    context=None,  # Contextual information for the email, possibly used in templates
    attachment=None,
):
    # Ensure to_email is a list
    if isinstance(to_email, QuerySet):
        to_email = list(to_email)
    elif not isinstance(to_email, list):
        to_email = [to_email]

    # Prepare EmailQueue instances for all emails in the list
    email_queue_instances = [
        EmailQueue(
            subject=subject,
            body=body,
            from_email=from_email,
            to_email=email,
            priority=priority,
            context=context,
            attachment=attachment if attachment else None,
        )
        for email in to_email
    ]

    with transaction.atomic():
        try:
            # Bulk create EmailQueue objects
            created_email_queue_objs = EmailQueue.objects.bulk_create(
                email_queue_instances
            )

            # If priority is HIGH, send the emails and update the relevant fields
            if priority == EmailPriorityStatus.HIGH:
                for email_queue_obj in created_email_queue_objs:
                    # print(email_queue_obj.to_email)
                    success = sent_mail(
                        subject=subject,
                        message=body,
                        to_email=email_queue_obj.to_email,
                        from_email=from_email,
                        attachment=attachment if attachment else None,
                    )
                    email_queue_obj.attempt += 1
                    if success:
                        email_queue_obj.sent_status = EmailSentStatus.SENT
                        email_queue_obj.sent_at = timezone.now()
                        email_queue_obj.save()

            # print(
            #     "created_email_queue_objs",
            #     created_email_queue_objs,
            #     len(created_email_queue_objs),
            #     priority,
            # )
            # for i in created_email_queue_objs:
            #     print(i.to_email)
            email_ids = [obj.id for obj in created_email_queue_objs]
            re = {"status": "added in queue", "email_ids": json.dumps(email_ids)}
            print(re)
            # return "added in queue"
        except Exception as e:
            print("In Queue remaster 91 ", str(e))
            transaction.set_rollback(True)
            # return {"status": ""}
