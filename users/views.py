from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth import login as dj_login
from django.contrib.auth import logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignupForm
from .utils import can_not_be_logged

User = get_user_model()


@can_not_be_logged
def signup(request):
    ctx = {}

    if request.method == "POST":
        form = SignupForm(request.POST)

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
