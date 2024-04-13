import logging

from page.models import Page
from page.paginations import CustomPageNumberPagination
from page.permissions import IsAuthenticated
from page.serializers import PageSerializer
from rest_framework import mixins, viewsets

from .models import Tag
from .serializers import TagSerializer

logger = logging.getLogger(__name__)


class TagViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "list": [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class TagsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    permission_classes_by_action = {
        "list": [IsAuthenticated],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        logger.info("Invoked get_queryset to get pages filtered by tag name.")
        queryset = Page.objects.all()

        filter_by_name = self.request.query_params.get("filter_by_name")
        if filter_by_name:
            queryset = queryset.filter(tags__name=filter_by_name)

        return queryset
