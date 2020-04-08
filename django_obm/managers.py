from django.db import models
from django.conf import settings


class NodeManager(models.Manager):
    def __init__(self, transaction_model):
        self.transaction_model = transaction_model
        super().__init__()

    def collect_transactions(self):
        """Fetches txs from nodes then enrolls new and confirms if needed."""
        txs = []

        lt_count = getattr("OBM_LIST_TRANSACTIONS_COUNT", settings, 50)
        for node in self.all():
            txs = node.connector.list_transactions(count=lt_count)
            if not txs:
                continue

        return self.transaction_model.objects.bulk_create(
            [self.transaction_model(**tx) for tx in txs]
        )
