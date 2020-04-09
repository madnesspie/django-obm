from django.conf import settings
from django.db import models


class NodeManager(models.Manager):

    transaction_model = None

    def __init__(self, transaction_model=None):
        super().__init__()
        self.transaction_model = transaction_model

    def collect_transactions(self):
        """Fetches txs from nodes then write them into database."""
        txs = []
        lt_count = getattr(settings, "OBM_LIST_TRANSACTIONS_COUNT", 50)
        for node in self.all():
            txs += node.list_transactions(count=lt_count)
        return self.transaction_model.objects.bulk_create(
            [self.transaction_model(**tx) for tx in txs]
        )
