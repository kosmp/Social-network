import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

logger = logging.getLogger(__name__)


class LikeManager(models.Manager):
    def like_post(self, post, user_id):
        logger.info(
            f"Invoked like post with id {post.id} from manager for user with id {user_id}."
        )
        result = None
        try:
            like = self.get(post=post, user_id=user_id)
            like.delete()
            result = False
        except ObjectDoesNotExist:
            logger.error("Like object does not exist.")
            self.create(post=post, user_id=user_id)
            logger.info(f"Liked post with id {post.id}")

            result = True
        return result
