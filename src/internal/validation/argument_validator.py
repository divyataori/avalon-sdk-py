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

from enums.worker import WorkerType, WorkerStatus
from exceptions.invalid_parameter import InvalidParamException


class ArgumentValidator(object):
    """
    Helper method for validating an argument that will be used by this API in any requests.
    """
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if ArgumentValidator.__instance == None:
            ArgumentValidator()
        return ArgumentValidator.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.enum_dic = {
            "WorkerType" : WorkerType,
            "WorkerStatus" : WorkerStatus
                        }
        if ArgumentValidator.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ArgumentValidator.__instance = self

    def enum_value(self,id, enum, value):
        enum_obj = self.enum_dic[enum]
        r_value = enum_obj.has_value(value)
        if not r_value:
            message = "Invalid " + enum 
            raise InvalidParamException(message, id)

        return r_value

    def not_null(self,id, *argv): 
        for arg in argv: 
            if arg is None:
                message = "Empty params in the request" 
                raise InvalidParamException(message, id)
        return True

    def check_path(self, id, path):
        if not isinstance(path, str):
            message = "Directory Path should be string" 
            raise InvalidParamException(message, id)
        if not os.path.isfile(filepath):
            message = "Invalid Filepath" 
            raise InvalidParamException(message, id)
        return 
    


 
