from page.utils import get_user_info
from rest_framework.permissions import BasePermission

from .models import Post


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return bool(
            user_data.get("user_id", None) is not None
            and user_data.get("group_id", None) is not None
        )


class IsAdminOrIsOwnerOrIsModeratorOfTheOwnerOfPost(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return bool(
            user_data.get("role", None) == "admin"
            or str(obj.page.user_id) == user_data.get("user_id", None)
            or user_data.get("role", None) == "moderator"
            and obj.page.owner_group_id == user_data.get("group_id", None)
        )
