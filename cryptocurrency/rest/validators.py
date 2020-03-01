from rest_framework import serializers

from cryptocurrency.blockchains import models


def currency_exists(value):
    symbols = models.Currency.objects.values_list('name', flat=True)
    if value not in symbols:
        raise serializers.ValidationError(f'Must be one of {symbols}')
