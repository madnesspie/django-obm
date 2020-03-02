import abc
import json

import requests

from cryptocurrency.blockchains import utils
from cryptocurrency.blockchains.connectors import base


class BaseBitcoinConnector(base.BaseConnector, abc.ABC):  # pylint: disable=abstract-method
    symbol = 'BTC'
    currency_name = 'Bitcoin'
    default_min_confirmations = 2


class BitcoinCoreConnector(BaseBitcoinConnector):
    node_name = 'bitcoin-core'

    def __init__(
        self,
        rpc_host,
        rpc_port,
        rpc_username,
        rpc_password,
        timeout=None,
    ):
        super().__init__(timeout)
        url = f"{rpc_host}:{rpc_port}"
        self.rpc_url = 'http://' + url if 'http://' not in url else url
        self.auth = (rpc_username, rpc_password)
        self.headers = {
            'content-type': 'application/json',
            'cache-control': 'no-cache'
        }

    @utils.validate_responce
    def _request(self, payload):
        response = requests.post(
            self.rpc_url,
            data=payload,
            headers=self.headers,
            auth=self.auth,
            timeout=self.timeout,
        ).json()
        return response['result']

    def format(self, txs):
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

    def get_receipts(self):
        payload = json.dumps({
            'method': 'listtransactions',
            'params': ['*', 1000]
        })
        recently_receipts = filter(lambda tx: tx['category'] == 'receive',
                                   self._request(payload))
        return self.format(recently_receipts)

    def get_new_address(self):
        return self._request(json.dumps({'method': 'getrawchangeaddress'}))

    def get_addresses(self):
        return self._request(json.dumps({'method': 'listaddressgroupings'}))

    def get_fee(self):
        payload = json.dumps({
            'method': 'estimatesmartfee',
            'params': [1],
        })
        return self._request(payload)


CONNECTOR_CLASSES = [BitcoinCoreConnector]
