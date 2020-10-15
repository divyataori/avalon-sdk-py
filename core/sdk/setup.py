#!/usr/bin/env python

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

import os
import sys
import subprocess

from setuptools import setup, find_packages


setup(name='avalon_sdk_direct',
      version='0.0.4',
      description='Avalon SDK Direct',
      author='Hyperledger Avalon Direct',
      author_email="karthika.murthy@intel.com",
      url='https://github.com/hyperledger/avalon_sdk_py/direct',
      packages=find_packages(),
      install_requires=[],
      entry_points={})

