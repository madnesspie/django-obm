from django.db import models

from . import connectors


class NodeManager(models.Manager):
    def process_receipts(self):
        for node in self.all():
            charged_receipts = node.txs.filter(category='receive')
            recently_receipts = node.connector.get_receipts()

            # Create new transaction
            charged_receipt_txids = [r.txid for r in charged_receipts]
            new_receipts = filter(
                lambda r: r['txid'] not in charged_receipt_txids,
                recently_receipts
            )
            Transaction.objects.bulk_create([
                Transaction.from_dict(receipt, node)
                for receipt in new_receipts
            ])

            # Confirm already charged transaction
            confirmed_receipts = [
                r['txid'] for r in recently_receipts
                if r['confirmations'] >= node.currency.confirmations_number
            ]
            new_confirmed_receipts = [
                Transaction.confirm(receipt)
                for receipt in charged_receipts.filter(is_confirmed=False)
                if receipt in confirmed_receipts
            ]
            Transaction.objects.bulk_update(
                new_confirmed_receipts, ['is_confirmed'])


class Currency(models.Model):
    symbol = models.CharField(max_length=20,
                              choices=connectors.register.symbols_as_choices(),
                              unique=True)
    name = models.CharField(max_length=200,
                            unique=True)
    confirmations_number = models.IntegerField(
        help_text='Minimum confirmations number after which a transaction will '
                  'get the status "is confirmed"')

    class Meta:
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.name


class Node(models.Model):
    name = models.CharField(max_length=200,
                            choices=connectors.register.connectors_as_choices())
    currency = models.ForeignKey(Currency,
                                 on_delete=models.CASCADE,
                                 related_name="nodes",
                                 related_query_name="node")
    rpc_username = models.CharField(verbose_name='RPC username',
                                    max_length=200,
                                    help_text='Username for JSON-RPC '
                                              'connections')
    rpc_password = models.CharField(verbose_name='RPC password',
                                    max_length=200,
                                    help_text='Password for JSON-RPC '
                                              'connections')
    rpc_host = models.URLField(verbose_name='RPC host',
                               help_text='Listen for JSON-RPC connections '
                                         'on this IP address')
    rpc_port = models.IntegerField(verbose_name='RPC port',
                                   help_text='Listen for JSON-RPC connections '
                                             'on this port')

    objects = NodeManager()

    class Meta:
        unique_together = (
            ('rpc_username', 'rpc_password', 'rpc_host', 'rpc_port'), )

    def __str__(self):
        return f"{self.get_name_display()} {self.rpc_host}:{self.rpc_port}"

    @property
    def connector(self):
        NodeConnector = connectors.register.get(self.name)
        return NodeConnector(
            self.rpc_host, self.rpc_port, self.rpc_username, self.rpc_password)


class Address(models.Model):
    address = models.CharField(max_length=500)
    currency = models.ForeignKey(Currency,
                                 on_delete=models.CASCADE,
                                 related_name="addrs",
                                 related_query_name="addr")
    # received = models.FloatField(verbose_name='received balance')

    class Meta:
        unique_together = (
            ('address', 'currency'), )

    def __str__(self):
        return self.address


class Transaction(models.Model):
    node = models.ForeignKey(Node,
                             on_delete=models.CASCADE,
                             related_name="txs",
                             related_query_name="tx")
    address = models.ForeignKey(Address,
                                on_delete=models.CASCADE,
                                related_name="txs",
                                related_query_name="tx")
    txid = models.CharField(verbose_name='transaction id',
                            max_length=500)
    category = models.CharField(max_length=30)
    amount = models.FloatField(help_text='The transaction amount in currency')
    fee = models.FloatField(help_text='The amount of the fee in currency. '
                                      'This is negative and only available for '
                                      'the "send" category of transactions.')
    is_confirmed = models.BooleanField(verbose_name='confirmed',
                                       default=False)
    ts = models.IntegerField(verbose_name='time',
                             help_text='transaction creation '
                                       'time in timestamp')
    ts_received = models.IntegerField(verbose_name='receipt time',
                                      help_text='transaction receipt'
                                                'time in timestamp')

    class Meta:
        unique_together = (
            ('node', 'txid'), )

    def __str__(self):
        return f"{self.txid[:100]}..."

    @staticmethod
    def from_dict(tx_dict, node):
        addr, _ = Address.objects.get_or_create(
            address=tx_dict['address'], currency=node.currency)
        is_confirmed = True if tx_dict['confirmations'] \
            > node.currency.confirmations_number else False
        tx = Transaction(
            node=node,
            address=addr,
            txid=tx_dict['txid'],
            category=tx_dict['category'],
            amount=tx_dict['amount'],
            fee=tx_dict.get('fee', 0),
            is_confirmed=is_confirmed,
            ts=tx_dict['time'],
            ts_received=tx_dict['timereceived']
        )
        return tx

    @staticmethod
    def confirm(tx):
        tx.is_confirmed = True
        return tx
