import pytest
from django import urls


class TestTransactionViewSet:

    @staticmethod
    @pytest.mark.django_db
    def test_get(client):
        responce = client.get(urls.reverse('transaction-list'))
        result = responce.json()
        assert responce.status_code == 200
        assert result == []
