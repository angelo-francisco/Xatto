from django.urls import path

from .api import api
from .views import (
    chat_home,
    add_contact,
    check_contact_status,
    create_room,
    chat_room,
    get_chat_list,
)

urlpatterns = [
    path("", chat_home, name="home"),
    path("add-contact/", add_contact, name="add-contact"),
    path("check-contact-status/", check_contact_status, name="check-contact-status"),
    path("create-room/", create_room, name="create-room"),
    path("room/<slug>", chat_room, name="chat-room"),
    path("get-chat-list/", get_chat_list, name="chat-list"),
    path("api/", api.urls),
]
