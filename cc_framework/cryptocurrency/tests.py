from unittest.mock import patch
from copy import deepcopy

from django.test import TestCase

from .models import Node, Currency, Transaction
from .connectors.btc.tests import TXS
from .connectors.btc.connector import BitcoinCoreConnector


class NodeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        # Below code will fix AttributeError: type object 'NodeTestCase'
        # has no attribute 'cls_atomics'
        super(NodeTestCase, cls).setUpClass()

        currency = Currency.objects.create(
            symbol='BTC',
            name='Bitcoin',
            min_confirmations=2
        )
        Node.objects.create(
            name='bitcoin-core',
            currency=currency,
            rpc_username='bitcoin',
            rpc_password='qwerty54',
            rpc_host='example.com',
            rpc_port=18332
        )

    def test_charge_new_receipts(self):
        with patch.object(BitcoinCoreConnector, 'get_txs', return_value=TXS) \
                as mock_method:
            Node.objects.process_receipts()

        mock_method.assert_called_once()
        txs = Transaction.objects.all()
        self.assertEqual(txs.count(), 2)
        self.assertEqual(txs.filter(is_confirmed=True).count(), 1)

    def test_confirm_charged_receipts(self):
        # Now increase confirmations for first tx in TXS
        return_txs = deepcopy(TXS)
        return_txs[0]['confirmations'] = 666

        with patch.object(
                BitcoinCoreConnector, 'get_txs', return_value=return_txs) \
                as mock_method:
            Node.objects.process_receipts()

        mock_method.assert_called_once()
        txs = Transaction.objects.all()
        self.assertEqual(txs.filter(is_confirmed=True).count(), 2)
