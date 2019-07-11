from django.db import models

from cryptocurrency import connectors, exceptions


class NodeManager(models.Manager):  # pylint: disable=too-few-public-methods
    @staticmethod
    def __get_new_receipts(recently_receipts, charged_receipts):
        charged_receipt_txids = [tx.txid for tx in charged_receipts]
        new_receipts = filter(
            lambda tx: tx['txid'] not in charged_receipt_txids,
            recently_receipts)
        return new_receipts

    @staticmethod
    def __get_recently_confirmed_txids(recently_receipts, min_confirmations):
        return filter(lambda tx: tx['confirmations'] >= min_confirmations,
                      recently_receipts)

    def process_receipts(self):
        for node in self.all():
            recently_receipts = node.connector.get_receipts()
            if not recently_receipts:
                continue
            charged_receipts = node.txs.filter(category='receive')

            # Create new transaction
            new_receipts = self.__get_new_receipts(recently_receipts,
                                                   charged_receipts)
            Transaction.objects.bulk_create_from_dicts(new_receipts, node)

            # Confirm already charged transaction
            confirmed_receipt_txids = self.__get_recently_confirmed_txids(
                recently_receipts,
                min_confirmations=node.currency.min_confirmations)
            Transaction.objects.bulk_confirm(confirmed_receipt_txids)


class TransactionManager(models.Manager):
    def bulk_confirm(self, txids):
        confirmed_txs = [
            Transaction.confirm(receipt)
            for receipt in self.filter(is_confirmed=False) if receipt in txids
        ]
        self.bulk_update(confirmed_txs, ['is_confirmed'])

    def bulk_create_from_dicts(self, tx_dicts, node):
        txs = []
        for tx_dict in tx_dicts:
            addr, _ = Address.objects.get_or_create(
                address=tx_dict['address'],
                currency=node.currency,
            )
            is_confirmed = tx_dict['confirmations'] \
                > node.currency.min_confirmations
            tx = Transaction(
                node=node,
                address=addr,
                txid=tx_dict['txid'],
                category=tx_dict['category'],
                amount=tx_dict['amount'],
                fee=tx_dict.get('fee', 0),
                is_confirmed=is_confirmed,
                timestamp=tx_dict['timestamp'],
                timestamp_received=tx_dict['timestamp_received'],
            )
            txs.append(tx)
        self.bulk_create(txs)


class Currency(models.Model):
    name = models.CharField(
        max_length=100,
        choices=connectors.register.currency_as_choices(),
        unique=True,
    )
    min_confirmations = models.IntegerField(
        help_text='Minimum confirmations number after which a transaction will '
        'get the status "is confirmed"', )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.name not in connectors.register.available_currencies:
            raise exceptions.CurrencyDoesNotExistError(
                f'The "{self.name}" node does\'t supported.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'currencies'

    def __str__(self):
        return self.get_name_display()


class Node(models.Model):
    name = models.CharField(
        max_length=200,
        choices=connectors.register.connectors_as_choices(),
    )
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name='nodes',
        related_query_name='node',
    )
    rpc_username = models.CharField(
        verbose_name='RPC username',
        max_length=200,
        help_text='Username for JSON-RPC connections',
    )
    rpc_password = models.CharField(
        verbose_name='RPC password',
        max_length=200,
        help_text='Password for JSON-RPC connections',
    )
    rpc_host = models.URLField(
        verbose_name='RPC host',
        help_text='Listen for JSON-RPC connections on this IP address',
    )
    rpc_port = models.PositiveIntegerField(
        verbose_name='RPC port',
        help_text='Listen for JSON-RPC connections on this port',
    )

    objects = NodeManager()

    class Meta:
        unique_together = (('rpc_host', 'rpc_port'), )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.name not in connectors.register.available_conectors:
            raise exceptions.NodeDoesNotExistError(
                f'The "{self.name}" node does\'t supported.')
        super().save(*args, **kwargs)

    @property
    def connector(self):
        node_connector = connectors.register.get_by_node_name(self.name)
        return node_connector(self.rpc_host, self.rpc_port, self.rpc_username,
                              self.rpc_password)


class Address(models.Model):
    address = models.CharField(
        max_length=500,
    )  # yapf: disable
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name='addrs',
        related_query_name='addr',
    )

    class Meta:
        unique_together = (('address', 'currency'), )

    def __str__(self):
        return self.address


class Transaction(models.Model):
    node = models.ForeignKey(
        to=Node,
        on_delete=models.CASCADE,
        related_name='txs',
        related_query_name='tx',
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        related_name='txs',
        related_query_name='tx',
    )
    txid = models.CharField(
        verbose_name='transaction id',
        max_length=500,
    )
    category = models.CharField(
        max_length=30,
    )  # yapf: disable
    amount = models.FloatField(
        help_text='The transaction amount in currency',
    )  # yapf: disable
    fee = models.FloatField(
        help_text='The amount of the fee in currency. This is negative and '
        'only available for the "send" category of transactions.', )
    is_confirmed = models.BooleanField(
        verbose_name='confirmed',
        default=False,
    )
    timestamp = models.PositiveIntegerField(
        verbose_name='time',
        help_text='transaction creation time in timestamp',
    )
    timestamp_received = models.PositiveIntegerField(
        verbose_name='receipt time',
        help_text='transaction receipt time in timestamp',
    )

    objects = TransactionManager()

    class Meta:
        unique_together = (('node', 'txid'), )

    def __str__(self):
        return self.txid

    @staticmethod
    def confirm(tx):
        tx.is_confirmed = True
        return tx
