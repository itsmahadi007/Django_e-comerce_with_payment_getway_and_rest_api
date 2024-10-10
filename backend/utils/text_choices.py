from django.db import models
from django.utils.translation.trans_null import gettext_lazy


class UserType(models.TextChoices):
    ADMIN = "admin", gettext_lazy("Admin")
    CUSTOMER = "customer", gettext_lazy("Customer")
