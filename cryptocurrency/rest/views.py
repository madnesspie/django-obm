from rest_framework import views, viewsets
from rest_framework.response import Response

from cryptocurrency.blockchains import models
from cryptocurrency.rest import serializers


class TransactionViewSet(viewsets.ModelViewSet):
    """The ViewSet for listing or retrieving transactions.  """

    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
