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

# import copy
# import io

# import pytest
# from django.core import management

# from django_obm import connectors

# class TestCommand:
#     @staticmethod
#     @pytest.mark.django_db
#     @pytest.mark.usefixtures("bitcoin_core_node")
#     def test_add_transaction(monkeypatch):

#         monkeypatch.setattr(
#             connectors.btc.BitcoinCoreConnector,
#             "_request",
#             lambda *_: data.BTC_TXS,
#         )

#         out = io.StringIO()
#         management.call_command(
#             "run_receipts_processing", once=True, stdout=out,
#         )
#         assert "Start" in out.getvalue()
#         assert "Run" in out.getvalue()
#         assert "Added" in out.getvalue()

#     @staticmethod
#     @pytest.mark.django_db
#     @pytest.mark.usefixtures("bitcoin_core_node", "btc_transaction")
#     def test_confirm_transaction(monkeypatch):
#         # Increases confirmations number for the fixture tx in test_btc.TXS
#         mock_txs = copy.deepcopy(data.BTC_TXS)
#         mock_txs[0]["confirmations"] = 666

#         monkeypatch.setattr(
#             connectors.btc.BitcoinCoreConnector,
#             "_request",
#             lambda *_: data.BTC_TXS,
#         )

#         out = io.StringIO()
#         management.call_command(
#             "run_receipts_processing", once=True, stdout=out,
#         )
#         assert "Start" in out.getvalue()
#         assert "Run" in out.getvalue()
#         assert "Added" in out.getvalue()

#     @staticmethod
#     @pytest.mark.django_db
#     @pytest.mark.usefixtures("bitcoin_core_node")
#     @pytest.mark.parametrize(
#         "options, output",
#         (
#             ({}, "10 sec. frequency",),
#             ({"frequency": 15}, "15 sec. frequency",),
#         ),
#     )
#     def test_frequency(options, output):
#         out = io.StringIO()
#         management.call_command(
#             "run_receipts_processing", **options, once=True, stdout=out,
#         )
#         assert output in out.getvalue()
