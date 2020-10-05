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

from enums.work_order_status import WorkOrderStatus
from exception.generic_error import GenericError

class InvalidParameterFormatOrValueException(Exception,GenericError):
    """All errors and status are returned in 
    the following generic JSON RPC error format"""

    def __init__(self, id, message, data):

        self.error = {
            "jsonrpc": "2.0",
            "id": id,
            "error": {       
                "code": WorkOrderStatus.INVALID_PARAMETER_FORMAT_OR_VALUE,
                "message": message,
                # Implementation specific data
                "data": data
            }   
        }

