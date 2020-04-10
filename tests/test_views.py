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

import pytest
from django import urls

from django_obm import models


class TestTransactionViewSet:
    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        response = client.get(urls.reverse("transaction-list"))
        assert response.status_code == 200
        result = response.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node")
    def test_post(monkeypatch, client):
        monkeypatch.setattr(
            models.Node,
            "send_transaction",
            lambda *_, **__: {
                # "fee": 0.00001,
                "txid": "fake-txid",
                "timestamp": 1562415913,
            },
        )
        # TODO: Add fee handling
        response = client.post(
            urls.reverse("transaction-list"),
            data={
                "currency": "bitcoin",
                "to_address": "fake-addr",
                "amount": 10,
            },
        )
        assert response.status_code == 201
        assert models.Transaction.objects.count() == 1
        result = response.json()
        assert result["txid"] == "fake-txid"
        # assert float(result["fee"]) == 0.00001


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
        assert response.json()["value"] == "fake-addr"



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
        address_value = response.json()["value"]
        assert isinstance(address_value, str)
        assert len(address_value) > 20


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
