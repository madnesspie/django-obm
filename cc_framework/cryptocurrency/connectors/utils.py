import functools
import warnings

import requests

from cryptocurrency import connectors
from cryptocurrency.connectors import base


def validate_responce(func):
    @functools.wraps(func)
    def wrapper(args, kwargs):
        result = []
        try:
            result = func(args, kwargs)
        except KeyError:
            warnings.warn(
                f'Node\'ve returned invalid result: {result}',
                connectors.exceptions.InvalidNodeResponseWarning,
            )
        except requests.exceptions.Timeout:
            warnings.warn(
                f'The request to node longer than timed out: {base.TIMEOUT}',
                connectors.exceptions.TimeoutNodeResponseWarning,
            )
        except requests.exceptions.RequestException as error:
            warnings.warn(
                f'RequestException: {error}',
                connectors.exceptions.BadRequestWarning,
            )
        return result

    return wrapper
