from django.urls import path
from .consumers import ChatConsumer, StatusConsumer

websocket_urlpatterns = [
    path("chat/chat-consumer/<room>/<from>/", ChatConsumer.as_asgi()),
    path("chat/status/<slug>/", StatusConsumer.as_asgi()),
]