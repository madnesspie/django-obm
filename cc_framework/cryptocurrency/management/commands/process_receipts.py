from django.core.management.base import BaseCommand

from ...models import Node


class Command(BaseCommand):
    help = 'Check cryptocurrency receipts and enroll if any exists'

    def handle(self, *args, **options):
        Node.objects.process_receipts()
        # self.stdout.write(self.style.SUCCESS('Successfully ....'))
