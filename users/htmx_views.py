from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()


def check_username(request, username):
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": False})
    return JsonResponse({"status": True})


def check_email(request, email):
    if User.objects.filter(email=email).exists():
        return JsonResponse({"status": False})
    return JsonResponse({"status": True})
