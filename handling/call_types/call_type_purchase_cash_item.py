from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.user_info import UserInfo
from ...utils.pets.types import RpcOwnedItem
from ...utils.hash import hashInt32
from ... import profile_handler
from ... import database_handler
from ...constants import Events

def handle_purchase_cash_item(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    purchase_data = {
        "networkUid":rpc_res.readNetworkUid(),
        "wrapperToken": rpc_res.readString(),
        "token": rpc_res.readString(),
        "itemId": rpc_res.readIntvar32(),
        "contaimedItemHash": rpc_res.readUintvar32()
    }

    purchased_item = database_handler.findItemByToken(purchase_data["token"])
    profile_handler.cash -= int(purchased_item["cost"])

    rpc_item = RpcOwnedItem()
    rpc_item.containedItem = purchase_data["contaimedItemHash"]
    rpc_item.itemId = purchase_data["itemId"]
    rpc_item.itemHash = hashInt32(purchased_item["name"])

    # Manually pushing item
    # Playfish currency is handled "carefully" server-side, probably idk

    profile_handler.user.ownedItems.append(rpc_item)
    
    rpc_req.writeUintvar31(Events.PURCHASE_CASH_OK)
    rpc_req.writeUintvar31(profile_handler.cash)
    rpc_req.writeOwnedItem(rpc_item)

    return response.getvalue()
