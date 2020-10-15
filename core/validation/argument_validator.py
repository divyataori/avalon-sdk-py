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
Argument Validation
""" 
from core.enums.worker import WorkerType
from core.exceptions.invalid_parameter import InvalidParamException
from core.handler.decorator import decorate


class ArgumentValidator(object):
    """
    Helper method for validating an argument that will be used by this API in any requests.
    """
    
    def __init__(self):

        self.enum_dic = {
            "WorkerType" : WorkerType
        }

    @decorate
    def enum_value(self,id, enum, value):

        enum_obj = self.enum_dic[enum]
        
        if not enum_obj.has_value(value):
            message = "Invalid " + enum 
            raise InvalidParamException(message, id)
        
        return None

    @decorate
    def not_null(self,id, *argv): 
        for arg in argv: 
            if arg is None:
                message = "Empty params in the request" 
                raise InvalidParamException(message, id)
        
        return None
        
    @decorate
    def check_path(self, id, path):
        if not isinstance(path, str):
            message = "Directory Path should be string" 
            raise InvalidParamException(message, id)
        if not os.path.isfile(filepath):
            message = "Invalid Filepath" 
            raise InvalidParamException(message, id)
    
    def checkHexLength(self, id, hex_value, length):
        if length != len("{:x}".format(hex_value)):
            message = "Invalid size of hex string: "+ hex_value
            raise InvalidParamException(message, id)
