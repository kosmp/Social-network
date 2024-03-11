import pytest
from page.models import Page
from page.permissions import (
    IsAdmin,
    IsAdminOrIsModeratorOfThePageOwner,
    IsAdminOrIsOwnerOrIsModeratorOfTheOwner,
    IsAuthenticated,
    IsModerator,
    IsModeratorOfThePageOwner,
    IsPageOwner,
)


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
