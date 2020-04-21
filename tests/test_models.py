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
import pytest

from django_obm import exceptions, models


class TestCurrency:
    # @staticmethod
    # @pytest.mark.django_db
    # TODO: Add validate currency name
    # def test_create_rises_node_does_not_exist_error():
    #     with pytest.raises(django_exceptions.ValidationError):
    #         models.Currency.objects.create(name="LOL")

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node")
    def test_default_node(bitcoin_currency):
        assert bitcoin_currency.default_node.name == "bitcoin-core"

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node")
    def test_create_two_default_node_raises_error(bitcoin_currency):
        with pytest.raises(exceptions.DefaultNodeAlreadyExists):
            models.Node.objects.create(
                name="bitcoin-core",
                currency=bitcoin_currency,
                is_default=True,
                rpc_username="bitcoin",
                rpc_password="qwerty54",
                rpc_host="example.com",
                rpc_port=18332,
            )

    @staticmethod
    @pytest.mark.django_db
    def test_update_default_node(bitcoin_core_node):
        bitcoin_core_node.rpc_port = 8332
        bitcoin_core_node.save()
        assert bitcoin_core_node.rpc_port == 8332


class TestNode:
    @staticmethod
    @pytest.mark.django_db
    def test_create_rises_validation_error_if_node_is_unsupported(
        bitcoin_currency,
    ):
        with pytest.raises(ValueError):
            models.Node.objects.create(
                name="bitcoin-lol",
                currency=bitcoin_currency,
                rpc_username="bitcoin",
                rpc_password="qwerty54",
                rpc_host="example.com",
                rpc_port=18332,
            )


class TestTransaction:
    @staticmethod
    @pytest.mark.django_db
    def test_confirmations_number(bitcoin_transaction):
        bitcoin_transaction.sync()
        assert bitcoin_transaction.confirmations_number > 0
