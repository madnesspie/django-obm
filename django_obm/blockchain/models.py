from decimal import Decimal
from typing import List, TypeVar

from django.conf import settings
from django.db import models

from django_obm.blockchain import connectors, exceptions

TransactionType = TypeVar("TransactionType", bound="Transaction")
NodeType = TypeVar("NodeType", bound="Node")


class NodeManager(models.Manager):
    @staticmethod
    def create_new_receipts(node: NodeType, recently_receipts: List[dict]):
        """Creates new receipts that mssing in database. """
        enrolled_txids = node.txs.filter(category="receive").values_list(
            "txid", flat=True
        )
        new_receipts = filter(
            lambda tx: tx["txid"] not in enrolled_txids, recently_receipts,
        )
        return Transaction.objects.bulk_create_from_dicts(new_receipts, node)

    @staticmethod
    def confirm_receipts(node: NodeType, recently_receipts: List[dict]):
        """Creates new receipts that mssing in database. """

        def filter_confirmed(recently_receipts, min_confirmations):
            return filter(
                lambda tx: tx["confirmations"] >= min_confirmations,
                recently_receipts,
            )

        recently_confirmed_receipts = filter_confirmed(
            recently_receipts,
            min_confirmations=node.currency.min_confirmations,
        )
        return Transaction.objects.bulk_confirm(
            [tx["txid"] for tx in recently_confirmed_receipts]
        )

    def process_receipts(self):
        """Fetches txs from nodes then enrolls new and confirms if needed."""
        new_txs, confirmed_txs = [], []

        for node in self.all():
            recently_receipts = node.connector.get_receipts()
            if not recently_receipts:
                continue

            new_txs += self.create_new_receipts(node, recently_receipts)
            confirmed_txs += self.confirm_receipts(node, recently_receipts)

        return {
            "added": new_txs,
            "confirmed": confirmed_txs,
        }


class TransactionManager(models.Manager):
    def bulk_confirm(self, txids: List[str]):
        """Confirms transactions group.

        Args:
            txids: A sequence of strings representing the txid that
                needed to confirm.
        """
        confirmed_txs = [
            tx.confirm()
            for tx in self.filter(is_confirmed=False)
            if tx.txid in txids
        ]
        self.bulk_update(confirmed_txs, ["is_confirmed"])
        return confirmed_txs

    def bulk_create_from_dicts(self, tx_dicts, node):
        """Creates transactions from dicts.

        Args:
            tx_dicts: A sequence of dicts with transaction data that
                needed to write in database.
            node: A node that receive that transactions.
        """
        txs = []
        for tx_dict in tx_dicts:
            addr, _ = Address.objects.get_or_create(
                address=tx_dict["address"], currency=node.currency,
            )
            is_confirmed = (
                tx_dict["confirmations"] > node.currency.min_confirmations
            )
            tx = Transaction(
                node=node,
                address=addr,
                txid=tx_dict["txid"],
                category=tx_dict["category"],
                amount=tx_dict["amount"],
                fee=tx_dict.get("fee", 0),
                is_confirmed=is_confirmed,
                timestamp=tx_dict["timestamp"],
                timestamp_received=tx_dict["timestamp_received"],
            )
            txs.append(tx)
        return self.bulk_create(txs)


class Currency(models.Model):
    name = models.CharField(
        max_length=100,
        choices=connectors.registry.currency_as_choices(),
        unique=True,
    )
    min_confirmations = models.IntegerField(
        help_text="Minimum confirmations number after which a transaction will "
        'get the status "is confirmed"',
    )

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.name not in connectors.registry.available_currencies:
            raise exceptions.CurrencyDoesNotExistError(
                f'The "{self.name}" node does\'t supported.'
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "currencies"

    def __str__(self):
        return self.name

    @property
    def default_node(self):
        default_nodes = self.nodes.filter(is_default=True)
        if len(default_nodes) == 0:
            raise exceptions.DefaultNodeDoesNotExistError(
                f"Missing default node for {self.name}"
            )
        if len(default_nodes) > 1:
            raise exceptions.TooManyDefaultNodes(
                f"Too many default nodes for {self.name}. "
                f"You can create only 1 default node."
            )
        return default_nodes.first()


class Node(models.Model):
    name = models.CharField(
        max_length=200,
        choices=connectors.registry.connectors_as_choices(),
        unique=True,
    )
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name="nodes",
        related_query_name="node",
    )
    is_default = models.BooleanField(
        default=True,
        help_text=(
            "If True the node will be used as default"
            " for transaction sending"
        ),
    )
    rpc_username = models.CharField(
        verbose_name="RPC username",
        max_length=200,
        help_text="Username for JSON-RPC connections",
    )
    rpc_password = models.CharField(
        verbose_name="RPC password",
        max_length=200,
        help_text="Password for JSON-RPC connections",
    )
    rpc_host = models.URLField(
        verbose_name="RPC host",
        help_text="Listen for JSON-RPC connections on this IP address",
    )
    rpc_port = models.PositiveIntegerField(
        verbose_name="RPC port",
        help_text="Listen for JSON-RPC connections on this port",
    )

    objects = NodeManager()

    class Meta:
        unique_together = (("rpc_host", "rpc_port"),)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.name not in connectors.registry.available_nodes:
            raise exceptions.NodeDoesNotExistError(
                f'The "{self.name}" node does\'t supported.'
            )

        default_nodes = self.currency.nodes.filter(is_default=True).exclude(
            id=self.id
        )
        if default_nodes.count() > 0:
            raise exceptions.DefaultNodeAlreadyExists(
                f"Default node for {self.name} already exist"
            )

        super().save(*args, **kwargs)

    @property
    def connector(self):
        """Fetches a connector from registry.

        Returns:
            A connector to node that can to interact with blockchain.
        """
        NodeConnector = connectors.registry.get_by_node_name(  # pylint: disable=invalid-name
            self.name
        )
        return NodeConnector(
            rpc_host=self.rpc_host,
            rpc_port=self.rpc_port,
            rpc_username=self.rpc_username,
            rpc_password=self.rpc_password,
            timeout=getattr(settings, "BLOCKCHAIN_NODE_TIMEOUT", None),
        )


class Address(models.Model):
    # TODO: Rename to value
    address = models.CharField(max_length=500,)  # yapf: disable
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name="addrs",
        related_query_name="addr",
    )

    class Meta:
        unique_together = (("address", "currency"),)

    def __str__(self):
        return self.address


class Transaction(models.Model):
    node = models.ForeignKey(
        to=Node,
        on_delete=models.CASCADE,
        related_name="txs",
        related_query_name="tx",
    )
    address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        related_name="txs",
        related_query_name="tx",
    )
    txid = models.CharField(
        null=True, verbose_name="transaction id", max_length=500,
    )
    category = models.CharField(max_length=30,)  # yapf: disable
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=10,
        help_text="The transaction amount in currency",
    )
    fee = models.DecimalField(
        null=True,
        max_digits=19,
        decimal_places=10,
        help_text=(
            "The amount of the fee in currency. This is negative and "
            'only available for the "send" category of transactions.'
        ),
    )
    # TODO: add confirmation number
    is_confirmed = models.BooleanField(verbose_name="confirmed", default=False,)
    # TODO: To count in ms.
    timestamp = models.PositiveIntegerField(
        null=True,
        verbose_name="time",
        help_text="transaction creation timestamp",
    )
    timestamp_received = models.PositiveIntegerField(
        null=True,
        verbose_name="receipt time",
        help_text="transaction receipt time in timestamp",
    )

    objects = TransactionManager()

    class Meta:
        unique_together = (("node", "txid"),)

    def __str__(self):
        return f"{self.node.currency}, {self.txid}, {self.amount}"

    @property
    def amount_with_fee(self):
        # TODO: amount with fee only for 'send' category
        return self.amount - abs(self.fee)

    @property
    def currency(self) -> Currency:
        return self.node.currency

    def confirm(self) -> TransactionType:
        """Confirms the transaction.

        Returns:
            A transaction that was confirmed.
        """
        self.is_confirmed = True
        return self

    def send(self) -> TransactionType:
        """Sends a transaction in a blockchain."""
        if self.category == "receive":
            raise exceptions.CanNotSendReceivedTransaction(
                f"You can't send the received transaction."
            )

        sent_tx = self.node.connector.send_transaction(
            address=self.address.address, amount=str(self.amount),
        )
        self.is_confirmed = True
        self.fee = Decimal(sent_tx["fee"])
        self.txid = sent_tx["txid"]
        self.timestamp = sent_tx["timestamp"]
        self.timestamp_received = sent_tx["timestamp_received"]
        self.save()
        return self
