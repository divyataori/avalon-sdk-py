All errors and status are returned in the following generic JSON RPC error format.
{
"jsonrpc": "2.0", // as per JSON RPC spec
"id": <integer>, // the same as in input
"error": { // as per JSON RPC spec
"code": <integer>,
"message": <string>,
"data": <implementation specific data>
}
}
jsonrpc must be 2.0 per JSON RPC specification
id is the same id that was sent in a corresponding request
error is a JSON object that defines an error or error status, with the following parameters:
code is an integer number defining an error or state. Supported values:
Values from -32768 to -32000 are reserved for pre-defined errors in JSON RPC spec
0 – success
1 – unknown error
2 – invalid parameter format or value
3 – access denied
4 – invalid signature
5 - no more look up results
6 - unsupported mode (e.g. synchronous, asynchronous, pull, or notification)
message is a string describing the errors and corresponding to code value.
data contains additional details about the error. Its format is error and implementation specific.




------------Work Order Specific ----------------------

6.1.3 Work Order Status Payload
{
"jsonrpc": "2.0",
"id": <integer>,
"error": {
"code": "integer",
"message": <string>,
"data": {
"workOrderId": <hex string>
}
}
}
Parameters
code is an integer number defining an error or Work Order state. Supported values:
Values from -32768 to -32000 are reserved for pre-defined errors in JSON RPC spec
5 means that the Work Order status is "pending" – scheduled to be executed, but not started
yet
6 means that the Work Order status is "processing" – its execution has started, but it has not
been completed yet
Values from 7 to 999 are reserved
All other values can be used by the Worker Service (a.k.a. implementation specific)
data contains additional details about the error that includes:
workOrderId which is a Work Order id as a hexadecimal string.