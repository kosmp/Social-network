import pytest
from page.models import Follower, Page


@pytest.fixture
def page(mocker, user_token_payload):
    page_mock = mocker.MagicMock(spec=Page)
    page_mock.id = 1
    page_mock.user_id = user_token_payload.get("user_id")
    page_mock.owner_group_id = user_token_payload.get("group_id")
    page_mock.name = "test_page"
    page_mock.tags = [1]

    return page_mock


@pytest.fixture
def page_from_user_with_other_id(mocker, user_token_payload_with_other_user_id):
    page_mock = mocker.MagicMock(spec=Page)
    page_mock.id = 1
    page_mock.user_id = user_token_payload_with_other_user_id.get("user_id")
    page_mock.owner_group_id = user_token_payload_with_other_user_id.get("group_id")
    page_mock.name = "test_page"
    page_mock.tags = [1]

    return page_mock


@pytest.fixture
def page_from_moderator_with_other_group_id(
    mocker, moderator_token_payload_with_other_group_id
):
    page_mock = mocker.MagicMock(spec=Page)
    page_mock.id = 1
    page_mock.user_id = moderator_token_payload_with_other_group_id.get("user_id")
    page_mock.owner_group_id = moderator_token_payload_with_other_group_id.get(
        "group_id"
    )
    page_mock.name = "test_page"
    page_mock.tags = [1]

    return page_mock
