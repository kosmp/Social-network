from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from innoter import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/page/", include("page.urls")),
    path("api/v1/", include("post.urls")),
    path("api/v1/tag/", include("tag.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
