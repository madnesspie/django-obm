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
from django.conf import settings
from django.db import models


class NodeManager(models.Manager):

    transaction_model = None

    def __init__(self, transaction_model=None, address_model=None):
        super().__init__()
        self.transaction_model = transaction_model
        self.address_model = address_model

    def collect_transactions(self):
        """Fetches txs from nodes then write them into database."""

        def omit_info(tx):
            return {key: value for key, value in tx.items() if key != "info"}

        def to_address(value, currency):
            address, _ = self.address_model.objects.get_or_create(
                value=value, currency=currency
            )
            return address

        collected_txs = []
        lt_count = getattr(settings, "OBM_LIST_TRANSACTIONS_COUNT", 50)
        for node in self.all():
            recent_txs = node.list_transactions(count=lt_count)
            collected_txs += self.transaction_model.objects.bulk_create(
                [
                    self.transaction_model(
                        node=node,
                        from_address=to_address(
                            tx.pop("from_address"), node.currency
                        ),
                        to_address=to_address(
                            tx.pop("to_address"), node.currency,
                        ),
                        **omit_info(tx),
                    )
                    for tx in recent_txs
                ],
                ignore_conflicts=True,
            )
            node.close()
        return collected_txs
