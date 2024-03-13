from page.utils import get_user_info
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return (
            user_data.get("user_id") is not None
            and user_data.get("group_id") is not None
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return user_data.get("role") == "admin"


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return user_data.get("role") == "moderator"


class IsPageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return str(obj.user_id) == user_data.get("user_id")


class IsModeratorOfThePageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return user_data.get(
            "role"
        ) == "moderator" and obj.owner_group_id == user_data.get("group_id")


class IsAdminOrIsOwnerOrIsModeratorOfTheOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return (
            user_data.get("role") == "admin"
            or str(obj.user_id) == user_data.get("user_id")
            or user_data.get("role") == "moderator"
            and obj.owner_group_id == user_data.get("group_id")
        )


class IsAdminOrIsModeratorOfThePageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return (
            user_data.get("role") == "admin"
            or user_data.get("role") == "moderator"
            and obj.owner_group_id == user_data.get("group_id")
        )
