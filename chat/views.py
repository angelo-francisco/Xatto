from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from .models import Contact, Message, Room

User = get_user_model()


@login_required
def chat_home(request):
    user = get_user(request)
    chats = Room.objects.filter(participants=user)

    ctx = {"chats": chats, "username": user.username}
    return render(request, "chat/home.html", ctx)


@login_required
def get_chat_list(request):
    user = get_user(request)
    chats = Room.objects.filter(participants=user)

    ctx = {"chats": chats}
    return render(request, "partials/chat-list.html", ctx)


@login_required
def check_contact_status(request):
    user = get_user(request)
    contact_username = request.GET.get("username", "").strip()

    if not contact_username:
        ctx = {"type": "empty"}
    elif contact_username == user.username:
        ctx = {"type": "error", "msg": "You can't reach yourself"}
    else:
        user_object = User.objects.filter(username=contact_username)

        if not user_object.exists():
            ctx = {"type": "error", "msg": "User doesn't exist"}
        else:
            target_user = user_object.first()
            ctx = {"type": "success", "user_slug": target_user.slug}

            if not Contact.objects.filter(
                owner=request.user, contact=target_user
            ).exists():
                ctx["msg"] = "This contact can be created!"
            else:
                ctx["msg"] = "This contact already exists!"
    return render(request, "partials/contact_status.html", ctx)


@login_required
def add_contact(request):
    return render(request, "partials/chat_add.html")


@login_required
def create_room(request):
    is_private = bool(request.GET.get("is_private"))

    if is_private:
        other_user_slug = request.GET.get("other_user")

        if not other_user_slug:
            return HttpResponseBadRequest("Other User Slug is needed!")

        other_user = get_object_or_404(User, slug=other_user_slug)

        user = get_user(request)
        contact = Contact.objects.create(owner=user, contact=other_user)  # noqa

        room = Room.objects.create(is_private=True)
        room.participants.set([user, other_user])
    else:
        # 127.0.0.1:8000/chat/create-chat/?users=[slug1, slug2, slug3]
        users = request.GET.getlist("users")

    return redirect(reverse("chat-room", args=[room.slug]))


@login_required
def chat_room(request, slug):
    user = get_user(request)
    
    room = get_object_or_404(Room, slug=slug)
    messages = get_list_or_404(Message, room=room)

    context = {"chat": room, "user_slug": user.slug, "messages": messages}
    return render(request, "chat/room.html", context)
