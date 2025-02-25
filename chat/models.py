import shortuuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.SlugField(unique=True, default=shortuuid.uuid, editable=False)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="owned_chatrooms",
        null=True,
        blank=True,
    )
    admins = models.ManyToManyField(User, related_name="chat_room_admins", blank=True)
    participants = models.ManyToManyField(
        User, related_name="chat_room_participants", blank=True
    )
    is_private = models.BooleanField(default=True)
    image = models.ImageField(upload_to="room/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.ForeignKey(
        "Message",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="room_set_like_last",
    )

    @property
    def get_last_message(self):
        if not self.last_message:
            return "..."
        return self.last_message.content[:25] + "..."

    def __str__(self):
        return (
            f"{self.name} ({'Private' if self.is_private else 'Group'})"
            if not self.is_private
            else f"{self.participants.first()}  ->  {self.participants.last()}"
        )


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="sent_messages",
        null=True,
    )
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    contact = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contact_of"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("owner", "contact")

    def __str__(self):
        return f"{self.owner} -> {self.contact}"
