from rest_framework.routers import DefaultRouter

from .views import PageViewSet

router = DefaultRouter()
router.register(r"", PageViewSet)

urlpatterns = router.urls
