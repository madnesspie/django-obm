from copy import deepcopy
from unittest.mock import patch

from django.test import TestCase

from cryptocurrency.blockchains import exceptions, models
from cryptocurrency.blockchains.connectors import btc
from tests.blockchains.connectors import test_btc

# class NodeTestCase(TestCase):
#     @classmethod
#     def setUpClass(cls):
#         # Below code will fix AttributeError: type object 'NodeTestCase'
#         # has no attribute 'cls_atomics'
#         super(NodeTestCase, cls).setUpClass()

#         cls.currency = models.Currency.objects.create(name='BTC',
#                                                       min_confirmations=2)
#         models.Node.objects.create(name='bitcoin-core',
#                                    currency=cls.currency,
#                                    rpc_username='bitcoin',
#                                    rpc_password='qwerty54',
#                                    rpc_host='example.com',
#                                    rpc_port=18332)

#     def test_charge_new_receipts(self):
#         with patch.object(btc.BitcoinCoreConnector,
#                           '_request',
#                           return_value=test_btc.TXS) as mock_method:
#             models.Node.objects.process_receipts()

#         mock_method.assert_called_once()
#         txs = models.Transaction.objects.all()
#         self.assertEqual(txs.count(), 2)
#         self.assertEqual(txs.filter(is_confirmed=True).count(), 1)

#     def test_confirm_charged_receipts(self):
#         # Now increase confirmations for first tx in TXS
#         return_txs = deepcopy(test_btc.TXS)
#         return_txs[0]['confirmations'] = 666

#         with patch.object(btc.BitcoinCoreConnector,
#                           '_request',
#                           return_value=return_txs) as mock_method:
#             models.Node.objects.process_receipts()

#         mock_method.assert_called_once()
#         txs = models.Transaction.objects.all()
#         self.assertEqual(txs.filter(is_confirmed=True).count(), 2)

#     def test_node_does_not_exist_error(self):
#         with self.assertRaises(exceptions.NodeDoesNotExistError):
#             models.Node.objects.create(
#                 name='bitcoin-lol',
#                 currency=self.currency,
#                 rpc_username='bitcoin',
#                 rpc_password='qwerty54',
#                 rpc_host='example.com',
#                 rpc_port=18332,
#             )


# class CurrencyTestCase(TestCase):
#     def test_node_does_not_exist_error(self):
#         with self.assertRaises(exceptions.CurrencyDoesNotExistError):
#             models.Currency.objects.create(
#                 name='LOL',
#                 min_confirmations=2,
#             )
