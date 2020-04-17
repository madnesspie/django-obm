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
import os
from decimal import Decimal

import pytest
from django import urls

from django_obm import models


class TestCurrencyViewSet:
    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_currency", "ethereum_currency")
    def test_get(client):
        response = client.get(urls.reverse("currency-list"))
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 2

    @staticmethod
    @pytest.mark.django_db
    def test_get_estimated_fee(monkeypatch, client, node):
        monkeypatch.setattr(
            models.Node, "estimate_fee", lambda *_, **__: 0.0001,
        )
        response = client.get(
            urls.reverse("currency-estimated-fee", args=(node.id,),)
        )
        assert response.status_code == 200
        result = response.json()
        assert result["estimated_fee"] == 0.0001


@pytest.mark.integration
class TestCurrencyViewSetIntegration:
    @staticmethod
    @pytest.mark.django_db
    def test_get_estimated_fee(client, node):
        ethereum_tx = {
            "to_address": str(os.environ.get("GETH_IN_WALLET_ADDRESS")),
            "amount": 10,
        }
        response = client.get(
            urls.reverse("currency-estimated-fee", args=(node.id,)),
            data=ethereum_tx,
        )
        assert response.status_code == 200
        result = response.json()
        assert isinstance(result["estimated_fee"], float)


class TestAddressViewSet:
    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        response = client.get(urls.reverse("address-list"))
        assert response.status_code == 200
        result = response.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    def test_post(monkeypatch, client, node):

        monkeypatch.setattr(
            models.Node, "create_address", lambda *_, **__: "fake-addr",
        )

        response = client.post(
            urls.reverse("address-list"),
            data={"currency": node.connector.currency},
        )
        assert response.status_code == 201
        assert models.Address.objects.count() == 1
        result = response.json()
        assert result["value"] == "fake-addr"
        if node.name == 'geth':
            assert result["password"] == ""


@pytest.mark.integration
class TestAddressViewSetIntegration:
    @staticmethod
    @pytest.mark.django_db
    def test_post(client, node):
        response = client.post(
            urls.reverse("address-list"),
            data={"currency": node.connector.currency},
        )
        assert response.status_code == 201
        assert models.Address.objects.count() == 1
        result = response.json()
        assert isinstance(result["value"], str)
        assert len(result["value"]) > 20
        if node.name == 'geth':
            assert result["password"] == ""


class TestTransactionViewSet:
    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("btc_transaction")
    def test_get(client):
        response = client.get(urls.reverse("transaction-list"))
        assert response.status_code == 200
        result = response.json()
        assert len(result) == 1

    @staticmethod
    @pytest.mark.django_db
    def test_get_empty(client):
        response = client.get(urls.reverse("transaction-list"))
        assert response.status_code == 200
        result = response.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    def test_post(monkeypatch, client, node):
        monkeypatch.setattr(
            models.Node,
            "send_transaction",
            lambda *_, **__: {
                "fee": 0.000001,
                "txid": "fake-txid",
                "timestamp": 1562415913,
                "amount": 0.00001,
            },
        )
        # TODO: Add fee handling
        response = client.post(
            urls.reverse("transaction-list"),
            data={
                "currency": node.connector.currency,
                "to_address": "fake-addr",
                "amount": 10,
            },
        )
        assert response.status_code == 201
        assert models.Transaction.objects.count() == 1
        result = response.json()
        assert result["txid"] == "fake-txid"
        assert Decimal(result["fee"]) == Decimal("0.000001")


@pytest.mark.integration
class TestTransactionViewSetIntegration:
    @staticmethod
    @pytest.mark.django_db
    def test_post_with_subtract_fee_from_amount(client, node):
        data_mapping = {
            "bitcoin": {
                "currency": "bitcoin",
                "to_address": os.environ.get("BITCOIN_CORE_IN_WALLET_ADDRESS"),
                "amount": Decimal('0.00001'),
            },
            "ethereum": {
                "currency": "ethereum",
                "from_address": os.environ.get("GETH_SEND_FROM_ADDRESS"),
                "to_address": os.environ.get("GETH_IN_WALLET_ADDRESS"),
                "amount": Decimal('0.00003'),
                # TODO: Create new addr with default password
                "password": "abc",
            },
        }
        response = client.post(
            urls.reverse("transaction-list"),
            data=data_mapping[node.connector.currency],
        )
        amount = data_mapping[node.connector.currency]["amount"]
        assert response.status_code == 201
        assert models.Transaction.objects.count() == 1
        result = response.json()
        assert Decimal(result["amount"]) + Decimal(result["fee"]) == amount
        assert isinstance(result["txid"], str)
        assert len(result["txid"]) > 20

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("geth_node")
    def test_post_without_password_to_ethereum_address(
        client, ethereum_address
    ):
        amount = 0.0000001
        response = client.post(
            urls.reverse("transaction-list"),
            data={
                "currency": "ethereum",
                "from_address": ethereum_address.value,
                "to_address": os.environ.get("GETH_IN_WALLET_ADDRESS"),
                "amount": 0.0000001,
                "subtract_fee_from_amount": False,
            },
        )
        assert response.status_code == 201
        assert models.Transaction.objects.count() == 1
        result = response.json()
        assert float(result["amount"]) == amount
        assert float(result["fee"])
        assert isinstance(result["txid"], str)
        assert len(result["txid"]) > 20
