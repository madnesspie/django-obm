# Copyright 2019-2020 Alexander Polishchuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import TypeVar

from django.conf import settings
from django.db import models
from obm import connectors, validators
from obm.sync import mixins

from django_obm import exceptions, managers

TTransaction = TypeVar("TTransaction", bound="Transaction")
TNode = TypeVar("TNode", bound="Node")


class Currency(models.Model):
    name = models.CharField(max_length=100, unique=True,)

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
    value = models.CharField(max_length=500,)
    currency = models.ForeignKey(
        to=Currency,
        on_delete=models.CASCADE,
        related_name="addresses",
        related_query_name="address",
    )
    password = models.CharField(max_length=500, default="")

    class Meta:
        unique_together = (("value", "currency"),)

    def __str__(self):
        return f"{self.currency}:{self.value}"


class Transaction(models.Model):
    node = models.ForeignKey(
        to="Node",
        on_delete=models.CASCADE,
        related_name="transactions",
        related_query_name="transaction",
    )
    from_address = models.ForeignKey(
        to=Address, on_delete=models.CASCADE, null=True,
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
        help_text="The transaction amount in currency.",
    )
    block_number = models.PositiveIntegerField(
        null=True, help_text="Number of block that contain the transaction.",
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
        null=True, help_text="Transaction creation or detection timestamp.",
    )

    class Meta:
        unique_together = (("node", "txid"),)

    def __str__(self):
        return f"{self.currency}:{self.txid}"

    # @property
    # def amount_with_fee(self):
    #     # TODO: amount with fee only for 'send' category
    #     return self.amount - abs(self.fee)

    @property
    def currency(self) -> Currency:
        return self.node.currency

    def send(self, subtract_fee_from_amount: bool = False):
        tx = {
            "amount": self.amount,
            "to_address": self.to_address.value,
        }
        if self.currency.name == "ethereum":
            if self.from_address:
                tx["from_address"] = self.from_address.value
                tx["password"] = self.from_address.password
        elif self.currency.name == "bitcoin" and self.fee:
            tx["fee"] = self.fee

        sent_tx = self.node.send_transaction(
            **tx, subtract_fee_from_amount=subtract_fee_from_amount,
        )
        self.node.close()
        self.txid = sent_tx["txid"]
        self.fee = sent_tx["fee"]
        self.amount = sent_tx["amount"]
        self.timestamp = sent_tx["timestamp"]
        self.save()
        return self


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
            "for transaction sending."
        ),
    )
    rpc_username = models.CharField(
        verbose_name="RPC username",
        max_length=200,
        help_text="Username for JSON-RPC connections.",
    )
    rpc_password = models.CharField(
        verbose_name="RPC password",
        max_length=200,
        help_text="Password for JSON-RPC connections.",
    )
    rpc_host = models.URLField(
        verbose_name="RPC host",
        default="127.0.0.1",
        help_text="Listen for JSON-RPC connections on this IP address.",
    )
    rpc_port = models.PositiveIntegerField(
        verbose_name="RPC port",
        help_text="Listen for JSON-RPC connections on this port.",
    )
    timeout = models.FloatField(
        default=getattr(
            settings, "OBM_NODE_TIMEOUT", connectors.DEFAULT_TIMEOUT
        ),
        help_text="Timeout for call of node JSON RPC.",
    )

    objects = managers.NodeManager(Transaction, Address)

    class Meta:
        unique_together = (("rpc_host", "rpc_port"),)

    def __init__(self, *args, **kwargs):
        self.loop = None
        self.session = None
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # pylint: disable=arguments-differ
        validators.validate_node_is_supported(self.name)
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
        super().delete(using, keep_parents)
