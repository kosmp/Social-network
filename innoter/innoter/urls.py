from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from innoter import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/page/", include("page.urls")),
    path("api/v1/", include("post.urls")),
    path("api/v1/tag/", include("tag.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
