from django.db import models
from django.utils.translation.trans_null import gettext_lazy


class UserType(models.TextChoices):
    ADMIN = "admin", gettext_lazy("Admin")
    CUSTOMER = "customer", gettext_lazy("Customer")


class VerificationForStatus(models.TextChoices):
    EMAIL_VERIFICATION = "email_verification", gettext_lazy("Email Verification")
    PASSWORD_RESET = "password_reset", gettext_lazy("Password Reset")
    NO_REQUEST = "no_request", gettext_lazy("No Request")


class EmailPriorityStatus(models.TextChoices):
    HIGH = "HIGH", gettext_lazy("High")  # High priority status
    NORMAL = "NORMAL", gettext_lazy("Normal")  # Normal priority status
    LOW = "LOW", gettext_lazy("Low")  # Low priority status


class EmailSentStatus(models.TextChoices):
    PENDING = "PENDING", gettext_lazy("Pending")  # Email is pending to be sent
    IN_PROGRESS = "IN_PROGRESS", gettext_lazy("In Progress")  # Email is in progress of being sent
    SENT = "SENT", gettext_lazy("Sent")  # Email has been sent successfully
    FAILED = "FAILED", gettext_lazy("Failed")  # Email failed to send
