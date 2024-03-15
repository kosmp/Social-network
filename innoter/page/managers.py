import logging

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

logger = logging.getLogger(__name__)


class FollowerManager(models.Manager):
    def follow_page(self, page, user_id):
        logger.info(
            f"Invoked follow/unfollow action from manager for page with id {page.id} for user with id {user_id}."
        )

        result = None
        try:
            follower = self.get(page=page, user_id=user_id)
            follower.delete()
            result = False
        except ObjectDoesNotExist:
            logger.error("Follower object does not exist.")
            self.create(page=page, user_id=user_id)
            logger.info(f"Followed page with id {page.id}")

            result = True
        return result
