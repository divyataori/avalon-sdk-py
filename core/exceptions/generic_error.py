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
Generic error class
"""

class GenericError():
    """All errors and status are returned in 
    the following generic JSON RPC error format"""
    
    def __init__(self):
    
        self.error = {
            "jsonrpc": "2.0",    # as per JSON RPC spec
            "id": 0,     # the same as in input
            "error": {           # as per JSON RPC spec
                "code": 1,
                "message": "unknown error",
                "data": " unknown error"
            }   
        }
    
    def __repr__(self):
        return "% s" % (self.error)
    
    def error_message(self):
        return self.error