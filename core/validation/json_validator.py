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


import json
import pkg_resources
from jsonschema import validate, ValidationError, SchemaError
from core.handler.decorator import decorate
from core.exceptions.invalid_parameter_format_or_value import InvalidParameterFormatOrValueException


class JsonValidator(object):
    """
    Helper class for validating the json inputs
    """

    def __init__(self,method,params):
        self.params = params
        self.method = method

    @decorate 
    def schema_validation(method, params, id):
    """
    Validate params dictionary for existence of
    fields and mandatory fields

    Parameters:
    params    Parameter dictionary to validate
    method    Method Name

    Returns:
    None      Schema validation is successful
    Invalid parameter format or value Exception     Schema validation fails
    
    """
    if len(params) == 0:
        message = "Invalid parameter format or value"
        data = "Empty dictionary object received" +params
        raise InvalidParameterFormatOrValueException(id, message, data)

    schema = {}
    file_name = "data/" + method + ".json"

    data_file = pkg_resources.resource_string(__name__, file_name)
    schema = json.loads(data_file)
    try:
        validate(params, schema)
    except ValidationError as e:
        message = "Invalid parameter format or value"
        if e.validator == 'additionalProperties' or \
                e.validator == 'required':
            raise InvalidParameterFormatOrValueException(id, message, e.message)
        else:
            return InvalidParameterFormatOrValueException(id, message, e.schema["error_msg"])
    except SchemaError as err:
        return InvalidParameterFormatOrValueException(id, message, err.message)
    except Exception as err:
        return InvalidParameterFormatOrValueException(id, message, str(err))

    return None
