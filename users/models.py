import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from .choices import StatusChoices


class User(AbstractUser):
    photo = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png",
        verbose_name="Profile Photo",
        null=True,
        help_text="Upload a profile photo (max 2MB, 1000x1000px)",
    )
    bio = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Biography",
        help_text="A short bio about yourself (max 255 characters)",
    )
    status = models.CharField(
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.OFFLINE,
        verbose_name="User Status",
        help_text="Current user status",
    )
    slug = models.SlugField(
        unique=True, default=uuid.uuid4, editable=False, null=True, blank=True
    )
