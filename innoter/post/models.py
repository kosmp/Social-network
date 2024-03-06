from django.db import models
from page.models import Page
from post.managers import LikeManager


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    reply_to_post_id = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="replies", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.UUIDField(null=False)

    objects = LikeManager()
