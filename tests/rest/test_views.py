import pytest
from django import urls

from cryptocurrency.blockchains import connectors, models
from cryptocurrency.rest import views


class TestTransactionViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        responce = client.get(urls.reverse('transaction-list'))
        assert responce.status_code == 200
        result = responce.json()
        assert result == []

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures('bitcoin_core_node')
    def test_post(client):
        # TODO: Add fee
        responce = client.post(
            urls.reverse('transaction-list'),
            data={
                'currency': 'BTC',
                'address': 'fake-addr',
                'category': 'send',
                'amount': 10,
                'is_confirmed': False,
                'timestamp': 1562415913,
                'timestamp_received': 1562415913,
            },
        )
        assert responce.status_code == 201
        assert models.Transaction.objects.count() == 1


class TestAddressViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        responce = client.get(urls.reverse('address-list'))
        assert responce.status_code == 200
        result = responce.json()
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

        responce = client.post(
            urls.reverse('address-list'),
            data={
                'currency': 'BTC',
            },
        )
        assert responce.status_code == 201
        assert models.Address.objects.count() == 1
        assert responce.json()['address'] == 'fake-addr'


class TestCurrencyViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        responce = client.get(urls.reverse('currency-list'))
        assert responce.status_code == 200
        result = responce.json()
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

        responce = client.get(
            urls.reverse(
                'currency-estimated-fee',
                args=(bitcoin_currency.id,),
            ))
        assert responce.status_code == 200
        result = responce.json()
        assert result['estimated_fee'] == 0.0001
