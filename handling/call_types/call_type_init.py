from utils.datastream.input_data_stream import InputDataStream
from utils.datastream.output_data_stream import OutputDataStream
from utils.pets.rpc_response import RpcResponse
from utils.pets.rpc_request import RpcRequest

def handle_init(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    server_string = stream.read_string()
    url_vars = stream.read_string()
    print(f"INIT: ServerString='{server_string}', UrlVars='{url_vars}'")
    
    # Response: Session ID (String)
    response.write_string(context.get('session_id', ''))
    return response.getvalue()