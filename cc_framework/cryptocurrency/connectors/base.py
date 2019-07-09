from abc import ABC, abstractmethod


class BaseConnector(ABC):
    @property
    @abstractmethod
    def symbol(self):
        pass

    @property
    @abstractmethod
    def currency_name(self):
        pass

    @property
    @abstractmethod
    def node_name(self):
        pass

    @abstractmethod
    def get_receipts(self):
        pass

    @abstractmethod
    def get_new_address(self):
        pass
