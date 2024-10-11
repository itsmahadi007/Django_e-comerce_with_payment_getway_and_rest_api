from django.db import models


class ECommerceBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        "users_management.UserManage",
        on_delete=models.CASCADE,
        related_name="created_%(class)ss",
    )
    updated_by = models.ForeignKey(
        "users_management.UserManage",
        on_delete=models.CASCADE,
        related_name="updated_%(class)ss",
        null=True,
        blank=True,
    )
