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
import asyncio
import logging
from os import environ

from enums.proxy.contract_response \
    import ContractResponse
from enums.worker import WorkerStatus, WorkerType
from avalon_sdk_ethereum.ethereum_wrapper \
    import EthereumWrapper
from avalon_sdk_ethereum.ethereum_listener \
    import BlockchainInterface, EventProcessor
from interfaces.work_order_proxy \
    import WorkOrderProxy
import validation.proxy.argument_validator
from validation.argument_validator import ArgumentValidator
from validation.json_validator import JsonValidator
from handler.error_handler import error_handler
from utility.hex_utils import is_valid_hex_of_length

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)


# Event Listener sleep duration
LISTENER_SLEEP_DURATION = 5


class EthereumWorkOrderProxyImpl(WorkOrderProxy):

    """
    This class is meant to write work order-related data to the Ethereum
    blockchain.
    Detailed method descriptions are available in the interfaces.
    """

    def __init__(self, config):
        """
        Parameters:
        config    Dictionary containing Ethereum-specific parameters
        """
        self.WORK_ORDER_GET_RESULT_TIMEOUT = 30
        self.__initialize(config)
        self.validation = ArgumentValidator().getInstance()


    @error_handler
    def __initialize(self, config):
        """
        Initialize the parameters from config to instance variables.

        Parameters:
        config    Configuration parameters to initialize
        """
        self.validation.not_valid_contract( 
            work_order_contract_file = config.get("work_order_contract_file") ,
            worker_order_contract_address = config.get("work_order_contract_address"))
        
        self.validation.valid_proxy_provider(
            ethereum_provider = config.get("ethereum_provider")
        )
        self.__eth_client = EthereumWrapper(config)
        self._config = config

        contract_file_name = config.get("work_order_contract_file")
        contract_address = \
            config.get("work_order_contract_address")
        logging.info("Contract_file_name {}".format(contract_file_name))
        logging.info("Contract address".format(contract_address))

        self.__contract_instance, self.__contract_instance_evt =\
            self.__eth_client.get_contract_instance(
                contract_file_name, contract_address
            )


    @error_handler
    def work_order_submit(self, work_order_request, id=None):
        """
        Submit work order request to the Ethereum block chain.

        Parameters:
        work_order_id      Unique ID of the work order request
        worker_id          Identifier for the worker
        requester_id       Unique id to identify the requester
        work_order_request JSON RPC string work order request.
                           Complete definition at work_order.py and
                           defined in EEA specification 6.1.1.
        id                 Optional JSON RPC request ID

        Returns:
        0 on success and non-zero on error.
        """
        self.validation.not_valid_contract(
            work_order_contract_instance = self.__contract_instance
        )
        self.validation.not_null(id, work_order_request)
        work_order_request_json = json.loads(work_order_request)

        JsonValidator.json_validation(id, "WorkOrderSubmit", work_order_request_json)
        self.validation.valid_hex_of_length(
            id,
            64,
            work_order_id = work_order_request_json["workOrderId"],
            worker_id = work_order_request_json["workerId"],
            requester_id = work_order_request_json["requesterId"]
        )
        contract_func = \
            self.__contract_instance.functions.workOrderSubmit(
                work_order_request_json["workOrderId"], work_order_request_json["workerId"],
                work_order_request_json["requesterId"], work_order_request)
        txn_receipt = self.__eth_client.build_exec_txn(contract_func)
        if txn_receipt['status'] == 1:
            return ContractResponse.SUCCESS
        else:
            return ContractResponse.ERROR

    def work_order_complete(self, work_order_id, work_order_response):
        """
        This function is called by the Worker Service to
        complete a work order successfully or in error.
        This API is for the proxy model.

        Parameters:
        work_order_id       Unique ID to identify the work order request
        work_order_response Work order response data in a string

        Returns:
        errorCode           0 on success or non-zero on error.
        """
        self.validation.not_valid_contract(
            work_order_contract_instance = self.__contract_instance
        )
        self.validation.valid_hex_of_length(
            None,
            64,
            work_order_id = work_order_id
        )
        try:
            contract_func = \
                self.__contract_instance.functions.workOrderComplete(
                    work_order_id, work_order_response)
            txn_receipt = self.__eth_client.build_exec_txn(contract_func)
            if txn_receipt['status'] == 1:
                return ContractResponse.SUCCESS
            else:
                return ContractResponse.ERROR
        except Exception as e:
            logging.error(
                "Exception occurred when trying to execute "
                + "workOrderComplete transaction on chain {}".format(e))
            return ContractResponse.ERROR

    def work_order_get_result(self, work_order_id, id=None):
        """
        Query blockchain to get a work order result.
        This function starts an event handler for handling the
        workOrderCompleted event from the Ethereum blockchain.

        Parameters:
        work_order_id Work Order ID that was sent in the
                      corresponding work_order_submit request
        id            Optional JSON RPC request ID

        Returns:
        Tuple containing work order status, worker id, work order request,
        work order response, and error code.
        None on error.
        """
        # Call the contract to get the result from blockchain
        # If we get the result from chain then return
        # Otherwise start the event listener to get work order
        # completed event.

        self.validation.not_valid_contract(
            work_order_contract_instance = self.__contract_instance
        )
        self.validation.valid_hex_of_length(
            id,
            64,
            work_order_id = work_order_id
        )
        # workOrderGet returns tuple containing work order
        # result params as defined in EEA spec 6.10.5
        _, _, _, work_order_res, _ = \
            self.__contract_instance.functions.workOrderGet(
                work_order_id).call()
        if len(work_order_res) > 0:
            return json.loads(work_order_res)
        else:
            logging.warn("Work order seems to be not computed yet, "
                            "going to listen for workOrderCompleted "
                            "event")


        # Start an event listener that listens for events from the proxy
        # blockchain, extracts response payload from there and passes it
        # on to the requestor

        w3 = BlockchainInterface(self._config)

        contract = self.__contract_instance_evt
        # Listening only for workOrderCompleted event now
        listener = w3.newListener(contract, "workOrderCompleted")

        daemon = EventProcessor(self._config)
        # Wait for the workOrderCompleted event after starting the
        # listener and handler
        try:
            event = asyncio.get_event_loop().run_until_complete(
                asyncio.wait_for(daemon.get_event_synchronously(
                    listener, is_wo_id_in_event, wo_id=work_order_id),
                    timeout=self.WORK_ORDER_GET_RESULT_TIMEOUT,
                )
            )
            # Get the first element as this is a list of one event
            # obtained from gather() in ethereum_listener
            work_order_response = event[0]["args"]["workOrderResponse"]

            return json.loads(work_order_response)
        except asyncio.TimeoutError:
            logging.error("Work order get result timed out."
                          " Either work order id is invalid or"
                          " Work order execution not completed yet")
        except Exception as e:
            logging.error("Exception occurred while listening"
                          " to an event: {}".format(e))
        finally:
            asyncio.get_event_loop().run_until_complete(daemon.stop())
        return None

    def encryption_key_retrieve(self, worker_id, last_used_key_nonce, tag,
                                requester_id, signature_nonce=None,
                                signature=None, id=None):
        """
        Get Encryption Key Request Payload.
        Not supported for Ethereum.
        """
        pass

    def encryption_key_start(self, tag, id=None):
        """
        Inform the Worker that it should start
        encryption key generation for this requester.
        Not supported for Ethereum.
        """
        pass

    def encryption_key_set(self, worker_id, encryption_key,
                           encryption_nonce, tag, signature, id=None):
        """
        Set Encryption Key Request Payload.
        Not supported for Ethereum.
        """
        pass

    def encryption_key_get(self, worker_id, requester_id,
                           last_used_key_nonce=None, tag=None,
                           signature_nonce=None,
                           signature=None, id=None):
        """
        Get Encryption Key Request Payload.
        Not supported for Ethereum.
        """
        pass


def is_wo_id_in_event(event, *kargs, **kwargs):
    """
    This function checks if a specific work order id(passed
    in via kwargs) is there in the event as well. So, it is
    basically trying to see if the event is meant for this
    work order id.
    Returns:
        True - if the work order id matches
        False - otherwise
    """
    try:
        wo_id_from_event_bytes = event["args"]["workOrderId"]
    except KeyError as e:
        logging.error("Exception caught when trying to read workOrderId"
                      + " from event {}".format(event))
        logging.error(e)
        return False
    # Work order id in event is bytes32. Convert to hex
    wo_id_from_event = wo_id_from_event_bytes.hex()
    work_order_id = kwargs.get("wo_id")
    if wo_id_from_event == work_order_id:
        logging.debug("Work order response event for work "
                      + "order id {} received".format(work_order_id))
        return True
    return False


