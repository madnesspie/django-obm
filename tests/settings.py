import os

SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_obm",
]
ROOT_URLCONF = "django_obm.urls"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

# Django OBM
OBM_NODE_TIMEOUT = 2
OBM_LIST_TRANSACTIONS_COUNT = 10

# TODO: Refactor it
RECEIPTS_PROCESSING_DEFAULT_FREQUENCY = 10
BLOCKCHAIN_NODES_INITIAL_CONFIG = [
    {
        "currency": {"name": "BTC"},
        "name": "bitcoin-core",
        "is_default": True,
        "rpc_username": "testnet_user",
        "rpc_password": "testnet_pass",
        "rpc_host": "localhost",
        "rpc_port": 18332,
    },
]
# OBM_PAGINATION_LIMIT = 1
# OBM_PAGINATION_MAX_LIMIT = 2
