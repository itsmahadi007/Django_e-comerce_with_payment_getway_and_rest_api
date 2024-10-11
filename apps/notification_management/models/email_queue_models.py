# Import necessary modules
from django.db import models

from backend.utils.text_choices import EmailSentStatus, EmailPriorityStatus


# Define the EmailQueue model
class EmailQueue(models.Model):
    MAX_ATTEMPTS = 3  # Maximum number of attempts to send an email

    event_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)  # Subject of the email
    body = models.TextField()  # Body of the email
    from_email = models.EmailField(null=True, blank=True)  # Sender email address
    to_email = models.EmailField()  # Recipient email address4
    attachment = models.FileField(upload_to="email_attachment", null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=EmailPriorityStatus.choices,  # Choices are given by the EmailPriorityStatus enum
        default=EmailPriorityStatus.NORMAL,  # Default priority is Normal
    )
    added = models.DateTimeField(
        auto_now_add=True
    )  # Timestamp for when the email was added to the queue
    sent_status = models.CharField(
        max_length=15,
        choices=EmailSentStatus.choices,  # Choices are given by the EmailSentStatus enum
        default=EmailSentStatus.PENDING,  # Default status is Pending
    )
    attempt = models.IntegerField(
        default=0
    )  # Counter for the number of attempts made to send the email
    sent_at = models.DateTimeField(
        blank=True, null=True
    )  # Timestamp for when the email was sent
    context = models.JSONField(
        blank=True, null=True
    )  # JSON context for the email, can be used in templates

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-priority",
            "-added",
        ]  # Default ordering for the EmailQueue is by priority and added timestamp

    def __str__(self):
        return f"{self.pk} : {self.subject} : {self.to_email}: {self.priority} : {self.sent_status} : {self.updated_at}"


class ErrorSendingEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + " : " + str(self.active)
