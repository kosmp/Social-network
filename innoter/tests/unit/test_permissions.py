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


@pytest.mark.django_db
class TestPermissions:
    def test_jwt_auth(self, mocker, admin_request, moderator_request, user_request):
        view = mocker.Mock()

        assert IsAuthenticated().has_permission(user_request, view) is True
        assert IsAuthenticated().has_permission(admin_request, view) is True
        assert IsAuthenticated().has_permission(moderator_request, view) is True

    def test_is_admin(self, mocker, admin_request):
        view = mocker.Mock()

        assert IsAuthenticated().has_permission(admin_request, view) is True

    def test_is_moderator(self, mocker, moderator_request):
        view = mocker.Mock()

        assert IsAuthenticated().has_permission(moderator_request, view) is True
