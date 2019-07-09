import os
import importlib
from collections import OrderedDict

from django.conf import settings


class ConnectorRegistry:
    PACKAGE = 'cryptocurrency.connectors'

    def __init__(self):
        self.connector_map = OrderedDict()
        self.loaded = False

    def __register(self, cls):
        self.connector_map[cls.node_name] = cls

    @property
    def built_in(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return [file for file in os.listdir(path)
                if os.path.isdir(os.path.join(path, file)) and file[0] != '_']

    def get(self, node_name):
        self.load()
        return self.connector_map[node_name]

    def symbols_as_choices(self):
        self.load()
        return set((cls.symbol, cls.symbol)
                   for cls in self.connector_map.values())

    def connectors_as_choices(self):
        self.load()
        return [(cls.node_name, cls.node_name)
                for cls in self.connector_map.values()]

    def load(self):
        if not self.loaded:
            connector_dirs = self.built_in
            for connector_dir in connector_dirs:
                try:
                    connector_module = importlib.import_module(
                        name=f".{connector_dir}.connector",
                        package=self.PACKAGE
                    )
                except ImportError:
                    # TODO: Add warning
                    raise
                else:
                    for cls in getattr(
                        connector_module, 'connector_classes', []
                    ):
                        self.__register(cls)
            self.loaded = True


register = ConnectorRegistry()
