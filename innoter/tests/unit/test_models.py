import pytest
from page.models import Follower, Page
from post.models import Like, Post
from tag.models import Tag


@pytest.mark.django_db
class TestModels:
    def test_tag_creation(self, tag):
        assert Tag.objects.count() == 1

    def test_page_creation(self, page):
        assert Page.objects.count() == 1

    def test_post_creation(self, post):
        assert Post.objects.count() == 1

    def test_follower_creation(self, follower):
        assert Follower.objects.count() == 1

    def test_like_creation(self, like):
        assert Like.objects.count() == 1
