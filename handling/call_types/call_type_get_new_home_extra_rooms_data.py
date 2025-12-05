from utils.datastream.input_data_stream import InputDataStream
from utils.datastream.output_data_stream import OutputDataStream
from utils.pets.rpc_response import RpcResponse
from utils.pets.rpc_request import RpcRequest

def handle_get_new_home_extra_rooms_data(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    response.write_uintvar32(6038)
    response.write_uintvar32(100)
    response.write_boolean(False)
    response.write_uintvar32(9)
    response.write_uintvar32(6)
    response.write_uintvar32(234660177)
    return response.getvalue()