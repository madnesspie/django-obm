from rest_framework import serializers

from cryptocurrency.blockchains import models
from cryptocurrency.rest import validators


class TransactionSerializer(serializers.ModelSerializer):
    # TODO: Add custom validators support
    # TODO: Adjust max_length
    address = serializers.CharField(max_length=500)
    currency = serializers.CharField(
        max_length=100,
        validators=[validators.currency_exists],
    )

    class Meta:
        model = models.Transaction
        read_only_fields = ['txid']
        fields = [
            'id', 'currency', 'address', 'txid', 'category', 'amount', 'fee',
            'is_confirmed', 'timestamp', 'timestamp_received'
        ]

    def validate(self, attrs):
        currency = models.Currency.objects.get(name=attrs.pop('currency'))

        # TODO: Add filter with default
        node = models.Node.objects.filter(
            currency=currency,
            is_default=True,
        ).first()
        if not node:
            raise serializers.ValidationError(
                f'Node for {currency} does not registered')

        address, _ = models.Address.objects.get_or_create(
            address=attrs.pop('address'),
            currency=currency,
        )

        return {
            'node': node,
            'address': address,
            **attrs,
        }


class AddressSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        slug_field='name',
        queryset=models.Currency.objects.all(),
    )

    class Meta:
        model = models.Address
        fields = '__all__'
