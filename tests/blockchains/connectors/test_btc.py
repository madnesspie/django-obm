import pytest
import requests

from cc_framework.blockchain import connectors
from tests.blockchains.connectors import data


class TestBitcoinCoreConnector:
    @staticmethod
    def test_get_receipts_format(monkeypatch, bitcoin_core_connector):
        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            "_request",
            lambda *_: data.BTC_TXS,
        )

        receipts = bitcoin_core_connector.get_receipts()
        assert isinstance(receipts, list)
        assert isinstance(receipts[0], dict)
        assert all([r["category"] == "receive" for r in receipts])
        # Check that keys mutch the format
        for tx in receipts:
            assert all(
                [
                    key in connectors.base.BaseConnector.TX_KEYS_FORMAT
                    for key in tx
                ]
            )

    @staticmethod
    @pytest.mark.parametrize(
        "origin_error, expected_error",
        (
            (
                requests.exceptions.RequestException,
                connectors.exceptions.NetworkError,
            ),
            (
                requests.exceptions.Timeout,
                connectors.exceptions.NetworkTimeoutError,
            ),
        ),
        ids=["network error", "network timeout error",],
    )
    def test_get_receipts_wrap_errors(
        monkeypatch, origin_error, expected_error, bitcoin_core_connector,
    ):
        def mock(*_, **__):
            raise origin_error()

        monkeypatch.setattr(requests, "post", mock)

        with pytest.raises(expected_error):
            bitcoin_core_connector.get_receipts()

    @staticmethod
    def test_estimate_fee(monkeypatch, bitcoin_core_connector):
        class MockedResponce:
            @staticmethod
            def json():
                return {
                    "result": {"feerate": 0.00001,},
                    "error": None,
                }

        monkeypatch.setattr(
            requests, "post", lambda *_, **__: MockedResponce(),
        )

        fee = bitcoin_core_connector.estimate_fee()
        assert isinstance(fee, float)


@pytest.mark.integration
class TestBitcoinCoreConnectorIntegration:
    @staticmethod
    def test_estimate_fee(bitcoin_core_connector):
        fee = bitcoin_core_connector.estimate_fee()
        assert isinstance(fee, float)

    @staticmethod
    def test_send_tansaction(bitcoin_core_connector):
        # TODO: Add ladger-fixture for tests that spend testnet money
        amount_to_send = 0.00001
        in_wallet_address = "2NAmne8BsSXWbV5iStkVzL4vW7Z4F6a5o68"
        sent_tx = bitcoin_core_connector.send_transaction(
            address=in_wallet_address, amount=amount_to_send,
        )
        assert isinstance(sent_tx, dict)
        assert isinstance(sent_tx["txid"], str)
        assert sent_tx["address"] == in_wallet_address
        assert sent_tx["category"] == "send"
        # tests that fee subtract from amount
        assert sent_tx["amount"] < amount_to_send

    @staticmethod
    def test_list_transactions(bitcoin_core_connector):
        txs = bitcoin_core_connector.list_transactions()
        assert isinstance(txs, list)
