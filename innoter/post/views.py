from page.models import Follower
from page.utils import get_user_info
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Like, Post
from .serializers import PostSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    serializer_class = PostSerializer

    @action(detail=True, methods=["patch"])
    def like(self, request, pk=None):
        post = self.get_object()
        user_id = get_user_info(self.request).get("id")
        response = None
        if Like.objects.like_post(post, user_id):
            response = Response({"message": f"You like post {post.id}."})
        else:
            response = Response({"message": f"You are already liked post {post.id}."})
        return response

    @action(detail=True, methods=["patch"])
    def remove_like(self, request, pk=None):
        post = self.get_object()
        user_id = get_user_info(self.request).get("id")
        response = None
        if Like.objects.remove_like_post(post, user_id):
            response = Response({"message": f"You removed like from post {post.id}."})
        else:
            response = Response({"message": f"You are didn't liked post {post.id}."})
        return response


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        user_data = get_user_info(self.request)
        following_pages = Follower.objects.filter(
            user_id=user_data.get("user_id", None)
        ).values_list("page_id", flat=True)
        return Post.objects.filter(page__in=following_pages).order_by("-created_at")
