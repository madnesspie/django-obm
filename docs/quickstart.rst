.. role:: python(code)
   :language: python
.. role:: bash(code)
   :language: bash

Quickstart
==========

.. note::
    This guide assume that you have installed and configured
    `bitcoin-core <https://bitcoincore.org/en/download/>`_ node. See
    :ref:`install-cryptocurrency-nodes` for instructions.

This guide will walk you through the basics of creating simple bitcoin payment
system that can receive and send transactions, create addresses, and estimate
fees.

Creating currency and node objects
----------------------------------
:bash:`django-cryptocurrency-framework` store configuration for specific node
in database. There are two ways to create them.

1. Managemant command
`````````````````````
Open :bash:`settings.py` and define :python:`BLOCKCHAIN_NODES_INITIAL_CONFIG`
setting. It maps on fields of :python:`cc_framework.blockchain.models.Node`
and related to it :python:`cc_framework.blockchain.models.Currency` models.

.. code-block:: python

    BLOCKCHAIN_NODES_INITIAL_CONFIG = [
        {
            'currency': {
                'name': 'BTC',
                'min_confirmations': 2,
            },
            'name': 'bitcoin-core',
            'is_default': True,
            'rpc_username': 'rpcuser',
            'rpc_password': '************',
            'rpc_host': 'localhost',
            'rpc_port': 18332,
        },
    ]

To apply the config on database execute command bellow in your Django root:

.. code-block:: bash

    $ python example/manage.py init_nodes
    <Currency: BTC> created successfully.
    <Node: bitcoin-core> created successfully.



It's worth clarifying, that you can't create :bash:`Node` or :bash:`Currency`
object if framework doesn't support corresponded cryptocurrency or node. To
discover supported things you can use special connectors registry property.

.. code-block:: python

    >>> from cc_framework.blockchain import connectors
    >>> connectors.registry.available_currencies
    {'BTC'}
    >>> connectors.registry.available_nodes
    {'bitcoin-core'}

2. Manual creation
``````````````````
Also it can be created in any place of your project then when you need it.

.. code-block:: python

    >>> from cc_framework.blockchain import models
    >>> currency = models.Currency.objects.create(
    ...     name='BTC',
    ...     min_confirmations=2,
    ... )
    >>> models.Node.objects.create(
    ...     name='bitcoin-core',
    ...     currency=currency,
    ...     is_default=True,
    ...     rpc_username='username',
    ...     rpc_password='password',
    ...     rpc_host='127.0.0.1',
    ...     rpc_port=18332,
    ... )
    <Node: bitcoin-core>


Receive payments
----------------

There are method and daemon to fetch received transactions from nodes
and write them into database. Each transaction will get status
:python:`tx.is_confirmed == True` if the conformations number greater
than :python:`tx.node.currency.min_conformations`, in our case it's 2.

Method
``````

Now you are ready to receive payments. For fetch new received transaction
call :python:`models.Node` manager :python:`process_receipts` method:

.. code-block:: python

    >>> models.Node.objects.process_receipts()

Daemon
``````

Also you can use built-in daemon, that will do it by timer. Just execute
:bash:`run_receipts_processing` django command.

.. code-block:: bash

    python manage.py run_receipts_processing --frequency=120

It runs :python:`process_receipts` :python:`models.Node` manager method with
specified frequency (defaults to 60 sec.). For defineing your own default
frequency set :python:`RECEIPTS_PROCESSING_DEFAULT_FREQUENCY` to needed value
in :bash:`settings.py`.

The daemon has the :bash:`--once` option that allow to execute
:python:`process_receipts` only once, like regular command. It might be helpful
if you wish to use some system-level (like systemd, crontab etc.) tool to
accept payments.

Example
-------

You can find the example in
`example project <https://github.com/HelloCreepy/django-cryptocurrency-framework/tree/master/example>`_.
