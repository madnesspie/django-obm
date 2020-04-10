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
from django.conf import settings
from rest_framework import decorators, response, viewsets

from django_obm import models, pagination, serializers


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
        node = currency.default_node
        estimated_fee = node.estimate_fee(
            from_address=request.query_params.get("from_address"),
            to_address=request.query_params.get("to_address"),
            amount=request.query_params.get("amount"),
            fee={
                "gas": request.query_params.get("gas"),
                "gas_price": request.query_params.get("gas_price"),
            },
            data=request.query_params.get("data"),
            conf_target=request.query_params.get("conf_target", 1),
        )
        node.close()
        return response.Response(
            {"currency": currency.name, "estimated_fee": estimated_fee,}
        )
