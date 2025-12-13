from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events

def handle_get_collaborative_items(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    rpc_req.writeUintvar31(Events.GET_COLLAB_ITEMS_SUCCESS)
    rpc_req.writeArray([], rpc_req.writeFeedLink)

    return response.getvalue()
