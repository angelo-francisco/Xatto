import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.shortcuts import get_object_or_404

from .models import Message, Room

User = get_user_model()


@database_sync_to_async
def get_something_by_slug(model, slug):
    return get_object_or_404(model, slug=slug)


# consumer para as last_messages


class StatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            user_slug = self.scope["url_route"]["kwargs"]["slug"]

            self.user = await get_something_by_slug(User, user_slug)
            self.group_name = "online_users"

            await self.accept()

            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.change_status_to("on")

            await self.channel_layer.group_send(
                self.group_name,
                {
                    "type": "update_user_status",
                    "status": "on",
                    "userSlug": self.user.slug,
                },
            )
        except Exception as e:
            print("On connecting", e)
            await self.close()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        await self.change_status_to("off")

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "update_user_status",
                "status": "off",
                "last_seen": f"{naturalday(self.user.updated_at)}, {naturaltime(self.user.updated_at)}",
                "userSlug": self.user.slug,
            },
        )

    async def update_user_status(self, event):
        try:
            await self.send(
                text_data=json.dumps(
                    {
                        "userSlug": event["userSlug"],
                        "status": event["status"],
                        "last_seen": event.get("last_seen", ""),
                    },
                )
            )
        except Exception as e:
            print(e)

    @database_sync_to_async
    def change_status_to(self, status):
        self.user.status = status
        self.user.save()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            room_slug = self.scope["url_route"]["kwargs"]["room"]
            from_slug = self.scope["url_route"]["kwargs"]["from"]

            self.room = await get_something_by_slug(Room, room_slug)
            self.user = await get_something_by_slug(User, from_slug)

            if not self.room or not self.user:
                await self.close()
                return

            self.group_name = f"room_{self.room.slug}"

            await self.accept()

            await self.channel_layer.group_add(self.group_name, self.channel_name)
        except Exception as e:
            print(e)
            await self.close()

    async def disconnect(self, close_data):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            content = data.get("content")

            if not content:
                return

            message = await self.create_message(self.room, self.user, content)
            self.room.last_message = message

            await self.channel_layer.group_send(
                self.group_name, {"type": "message_handler", "message_id": message.id}
            )
        except Exception as e:
            print(e)

    async def message_handler(self, event):
        try:
            message = await self.get_message(event["message_id"])
            self.room.last_message = message

            await self.room.asave()

            await self.send(
                text_data=json.dumps(
                    {
                        "type": "message",
                        "content": message.content,
                        "timestamp": message.timestamp.isoformat(),
                        "username": message.sender.username,
                    }
                )
            )
        except Exception as e:
            print(e)

    @database_sync_to_async
    def create_message(self, room, user, content):
        return Message.objects.create(room=room, sender=user, content=content)

    @database_sync_to_async
    def get_message(self, message_id):
        return Message.objects.select_related("sender").get(id=message_id)
