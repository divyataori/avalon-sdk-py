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

"""
Perform worker-related functions based on EEA Spec 1.0.
"""

from enum import Enum, unique


@unique
class WorkerType(Enum):
    """
    Worker types are:
    1 = TEE-SGX: Intel SGX Trusted Execution Environment (hardware based)
    2 = MPC: Trusted Multi-Party Compute (software/hardware based)
    3 = ZK: Zero-knowledge proofs (software based)
    """
    TEE_SGX = 1
    MPC = 2
    ZK = 3
    
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 

@unique
class WorkerStatus(Enum):
    """
    Worker status values:
    1 - worker is ACTIVE
    2 - worker is temporarily OFF_LINE
    3 - worker is DECOMMISSIONED
    4 - worker is COMPROMISED

    From EEA spec 5.2.
    """
    ACTIVE = 1
    OFF_LINE = 2
    DECOMMISSIONED = 3
    COMPROMISED = 4
    
    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_ 