from page.utils import get_user_info
from rest_framework.permissions import BasePermission


class IsAdminOrIsOwnerOrIsModeratorOfThePostOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return (
            user_data.get("role") == "admin"
            or str(obj.page.user_id) == user_data.get("user_id")
            or user_data.get("role") == "moderator"
            and obj.page.owner_group_id == user_data.get("group_id")
        )
