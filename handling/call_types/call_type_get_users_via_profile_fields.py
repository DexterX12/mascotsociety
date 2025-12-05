from utils.datastream.output_data_stream import OutputDataStream
from utils.pets.rpc_response import InputDataStream
from utils.pets.rpc_request import RpcRequest


def handle_get_users_via_profile_fields(stream:InputDataStream, context={}) -> bytes:
    response = RpcRequest(OutputDataStream())
    response.writeArray([], response.writeUserInfo)

    return response.getvalue()