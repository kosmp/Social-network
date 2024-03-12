import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

logger = logging.getLogger(__name__)


class FollowerManager(models.Manager):
    def follow_page(self, page, user_id):
        logger.info(
            f"Invoked follow page with id {page.id} from manager for user with id {user_id}."
        )
        _, created = self.get_or_create(page=page, user_id=user_id)
        return created

    def unfollow_page(self, page, user_id):
        logger.info(
            f"Invoked unfollow page with id {page.id} from manager for user with id {user_id}."
        )
        result = None
        try:
            follower = self.get(page=page, user_id=user_id)
            follower.delete()
            result = True
        except ObjectDoesNotExist:
            logger.error("Follower object does not exist.")
            result = False
        return result
