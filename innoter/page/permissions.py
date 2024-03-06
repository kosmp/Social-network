from page.utils import get_user_info
from rest_framework.permissions import BasePermission


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return bool(
            user_data.get("user_id", None) is not None
            and user_data.get("group_id", None) is not None
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return bool(user_data.get("user_role", None) == "admin")


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        user_data = get_user_info(request)
        return bool(user_data.get("user_role", None) == "moderator")


class IsPageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return bool(str(obj.user_id) == user_data.get("user_id", None))


class IsModeratorOfThePageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return bool(
            user_data.get("role", None) == "moderator"
            and obj.owner_group_id == user_data.get("group_id", None)
        )


class IsAdminOrIsOwnerOrIsModeratorOfTheOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return bool(
            user_data.get("role", None) == "admin"
            and str(obj.user_id) == user_data.get("user_id", None)
            or user_data.get("role", None) == "moderator"
            and obj.owner_group_id == user_data.get("group_id", None)
        )


class IsAdminOrIsModeratorOfThePageOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_data = get_user_info(request)
        return bool(
            user_data.get("role", None) == "admin"
            or user_data.get("role", None) == "moderator"
            and obj.owner_group_id == user_data.get("group_id", None)
        )
