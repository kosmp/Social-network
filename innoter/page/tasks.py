from datetime import date

from innoter.celery import app

from .models import Page


@app.task
def unblock_pages():
    Page.objects.filter(is_blocked=True, unblock_date__lte=date.today()).update(
        is_blocked=False, unblock_date=None
    )
