from django.db import models

from . import connectors 


class Currency(models.Model):
    symbol = models.CharField(max_length=20,
                              choices=connectors.register.as_choices())
    name = models.CharField(max_length=200)

    rpc_user = models.CharField(verbose_name='RPC username',
                                max_length=200,
                                help_text='Username for JSON-RPC connections')
    rpc_password = models.CharField(verbose_name='RPC password',
                                    max_length=200,
                                    help_text='Password for JSON-RPC '
                                              'connections')
    rpc_host = models.URLField(verbose_name='RPC host',
                               help_text='Listen for JSON-RPC connections '
                                         'on this IP address')
    rpc_port = models.IntegerField(verbose_name='RPC port',
                                   default=8332,
                                   help_text='Listen for JSON-RPC connections '
                                             'on this port')

    class Meta:
        verbose_name_plural = 'currencies'
        unique_together = (
            ('rpc_user', 'rpc_password', 'rpc_host', 'rpc_port'),
            ('symbol', 'currency_name', 'node_name'))

    def __str__(self):
        return self.name


class Transaction(models.Model):
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    txid = models.CharField(verbose_name='transaction id',
                            max_length=500)
    category = models.CharField(max_length=30)
    amount = models.FloatField(help_text='The transaction amount in currency')
    fee = models.FloatField(help_text='The amount of the fee in currency. '
                                      'This is negative and only available for '
                                      'the "send" category of transactions.')
    is_confirmed = models.BooleanField(verbose_name='confirmed',
                                       default=False)
    ts = models.IntegerField(verbose_name='time',
                             help_text='transaction creation '
                                       'time in timestamp')
    ts_received = models.IntegerField(verbose_name='receipt time',
                                      help_text='transaction receipt'
                                                'time in timestamp')

    class Meta:
        unique_together = (
            ('currency', 'txid'), )

    def __str__(self):
        return f"{self.txid[:10]}..."
