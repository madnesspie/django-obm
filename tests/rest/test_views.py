import pytest
from django import urls

from cryptocurrency.blockchains import models


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
