import logging
from datetime import date

from innoter.celery import app

from .models import Page

logger = logging.getLogger(__name__)


@app.task
def unblock_pages():
    logger.info("Invoked unblocking pages cron task...")
    Page.objects.filter(is_blocked=True, unblock_date__lte=date.today()).update(
        is_blocked=False, unblock_date=None
    )
