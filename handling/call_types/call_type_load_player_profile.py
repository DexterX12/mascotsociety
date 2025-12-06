from datetime import datetime, timezone
from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream
from ...utils.pets.types import DailyBonusInfo
from ...utils.pets.user_info import UserInfo
from ... import profile_handler

def handle_load_player_profile(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    rpc_req = RpcRequest(response)

    rpc_req.writeUintvar31(900)

    user_info = profile_handler.user or UserInfo()
    rpc_req.writeUserInfo(user_info)

    rpc_req.writeString("SA")

    friends = profile_handler.friends or []
    rpc_req.writeArray(friends, rpc_req.writeUserInfo)
    rpc_req.writeArray(friends, rpc_req.writeUserInfo)

    rpc_req.writeDate(datetime.now(timezone.utc))
    rpc_req.writeUintvar31(1)
    rpc_req.writeBoolean(False)

    rpc_req.writeDailyBonusInfo(DailyBonusInfo())

    rpc_req.writeVersionArray(0, [], rpc_req.writeRpcCounterEvent)

    rpc_req.writeArray([], rpc_req.writeFeedLink)

    return response.getvalue()