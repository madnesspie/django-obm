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
import logging
import os
import sys

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

# Logging
logging.addLevelName(logging.DEBUG, "🐛 DEBUG")
logging.addLevelName(logging.INFO, "📑 INFO")
logging.addLevelName(logging.WARNING, "⚠️ WARNING")
logging.addLevelName(logging.ERROR, "🚨 ERROR")
logging.addLevelName(logging.CRITICAL, "💥 CRITICAL")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)-7s  %(name)-25s %(message)s",
            "formatTime": "%d/%m/%Y %H:%M:%S",
            "style": "%",
        },
    },
    "filters": {
        "info_filter": {
            "()": "django.utils.log.CallbackFilter",
            "callback": lambda record: record.levelno < logging.WARNING,
        },
    },
    "handlers": {
        "stdout": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "filters": ["info_filter"],
            "formatter": "verbose",
        },
        "stderr": {
            "level": "WARNING",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django_obm.management.commands.synctransactions": {
            "handlers": ["stdout", "stderr"],
            "level": "DEBUG",
        }
    },
}

# Django OBM
OBM_LIST_TRANSACTIONS_COUNT = 10
OBM_REST_SUBTRACT_TRANSACTION_FEE_FROM_AMOUNT_DEFAULT = True
OBM_COLLECT_TRANSACTION_FREQUENCY = 10
OBM_NODES_INITIAL_CONFIG = [
    {
        "currency": {"name": "bitcoin"},
        "name": "bitcoin-core",
        "is_default": True,
        "rpc_username": "testnet_user",
        "rpc_password": "testnet_pass",
        "rpc_host": "localhost",
        "rpc_port": 18332,
    },
    {
        "currency": {"name": "ethereum"},
        "name": "geth",
        "is_default": True,
        "rpc_host": "localhost",
        "rpc_port": 8545,
    },
]

# OBM_PAGINATION_LIMIT = 1
# OBM_PAGINATION_MAX_LIMIT = 2
