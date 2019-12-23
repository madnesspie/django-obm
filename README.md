# Django cryptocurrency framework

[![Build Status](https://travis-ci.org/madnesspie/django-cryptocurrency-framework.svg?branch=master)](https://travis-ci.org/madnesspie/django-cryptocurrency-framework)
[![PyPI version](https://badge.fury.io/py/django-cryptocurrency-framework.svg)](https://badge.fury.io/py/django-cryptocurrency-framework)

## Introduction
The Django application that can halp to implement payments receiving in cryptocurrency.

The project is now under active development. But in this moment it can much facilitate in the task of creation bitcoin wallet or other app that use bitcoin payments.

## Requirements
- [bitcoin-core](https://bitcoincore.org/en/download/)
- job scheduler or queue to your taste


## Installation
```bash
$ pip install django-cryptocurrency-framework
```

## Example
First of all you need to install `bitcoin-core` and to allow RPC access.

Next add a reference in your project settings and set up timeout for `bitcoin-core` node response.
```python
INSTALLED_APPS = [
    ...
    'cryptocurrency.blockchains'
]

...

# Cryptocurrency framework setting
CC_FRAMEWORK = {
    'TIMEOUT': 5,
}
```

Then create a `Currency` and `Node` objects.
```python
>>> from cryptocurrency.blockchains import models
>>> currency = models.Currency.objects.create(
... name='BTC',
... min_confirmations=2,
)
>>> models.Node.objects.create(
...     name='bitcoin-core',
...     currency=currency,
...     rpc_username='username',
...     rpc_password='password',
...     rpc_host='127.0.0.1',
...     rpc_port=18332,
... )
<Node: bitcoin-core>
```

It's worth clarifying, that you can't create 'Node' or 'Currency' object if framework doesn't support corresponded cryptocurrency or node. To discover supported things you can to execute code below.
```python
>>> from cryptocurrency.blockchains import connectors
>>> connectors.registry.available_currencies
{'BTC'}
>>> connectors.registry.available_nodes
{'bitcoin-core'}
```

Now you are ready to receive payments. For fetch new transaction call `process_receipts` method or execute one managment command.
```python
>>> models.Node.objects.process_receipts()
```
```bash
$ python manage.py process_receipts
```
This method or command one fetch receive transactions from each node object and write them into database. Each trasaction will get status `tx.is_confirmed == True` if conformations number of transaction greater than `tx.node.currency.min_conformations`, in our case it's 2.

You can use any job scheduler or queue (celery, crontab, etc.) that will check your nodes as often as you want.
Example with `Celery` you can find in this repo [example](https://github.com/HelloCreepy/django-cryptocurrency-framework/tree/master/example) dir.


## Future features
- connectors for: ETH, ETC, DASH, BCHABC, BCHSV, LTC and so on
- `cryptocurrency.wallet` app that help in implementation multi cryptocurrency wallet
