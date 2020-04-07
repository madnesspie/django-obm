import importlib
import os
from collections import OrderedDict


class ConnectorRegistry:
    PACKAGE = "django_obm.blockchain.connectors"

    def __init__(self):
        self.connector_map = OrderedDict()
        self.available_currencies = set()
        self.loaded = False

    def __register(self, cls):
        self.connector_map[cls.node_name] = cls
        self.available_currencies.add(cls.symbol)

    @property
    def available_nodes(self):
        return set(self.connector_map.keys())

    @property
    def built_in(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return [
            file.replace(".py", "")
            for file in os.listdir(path)
            if os.path.isfile(os.path.join(path, file)) and file[0] != "_"
        ]

    def get_by_node_name(self, node_name):
        self.load()
        return self.connector_map[node_name]

    def currency_as_choices(self):
        self.load()
        return set(
            (cls.symbol, cls.currency_name)
            for cls in self.connector_map.values()
        )

    def connectors_as_choices(self):
        self.load()
        return [
            (cls.node_name, cls.node_name)
            for cls in self.connector_map.values()
        ]

    def load(self):
        if not self.loaded:
            module_names = self.built_in
            for module_name in module_names:
                try:
                    module = importlib.import_module(
                        name=f".{module_name}", package=self.PACKAGE,
                    )
                except ImportError:
                    pass
                else:
                    for cls in getattr(module, "CONNECTOR_CLASSES", []):
                        self.__register(cls)
            self.loaded = True
