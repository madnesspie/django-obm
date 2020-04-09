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
OBM_NODES_INITIAL_CONFIG = [
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


# TODO: Refactor it
RECEIPTS_PROCESSING_DEFAULT_FREQUENCY = 10
# OBM_PAGINATION_LIMIT = 1
# OBM_PAGINATION_MAX_LIMIT = 2
