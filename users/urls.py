from django.urls import path
from .views import signup, login, logout
from .htmx_views import check_email, check_username


urlpatterns = [
    #  Django App views
    path("signup/", signup, name="signup"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),

    # Htmx views
    path("check-username/<username>", check_username, name="check-username"),
    path("check-email/<email>", check_email, name="check-email"),
]
