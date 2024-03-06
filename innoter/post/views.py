from page.models import Follower
from page.utils import get_user_info
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Like, Post
from .permissions import IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost, IsAuthenticated
from .serializers import PostSerializer


class PostViewSet(mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
    queryset = Post.objects.all()

    serializer_class = PostSerializer

    permission_classes_by_action = {
        "update": [IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost],
        "partial_update": [IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost],
        "destroy": [IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost],
    }

    def get_permissions(self):
        try:
            return [
                permission()
                for permission in self.permission_classes_by_action[self.action]
            ]
        except KeyError:
            return [permission() for permission in self.permission_classes]

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user_id = get_user_info(self.request).get("user_id", None)
        response = None
        if Like.objects.like_post(post, user_id):
            response = Response({"message": f"You've liked post {post.id}."})
        else:
            response = Response({"message": f"You've already liked post {post.id}."})
        return response

    @action(detail=True, methods=["patch"], permission_classes=[IsAuthenticated])
    def remove_like(self, request, pk=None):
        post = self.get_object()
        user_id = get_user_info(self.request).get("user_id", None)
        response = None
        if Like.objects.remove_like_post(post, user_id):
            response = Response(
                {"message": f"You've removed like from post {post.id}."}
            )
        else:
            response = Response({"message": f"Post {post.id} wasn't liked yet by you."})
        return response


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_data = get_user_info(self.request)
        following_pages = Follower.objects.filter(
            user_id=user_data.get("user_id", None)
        ).values_list("page_id", flat=True)
        return Post.objects.filter(page__in=following_pages).order_by("-created_at")
