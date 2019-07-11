class CryprocerrencyError(Exception):
    """Base cryprocerrency exception."""


class CryprocerrencyWarning(Warning):
    """Base warning for cryprocerrency."""


class CurrencyDoesNotExistError(CryprocerrencyError):
    """This currency doesn't supported yet"""


class NodeDoesNotExistError(CryprocerrencyError):
    """This node doesn't supported yet"""
