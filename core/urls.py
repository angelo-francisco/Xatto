from django.conf import settings
from django.urls import reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("chat.urls")),
        path("auth/", include("users.urls")),
        path("", RedirectView.as_view(url=reverse_lazy("home"))),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
