from ...utils.datastream.input_data_stream import InputDataStream
from ...utils.datastream.output_data_stream import OutputDataStream

def handle_get_new_home_extra_rooms_data(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    response.writeUintvar32(6038)
    response.writeUintvar32(100)
    response.writeBoolean(False)
    response.writeUintvar32(9)
    response.writeUintvar32(6)
    response.writeUintvar32(234660177)
    return response.getvalue()