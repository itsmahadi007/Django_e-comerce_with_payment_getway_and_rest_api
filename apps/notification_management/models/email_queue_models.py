from django.db import models

from backend.utils.text_choices import EmailSentStatus, EmailPriorityStatus


class EmailQueue(models.Model):
    MAX_ATTEMPTS = 3

    event_name = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField()
    from_email = models.EmailField(null=True, blank=True)
    to_email = models.EmailField()
    attachment = models.FileField(upload_to="email_attachment", null=True, blank=True)
    priority = models.CharField(
        max_length=10,
        choices=EmailPriorityStatus.choices,
        default=EmailPriorityStatus.NORMAL,
    )
    added = models.DateTimeField(
        auto_now_add=True
    )
    sent_status = models.CharField(
        max_length=15,
        choices=EmailSentStatus.choices,
        default=EmailSentStatus.PENDING,
    )
    attempt = models.IntegerField(
        default=0
    )
    sent_at = models.DateTimeField(
        blank=True, null=True
    )
    context = models.JSONField(
        blank=True, null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "-priority",
            "-added",
        ]

    def __str__(self):
        return f"{self.pk} : {self.subject} : {self.to_email}: {self.priority} : {self.sent_status} : {self.updated_at}"


class ErrorSendingEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + " : " + str(self.active)
