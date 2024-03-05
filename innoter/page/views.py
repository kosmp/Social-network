from rest_framework.viewsets import ModelViewSet

from .models import Page
from .paginations import CustomPageNumberPagination
from .serializers import PageSerializer


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()

    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination
