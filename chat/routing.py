from django.urls import path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    path("chat/chat-consumer/<room>/<from>/", ChatConsumer.as_asgi()),
]