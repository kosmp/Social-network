import pytest
from page.permissions import (
    IsAdmin,
    IsAdminOrIsModeratorOfThePageOwner,
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
    IsModerator,
    IsModeratorOfThePageOwner,
    IsPageOwner,
)
from page.serializers import PageSerializer
from page.utils import get_user_info
from page.views import PageViewSet


@pytest.mark.django_db
class TestPermissions:
    def test_jwt_auth(self, mocker, admin_request, moderator_request, user_request):
        view = mocker.Mock()

        assert IsAuthenticated().has_permission(user_request, view) is True
        assert IsAuthenticated().has_permission(admin_request, view) is True
        assert IsAuthenticated().has_permission(moderator_request, view) is True

    def test_is_admin(self, mocker, admin_request, moderator_request, user_request):
        view = mocker.Mock()

        assert IsAdmin().has_permission(admin_request, view) is True
        assert IsAdmin().has_permission(moderator_request, view) is False
        assert IsAdmin().has_permission(user_request, view) is False

    def test_is_moderator(self, mocker, admin_request, moderator_request, user_request):
        view = mocker.Mock()

        assert IsModerator().has_permission(moderator_request, view) is True
        assert IsModerator().has_permission(admin_request, view) is False
        assert IsModerator().has_permission(user_request, view) is False

    def test_is_page_owner(
        self, user_request, user_token_payload, page, page_from_user_with_other_id
    ):
        assert IsPageOwner().has_object_permission(user_request, None, page) is True
        assert (
            IsPageOwner().has_object_permission(
                user_request, None, page_from_user_with_other_id
            )
            is False
        )

    def test_is_moderator_of_page_owner_group(
        self,
        admin_request,
        moderator_request,
        user_request,
        page,
        page_from_moderator_with_other_group_id,
    ):
        assert (
            IsModeratorOfThePageOwner().has_object_permission(
                moderator_request, None, page
            )
            is True
        )
        assert (
            IsModeratorOfThePageOwner().has_object_permission(
                moderator_request, None, page_from_moderator_with_other_group_id
            )
            is False
        )
        assert (
            IsModeratorOfThePageOwner().has_object_permission(user_request, None, page)
            is False
        )
        assert (
            IsModeratorOfThePageOwner().has_object_permission(admin_request, None, page)
            is False
        )
