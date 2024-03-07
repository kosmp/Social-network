from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class LikeManager(models.Manager):
    def like_post(self, post_id, user_id):
        _, created = self.get_or_create(post_id=post_id, user_id=user_id)
        return created

    def remove_like_post(self, post_id, user_id):
        result = None
        try:
            like = self.get(post_id=post_id, user_id=user_id)
            like.delete()
            result = True
        except ObjectDoesNotExist:
            result = False
        return result
