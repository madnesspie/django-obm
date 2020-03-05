import abc
import json

import requests

from cc_framework.blockchain.connectors import _base as base
from cc_framework.blockchain.connectors import _exceptions as exceptions
from cc_framework.blockchain.connectors import _utils as utils


class BaseBitcoinConnector(base.BaseConnector, abc.ABC):  # pylint: disable=abstract-method
    symbol = 'BTC'
    currency_name = 'Bitcoin'
    default_min_confirmations = 2


class BitcoinCoreConnector(BaseBitcoinConnector):
    node_name = 'bitcoin-core'

    def __init__(self,
                 rpc_host,
                 rpc_port,
                 rpc_username,
                 rpc_password,
                 timeout=None):
        super().__init__(timeout)
        url = f"{rpc_host}:{rpc_port}"
        self.rpc_url = 'http://' + url if 'http://' not in url else url
        self.auth = (rpc_username, rpc_password)
        self.headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

    @utils.catch_errors
    def _request(self, payload, return_key=None):
        response = requests.post(
            self.rpc_url,
            data=payload,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        ).json()

        try:
            error = response['error']
            if error:
                raise exceptions.NodeError(error)
            result = response['result']
            return result[return_key] if return_key else result
        except KeyError:
            raise exceptions.NodeInvalidResponceError(response)

    def list_transactions(self):

        def _format(txs):
            formated_txs = []
            for tx in txs:
                formated_txs.append({
                    'txid': tx['txid'],
                    'address': tx['address'],
                    'category': tx['category'],
                    'amount': tx['amount'],
                    'fee': tx.get('fee', 0),
                    'confirmations': tx['confirmations'],
                    'timestamp': tx['time'],
                    'timestamp_received': tx['timereceived'],
                })
            return formated_txs

        payload = json.dumps({
            'method': 'listtransactions',
            'params': ['*', 1000]
        })
        return _format(self._request(payload))

    def get_receipts(self):
        return [
            tx for tx in self.list_transactions() if tx['category'] == 'receive'
        ]

    def get_new_address(self):
        return self._request(json.dumps({'method': 'getrawchangeaddress'}))

    def get_addresses(self):
        return self._request(json.dumps({'method': 'listaddressgroupings'}))

    def estimate_fee(self):
        payload = json.dumps({
            'method': 'estimatesmartfee',
            'params': [1],
        })
        return self._request(payload, return_key='feerate')

    # pylint: disable=arguments-differ
    def send_transaction(self,
                         address,
                         amount,
                         comment="",
                         comment_to="",
                         subtractfeefromamount=True):
        payload = json.dumps({
            'method': 'sendtoaddress',
            'params': [
                address, amount, comment, comment_to, subtractfeefromamount
            ],
        })
        return self._request(payload)


CONNECTOR_CLASSES = [BitcoinCoreConnector]
