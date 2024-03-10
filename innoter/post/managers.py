import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

logger = logging.getLogger(__name__)


class LikeManager(models.Manager):
    def like_post(self, post_id, user_id):
        logger.info(
            f"Invoked like post with id {post_id} from manager for user with id {user_id}."
        )
        _, created = self.get_or_create(post_id=post_id, user_id=user_id)
        return created

    def remove_like_post(self, post_id, user_id):
        logger.info(
            f"Invoked remove like post with id {post_id} from manager for user with id {user_id}."
        )
        result = None
        try:
            like = self.get(post_id=post_id, user_id=user_id)
            like.delete()
            result = True
        except ObjectDoesNotExist:
            logger.error("Like object does not exist.")
            result = False
        return result
