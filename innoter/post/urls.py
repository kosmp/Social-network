from rest_framework.routers import DefaultRouter

from .views import FeedViewSet, PostViewSet

router = DefaultRouter()
router.register(r"post", PostViewSet)
router.register(r"feed", FeedViewSet, basename="feed")

urlpatterns = router.urls
