# pylint: disable=multiple-statements
import abc


class BaseConnector(abc.ABC):

    DEFAULT_TIMEOUT = 3
    TX_KEYS_FORMAT = (
        "address",
        "amount",
        "category",
        "confirmations",
        "timestamp",
        "timestamp_received",
        "txid",
        "fee",
    )

    def __init__(self, timeout=None):
        self.timeout = self.__validate_timeout(timeout)

    @classmethod
    def __validate_timeout(cls, value):
        try:
            if value is None:
                return cls.DEFAULT_TIMEOUT
            if float(value) > 0:
                return value
        except ValueError:
            raise ValueError("Timeout must be a number")
        raise ValueError("Timeout must be greater than zero")

    @property
    @abc.abstractmethod
    def symbol(self):
        ...

    @property
    @abc.abstractmethod
    def currency_name(self):
        ...

    @property
    @abc.abstractmethod
    def node_name(self):
        ...

    @property
    @abc.abstractmethod
    def default_min_confirmations(self):
        ...

    @abc.abstractmethod
    def get_receipts(self):
        ...

    @abc.abstractmethod
    def get_new_address(self):
        ...

    @abc.abstractmethod
    def estimate_fee(self):
        ...

    @abc.abstractmethod
    def send_transaction(self, address, amount, **kwargs):
        ...
