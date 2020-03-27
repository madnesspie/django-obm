from django.conf import settings
from rest_framework import decorators, response, viewsets

from cc_framework.blockchain import models
from cc_framework.rest import pagination, serializers


# fmt: off
def get_pagination_class():
    # TODO: Add pagination class setting
    has_pagination = getattr(settings, "CC_FRAMEWORK_PAGINATION_LIMIT", None) \
        or getattr(settings, "CC_FRAMEWORK_PAGINATION_MAX_LIMIT", None)
    return pagination.CustomLimitOffsetPagination if has_pagination else None


class TransactionViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with transactions.  """

    serializer_class = serializers.TransactionSerializer
    queryset = models.Transaction.objects.all()
    pagination_class = get_pagination_class()


class AddressViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with addresses.  """

    serializer_class = serializers.AddressSerializer
    queryset = models.Address.objects.all()
    pagination_class = get_pagination_class()


class CurrencyViewSet(viewsets.ModelViewSet):
    """The ViewSet for work with currencies.  """

    serializer_class = serializers.CurrencySerializer
    queryset = models.Currency.objects.all()

    @decorators.action(detail=True, methods=["get"])
    def estimated_fee(
        self, request, pk=None
    ):  # pylint: disable=unused-argument
        currency = self.get_object()
        return response.Response(
            {
                "currency": currency.name,
                "estimated_fee": currency.default_node.connector.estimate_fee(),
            }
        )
