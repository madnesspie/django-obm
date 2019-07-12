from django.core.management.base import BaseCommand

from cryptocurrency.blockchains import models


class Command(BaseCommand):
    help = 'Check cryptocurrency receipts and enroll if any exists'

    def handle(self, *args, **options):
        models.Node.objects.process_receipts()
