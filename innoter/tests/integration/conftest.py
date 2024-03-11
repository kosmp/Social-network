import string
from random import choices
from uuid import uuid4

import pytest
from page.models import Follower, Page
from page.utils import get_user_info
from post.models import Like, Post
from rest_framework.test import APIClient
from tag.models import Tag


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def tag():
    return Tag.objects.create(
        name="".join(choices(string.ascii_lowercase, k=9)),
    )


@pytest.fixture
def page(tag, user_token_payload):
    page_obj = Page.objects.create(
        name="".join(choices(string.ascii_lowercase, k=9)),
        user_id=user_token_payload.get("user_id"),
        owner_group_id=user_token_payload.get("group_id"),
    )
    page_obj.tags.set([tag.id])
    return page_obj


@pytest.fixture
def post(page):
    return Post.objects.create(page=page, content="test_content")


@pytest.fixture
def follower(page, user_id):
    return Follower.objects.create(page_id=page, user_id=user_id)


@pytest.fixture
def like(post, user_id):
    return Like.objects.create(post_id=post, user_id=user_id)


@pytest.fixture
def setup_feed(user_request):
    page = Page.objects.create(
        name="".join(choices(string.ascii_lowercase, k=5)), user_id=uuid4()
    )
    post1 = Post.objects.create(
        page=page, content="".join(choices(string.ascii_lowercase, k=20))
    )
    post2 = Post.objects.create(
        page=page, content="".join(choices(string.ascii_lowercase, k=20))
    )
    follower = Follower.objects.create(
        page_id=page, user_id=get_user_info(user_request).get("user_id")
    )
    return page, post1, post2, follower
