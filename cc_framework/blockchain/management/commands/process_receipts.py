import time

from django.core.management.base import BaseCommand

from cc_framework.blockchain import models


class Command(BaseCommand):
    help = 'Fetches txs from nodes then enrolls new and confirms if needed.'

    def add_arguments(self, parser):
        parser.add_argument(
            '-d',
            '--daemon',
            action='store_true',
            default=False,
            help='Run in the background as a daemon.',
        )
        parser.add_argument(
            '--once',
            action='store_true',
            default=False,
            help='Run in the background as a daemon.',
        )

    def handle(self, *args, **options):
        while True:
            result = models.Node.objects.process_receipts()
            time.time(60)
