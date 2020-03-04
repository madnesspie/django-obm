from cryptocurrency.blockchain.connectors import _base as base
from cryptocurrency.blockchain.connectors import _registry, btc

registry = _registry.ConnectorRegistry()  # pylint: disable=invalid-name
