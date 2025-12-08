from ...utils.datastream.input_data_stream import InputDataStream
from ...utils.datastream.output_data_stream import OutputDataStream

def handle_init(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    server_string = stream.readString()
    url_vars = stream.readString()
    print(f"INIT: ServerString='{server_string}', UrlVars='{url_vars}'")
    
    # Response: Session ID (String)
    response.writeString(context.get('session_id', ''))
    return response.getvalue()