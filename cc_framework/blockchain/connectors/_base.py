# pylint: disable=multiple-statements
import abc

from cc_framework.blockchain import utils

TX_KEYS_FORMAT = ('address', 'amount', 'category', 'confirmations', 'timestamp',
                  'timestamp_received', 'txid', 'fee')


class BaseConnector(abc.ABC):

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
            value = utils.get_timeout_setting()
        self.__timeout = self.__validate_timeout(value)

    @property
    @abc.abstractmethod
    def symbol(self): ...

    @property
    @abc.abstractmethod
    def currency_name(self): ...

    @property
    @abc.abstractmethod
    def node_name(self): ...

    @property
    @abc.abstractmethod
    def default_min_confirmations(self): ...

    @abc.abstractmethod
    def format(self, txs): ...

    @abc.abstractmethod
    def get_receipts(self): ...

    @abc.abstractmethod
    def get_new_address(self): ...

    @abc.abstractmethod
    def estimate_fee(self): ...

    @abc.abstractmethod
    def send_transaction(self): ...
