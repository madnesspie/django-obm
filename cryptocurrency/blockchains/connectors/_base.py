import abc

from django.conf import settings

CC_FRAMEWORK = getattr(settings, 'CC_FRAMEWORK', {})
TIMEOUT = CC_FRAMEWORK.get('NODE_TIMEOUT', 5)
TX_KEYS_FORMAT = (
    'address', 'amount', 'category', 'confirmations', 'timestamp',
    'timestamp_received', 'txid', 'fee'
)


class BaseConnector(abc.ABC):
    @property
    @abc.abstractmethod
    def symbol(self):
        pass

    @property
    @abc.abstractmethod
    def currency_name(self):
        pass

    @property
    @abc.abstractmethod
    def node_name(self):
        pass

    @property
    @abc.abstractmethod
    def default_min_confirmations(self):
        pass

    @abc.abstractmethod
    def format(self, txs):
        pass

    @abc.abstractmethod
    def get_receipts(self):
        pass

    @abc.abstractmethod
    def get_new_address(self):
        pass
