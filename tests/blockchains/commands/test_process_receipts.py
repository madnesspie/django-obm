import copy
import io

import pytest
from django.core import management

from cc_framework.blockchain import connectors
from tests.blockchains.connectors import data


class TestCommand:

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_add_transaction(monkeypatch):

        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            '_request',
            lambda *_: data.BTC_TXS,
        )

        out = io.StringIO()
        management.call_command('process_receipts', once=True, stdout=out)
        assert 'Start' in out.getvalue()
        assert 'Run' in out.getvalue()
        assert 'Added' in out.getvalue()

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node', 'btc_transaction')
    def test_confirm_transaction(monkeypatch):
        # Increases confirmations number for the fixture tx in test_btc.TXS
        mock_txs = copy.deepcopy(data.BTC_TXS)
        mock_txs[0]['confirmations'] = 666

        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            '_request',
            lambda *_: data.BTC_TXS,
        )

        out = io.StringIO()
        management.call_command('process_receipts', once=True, stdout=out)
        assert 'Start' in out.getvalue()
        assert 'Run' in out.getvalue()
        assert 'Added' in out.getvalue()
