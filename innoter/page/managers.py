from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class FollowerManager(models.Manager):
    def follow_page(self, page, user_id):
        result = None
        try:
            self.get(page=page, user_id=user_id)
            result = False
        except ObjectDoesNotExist:
            self.create(page=page, user_id=user_id)
            result = True
        return result

    def unfollow_page(self, page, user_id):
        result = None
        try:
            follower = self.get(page=page, user_id=user_id)
            follower.delete()
            result = True
        except ObjectDoesNotExist:
            result = False
        return result
