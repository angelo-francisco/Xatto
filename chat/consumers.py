import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .models import Message, Room
from .utils import aget_something_by_slug

User = get_user_model()


class OnlineUserConsumer(AsyncWebsocketConsumer):
    """
    OnlineUserConsumer: AsyncWebsocketConsumer

    This websocket consumer allows us to change the user status (online, offile).
    When user connects it'll add user to the channel_group and set the status to "on",
    when disconnected it'll be set to "off".
    """

    async def connect(self):
        try:
            slug = self.scope["url_route"]["kwargs"]["slug"]

            self.user = await aget_something_by_slug(User, slug)
            self.group_name = "online_users"

            await self.accept()
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.update_user_status(self.user, "on")
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "user_status",
                    "status": "on",
                    "user_id": self.user.id,
                    "msg": "You're online",
                },
            )
        except Exception as e:
            print(e)
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        if hasattr(self, "user"):
            await self.update_user_status(self.user, "off")
            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "user_status",
                    "status": "off",
                    "last_seen": self.user.updated_at.isoformat(),
                    "user_id": self.user.id,
                    "msg": "You're offline",
                },
            )

    async def user_status(self, event):
        try:
            await self.send(
                text_data=json.dumps(
                    {
                        "user_id": event["user_id"],
                        "status": event["status"],
                        "message": event["msg"],
                        "last_seen": event.get("last_seen", ""),
                    },
                )
            )
        except Exception as e:
            print(e)

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.status = status
        user.save()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            room_slug = self.scope["url_route"]["kwargs"]["room"]
            from_slug = self.scope["url_route"]["kwargs"]["from"]

            self.room = await aget_something_by_slug(Room, room_slug)
            self.sender = await aget_something_by_slug(User, from_slug)

            if not self.room or not self.sender:
                await self.close()
                return

            await self.channel_layer.group_add(self.room.slug, self.channel_name)
            await self.accept()
        except Exception as e:
            print(e)

    async def disconnect(self, close_data):
        try:
            await self.channel_layer.group_discard(self.room.slug, self.channel_name)
        except Exception as e:
            print(e)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            content = data.get("content")

            if not content:
                return

            message = await self.create_message(self.room, self.sender, content)

            await self.channel_layer.group_send(
                self.room.slug, {"type": "message_handler", "message_id": message.id}
            )
        except Exception as e:
            print(e)

    async def message_handler(self, event):
        try:
            message = await self.get_message(event["message_id"])

            await self.send(
                text_data=json.dumps(
                    {
                        "content": message.content,
                        "timestamp": message.timestamp.isoformat(),
                        "sender": message.sender.username,
                    }
                )
            )
        except Exception as e:
            print(e)

    @database_sync_to_async
    def create_message(self, room, sender, content):
        return Message.objects.create(room=room, sender=sender, content=content)

    @database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.select_related("sender").get(id=message_id)
