import pytest
from django import urls

from cc_framework.blockchain import connectors, models


class TestTransactionViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        response = client.get(urls.reverse('transaction-list'))
        assert response.status_code == 200
        result = response.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_post(monkeypatch, client):
        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            'send_transaction',
            lambda *_, **__: {
                'fee': 0.0000001,
                'txid': 'fake-txid',
                'timestamp': 1562415913,
                'timestamp_received': 1562415913,
            },
        )

        # TODO: Add fee
        response = client.post(
            urls.reverse('transaction-list'),
            data={
                'currency': 'BTC',
                'address': 'fake-addr',
                'amount': 10,
            },
        )
        assert response.status_code == 201
        assert models.Transaction.objects.count() == 1
        result = response.json()
        assert result['txid'] == 'fake-txid'
        assert float(result['fee']) == 0.0000001


@pytest.mark.integration
class TestTransactionViewSetIntegration:

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_post(client):
        amount_to_send = 0.00001
        in_wallet_address = '2NAmne8BsSXWbV5iStkVzL4vW7Z4F6a5o68'
        # TODO: Add fee
        response = client.post(
            urls.reverse('transaction-list'),
            data={
                'currency': 'BTC',
                'address': in_wallet_address,
                'amount': str(amount_to_send),
            },
        )
        assert response.status_code == 201
        assert models.Transaction.objects.count() == 1
        result = response.json()
        assert isinstance(result, dict)
        assert isinstance(result['txid'], str)
        assert result['address'] == in_wallet_address
        assert result['category'] == 'send'
        assert result['is_confirmed'] is True
        # tests that fee subtract from amount
        assert float(result['amount']) == amount_to_send
        assert float(result['amount_with_fee']) < amount_to_send



class TestAddressViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        response = client.get(urls.reverse('address-list'))
        assert response.status_code == 200
        result = response.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_post(monkeypatch, client):

        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            'get_new_address',
            lambda *_, **__: 'fake-addr',
        )

        response = client.post(
            urls.reverse('address-list'),
            data={
                'currency': 'BTC',
            },
        )
        assert response.status_code == 201
        assert models.Address.objects.count() == 1
        assert response.json()['address'] == 'fake-addr'


class TestCurrencyViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        response = client.get(urls.reverse('currency-list'))
        assert response.status_code == 200
        result = response.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_get_estimate_fee(monkeypatch, client, bitcoin_currency):
        monkeypatch.setattr(
            connectors.btc.BitcoinCoreConnector,
            'estimate_fee',
            lambda *_, **__: 0.0001,
        )

        response = client.get(
            urls.reverse(
                'currency-estimated-fee',
                args=(bitcoin_currency.id,),
            ))
        assert response.status_code == 200
        result = response.json()
        assert result['estimated_fee'] == 0.0001
