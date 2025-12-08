from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream
from ... import profile_handler

def handle_get_cafe_users(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_req = RpcRequest(response)

    friends = profile_handler.friends or []
    rpc_req.writeArray(friends, rpc_req.writeUserInfo)

    return response.getvalue()