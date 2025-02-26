from django.db import models


class StatusChoices(models.TextChoices):
    ONLINE = "on", "Online"
    OFFLINE = "off", "Offline"
