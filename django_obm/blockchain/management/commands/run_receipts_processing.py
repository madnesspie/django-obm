import time
import traceback
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from django_obm.blockchain import models


class Command(BaseCommand):
    DEFAULT_FREQUENCY = 60
    help = "Processes receipts with specified frequency."

    def add_arguments(self, parser):
        parser.add_argument(
            "--once",
            action="store_true",
            default=False,
            help="Run receipts processing only once.",
        )
        parser.add_argument(
            "--raise-errors",
            action="store_true",
            default=False,
            help="Raise any error that occur when method.",
        )
        parser.add_argument(
            "--frequency",
            action="store",
            default=getattr(
                settings,
                "RECEIPTS_PROCESSING_DEFAULT_FREQUENCY",
                self.DEFAULT_FREQUENCY,
            ),
            type=int,
            help="Raise any error that occur due execution.",
        )

    def log(self, msg, style=None):
        msg = f"{datetime.now()}:   {msg}"
        self.stdout.write(style(msg) if style else msg)

    def handle(self, *args, **options):
        frequency = options["frequency"]
        self.log(f"Start receipts processing with {frequency} sec. frequency")

        while True:
            self.log("Run receipts processing")
            try:
                result = models.Node.objects.process_receipts()
            except Exception as exc:  # pylint: disable=broad-except
                if options["raise_errors"]:
                    raise exc
                self.log(traceback.format_exc(), style=self.style.ERROR)
            else:
                for new_tx in result["added"]:
                    self.log(f"Added {repr(new_tx)}", style=self.style.SUCCESS)
                for confirmed_tx in result["confirmed"]:
                    self.log(
                        f"Confirmed {repr(confirmed_tx)}",
                        style=self.style.SUCCESS,
                    )

            if options["once"]:
                break
            time.sleep(frequency)
