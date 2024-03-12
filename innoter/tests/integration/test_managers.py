from page.models import Follower
from post.models import Like


class TestFollowerManager:
    def test_follow_page(self, page, user_id):
        Follower.objects.follow_page(page, user_id)
        assert Follower.objects.count() == 1
        Follower.objects.follow_page(page, user_id)
        assert Follower.objects.count() == 1

    def test_unfollow_page(self, page, user_id):
        Follower.objects.follow_page(page, user_id)
        Follower.objects.unfollow_page(page, user_id)
        assert Follower.objects.count() == 0
        Follower.objects.unfollow_page(page, user_id)
        assert Follower.objects.count() == 0


class TestLikeManager:
    def test_like_post(self, post, user_id):
        Like.objects.like_post(post, user_id)
        assert Like.objects.count() == 1
        Like.objects.like_post(post, user_id)
        assert Like.objects.count() == 1

    def test_remove_like_post(self, post, user_id):
        Like.objects.like_post(post, user_id)
        Like.objects.remove_like_post(post, user_id)
        assert Like.objects.count() == 0
        Like.objects.remove_like_post(post, user_id)
        assert Like.objects.count() == 0
