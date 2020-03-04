from django.core.management.base import BaseCommand

from cc_framework.blockchain import models


class Command(BaseCommand):
    help = 'Fetches txs from nodes then enrolls new and confirms if needed.'

    def handle(self, *args, **options):
        models.Node.objects.process_receipts()
