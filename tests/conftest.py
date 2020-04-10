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

# pylint: disable = redefined-outer-name

import os

import dotenv
import pytest
from rest_framework import test as drf_test

from django_obm import models

# TODO: Check node balance before integration tests

# console options


def pytest_addoption(parser):
    parser.addoption(
        "--integration",
        action="store_true",
        default="",
        help="Run integration tests with main test suite.",
    )


# pytest hooks


def pytest_runtest_setup(item):
    """Pytest hook that called before each test.

    Docs:
        https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_runtest_setup

    Args:
        item: Pytest item object (conceptually is test).
    """
    markers = [marker.name for marker in item.iter_markers()]
    is_integration_test_session = item.config.getoption("--integration")
    if not is_integration_test_session and "integration" in markers:
        pytest.skip("skipped integration test")


def pytest_configure(config):  # pylint: disable=unused-argument
    """Pytest hook that called before test session.

    Docs:
        https://docs.pytest.org/en/latest/reference.html#_pytest.hookspec.pytest_configure

    Args:
        config: Pytest config object.
    """
    dotenv.load_dotenv(dotenv_path="./.env")


@pytest.fixture
def client():
    return drf_test.APIClient()


@pytest.fixture
def bitcoin_currency():
    currency = models.Currency.objects.create(name="bitcoin")
    yield currency
    currency.delete()


@pytest.fixture
def ethereum_currency():
    currency = models.Currency.objects.create(name="ethereum")
    yield currency
    currency.delete()


@pytest.fixture
def ethereum_address(ethereum_currency):
    address = models.Address.objects.create(
        value=os.environ.get("GETH_SEND_FROM_ADDRESS"),
        currency=ethereum_currency,
        password="abc"
    )
    yield address
    address.delete()


@pytest.fixture
def bitcoin_core_node(bitcoin_currency):
    node = models.Node.objects.create(
        name="bitcoin-core",
        currency=bitcoin_currency,
        is_default=True,
        rpc_username="testnet_user",
        rpc_password="testnet_pass",
        rpc_host="127.0.0.1",
        rpc_port=18332,
    )
    yield node
    node.delete()


@pytest.fixture
def geth_node(ethereum_currency):
    node = models.Node.objects.create(
        name="geth",
        currency=ethereum_currency,
        is_default=True,
        rpc_host="127.0.0.1",
        rpc_port=8545,
    )
    yield node
    node.delete()


@pytest.fixture(params=["bitcoin-core", "geth"])
def node(
    request, geth_node, bitcoin_core_node
):  # pylint: disable=unused-argument
    node_mapping = {
        'bitcoin-core': bitcoin_core_node,
        'geth': geth_node,
    }
    return node_mapping[request.param]

# @pytest.fixture
# def btc_transaction(bitcoin_core_node):
#     tx = models.Transaction.objects.create(
#         node=bitcoin_core_node,
#         address=models.Address.objects.create(
#             address=data.BTC_TXS[0]["address"],
#             currency=bitcoin_core_node.currency,
#         ),
#         txid=data.BTC_TXS[0]["txid"],
#         category=data.BTC_TXS[0]["category"],
#         amount=data.BTC_TXS[0]["amount"],
#         is_confirmed=False,
#         timestamp=data.BTC_TXS[0]["time"],
#     )
#     yield tx
#     tx.delete()
