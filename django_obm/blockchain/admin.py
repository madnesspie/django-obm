from django.contrib import admin, messages
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.shortcuts import resolve_url
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django_obm.blockchain import models


@admin.register(models.Currency)
class CurrencyAdmin(admin.ModelAdmin):
    readonly_fields = ("symbol",)
    list_display = ("__str__", "symbol", "min_confirmations")
    fieldsets = [
        (None, {"fields": ("name", "symbol")}),
        ("Settings", {"fields": ("min_confirmations",)}),
    ]

    @staticmethod
    def symbol(obj):
        return obj.name


@admin.register(models.Node)
class NodeAdmin(admin.ModelAdmin):
    readonly_fields = ("currency",)
    list_display = ("__str__", "currency", "rpc_host", "rpc_port", "is_default")
    fieldsets = (
        (None, {"fields": ("name", "currency")}),
        (
            "RPC settings",
            {
                "fields": (
                    "rpc_username",
                    "rpc_password",
                    "rpc_host",
                    "rpc_port",
                )
            },
        ),
    )

    @staticmethod
    def __currency_added_message(request, currency):
        url = resolve_url(
            admin_urlname(models.Currency._meta, "change"), currency.pk
        )
        link = format_html(f'<a href="{url}">{currency}</a>')
        msg = f'The currency "{link}" was added successfully.'
        messages.add_message(request, messages.SUCCESS, mark_safe(msg))

    def set_currency(self, request, obj):
        symbol = obj.connector.symbol
        currency, created = models.Currency.objects.get_or_create(
            name=symbol,
            defaults={
                "min_confirmations": obj.connector.default_min_confirmations
            },
        )
        obj.currency = currency
        if created:
            self.__currency_added_message(request, currency)

    def save_model(self, request, obj, form, change):
        if not models.Currency.objects.filter(node=obj).exists():
            self.set_currency(request, obj)
        super().save_model(request, obj, form, change)


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ("currency", "address")
    list_display = ("__str__", "currency")


@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = (
        "node",
        "address",
        "txid",
        "category",
        "amount",
        "fee",
        "is_confirmed",
        "timestamp",
        "timestamp_received",
    )
    list_display = (
        "__str__",
        "currency_display",
        "category",
        "amount",
        "is_confirmed",
        "timestamp",
    )

    @staticmethod
    def currency_display(tx):
        return tx.node.currency

    currency_display.short_description = "Symbol"
