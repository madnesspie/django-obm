from rest_framework import viewsets

from cryptocurrency.blockchains import models
from cryptocurrency.rest import serializers


class TransactionViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with transactions.  """

    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()

class AddressViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with addresses.  """

    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()


class CurrencyViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with currencies.  """

    serializer_class = serializers.CurrencySerializer
    queryset = models.Currency.objects.all()
