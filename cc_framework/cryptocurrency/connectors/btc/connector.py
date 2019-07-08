import requests
import json

from .. import base


class BitcoinCoreConnector(base.BaseConnector):
    symbol = 'BTC'
    currency_name = 'Bitcoin'
    node_name = 'bitcoin-core'

    def __init__(self, rpc_host, rpc_port, rpc_username, rpc_password):
        self.rpc_url = f"{rpc_host}:{rpc_port}/"
        self.auth = (rpc_username, rpc_password)
        self.headers = {'content-type': "application/json",
                        'cache-control': "no-cache"}

    def __request(self, payload):
        response = requests.post(
            self.rpc_url, data=payload, headers=self.headers, auth=self.auth
        ).json()
        return response['result']

    def get_receipts(self):
        payload = json.dumps({"method": 'listtransactions',
                              "params": ['*', 1000]})
        recently_receipts = filter(
            lambda tx: tx['category'] == 'receive',
            self.__request(payload)
        )
        return recently_receipts

    def get_new_address(self):
        payload = json.dumps({"method": 'getrawchangeaddress'})
        return self.__request(payload)

    def get_addresses(self):
        payload = json.dumps({"method": 'listaddressgroupings'})
        return self.__request(payload)


connector_classes = [BitcoinCoreConnector]
