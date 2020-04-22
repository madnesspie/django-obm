# Copyright 2019-2020 Alexander Polishchuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
import traceback
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand

from django_obm import models


class Command(BaseCommand):
    DEFAULT_FREQUENCY = 60
    help = "Sync transactions with blockchain with specified frequency."

    def add_arguments(self, parser):
        parser.add_argument(
            "--once",
            action="store_true",
            default=False,
            help="Run sync transaction only once.",
        )
        parser.add_argument(
            "--raise-errors",
            action="store_true",
            default=False,
            help="Raise any error that occur and stop the daemon.",
        )
        parser.add_argument(
            "--frequency",
            action="store",
            default=getattr(
                settings,
                "OBM_COLLECT_TRANSACTION_FREQUENCY",
                self.DEFAULT_FREQUENCY,
            ),
            type=int,
            help="The frequency of sync transactions running.",
        )

    def log(self, msg, style=None):
        msg = f"{datetime.now()}:   {msg}"
        self.stdout.write(style(msg) if style else msg)

    def handle(self, *args, **options):
        frequency = options["frequency"]
        self.log(
            f"Start sync transactions proccess with "
            f"{frequency} sec. frequency"
        )

        while True:
            self.log("Run synchronization")
            try:
                result = models.Node.objects.sync_transactions()
            except Exception as exc:  # pylint: disable=broad-except
                if options["raise_errors"]:
                    raise exc
                self.log(traceback.format_exc(), style=self.style.ERROR)
            else:
                self.log("Synchronized transactions", style=self.style.SUCCESS)

            if options["once"]:
                break
            time.sleep(frequency)
