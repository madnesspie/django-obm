from celery import shared_task

from cc_framework.blockchain import models


@shared_task
def process_receipts():
    models.Node.objects.process_receipts()
    return 'OK'
