# Copyright 2020 Intel Corporation
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

"""
Argument Validation Extension
""" 

from validation.argument_validator import ArgumentValidator
from exceptions.proxy.contract_error import ContractFailed
from exceptions.proxy.provider_error import ProxyProviderMissingOrInvalid
from urllib.parse import urlparse

def not_valid_contract(self, **kwargs): 
    for key, value in kwargs.items():
        if value is None:
            message = key.replace("_", " ") + " is not avaliable !!"
            raise ContractFailed(message)
    return True

setattr(ArgumentValidator,'not_valid_contract', not_valid_contract)

def valid_proxy_provider(self, **kwargs):
    for key, value in kwargs.items():
        if value is None:
            message = key.replace("_"," ") + "is not available !!"
            raise ProxyProviderMissingOrInvalid(message)
        else:
            if "scheme" and netloc not in urlparse(value):
                message = key.replace("_"," ") + "is not a valid url"
                raise ProxyProviderMissingOrInvalid(message)
    return True

setattr(ArgumentValidator,'valid_proxy_provider', valid_proxy_provider)


def valid_hex_of_length(self, **kwargs, length, id=None):
    for key, value in kwargs.items():
        if not_valid_hex_of_length(value, length):
            message = key.replace("_", " ") + "is either not a hex string or is of invalid length"
            raise InvalidParamException(message, id)
        else:
            return

setattr(ArgumentValidator,'valid_hex_of_length', valid_hex_of_length)






 
