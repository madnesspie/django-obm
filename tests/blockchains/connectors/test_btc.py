import pytest
import requests

from cryptocurrency import blockchains
from cryptocurrency.blockchains import connectors

TXS = [
    {
        'address': '2MsYTTPi276Q7yTZXxEiuCiAmfk9naKE7Gh',
        'amount': 0.08647872,
        'category': 'receive',
        'confirmations': 1,
        'time': 1562415913,
        'timereceived': 1562415913,
        'txid': 'd2f2679a65f012c0ce7bde59a2ae43af75e82f326600afd044',
    },
    {
        'address': '2MsGTPi27QQ7yFZXxEiuCiAmfk9nbKE7Gh',
        'amount': 1,
        'category': 'receive',
        'confirmations': 374,
        'time': 1562415913,
        'timereceived': 1562415913,
        'txid': 'd2f2679a67f0132c0ce7bde59a2ae43af75e82f326600afd0',
    },
    {
        'address': '2N5QTaxHBCmMyxCHveZTB5ecpCbwiGuC2gr',
        'amount': 0.01,
        'category': 'send',
        'confirmations': 367,
        'time': 1562419693,
        'timereceived': 1562419693,
        'txid': '81ff6c37547d3d13593bfe74b23c8a4f8da1379efdcb3be5fad77257d...',
    },
]


class TestBitcoinCoreConnector:

    @staticmethod
    def test_get_receipts_format(monkeypatch, bitcoin_core_connector):
        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            '_request',
            lambda *_: TXS,
        )

        receipts = bitcoin_core_connector.get_receipts()
        assert isinstance(receipts, list)
        assert isinstance(receipts[0], dict)
        assert all([r['category'] == 'receive' for r in receipts])
        # Check that keys mutch the format
        for tx in receipts:
            assert all([key in connectors.base.TX_KEYS_FORMAT for key in tx])

    @staticmethod
    @pytest.mark.parametrize(
        'error',
        (
            KeyError,
            requests.exceptions.RequestException,
            requests.exceptions.Timeout,
        ),
        ids=[
            'bad response',
            'bad request',
            'timeout',
        ]
    )
    def test_get_receipts_rises_warning(
            monkeypatch,
            recwarn,
            error,
            bitcoin_core_connector,
    ):

        def mock(*_, **__):
            raise error()

        monkeypatch.setattr(requests, 'post', mock)

        bitcoin_core_connector.get_receipts()
        assert len(recwarn) == 1
        assert issubclass(
            recwarn[-1].category,
            blockchains.exceptions.ConnectorWarning,
        )
