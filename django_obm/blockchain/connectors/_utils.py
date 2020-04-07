import functools

import requests

from django_obm.blockchain.connectors import _exceptions as exceptions


def catch_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.Timeout:
            self = args[0]
            raise exceptions.NetworkTimeoutError(
                f"The request to node was longer "
                f"than timeout: {self.timeout}"
            )
        except requests.exceptions.RequestException as exc:
            raise exceptions.NetworkError(exc)

    return wrapper
