from page.models import Page
from page.paginations import CustomPageNumberPagination
from page.serializers import PageSerializer
from rest_framework import mixins, viewsets

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Page.objects.all()

        filter_by_name = self.request.query_params.get("filter_by_name")
        if filter_by_name:
            queryset = queryset.filter(tags__name=filter_by_name)

        return queryset
