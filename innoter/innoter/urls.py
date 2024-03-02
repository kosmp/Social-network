from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("api/v1/admin/", admin.site.urls),
    path("api/v1/page/", include("page.urls")),
    path("api/v1", include("post.urls")),
    path("api/v1/tag/", include("tag.urls")),
]
