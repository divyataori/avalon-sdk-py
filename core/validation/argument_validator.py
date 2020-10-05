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
import avalon_sdks
from avalon_sdks.EncodingConventions.WorkerStateCode import WorkerType
from avalon_sdks.Exception.InvalidException import InvalidParamException
from avalon_sdks.Handler.Decorator import decorate  


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
        