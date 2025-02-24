import asyncio
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Message, Room

User = get_user_model()


@database_sync_to_async
def get_something_by_slug(model, slug):
    return get_object_or_404(model, slug=slug)


class OnlineUserConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            slug = self.scope["url_route"]["kwargs"]["slug"]

            self.user = await get_something_by_slug(User, slug)
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
            print(f"Erro ao conectar: {e}")
            await self.close()

    async def disconnect(self, close_code):
        if hasattr(self, "user"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
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
            # await asyncio.sleep(1)
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
            print("Error: ", e)

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.status = status
        user.save()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_slug = self.scope["url_route"]["kwargs"]["room"]
        from_slug = self.scope["url_route"]["kwargs"]["from"]

        self.room = await get_something_by_slug(Room, room_slug)
        self.sender = await get_something_by_slug(User, from_slug)

        if not self.room or not self.sender:
            await self.close()
            return

        await self.channel_layer.group_add(self.room.slug, self.channel_name)
        await self.accept()

    async def disconnect(self, close_data):
        await self.channel_layer.group_discard(self.room.slug, self.channel_name)

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
