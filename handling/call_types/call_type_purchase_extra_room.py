from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcOwnedItem
from ...utils.hash import hashInt32
from ... import profile_handler
from ... import database_handler
from ...constants import Events

def handle_purchase_extra_room(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    purchase_data = {
        "token": rpc_res.readString()
    }

    purchased_item = database_handler.findItemByToken(purchase_data["token"])
    profile_handler.cash -= int(purchased_item["cost"])

    rpc_item = RpcOwnedItem()
    max_item_id = max(item.itemId for item in profile_handler.user.ownedItems)
    rpc_item.itemId = max_item_id + 1
    rpc_item.itemHash = hashInt32(purchased_item["name"])

    profile_handler.user.ownedItems.append(rpc_item)
    
    rpc_req.writeUintvar31(Events.PURCHASE_CASH_OK)
    rpc_req.writeUintvar31(profile_handler.cash)

    return response.getvalue()
