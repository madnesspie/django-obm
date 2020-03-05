import functools

import requests
from django.conf import settings

from cc_framework.blockchain.connectors import _exceptions as exceptions

_DEFAULT_TIMEOUT = 3


def get_timeout_setting():
    return getattr(settings, 'CC_FRAMEWORK', {}).get(
        'TIMEOUT',
        _DEFAULT_TIMEOUT,
    )


def catch_errors(func):

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            raise exceptions.NetworkTimeoutError(
                f'The request to node was longer '
                f'than timeout: {get_timeout_setting()}')
        except requests.exceptions.RequestException as exc:
            raise exceptions.NetworkError(exc)

    return wrapper
