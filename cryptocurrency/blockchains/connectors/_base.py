import abc

from django.conf import settings

TX_KEYS_FORMAT = ('address', 'amount', 'category', 'confirmations', 'timestamp',
                  'timestamp_received', 'txid', 'fee')


class BaseConnector(abc.ABC):
    DEFAULT_TIMEOUT = 5

    def __init__(self, timeout):
        self.timeout = timeout

    @staticmethod
    def __validate_timeout(value):
        try:
            if float(value) > 0:
                return value
        except ValueError:
            raise ValueError('Timeout must be a number')
        raise ValueError('Timeout must be greater than zero')

    @property
    def timeout(self):
        return self.__timeout

    @timeout.setter
    def timeout(self, value):
        if not value:
            value = getattr(settings, 'CC_FRAMEWORK', {}).get(
                'TIMEOUT',
                self.DEFAULT_TIMEOUT,
            )
        self.__timeout = self.__validate_timeout(value)

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
