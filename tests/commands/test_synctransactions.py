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
import io

import pytest
from django.core import management


@pytest.mark.integration
class TestCommand:
    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node")
    def test_command(caplog):
        management.call_command(
            "synctransactions", once=True
        )
        assert "Start" in caplog.text
        assert "Synchronized" in caplog.text

    @staticmethod
    @pytest.mark.django_db
    @pytest.mark.usefixtures("bitcoin_core_node")
    @pytest.mark.parametrize(
        "options, output",
        (
            ({}, "10 sec. frequency",),
            ({"frequency": 15}, "15 sec. frequency",),
        ),
    )
    def test_command_with_frequency(caplog, options, output):
        management.call_command(
            "synctransactions", **options, once=True
        )
        assert output in caplog.text
