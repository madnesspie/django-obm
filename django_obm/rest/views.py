from django.conf import settings
from rest_framework import decorators, response, viewsets

from django_obm.blockchain import models
from django_obm.rest import pagination, serializers


def get_pagination_class():
    # TODO: Add pagination class setting
    # fmt: off
    has_pagination = getattr(settings, "OBM_PAGINATION_LIMIT", None) \
        or getattr(settings, "OBM_PAGINATION_MAX_LIMIT", None)
    # fmt: on
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
