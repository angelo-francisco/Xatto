from django.urls import path
from .consumers import OnlineUserConsumer, ChatConsumer

websocket_urlpatterns = [
    path("chat/update-user-status/<slug:slug>/", OnlineUserConsumer.as_asgi()),
    path("chat/chat-consumer/<room>/<from>/", ChatConsumer.as_asgi()),
]