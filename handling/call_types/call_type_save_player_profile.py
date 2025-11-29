from py_as.datastream.output_data_stream import OutputDataStream
from py_as.datastream.input_data_stream import InputDataStream
from py_as.pets.rpc_request import RpcRequest
from constants import EVENTS, type_to_int
from py_as.pets.types import DailyBonusInfo

def handle_save_player_profile(stream:InputDataStream, context={}) -> bytes:
    response = RpcRequest(OutputDataStream())

    response.writeUintvar31(type_to_int(EVENTS, "SAVE_STATUS_OK"))
    response.writeUintvar32(0)
    response.writeBoolean(0)
    response.writeDailyBonusInfo(DailyBonusInfo)

    return b''