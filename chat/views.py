from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from .models import Contact, Message, Room

User = get_user_model()


@login_required
def chat_home(request):
    ctx = {}
    chats = Room.objects.filter(participants=request.user)

    ctx["chats"] = chats
    ctx["username"] = request.user.username
    return render(request, "chat/home.html", ctx)


@login_required
def get_chat_list(request):
    ctx = {}
    chats = Room.objects.filter(participants=request.user)

    ctx["chats"] = chats
    return render(request, "partials/chat-list.html", ctx)


@login_required
def check_contact_status(request):
    ctx = {}
    username = request.GET.get("username", "").strip()

    if not username:
        ctx["type"] = "empty"
    elif username == request.user.username:
        ctx["type"] = "error"
        ctx["msg"] = "You can't reach yourself"
    else:
        user_object = User.objects.filter(username=username)

        if not user_object.exists():
            ctx["type"] = "error"
            ctx["msg"] = "User doesn't exist"
        else:
            target_user = user_object.first()

            if not Contact.objects.filter(
                owner=request.user, contact=target_user
            ).exists():
                ctx["type"] = "success"
                ctx["msg"] = "This contact can be created!"
            else:
                ctx["type"] = "success"
                ctx["msg"] = "This contact already exists!"
            ctx["user_slug"] = target_user.slug

    return render(request, "partials/contact_status.html", ctx)


@login_required
def add_contact(request):
    return render(request, "partials/chat_add.html")


@login_required
def create_room(request):
    is_private = bool(request.GET.get("is_private"))
    other_user_slug = request.GET.get("other_user")

    if not other_user_slug:
        return HttpResponseBadRequest("Other User Slug is needed!")

    if is_private:
        other_user = get_object_or_404(User, slug=other_user_slug)
        contact = Contact.objects.create(owner=request.user, contact=other_user)

        room = Room.objects.create(is_private=True)
        room.participants.set([request.user, other_user])
    else:
        ...

    return redirect(reverse("chat-room", args=[room.slug]))


@login_required
def chat_room(request, slug):
    ctx = {}
    room = get_object_or_404(Room, slug=slug)
    messages = get_list_or_404(Message, room=room)

    ctx["chat"] = room
    ctx["user_slug"] = request.user.slug
    ctx["messages"] = messages
    return render(request, "chat/room.html", ctx)
