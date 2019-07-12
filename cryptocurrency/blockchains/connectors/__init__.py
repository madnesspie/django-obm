from cryptocurrency.blockchains.connectors import _registry
from cryptocurrency.blockchains.connectors._base import BaseConnector
from cryptocurrency.blockchains.connectors.btc import BitcoinCoreConnector

registry = _registry.ConnectorRegistry()  # pylint: disable=invalid-name
