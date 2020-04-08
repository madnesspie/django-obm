from django.db import models
from django.conf import settings


class NodeManager(models.Manager):

    transaction_model: type = None

    @classmethod
    def set_transaction_model(cls, transaction_model: type):
        cls.transaction_model = transaction_model

    def collect_transactions(self):
        """Fetches txs from nodes then write them into database."""
        txs = []
        lt_count = getattr("OBM_LIST_TRANSACTIONS_COUNT", settings, 50)
        for node in self.all():
            txs = node.connector.list_transactions(count=lt_count)
            if not txs:
                continue
        return self.transaction_model.objects.bulk_create(
            [self.transaction_model(**tx) for tx in txs]
        )
