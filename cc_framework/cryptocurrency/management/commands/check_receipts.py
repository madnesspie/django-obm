from django.core.management.base import BaseCommand, CommandError

from ...models import Node


class Command(BaseCommand):
    help = 'Check cryptocurrency receipts and enroll if any exists'

    def handle(self, *args, **options):
        Node.objects.check_receipts()
        # self.stdout.write(self.style.SUCCESS('Successfully ....'))