import os
from datetime import datetime, timedelta

import jwt
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


####################################### permissions #######################################
@pytest.fixture
def is_authenticated_mock(mocker):
    mock = mocker.patch.object(IsAuthenticated, "has_permission")
    return mock


@pytest.fixture
def is_page_owner_mock(mocker):
    mock = mocker.patch.object(IsPageOwner, "has_object_permission")
    return mock


@pytest.fixture
def is_admin_mock(mocker):
    mock = mocker.patch.object(IsAdmin, "has_permission")
    return mock


@pytest.fixture
def is_moderator_mock(mocker):
    mock = mocker.patch.object(IsModerator, "has_permission")
    return mock


@pytest.fixture
def is_owner_moderator_mock(mocker):
    mock = mocker.patch.object(IsModeratorOfThePageOwner, "has_object_permission")
    return mock


@pytest.fixture
def is_owner_or_admin_or_moderator_mock(mocker):
    mock = mocker.patch.object(
        IsAdminOrIsOwnerOrIsModeratorOfTheOwner, "has_object_permission"
    )
    return mock


@pytest.fixture
def is_admin_or_owner_moderator_mock(mocker):
    mock = mocker.patch.object(
        IsAdminOrIsModeratorOfThePageOwner, "has_object_permission"
    )
    return mock


####################################### payloads #######################################
@pytest.fixture
def user_token_payload():
    return {
        "user_id": "d7d5a661-3571-4df2-9d66-ca063bbddd41",
        "role": "user",
        "group_id": "9f0a86f0-4d46-416b-bd59-d8c8ecc6a319",
        "is_blocked": False,
        "token_type": "access",
        "exp": datetime.now() + timedelta(minutes=10),
    }


@pytest.fixture
def user_token_payload_with_other_user_id():
    return {
        "user_id": "d7d5a661-3571-4df2-9d66-ca063bbddd67",
        "role": "user",
        "group_id": "9f0a86f0-4d46-416b-bd59-d8c8ecc6a319",
        "is_blocked": False,
        "token_type": "access",
        "exp": datetime.now() + timedelta(minutes=10),
    }


@pytest.fixture
def moderator_token_payload():
    return {
        "user_id": "d7d5a661-3571-4df2-9d66-ca063bbddd41",
        "role": "moderator",
        "group_id": "9f0a86f0-4d46-416b-bd59-d8c8ecc6a319",
        "is_blocked": False,
        "token_type": "access",
        "exp": datetime.now() + timedelta(minutes=10),
    }


@pytest.fixture
def moderator_token_payload_with_other_group_id():
    return {
        "user_id": "d7d5a661-3571-4df2-9d66-ca063bbddd46",
        "role": "moderator",
        "group_id": "1f0a86f0-4d46-416b-bd59-d8c8ecc6a175",
        "is_blocked": False,
        "token_type": "access",
        "exp": datetime.now() + timedelta(minutes=10),
    }


@pytest.fixture
def admin_token_payload():
    return {
        "user_id": "d7d5a661-3571-4df2-9d66-ca063bbddd41",
        "role": "admin",
        "group_id": "9f0a86f0-4d46-416b-bd59-d8c8ecc6a319",
        "is_blocked": False,
        "token_type": "access",
        "exp": datetime.now() + timedelta(minutes=10),
    }


####################################### tokens #######################################
def jwt_token(payload):
    return jwt.encode(
        payload, os.environ.get("JWT_SECRET_KEY"), algorithm=os.environ.get("ALGORITHM")
    )


@pytest.fixture
def user_jwt_token(user_token_payload):
    return jwt_token(user_token_payload)


@pytest.fixture
def moderator_jwt_token(moderator_token_payload):
    return jwt_token(moderator_token_payload)


@pytest.fixture
def admin_jwt_token(admin_token_payload):
    return jwt_token(admin_token_payload)


@pytest.fixture
def user_headers(user_jwt_token):
    return {
        "Authorization": f"Bearer {user_jwt_token}",
        "Content-Type": "application/json",
    }


####################################### headers #######################################
@pytest.fixture
def moderator_headers(moderator_jwt_token):
    return {
        "Authorization": f"Bearer {moderator_jwt_token}",
        "Content-Type": "application/json",
    }


@pytest.fixture
def admin_headers(admin_jwt_token):
    return {
        "Authorization": f"Bearer {admin_jwt_token}",
        "Content-Type": "application/json",
    }


####################################### requests with headers #######################################
@pytest.fixture
def user_request(mocker, user_headers):
    return mocker.Mock(headers=user_headers)


@pytest.fixture
def moderator_request(mocker, moderator_headers):
    return mocker.Mock(headers=moderator_headers)


@pytest.fixture
def admin_request(mocker, admin_headers):
    return mocker.Mock(headers=admin_headers)
