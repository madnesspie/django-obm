import time
import traceback
from datetime import datetime

from django.core.management.base import BaseCommand

from cc_framework.blockchain import models


class Command(BaseCommand):
    help = 'Fetches txs from nodes then enrolls new and confirms if needed.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--once',
            action='store_true',
            default=False,
            help='Run receipts processing only once.',
        )
        parser.add_argument(
            '--raise-errors',
            action='store_true',
            default=False,
            help='Raise any error that occur when method .',
        )

    def log(self, msg, style=None):
        msg = f'{datetime.now()}:   {msg}'
        self.stdout.write(style(msg) if style else msg)

    def handle(self, *args, **options):
        self.log('Start receipts processing')
        while True:
            self.log('Run receipts processing')
            try:
                result = models.Node.objects.process_receipts()
            except Exception as exc:  # pylint: disable=broad-except
                if options['raise_errors']:
                    raise exc
                self.log(traceback.format_exc(), style=self.style.ERROR)
            else:
                for new_tx in result['added']:
                    self.log(f'Added {repr(new_tx)}', style=self.style.SUCCESS)
                for confirmed_tx in result['confirmed']:
                    self.log(f'Confirmed {repr(confirmed_tx)}', style=self.style.SUCCESS)

            if options['once']:
                break
            time.sleep(1)
