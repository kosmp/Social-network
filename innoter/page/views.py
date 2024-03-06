from post.serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Page
from .paginations import CustomPageNumberPagination
from .permissions import (
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
    IsPageOwner,
)
from .serializers import PageSerializer
from .utils import get_user_info


class PageViewSet(ModelViewSet):
    queryset = Page.objects.all()

    serializer_class = PageSerializer
    pagination_class = CustomPageNumberPagination

    permission_classes_by_action = {
        "create": [IsAuthenticated],
        "destroy": [IsAuthenticated, IsAdminOrIsOwnerOrIsModeratorOfTheOwner],
        "retrieve": [IsAuthenticated],
        "list": [IsAuthenticated],
        "update": [IsAuthenticated, IsPageOwner],
        "partial_update": [IsAuthenticated, IsPageOwner],
    }

    def perform_create(self, serializer):
        user_data = get_user_info(self.request)
        serializer.save(
            user_id=user_data.get("user_id", None),
            owner_group_id=user_data.get("group_id", None),
        )

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        queryset = instance.posts.all()

        posts = self.paginate_queryset(queryset)
        serializer = PostSerializer(posts, many=True)

        response = self.get_paginated_response(serializer.data)

        page_data = self.get_serializer(instance).data
        page_data.update(response.data)

        response.data = page_data
        return response

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def post(self, request, pk=None):
        page = self.get_object()
        data = request.data.copy()
        data["page"] = page.id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
