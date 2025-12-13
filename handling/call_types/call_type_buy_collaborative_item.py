from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events
from ... import database_handler, profile_handler

def handle_buy_collaborative_item(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    item = {
        "itemHash": rpc_res.readUintvar32()
    }

    collaborative_db_item = database_handler.find_item_by_hash(item["itemHash"])
    profile_handler.cash -= int(collaborative_db_item["cost"])

    rpc_req.writeUintvar31(Events.ITEM_PURCHASED)
    rpc_req.writeUintvar31(profile_handler.cash)

    rpc_req.writeUintvar31(0)
    rpc_req.writeBoolean(True)

    return response.getvalue()
