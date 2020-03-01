from rest_framework import serializers

from cryptocurrency.blockchains import models
from cryptocurrency.rest import validators


class TransactionSerializer(serializers.ModelSerializer):
    # TODO: Add custom validators support
    # TODO: Adjust max_length
    currency = serializers.CharField(
        max_length=100,
        validators=[validators.currency_exists],
    )
    address = serializers.CharField(max_length=500)

    class Meta:
        model = models.Transaction
        read_only_fields = ['txid']
        fields = [
            'currency', 'address', 'txid', 'category', 'amount', 'fee',
            'is_confirmed', 'timestamp', 'timestamp_received'
        ]

    def validate(self, attrs):
        currency = attrs.pop('currency')

        # TODO: Add filter with default
        node = models.Node.objects.filter(currency__name=currency).first()
        if not node:
            raise serializers.ValidationError(
                f'Node for {currency} does not registred')

        address, _ = models.Address.objects.get_or_create(
            address=attrs.pop('address'),
            currency=models.Currency.objects.get(name=currency),
        )

        return {
            'node': node,
            'address': address,
            **attrs,
        }


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Address
        fields = '__all__'
