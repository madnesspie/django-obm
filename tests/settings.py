import os

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'cc_framework.blockchain',
    'cc_framework.rest',
]
ROOT_URLCONF = 'cc_framework.rest.urls'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Django cryptocurrency framework
BLOCKCHAIN_NODE_TIMEOUT = 1
BLOCKCHAIN_NODES_INITIAL_CONFIG = [
    {
        'currency': {
            'name': 'BTC',
            'min_confirmations': 2,
        },
        'name': 'bitcoin-core',
        'is_default': True,
        'rpc_username': 'testnet_user',
        'rpc_password': 'testnet_pass',
        'rpc_host': 'localhost',
        'rpc_port': 18332,
    },
]
