from rest_framework.routers import DefaultRouter

from .views import TagsViewSet, TagViewSet

router = DefaultRouter()
router.register(r"tag", TagViewSet, basename="tag")
router.register(r"tags", TagsViewSet, basename="tags")

urlpatterns = router.urls
