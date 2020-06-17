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
import collections
import sys

from django.db import models


class NodeManager(models.Manager):

    transaction_model = None

    def __init__(self, transaction_model=None, address_model=None):
        super().__init__()
        # Hack to avoid cyclic import
        # TODO: Point out how ti improve it
        self.transaction_model = transaction_model
        self.address_model = address_model

    def fetch_recent_transactions(self, limit: int = 50):
        """Fetches recent transactions from a blockchain."""

        def omit_info(tx):
            return {key: value for key, value in tx.items() if key != "info"}

        def to_address(value, currency):
            if value is None:
                return value
            address, _ = self.address_model.objects.get_or_create(
                value=value,
                currency=currency,
            )
            return address

        recent_transactions = []
        for node in self.all():
            with node:
                node_recent_transactions = node.fetch_recent_transactions(limit)
            recent_transactions += [
                self.transaction_model(  # type: ignore
                    node=node,
                    from_address=to_address(
                        tx.pop("from_address"),
                        node.currency,
                    ),
                    to_address=to_address(
                        tx.pop("to_address"),
                        node.currency,
                    ),
                    **omit_info(tx),
                )
                for tx in node_recent_transactions
            ]
        return recent_transactions

    def bulk_create_recent_transactions(self, limit: int = 50) -> list:
        """Create in the database recent transactions from blockchain.

        Args:
            limit: Limit of recent transactions to create. Defaults to 50.

        Returns:
            List of created recent transactions.
        """
        recent_tx = self.fetch_recent_transactions(limit)
        return self.transaction_model.objects.bulk_create(  # type: ignore
            recent_tx, ignore_conflicts=True,
        )

    def sync_transactions(self, recent_limit: int = 50):
        def remove_duplicates(recent_txs, synchronized_txs):
            recent_txs = {tx.txid: tx for tx in recent_txs}
            synchronized_txs = {tx.txid: tx for tx in synchronized_txs}
            for txid, tx in recent_txs.items():
                if txid not in synchronized_txs:
                    synchronized_txs[txid] = tx
            return sorted(
                synchronized_txs.values(),
                key=lambda tx: (
                    # If block_number is None it means that transaction still
                    # in mempool (wait for confirmation). In this case, it
                    # should be considered as the newest (with the highest
                    # block number).
                    sys.maxsize if tx.block_number is None else tx.block_number
                ),
                reverse=True,
            )

        recent_txs = self.bulk_create_recent_transactions(recent_limit)
        # TODO: Exclude transactions that have just added
        synchronized_txs = self.transaction_model.objects.sync()  # type: ignore
        return remove_duplicates(recent_txs, synchronized_txs)


class TransactionManager(models.Manager):
    def sync(self) -> list:
        """Synchronize still unconfirmed transactions with blockchain.

        Make sense to synchronize only a transaction that still have
        block_number = None. Because transaction that have already added to
        block is unchanging by blockchain design.

        Returns:
            Updated transactions list.
        """

        def update(txs, current_txs):
            txs = {tx.txid: tx for tx in txs}
            for current_tx in current_txs:
                tx = txs[current_tx["txid"]]
                tx.block_number = current_tx["block_number"]
            return list(txs.values())

        txs_by_node = collections.defaultdict(list)
        for tx in self.filter(block_number=None):
            txs_by_node[tx.node].append(tx)

        synchronized_txs = []
        for node, txs in txs_by_node.items():
            with node:
                current_txs = node.fetch_in_wallet_transactions(
                    [tx.txid for tx in txs]
                )
            updated_txs = update(txs, current_txs)
            synchronized_txs += updated_txs
            self.bulk_update(updated_txs, ["block_number"])

        return synchronized_txs
