from django.db import models


class MessageStatusChoices(models.TextChoices):
    RECEIVED = "received", "Received"
    SENT = "sent", "Sent"
