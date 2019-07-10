import functools
import warnings

import requests

from cryptocurrency.connectors import base, exceptions


def validate_responce(func):
    @functools.wraps(func)
    def wrapper(args, kwargs):
        result = []
        try:
            result = func(args, kwargs)
        except KeyError:
            warnings.warn(
                f'Node\'ve returned invalid result: {result}',
                exceptions.InvalidNodeResponseWarning,
            )
        except requests.exceptions.Timeout:
            warnings.warn(
                f'The request to node longer than timed out: {base.TIMEOUT}',
                exceptions.TimeoutNodeResponseWarning,
            )
        except requests.exceptions.RequestException as error:
            warnings.warn(
                f'RequestException: {error}',
                exceptions.BadRequestWarning,
            )
        return result

    return wrapper
