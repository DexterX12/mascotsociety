from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events
from datetime import datetime

def handle_reset_map(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    rpc_req.writeUintvar31(Events.SUCCESS)
    rpc_req.writeUintvar32(datetime.today().weekday())

    return response.getvalue()
