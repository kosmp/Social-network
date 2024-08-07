from django.db import models
from page.managers import FollowerManager
from tag.models import Tag


class Page(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    description = models.CharField(max_length=300, default=None, blank=True, null=True)
    user_id = models.UUIDField(null=True, blank=True)
    owner_group_id = models.UUIDField(null=True, blank=True)
    image_url = models.URLField(default=None, blank=True, null=True)
    tags = models.ManyToManyField(Tag)
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(default=None, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["updated_at"]


class Follower(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user_id = models.UUIDField(null=False)

    objects = FollowerManager()
