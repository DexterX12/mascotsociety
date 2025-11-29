from py_as.datastream.input_data_stream import InputDataStream
from py_as.datastream.output_data_stream import OutputDataStream
from py_as.pets.rpc_response import RpcResponse
from py_as.pets.rpc_request import RpcRequest

def handle_init(stream:InputDataStream, context={}):
    response = OutputDataStream()
    server_string = stream.read_string()
    url_vars = stream.read_string()
    print(f"INIT: ServerString='{server_string}', UrlVars='{url_vars}'")
    
    # Response: Session ID (String)
    response.write_string(context.get('session_id', ''))
    return response.getvalue()