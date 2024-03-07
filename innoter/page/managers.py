from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class FollowerManager(models.Manager):
    def follow_page(self, page_id, user_id):
        _, created = self.get_or_create(page_id=page_id, user_id=user_id)
        return created

    def unfollow_page(self, page_id, user_id):
        result = None
        try:
            follower = self.get(page_id=page_id, user_id=user_id)
            follower.delete()
            result = True
        except ObjectDoesNotExist:
            result = False
        return result
