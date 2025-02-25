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


# criar um consumer para o status do usuario
# ele vai ser colocado na home, e vai verificar se o username da room aberta é igual ao username q esta on ou off agr
# organizar codigo do projecto
# SEPARAR HTML, CSS, E JS

# consumer para as last_messages

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

            if self.room.is_private:
                self.online_group = "online_users"

                await self.channel_layer.group_add(self.online_group, self.channel_name)
                await self.update_user_status(self.user, "on")

                await self.channel_layer.group_send(
                    self.online_group,
                    {
                        "type": "user_status",
                        "status": "on",
                        "username": self.user.username,
                    },
                )
        except Exception as e:
            print(e)
            await self.close()

    async def disconnect(self, close_data):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

        if self.room.is_private:
            await self.channel_layer.group_discard(self.online_group, self.channel_name)

            await self.update_user_status(self.user, "off")

            await self.channel_layer.group_send(
                self.online_group,
                {
                    "type": "user_status",
                    "status": "off",
                    "last_seen": self.user.updated_at.isoformat(),
                    "username": self.user.username,
                },
            )

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

    async def user_status(self, event):
        try:
            await self.send(
                text_data=json.dumps(
                    {   
                        "type": "user-status",
                        "username": event["username"],
                        "status": event["status"],
                        "last_seen": event.get("last_seen", ""),
                    },
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

    @database_sync_to_async
    def update_user_status(self, user, status):
        user.status = status
        user.save()
