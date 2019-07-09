import abc


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

    @abc.abstractmethod
    def get_receipts(self):
        pass

    @abc.abstractmethod
    def get_new_address(self):
        pass
