.. role:: python(code)
   :language: python
.. role:: bash(code)
   :language: bash

Configuration
=============

Available settings:

BLOCKCHAIN_NODE_TIMEOUT (=3)
  Specifies the timeout for request to blockchain node.

BLOCKCHAIN_NODES_INITIAL_CONFIG (=[])
  Specifies the initial database state for nodes and currencies related to
  them. It is a list of dicts that represents the :python:`Node` object
  with nested :python:`Currency` that look like below:

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

  You can apply it on your database with :bash:`init_nodes` managemant
  command.
