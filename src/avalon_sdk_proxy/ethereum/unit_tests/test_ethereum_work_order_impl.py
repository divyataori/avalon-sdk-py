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


from os import urandom, path, environ, getcwd
import errno
import logging
import json
import unittest
from utility.file_utils import read_json_file

from avalon_sdk_ethereum.ethereum_work_order \
    import EthereumWorkOrderProxyImpl, \
    is_wo_id_in_event
from enums.worker import WorkerType, WorkerStatus



logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


class TestEthereumWorkOrderProxyImpl(unittest.TestCase):
    def __init__(self, config):
        super(TestEthereumWorkOrderProxyImpl, self).__init__()
        self.__config = config
        self.__eth_conn = EthereumWorkOrderProxyImpl(self.__config)

    def test_work_order_submit_positive(self):
        read_json = read_json_file(
            "work_order_req.json", ["./"])
        wo_id = urandom(32).hex()
        worker_id = urandom(32).hex()
        requester_id = urandom(32).hex()

        wo_req = json.loads(read_json)["params"]
        wo_req["workOrderId"] = wo_id
        wo_req["workerId"] = worker_id
        wo_req["requesterId"] = requester_id

        result = self.__eth_conn.work_order_submit(
                                                json.dumps(wo_req))
        self.assertEqual(result, 0, "Work order should pass")

    def test_work_order_submit_inavlid_length(self):
        read_json = read_json_file(
            "work_order_req.json", ["./"])
        wo_id = urandom(31).hex()
        worker_id = urandom(32).hex()
        requester_id = urandom(32).hex()

        wo_req = json.loads(read_json)["params"]
        wo_req["workOrderId"] = wo_id
        wo_req["workerId"] = worker_id
        wo_req["requesterId"] = requester_id

        result = self.__eth_conn.work_order_submit(wo_id,
                                                   worker_id,
                                                   requester_id,
                                                   json.dumps(wo_req))
        self.assertEqual(result, 1, "Work order submission should fail")

    def test_work_order_get_result(self):
        pass

    def test_work_order_complete(self):
        """
        This function verifies if work order complete function
        succeeds when the in work order execution is done.
        """
        read_json = read_json_file(
            "work_order_get_result.json", ["./"])
        wo_id = urandom(32).hex()

        result = self.__eth_conn.work_order_complete(wo_id,
                                                     read_json)
        self.assertEqual(
            result, 0, "Work order result submission should succeed")

    def test_work_order_complete_error(self):
        """
        This function verifies if work order complete function
        succeeds when there is an error in work order execution.
        """
        read_json = read_json_file(
            "work_order_get_result_error.json", ["./"])
        wo_id = urandom(32).hex()

        result = self.__eth_conn.work_order_complete(wo_id,
                                                     read_json)
        self.assertEqual(
            result, 0, "Work order result submission should succeed")

    def test_is_wo_id_in_event_positive(self):
        """
        This case mocks an event and verifies the wo_id_in_event function
        for a positive result.
        """
        response_event = {"args": {"workOrderId": b'g7V\xc7A',
                                   "workOrderResponse":
                                   '{"result":{"workloadId":"6563686f2",'
                                   + '"workOrderId": "673756c741",'
                                   + '"workerId":"3686f2d72"},"errorCode": 0}'
                                   }}
        self.assertTrue(is_wo_id_in_event(response_event, wo_id="673756c741"))

    def test_is_wo_id_in_event_wo_id_not_matched(self):
        """
        This case mocks an event and verifies the wo_id_in_event function
        for a negative result. The wo_id does not match.
        """
        response_event = {"args": {"workOrderId": b'g7V\xc7A',
                                   "workOrderResponse":
                                   '{"result":{"workloadId":"6563686f2",'
                                   + '"workOrderId":"673756c74",'
                                   + '"workerId": "3686f2d72"},'
                                   + '"errorCode": 0}'}}
        self.assertFalse(is_wo_id_in_event(
            response_event, wo_id="abcabcabcbc"))

    def test_is_wo_id_in_event_error_result(self):
        """
        This case mocks an event and verifies the wo_id_in_event function
        for a positive result. The event has an error response from
        work order execution.
        """
        response_event = {"args": {"workOrderId": b'g7V\xc7A',
                                   "workOrderResponse": '{"error":{"code":2,'
                                   + '"message": "Indata is empty"},'
                                   + '"errorCode": 2}'}}
        self.assertTrue(is_wo_id_in_event(response_event, wo_id="673756c741"))

    def test_is_wo_id_in_event_no_wo_id(self):
        response_event = {"args": {"workOrderResponse": '{"error":{"code":2,'
                                   + '"message": "Indata is empty"},'
                                   + '"errorCode": 2}'}}
        self.assertFalse(is_wo_id_in_event(response_event, wo_id="673756c741"))

    # def test_is_valid_work_order_json(self):
    #     wo_request = '{"workOrderId":"abcabcabc123123123",'\
    #                  + '"workerId":"bcdbcdbcd123123123",'\
    #                  + '"requesterId":"cdecdecde123123123"}'
    #     self.assertTrue(_is_valid_work_order_json(
    #         "abcabcabc123123123", "bcdbcdbcd123123123",
    #         "cdecdecde123123123", wo_request))


def main():
    logging.info("Running test cases...")
    tcf_home = environ.get("TCF_HOME", "../../../../")
    config = {
        # Direct registry contract file
        "direct_registry_contract_file" : "sdk/avalon_sdk/connector/blockchains/ethereum/contracts/WorkerRegistryList.sol",
        # Worker registry contract file
        "worker_registry_contract_file" : "sdk/avalon_sdk/connector/blockchains/ethereum/contracts/WorkerRegistry.sol",
        # Work Order registry contract file
        "work_order_contract_file" : "sdk/avalon_sdk/connector/blockchains/ethereum/contracts/WorkOrderRegistry.sol",

        # Initially deploy the contracts using eth_cli.py to get the these addresses
        # Deployed contract address of direct registry contract address.
        "direct_registry_contract_address" : "0xD5A613945DE851C7c2f83fFDA4de0aE01CE980c0",
        # Deployed contract address of worker registry contract address.
        "worker_registry_contract_address" : "0x75a3Fd17E8c5CceAa9121251c359bFe4b9C343C8",
        # Deployed contract address of worker registry contract address.
        "work_order_contract_address" : "0xf873133fae1d1f80642c551a6edd5A14f37129c2",

        # Ethereum account details
        "eth_account" : "",
        # Ethereum account private key
        "acc_pvt_key" : "",

        # Version of solc to be used for compiling Solidity contracts
        "solc_version" : "v0.5.15",
        # Provider/event_provider for test network. The default urls are for a
        # Hyperledger Besu client. These addresses need to be consistent with that in
        # docs/dev-environments/ethereum/besu/docker-compose.yaml.
        # This could be replaced with a Ropsten(Infura as the IAAS) provider or a
        # Ganache client.
        "provider" : "http://rpc.node1.avalon.local:8555", # http://local-ganache:8545 for Ganache
        "event_provider" : "http://node1.avalon.local:8545", # http://local-ganache:8545 for Ganache
        # chain_id is 3 for ropsten test network
        # "1": Ethereum Mainnet
        # "2": Morden Testnet (deprecated)
        # "3": Ropsten Testnet
        # "4": Rinkeby Testnet
        # "42": Kovan Testnet

        "chain_id" : 3,
        "gas_limit" : 300000000,
        "gas_price" : "100"
        }


    test = TestEthereumWorkOrderProxyImpl(config)
    test.test_work_order_submit_positive()
    test.test_work_order_submit_mismatch()
    test.test_work_order_complete()
    test.test_work_order_complete_error()
    test.test_work_order_get_result()
    # test.test_is_valid_work_order_json()
    test.test_is_wo_id_in_event_positive()
    test.test_is_wo_id_in_event_wo_id_not_matched()
    test.test_is_wo_id_in_event_error_result()
    test.test_is_wo_id_in_event_no_wo_id()
    # Not properly defined in EEA spec. To be enabled as feature is enabled.
    # test.test_worker_lookup_next()


if __name__ == "__main__":
    main()
