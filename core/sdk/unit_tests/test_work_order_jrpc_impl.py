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

import logging
from encodings.hex_codec import hex_encode
import unittest
import toml
from os import path, environ
import errno
import secrets
import time
import base64
import json

from avalon_sdk_direct.jrpc_work_order import JRPCWorkOrderImpl

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

class TestJRPCWorkOrderImpl(unittest.TestCase):
    def __init__(self, config_file):
        super(TestJRPCWorkOrderImpl, self).__init__()
        if not path.isfile(config_file):
            raise FileNotFoundError(
                "File not found at path: {0}".format(
                    path.realpath(config_file)))
        try:
            with open(config_file) as fd:
                self.__config = toml.load(fd)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise Exception("Could not open config file: %s", e)

        self.__work_order_wrapper = JRPCWorkOrderImpl(self.__config)
        self.__work_order_id = secrets.token_hex(32)
        self.__work_order_submit_request = {
            "responseTimeoutMSecs": 6000,
            "payloadFormat": "JSON-RPC",
            "resultUri": "http://result-uri:8080",
            "notifyUri": "http://notify-uri:8080",
            "workOrderId": self.__work_order_id,
            "workerId": "0",
            "workloadId": "heart-disease-eval".encode("utf-8").hex(),
            "requesterId": secrets.token_hex(32),
            "workerEncryptionKey": secrets.token_hex(32),
            "dataEncryptionAlgorithm": "AES-GCM-256",
            "encryptedSessionKey": "sessionkey".encode("utf-8").hex(),
            "sessionKeyIv": "ivSessionKey".encode("utf-8").hex(),
            "requesterNonce": secrets.token_hex(16),
            "encryptedRequestHash": "requesthash".encode("utf-8").hex(),
            "requesterSignature": base64.b64encode(str.encode(
                "SampleRequesterSignature", "utf-8")).decode("utf-8"),
            }
#           "verifyingKey": "-----BEGIN PUBLIC KEY-----\n" +
#           "MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEW" +
#           "PblapM4eJI3vg8I8DhoKAeceop2VnqK\n" +
#           "40Yqs6WhLpxYvbYGrDsrIwNTZHrxNSHaX59APUpWamulen25G3LFCw==\n" +
#           "-----END PUBLIC KEY-----\n"
        self.__in_data = [
            {"index": 1,
             "dataHash": "mhash444".encode("utf-8").hex(),
             "data": base64.b64encode(str.encode(
                  "Heart disease evaluation data: " +
                  "32 1 1 156  132 125 1 95  1 0 1 1 3 1", "utf-8")).decode(
                  "utf-8"),
             "encryptedDataEncryptionKey": "12345".encode("utf-8").hex(),
             "iv": "iv_1".encode("utf-8").hex()},
            {"index": 0,
             "dataHash": "mhash555".encode("utf-8").hex(),
             "data": base64.b64encode(str.encode("heart-disease-eval:",
                                      "utf-8")).decode("utf-8"),
             "encryptedDataEncryptionKey": "12345".encode("utf-8").hex(),
             "iv": "iv_0".encode("utf-8").hex()}]
        self.__out_data = [
            {"index": 1, "dataHash": "mhash444".encode("utf-8").hex(),
             "data":"Heart disease evaluation data: " +
                 "32 1 1 156  132 125 1 95  1 0 1 1 3 1",
             "encryptedDataEncryptionKey": "12345".encode("utf-8").hex(),
             "iv": "iv_1".encode("utf-8").hex()},
            {"index": 0, "dataHash": "mhash555".encode("utf-8").hex(),
             "encryptedDataEncryptionKey": "12345".encode("utf-8").hex(),
             "iv": "iv_0".encode("utf-8").hex()}]

    def test_work_order_submit(self):
        req_id = 21
        logging.info(
            "Calling work_order_submit with params " +
            "%s\nin_data %s\nout_data %s\n",
            json.dumps(self.__work_order_submit_request, indent=4),
            json.dumps(self.__in_data, indent=4),
            json.dumps(self.__out_data, indent=4))
        work_order_request = self.__work_order_submit_request
        work_order_request["inData"] = self.__in_data
        work_order_request["outData"] = self.__out_data
        logging.info(
            "Calling work_order_submit with work_order_id " +
            "%s\nworker_id %s\nrequester_id %s\nrequester_id %s\nwork_order_request",
            work_order_request["workOrderId"],
            work_order_request["workerId"],
            work_order_request["requesterId"], 
            json.dumps(work_order_request, indent=4))

        res = self.__work_order_wrapper.work_order_submit(
                work_order_request["workOrderId"], work_order_request["workerId"],
                work_order_request["requesterId"], json.dumps(work_order_request), req_id)
        logging.info("Result: %s\n", res)
        self.assertEqual(
            res['id'], req_id, "work_order_submit Response id doesn't match")

    def test_work_order_get_result(self):
        req_id = 22
        res = {}
        logging.info(
            "Calling work_order_get_result with workOrderId %s\n",
            self.__work_order_id)
        res = self.__work_order_wrapper.work_order_get_result(
                self.__work_order_id, req_id)
        logging.info("Result: %s\n", res)


def main():
    logging.info("Running test cases...\n")
    tcf_home = environ.get("TCF_HOME", "../../")
    test = TestJRPCWorkOrderImpl(
        tcf_home + "/"
        "tcf_connector.toml")
    test.test_work_order_submit()
    test.test_work_order_get_result()


if __name__ == "__main__":
    main()

