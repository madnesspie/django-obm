import abc
import json

import requests

from django_obm.blockchain.connectors import _base as base
from django_obm.blockchain.connectors import _exceptions as exceptions
from django_obm.blockchain.connectors import _utils as utils


class BaseBitcoinConnector(
    base.BaseConnector, abc.ABC
):  # pylint: disable=abstract-method
    symbol = "BTC"
    currency_name = "Bitcoin"
    default_min_confirmations = 2


class BitcoinCoreConnector(BaseBitcoinConnector):
    node_name = "bitcoin-core"

    def __init__(
        self, rpc_host, rpc_port, rpc_username, rpc_password, timeout=None
    ):
        super().__init__(timeout)
        url = f"{rpc_host}:{rpc_port}"
        self.rpc_url = "http://" + url if "http://" not in url else url
        self.auth = (rpc_username, rpc_password)
        self.headers = {
            "content-type": "application/json",
            "cache-control": "no-cache",
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
            error = response["error"]
            if error:
                raise exceptions.NodeError(error)
            result = response["result"]
            return result[return_key] if return_key else result
        except KeyError:
            raise exceptions.NodeInvalidResponceError(response)

    @staticmethod
    def format_transaction(tx):
        return {
            "txid": tx["txid"],
            "address": tx["address"] if "address" in tx else tx["de"],
            "category": tx["category"],
            "amount": tx["amount"],
            "fee": tx.get("fee", 0),
            "confirmations": tx["confirmations"],
            "timestamp": tx["time"],
            "timestamp_received": tx["timereceived"],
        }

    def list_transactions(self):
        txs = self._request(
            json.dumps({"method": "listtransactions", "params": ["*", 1000]})
        )
        return [self.format_transaction(tx) for tx in txs]

    def get_in_wallet_transaction(self, txid):
        return self._request(
            json.dumps({"method": "gettransaction", "params": [txid],})
        )

    def get_receipts(self):
        return [
            tx for tx in self.list_transactions() if tx["category"] == "receive"
        ]

    def get_new_address(self):
        return self._request(json.dumps({"method": "getrawchangeaddress"}))

    def get_addresses(self):
        return self._request(json.dumps({"method": "listaddressgroupings"}))

    def estimate_fee(self):
        return self._request(
            json.dumps({"method": "estimatesmartfee", "params": [1],}),
            return_key="feerate",
        )

    # pylint: disable=arguments-differ
    def send_transaction(
        self,
        address,
        amount,
        comment="",
        comment_to="",
        subtract_fee_from_amount=True,
    ):
        txid = self._request(
            json.dumps(
                {
                    "method": "sendtoaddress",
                    "params": [
                        address,
                        amount,
                        comment,
                        comment_to,
                        subtract_fee_from_amount,
                    ],
                }
            )
        )
        tx = self.get_in_wallet_transaction(txid)
        # Add address and category because otherwise it will be
        # in details list in response
        return self.format_transaction(
            {"address": address, "category": "send", **tx,}
        )


CONNECTOR_CLASSES = [BitcoinCoreConnector]
