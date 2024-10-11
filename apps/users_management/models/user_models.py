from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_advance_thumbnail.fields import AdvanceThumbnailField

from backend.utils.text_choices import UserType


def attachment_path(instance, filename):
    time = timezone.now().strftime("%Y%m%d%H%M%S")
    filename_update = f"{time}_{filename}"
    return "users/{username}/{file}".format(
        username=instance.username, file=filename_update
    )


class UserManage(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=15,
        unique=True,
        help_text=_(
            "Required. 15 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), unique=True)
    email_verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to=attachment_path, blank=True, null=True)
    profile_image_thumbnail = AdvanceThumbnailField(
        source_field="profile_image",
        upload_to=attachment_path,
        null=True,
        blank=True,
    )
    user_type = models.CharField(
        max_length=50, choices=UserType.choices, default=UserType.CUSTOMER
    )

    def __str__(self):
        return str(self.pk) + " - " + self.username + " - " + self.email

    def get_profile_image(self):
        return self.profile_image.url

    @property
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()
