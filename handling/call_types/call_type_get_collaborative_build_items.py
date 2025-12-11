from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events
from datetime import datetime

def handle_get_collaborative_build_items(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    rpc_req.writeUintvar31(Events.ITEM_INFO_FOUND)
    rpc_req.writeArray([], lambda x: None)

    return response.getvalue()
