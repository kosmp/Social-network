from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Post


class PostSerializer(ModelSerializer):
    likes_count = serializers.SerializerMethodField(method_name="get_likes_count")

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("page",)

    def get_likes_count(self, obj):
        return obj.likes.count()
