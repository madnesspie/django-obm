import json
import requests

from cryptocurrency.connectors import base


class BitcoinCoreConnector(base.BaseConnector):
    symbol = 'BTC'
    currency_name = 'Bitcoin'
    node_name = 'bitcoin-core'

    def __init__(self, rpc_host, rpc_port, rpc_username, rpc_password):
        self.rpc_url = f"{rpc_host}:{rpc_port}"
        self.auth = (rpc_username, rpc_password)
        self.headers = {'content-type': 'application/json',
                        'cache-control': 'no-cache'}

    def __request(self, payload):
        response = requests.post(
            self.rpc_url,
            data=payload,
            headers=self.headers,
            auth=self.auth,
            timeout=5
        ).json()
        return response['result']

    def get_txs(self):
        payload = json.dumps({'method': 'listtransactions',
                              'params': ['*', 1000]})
        return self.__request(payload)

    def get_receipts(self):
        recently_receipts = filter(
            lambda tx: tx['category'] == 'receive',
            self.get_txs()
        )
        return list(recently_receipts)

    def get_new_address(self):
        payload = json.dumps({'method': 'getrawchangeaddress'})
        return self.__request(payload)

    def get_addresses(self):
        payload = json.dumps({'method': 'listaddressgroupings'})
        return self.__request(payload)


CONNECTOR_CLASSES = [BitcoinCoreConnector]
