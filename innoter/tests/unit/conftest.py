import string
from random import choices
from uuid import uuid4

import pytest
from page.models import Follower, Page
from post.models import Like, Post
from tag.models import Tag


@pytest.fixture
def user_id():
    return uuid4()


@pytest.fixture
def tag():
    return Tag.objects.create(
        name="".join(choices(string.ascii_lowercase, k=9)),
    )


@pytest.fixture
def page(tag):
    page_obj = Page.objects.create(
        name="".join(choices(string.ascii_lowercase, k=9)),
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
