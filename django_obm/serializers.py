# Copyright 2019-2020 Alexander Polishchuk
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from rest_framework import serializers

from django_obm import models


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    # TODO: Add custom validators support
    # TODO: Adjust max_length
    address = serializers.CharField(max_length=500)
    currency = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Currency.objects.all(),
    )

    class Meta:
        model = models.Transaction
        read_only_fields = [
            "txid",
            "category",
            "fee",
            "timestamp",
            "timestamp_received",
            "amount_with_fee",
        ]
        fields = [
            "id",
            "currency",
            "address",
            "txid",
            "category",
            "amount",
            "fee",
            "amount_with_fee",
            "is_confirmed",
            "timestamp",
            "timestamp_received",
        ]

    def validate(self, attrs):
        currency = attrs.pop("currency")

        # TODO: Add filter with default
        node = models.Node.objects.filter(
            currency=currency, is_default=True,
        ).first()
        if not node:
            raise serializers.ValidationError(
                f"Node for {currency.name} does not registered"
            )

        address, _ = models.Address.objects.get_or_create(
            address=attrs.pop("address"), currency=currency,
        )

        return {
            "node": node,
            "address": address,
            **attrs,
        }

    def create(self, validated_data):
        tx = models.Transaction.objects.create(
            category="send", **validated_data,
        )
        return tx.send()


class AddressSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        slug_field="name", queryset=models.Currency.objects.all(),
    )

    class Meta:
        model = models.Address
        read_only_fields = ["value"]
        fields = "__all__"

    def create(self, validated_data):
        currency = validated_data.pop("currency")
        node = models.Node.objects.filter(
            currency=currency, is_default=True,
        ).first()
        if not node:
            raise serializers.ValidationError(
                f"Node for {currency.name} does not registered"
            )

        return models.Address.objects.create(
            value=node.create_address(), currency=currency,
        )
