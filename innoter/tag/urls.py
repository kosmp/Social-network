from rest_framework.routers import DefaultRouter

from .views import TagViewSet

router = DefaultRouter()
router.register(r"", TagViewSet)

urlpatterns = router.urls
