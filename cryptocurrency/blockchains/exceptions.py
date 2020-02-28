class CryprocerrencyError(Exception):
    """Base cryprocerrency exception."""


class CryprocerrencyWarning(Warning):
    """Base warning for cryprocerrency."""


class CurrencyDoesNotExistError(CryprocerrencyError):
    """This currency doesn't supported yet"""



class NodeDoesNotExistError(CryprocerrencyError):
    """This node doesn't supported yet"""


# connectors warnings


class ConnectorWarning(CryprocerrencyWarning):
    """Base warning for connectors."""


class BadRequestWarning(ConnectorWarning):
    """An error occurred during the request."""


class InvalidNodeResponseWarning(ConnectorWarning):
    """Node've returned invalid result."""


class TimeoutNodeResponseWarning(ConnectorWarning):
    """The request to node timed out. """
