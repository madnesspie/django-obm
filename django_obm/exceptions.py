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
class BaseError(Exception):
    """Base cryprocerrency exception."""


class CurrencyDoesNotExistError(BaseError):
    """This currency doesn't supported yet."""


class NodeDoesNotExistError(BaseError):
    """This node doesn't supported yet."""


class DefaultNodeDoesNotExistError(NodeDoesNotExistError):
    """Missing default node for currency."""


class TooManyDefaultNodes(BaseError):
    """Default nodes number greater than one."""


class DefaultNodeAlreadyExists(BaseError):
    """Default node already exists for currency."""


class CanNotSendReceivedTransaction(BaseError):
    """Trying to send received transaction wth ORM."""
