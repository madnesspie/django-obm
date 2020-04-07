import time
import traceback
from datetime import datetime

from django.core.management.base import BaseCommand

from django_obm import models


class Command(BaseCommand):
    help = "Cleans database."

    def handle(self, *args, **options):
        models.Node.objects.all().delete()
        models.Currency.objects.all().delete()
        models.Transaction.objects.all().delete()
        models.Address.objects.all().delete()
