#!/usr/bin/env python

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

import os
import sys
import subprocess
import re


from setuptools import setup, find_packages

include_dirs = [ "common/enums/proxy"]
setup(name='avalon_sdk_ethereum',
      version='0.0.4',
      description='Avalon SDK ',
      author='Hyperledger Avalon ',
      author_email="karthika.murthy@intel.com",                                               
      url='https://github.com/hyperledger/avalon_sdk_py',       
      package_dir = {'enums' : 'common/enums',
                     'enums.proxy' : 'common/enums/proxy',
                     'handler' : 'internal/handler/proxy',
                     'interfaces' : 'common/interfaces',
                     'exceptions' : 'internal/exceptions',
                     'exceptions.proxy' : 'internal/exceptions/proxy',
                     'validation' : 'internal/validation',
                     'validation.proxy' : 'internal/validation/proxy',
                     'utility' : 'common/utility',
                     'avalon_sdk_ethereum' : 'avalon_sdk_proxy/ethereum'
                    }, 
      
      packages=['enums',
                'enums.proxy',
                'handler', 
                'interfaces',
                'exceptions',
                'exceptions.proxy',
                'validation',
                'validation.proxy',
                'utility',
                'avalon_sdk_ethereum'
               ],
        
      package_data={'validation': ['data/*.json'],
                    'avalon_sdk_ethereum': ['ethereum_contracts/*.sol']},
      include_dirs = include_dirs,
      include_package_data=True,
      install_requires=['jsonschema'],
      entry_points={})