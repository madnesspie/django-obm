import importlib
from collections import OrderedDict

from django.conf import settings


class ConnectorRegistry:
    def __init__(self):
        self.connector_map = OrderedDict()
        self.loaded = False

    def get_list(self, request=None):
        self.load()
        return [
            connector_cls(request)
            for connector_cls in self.connector_map.values()]

    def register(self, cls):
        self.connector_map[cls.id] = cls

    def by_symbol(self, symbol, request=None):
        self.load()
        return self.connector_map[symbol](request=request)

    def as_choices(self):
        self.load()
        for connector_cls in self.connector_map.values():
            yield (connector_cls.symbol, connector_cls.name)

    def load(self):
        if not self.loaded:
            for app in settings.INSTALLED_APPS:
                try:
                    connector_module = importlib.import_module(
                        app + '.connector'
                    )
                except ImportError:
                    pass
                else:
                    for cls in getattr(
                        connector_module, 'connector_classes', []
                    ):
                        self.register(cls)
            self.loaded = True


register = ConnectorRegistry()
