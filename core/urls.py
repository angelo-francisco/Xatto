from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("chat/", include("chat.urls")),
        path("auth/", include("users.urls")),
        path("", RedirectView.as_view(url="/chat/")),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
