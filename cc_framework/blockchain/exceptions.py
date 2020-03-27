class BaseError(Exception):
    """Base cryprocerrency exception."""


class CurrencyDoesNotExistError(BaseError):
    """This currency doesn't supported yet."""


class NodeDoesNotExistError(BaseError):
    """This node doesn't supported yet."""


class DefaultNodeDoesNotExistError(NodeDoesNotExistError):
    """Missing default node for currency."""


class TooManyDefaultNodes(BaseError):
    """Default nodes number greater than one."""


class DefaultNodeAlreadyExists(BaseError):
    """Default node already exists for currency."""


class CanNotSendReceivedTransaction(BaseError):
    """Trying to send received transaction wth ORM."""
