from abc import ABC, abstractmethod


class BaseConnector(ABC):
    # @abstractmethod
    # def __init__(self, rpc_host, rpc_port, rpc_username, rpc_password):
    #     pass

    @property
    @abstractmethod
    def symbol(self):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def check_txs(self):
        pass
