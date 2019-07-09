from unittest.mock import MagicMock
from typing import List, Dict

from django.test import SimpleTestCase

from .connector import BitcoinCoreConnector

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
    }
]


class BitcoinCoreConnectorTests(SimpleTestCase):
    def setUp(self):
        self.connector = BitcoinCoreConnector(
            rpc_username='bitcoin',
            rpc_password='qwerty54',
            rpc_host='http://example.com',
            rpc_port=18332
        )
        self.connector.get_txs = MagicMock(return_value=TXS)

    def test_get_receipts(self):
        receipts = self.connector.get_receipts()
        self.assertIsInstance(receipts, List)
        self.assertIsInstance(receipts[0], Dict)
        self.assertTrue(all([r['category'] == 'receive' for r in receipts]))

