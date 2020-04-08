from typing import TypeVar

from django.db import models
from obm import connectors
from obm.sync import mixins

from django_obm import exceptions, managers

TTransaction = TypeVar("TTransaction", bound="Transaction")
TNode = TypeVar("TNode", bound="Node")


class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True)
    min_confirmations = models.IntegerField(
        help_text=(
            "Minimum confirmations number after which a transaction will "
            "get the status 'is confirmed'"
        ),
    )

    class Meta:
        verbose_name_plural = "currencies"

    def __str__(self):
        return self.name

    @property
    def default_node(self) -> TNode:
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


class Address(models.Model):
    # TODO: Rename to value
    address = models.CharField(max_length=500,)
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name="addresses",
        related_query_name="address",
    )

    class Meta:
        unique_together = (("address", "currency"),)

    def __str__(self):
        return f"{self.currency}:{self.address}"


class Transaction(models.Model):
    node = models.ForeignKey(
        to="Node",
        on_delete=models.CASCADE,
        related_name="transactions",
        related_query_name="transaction",
    )
    from_address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        null=True,
    )
    to_address = models.ForeignKey(
        to=Address,
        on_delete=models.CASCADE,
        related_name="transactions",
        related_query_name="transaction",
    )
    txid = models.CharField(
        null=True, verbose_name="transaction id", max_length=500,
    )
    category = models.CharField(max_length=30)
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=10,
        help_text="The transaction amount in currency",
    )
    block_number = models.PositiveIntegerField(
        null=True,
        help_text="Number of block that contain the transaction.",
    )
    fee = models.DecimalField(
        null=True,
        max_digits=19,
        decimal_places=10,
        help_text=(
            "The amount of the fee in currency. This is only available for "
            "the 'send' category of transactions."
        ),
    )
    timestamp = models.PositiveIntegerField(
        null=True,
        help_text="Transaction creation or detection timestamp.",
    )

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


class Node(models.Model, mixins.ConnectorMixin):
    # TODO: Add validators
    name = models.CharField(max_length=200, unique=True,)
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name="nodes",
        related_query_name="node",
    )
    is_default = models.BooleanField(
        default=True,
        help_text=(
            "If True the node will be used as default "
            "for transaction sending"
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
        default="127.0.0.1",
        help_text="Listen for JSON-RPC connections on this IP address",
    )
    rpc_port = models.PositiveIntegerField(
        verbose_name="RPC port",
        help_text="Listen for JSON-RPC connections on this port",
    )

    objects = managers.NodeManager(Transaction)

    class Meta:
        unique_together = (("rpc_host", "rpc_port"),)

    def __init__(self, *args, **kwargs):
        self.loop = None
        self.session = None
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        if self.name not in connectors.MAPPING:
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

    def delete(self, using=None, keep_parents=False):
        self.close()
        super().save(using, keep_parents)
