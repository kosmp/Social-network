#!/bin/bash
celery -A innoter.celery worker --detach
celery -A innoter.celery beat --loglevel=info
