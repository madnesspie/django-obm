# pylint: disable = redefined-outer-name

import pytest
from rest_framework import test as drf_test

from django_obm import models

# TODO: Check node balance before integration tests


@pytest.fixture
def client():
    return drf_test.APIClient()


@pytest.fixture
def bitcoin_currency():
    currency = models.Currency.objects.create(
        name="Bitcoin", min_confirmations=2
    )
    yield currency
    currency.delete()


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
    assert node.close() is None
    node.delete()


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


@pytest.fixture
def set_timeout_setting_is_none(settings):
    origin = settings.BLOCKCHAIN_NODE_TIMEOUT
    settings.BLOCKCHAIN_NODE_TIMEOUT = None
    yield None
    settings.BLOCKCHAIN_NODE_TIMEOUT = origin
