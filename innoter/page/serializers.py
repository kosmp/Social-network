from rest_framework.serializers import ModelSerializer

from .models import Page


class PageSerializer(ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"
        read_only_fields = ("user_id", "owner_group_id")
