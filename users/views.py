from django.contrib.auth import authenticate
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render

from .forms import SignupForm


def can_not_be_logged(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        return func(request, *args, **kwargs)

    return wrapper


def check_username(request, username):
    if User.objects.filter(username=username).exists():
        return JsonResponse({"status": False})
    return JsonResponse({"status": True})


def check_email(request, email):
    if User.objects.filter(email=email).exists():
        return JsonResponse({"status": False})
    return JsonResponse({"status": True})


@can_not_be_logged
def signup(request):
    ctx = {}

    if request.method == "POST":
        form = SignupForm(request.POST)
        print(form.errors)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = SignupForm()

    ctx["form"] = form
    return render(request, "users/signup.html", ctx)


@can_not_be_logged
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            dj_login(request, user)
            return redirect("home")
    return render(request, "users/login.html")


@login_required
def logout(request):
    if request.method == "POST":
        dj_logout(request)

    return render(request, "users/logout.html")
