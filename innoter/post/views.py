from page.models import Follower
from rest_framework import mixins, viewsets
from rest_framework.viewsets import ModelViewSet

from .models import Post
from .serializers import PostSerializer
from .utils import get_user_info


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()

    serializer_class = PostSerializer


class FeedViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = get_user_info(self.request)
        following_pages = Follower.objects.filter(user_id=user["id"]).values_list(
            "page_id", flat=True
        )
        return Post.objects.filter(page__in=following_pages).order_by("-created_at")
