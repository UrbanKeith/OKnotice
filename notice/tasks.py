from celery import shared_task

from notice.utils import check_pending_message, check_recipients
