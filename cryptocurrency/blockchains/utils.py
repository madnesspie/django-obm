import functools
import warnings

import requests
from django.conf import settings

from cryptocurrency import blockchains

_DEFAULT_TIMEOUT = 5


def get_timeout_setting():
    return getattr(settings, 'CC_FRAMEWORK', {}).get(
        'TIMEOUT',
        _DEFAULT_TIMEOUT,
    )


def validate_responce(func):

    @functools.wraps(func)
    def wrapper(args, kwargs):
        result = []
        try:
            result = func(args, kwargs)
        except KeyError:
            warnings.warn(
                f'Node\'ve returned invalid result: {result}',
                blockchains.exceptions.InvalidNodeResponseWarning,
            )
        except requests.exceptions.Timeout:
            warnings.warn(
                f'The request to node was longer '
                f'than timeout: {get_timeout_setting()}',
                blockchains.exceptions.TimeoutNodeResponseWarning,
            )
        except requests.exceptions.RequestException as error:
            warnings.warn(
                f'RequestException: {error}',
                blockchains.exceptions.BadRequestWarning,
            )
        return result

    return wrapper
