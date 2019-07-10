import json
import requests

from cryptocurrency.connectors import base, utils


class BitcoinCoreConnector(base.BaseConnector):
    symbol = 'BTC'
    currency_name = 'Bitcoin'
    node_name = 'bitcoin-core'

    def __init__(self, rpc_host, rpc_port, rpc_username, rpc_password):
        self.rpc_url = f"{rpc_host}:{rpc_port}"
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
            timeout=base.TIMEOUT,
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
        payload = json.dumps({'method': 'getrawchangeaddress'})
        return self._request(payload)

    def get_addresses(self):
        payload = json.dumps({'method': 'listaddressgroupings'})
        return self._request(payload)


CONNECTOR_CLASSES = [BitcoinCoreConnector]
