#! /bin/bash

# Copyright 2019 Intel Corporation
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


cd ../../..
export TCF_HOME=`pwd`
pip uninstall dist/avalon_sdk_py-0.0.4-py3-none-any.whl 
make clean
make
pip install dist/avalon_sdk_py-0.0.4-py3-none-any.whl

cd core/sdk
pip uninstall dist/avalon_sdk_direct-0.0.4-py3-none-any.whl 
make clean
make
pip install dist/avalon_sdk_direct-0.0.4-py3-none-any.whl

cd unit_tests
python test_work_order_jrpc_impl.py
#python test_worker_registry_jrpc_impl.py

