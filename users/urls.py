from django.urls import path
from .views import signup, login, logout, check_username, check_email

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("check-username/<username>", check_username, name="check-username"),
    path("check-email/<email>", check_email, name="check-email"),
]
