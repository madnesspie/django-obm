import warnings
from typing import Dict, List
from unittest import mock

import requests
from django.test import SimpleTestCase

from cryptocurrency import blockchains
from cryptocurrency.blockchains.connectors import base, btc

TXS = [{
    'address': '2MsYTTPi276Q7yTZXxEiuCiAmfk9naKE7Gh',
    'amount': 0.08647872,
    'category': 'receive',
    'confirmations': 1,
    'time': 1562415913,
    'timereceived': 1562415913,
    'txid': 'd2f2679a65f012c0ce7bde59a2ae43af75e82f326600afd044',
}, {
    'address': '2MsGTPi27QQ7yFZXxEiuCiAmfk9nbKE7Gh',
    'amount': 1,
    'category': 'receive',
    'confirmations': 374,
    'time': 1562415913,
    'timereceived': 1562415913,
    'txid': 'd2f2679a67f0132c0ce7bde59a2ae43af75e82f326600afd0',
}, {
    'address': '2N5QTaxHBCmMyxCHveZTB5ecpCbwiGuC2gr',
    'amount': 0.01,
    'category': 'send',
    'confirmations': 367,
    'time': 1562419693,
    'timereceived': 1562419693,
    'txid': '81ff6c37547d3d13593bfe74b23c8a4f8da1379efdcb3be5fad77257d...',
}]


class BitcoinCoreConnectorTests(SimpleTestCase):
    @classmethod
    def setUpClass(cls):
        # Below code will fix AttributeError: type object
        # 'BitcoinCoreConnectorTests' has no attribute 'cls_atomics'
        super(BitcoinCoreConnectorTests, cls).setUpClass()

        warnings.simplefilter("always")
        cls.connector = btc.BitcoinCoreConnector(
            rpc_username='bitcoin',
            rpc_password='qwerty54',
            rpc_host='http://example.com',
            rpc_port=18332,
        )

        cls.CoSD = None

    def test_get_receipts_format(self):
        stash = self.connector._request
        self.connector._request = mock.MagicMock(return_value=TXS)

        receipts = self.connector.get_receipts()
        self.assertIsInstance(receipts, List)
        self.assertIsInstance(receipts[0], Dict)
        self.assertTrue(all([r['category'] == 'receive' for r in receipts]))
        for tx in receipts:
            self.assertTrue(all([key in base.TX_KEYS_FORMAT for key in tx]))

        self.connector._request = stash

    def test_bad_response_warning(self):
        stash = requests.post
        requests.post = mock.Mock(side_effect=KeyError())

        with warnings.catch_warnings(record=True) as warns:
            self.connector.get_receipts()
            assert len(warns) == 1
            assert issubclass(
                warns[-1].category,
                blockchains.exceptions.InvalidNodeResponseWarning)

        requests.post = stash

    def test_timeout_warning(self):
        stash = requests.post
        requests.post = mock.Mock(side_effect=requests.exceptions.Timeout)

        with warnings.catch_warnings(record=True) as warns:
            self.connector.get_receipts()
            assert len(warns) == 1
            assert issubclass(
                warns[-1].category,
                blockchains.exceptions.TimeoutNodeResponseWarning)

        requests.post = stash

    def test_requests_warning(self):
        stash = requests.post
        requests.post = mock.Mock(
            side_effect=requests.exceptions.RequestException)

        with warnings.catch_warnings(record=True) as warns:
            self.connector.get_receipts()
            assert len(warns) == 1
            assert issubclass(warns[-1].category,
                              blockchains.exceptions.BadRequestWarning)

        requests.post = stash
